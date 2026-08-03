#!/usr/bin/env python3
"""Deterministic scalability experiments for the software-only simulator."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import statistics
import sys
import tempfile
import time
from elevator_access_sim import Controller, encode_frame, load_config_json
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.event_log import EventLog
from elevator_access_sim.models import (
    ConfigurationError,
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
)


OFFICIAL_CONFIGURATION_ID = "SP06_SCALABILITY_V1"
OFFICIAL_WORKLOAD_ID = "MIXED_REQUESTS_V1"
OFFICIAL_SEED = 260516
OFFICIAL_COUNTS = (10, 100, 1000, 10000)
TIMER_NAME = "time.perf_counter_ns"
PROFILE = "PROJECT_WIEGAND_26"
CATEGORIES = (
    "granted",
    "unauthorized_floor",
    "disabled_credential",
    "unknown_credential",
    "invalid_frame",
)
OFFICIAL_MIX = (
    ("granted", 40),
    ("unauthorized_floor", 20),
    ("disabled_credential", 15),
    ("unknown_credential", 15),
    ("invalid_frame", 10),
)
CONFIG_FIELDS = (
    "schema_version",
    "configuration_id",
    "workload_id",
    "seed",
    "credential_counts",
    "minimum_request_count",
    "warmup_repetitions",
    "measured_repetitions",
    "profile",
    "output_duration_ms",
    "watchdog_timeout_ms",
    "watchdog_enabled",
    "workload_mix_percent",
)
RESULT_FIELDS = (
    "credential_count",
    "request_count",
    "repetition",
    "processed",
    "granted",
    "denied_by_reason",
    "validation_failures",
    "validation_by_reason",
    "other_outcomes",
    "average_ns",
    "median_ns",
    "p95_ns",
    "throughput_cases_per_second",
    "credential_checksum_sha256",
    "request_checksum_sha256",
    "environment_id",
    "python_version",
    "python_implementation",
    "platform_system",
    "platform_release",
    "machine",
)
ENVIRONMENT_FIELDS = (
    "schema_version",
    "environment_id",
    "python_version",
    "python_implementation",
    "platform_system",
    "platform_release",
    "platform_machine",
    "platform_processor",
    "cpu_count",
    "timer",
    "configuration_id",
    "workload_id",
    "seed",
    "credential_counts",
    "minimum_request_count",
    "warmup_repetitions",
    "measured_repetitions",
    "interpretation_limits",
)
INTERPRETATION_LIMITS = (
    "Measurements describe one Python software model and were observed on the recorded host environment.",
    "Host timing uses time.perf_counter_ns around only Controller.submit; generation, initialization, output-expiry cleanup, validation, environment collection, and export are excluded.",
    "The simulated watchdog is disabled in the frozen experiment configuration, and output-expiry cleanup occurs outside the measured interval.",
    "Results are observational, no strict latency objective exists, and values may vary across hosts and runs.",
    "Measurements are not real-time guarantees and do not measure RFID hardware or electrical outputs.",
    "Measurements do not measure elevator movement or safety and do not establish reliability or commercial-controller equivalence.",
    "Results must not be compared across hosts without considering recorded environment differences.",
)


class ExperimentError(Exception):
    """A handled experiment configuration, execution, validation, or export error."""


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    schema_version: int
    configuration_id: str
    workload_id: str
    seed: int
    credential_counts: tuple[int, ...]
    minimum_request_count: int
    warmup_repetitions: int
    measured_repetitions: int
    profile: str
    output_duration_ms: int
    watchdog_timeout_ms: int
    watchdog_enabled: bool
    workload_mix_percent: tuple[tuple[str, int], ...]

    def mix(self) -> dict[str, int]:
        return dict(self.workload_mix_percent)

    def simulator_config(self) -> SimulatorConfig:
        return SimulatorConfig(
            1,
            self.profile,
            self.output_duration_ms,
            self.watchdog_timeout_ms,
            self.watchdog_enabled,
        )


@dataclass(frozen=True, slots=True)
class GeneratedRequest:
    category: str
    request: CredentialRequest


def _exact_integer(value: object, field: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise ExperimentError(f"{field} must be an integer")
    if minimum is not None and value < minimum:
        raise ExperimentError(f"{field} must be at least {minimum}")
    return value


def _nonempty_string(value: object, field: str) -> str:
    if type(value) is not str or not value.strip():
        raise ExperimentError(f"{field} must be a nonempty string")
    return value


def _object_from_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, member in pairs:
        if key in value:
            raise ExperimentError(f"duplicate JSON member: {key}")
        value[key] = member
    return value


def _reject_constant(value: str) -> object:
    raise ExperimentError(f"non-finite JSON constant is not allowed: {value}")


def parse_experiment_config(text: str) -> ExperimentConfig:
    """Strictly parse one complete experiment configuration document."""

    if type(text) is not str:
        raise ExperimentError("experiment configuration must be UTF-8 text")
    try:
        raw = json.loads(
            text,
            object_pairs_hook=_object_from_pairs,
            parse_constant=_reject_constant,
        )
    except ExperimentError:
        raise
    except (json.JSONDecodeError, RecursionError) as error:
        raise ExperimentError("experiment configuration is not valid JSON") from error
    if type(raw) is not dict:
        raise ExperimentError("experiment configuration must be a JSON object")
    if set(raw) != set(CONFIG_FIELDS):
        missing = sorted(set(CONFIG_FIELDS) - set(raw))
        unknown = sorted(set(raw) - set(CONFIG_FIELDS))
        if missing:
            raise ExperimentError(f"missing experiment field: {missing[0]}")
        raise ExperimentError(f"unknown experiment field: {unknown[0]}")

    schema_version = _exact_integer(raw["schema_version"], "schema_version")
    if schema_version != 1:
        raise ExperimentError("unsupported experiment schema_version")
    configuration_id = _nonempty_string(raw["configuration_id"], "configuration_id")
    workload_id = _nonempty_string(raw["workload_id"], "workload_id")
    seed = _exact_integer(raw["seed"], "seed", minimum=0)

    counts_value = raw["credential_counts"]
    if type(counts_value) is not list or not counts_value:
        raise ExperimentError("credential_counts must be a nonempty array")
    counts = tuple(
        _exact_integer(value, "credential_count", minimum=1)
        for value in counts_value
    )
    if len(counts) != len(set(counts)):
        raise ExperimentError("credential_counts must not contain duplicates")
    if any(value > 65536 for value in counts):
        raise ExperimentError("credential_count exceeds the deterministic key namespace")

    minimum_request_count = _exact_integer(
        raw["minimum_request_count"],
        "minimum_request_count",
        minimum=1,
    )
    warmup_repetitions = _exact_integer(
        raw["warmup_repetitions"],
        "warmup_repetitions",
        minimum=1,
    )
    if warmup_repetitions != 1:
        raise ExperimentError("warmup_repetitions must be exactly 1")
    measured_repetitions = _exact_integer(
        raw["measured_repetitions"],
        "measured_repetitions",
        minimum=1,
    )
    profile = _nonempty_string(raw["profile"], "profile")
    output_duration_ms = _exact_integer(
        raw["output_duration_ms"],
        "output_duration_ms",
    )
    watchdog_timeout_ms = _exact_integer(
        raw["watchdog_timeout_ms"],
        "watchdog_timeout_ms",
    )
    watchdog_enabled = raw["watchdog_enabled"]
    if type(watchdog_enabled) is not bool:
        raise ExperimentError("watchdog_enabled must be a Boolean")

    mix_value = raw["workload_mix_percent"]
    if type(mix_value) is not dict:
        raise ExperimentError("workload_mix_percent must be an object")
    if set(mix_value) != set(CATEGORIES):
        missing = sorted(set(CATEGORIES) - set(mix_value))
        unknown = sorted(set(mix_value) - set(CATEGORIES))
        if missing:
            raise ExperimentError(f"missing workload category: {missing[0]}")
        raise ExperimentError(f"unknown workload category: {unknown[0]}")
    mix: list[tuple[str, int]] = []
    for category in CATEGORIES:
        percent = _exact_integer(
            mix_value[category],
            f"workload percentage {category}",
            minimum=0,
        )
        mix.append((category, percent))
    if sum(percent for _, percent in mix) != 100:
        raise ExperimentError("workload percentages must total exactly 100")

    simulator_payload = {
        "schema_version": 1,
        "profile": profile,
        "output_duration_ms": output_duration_ms,
        "watchdog_timeout_ms": watchdog_timeout_ms,
        "watchdog_enabled": watchdog_enabled,
    }
    try:
        load_config_json(json.dumps(simulator_payload))
    except ConfigurationError as error:
        raise ExperimentError(f"invalid simulator configuration: {error}") from error

    if configuration_id == OFFICIAL_CONFIGURATION_ID:
        official_values = (
            workload_id == OFFICIAL_WORKLOAD_ID,
            seed == OFFICIAL_SEED,
            counts == OFFICIAL_COUNTS,
            minimum_request_count == 1000,
            warmup_repetitions == 1,
            measured_repetitions == 3,
            profile == PROFILE,
            output_duration_ms == 100,
            watchdog_timeout_ms == 2000,
            watchdog_enabled is False,
            tuple(mix) == OFFICIAL_MIX,
        )
        if not all(official_values):
            raise ExperimentError("official configuration values must not be substituted")

    return ExperimentConfig(
        schema_version,
        configuration_id,
        workload_id,
        seed,
        counts,
        minimum_request_count,
        warmup_repetitions,
        measured_repetitions,
        profile,
        output_duration_ms,
        watchdog_timeout_ms,
        watchdog_enabled,
        tuple(mix),
    )


def load_experiment_config(path: str | os.PathLike[str]) -> ExperimentConfig:
    """Load strict UTF-8 experiment JSON without fallback or defaults."""

    try:
        text = Path(path).read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        raise ExperimentError("could not read experiment configuration as strict UTF-8") from error
    return parse_experiment_config(text)


def _derived_seed(seed: int, credential_count: int, domain: str) -> int:
    material = f"SP06_GENERATION_V1|{domain}|{seed}|{credential_count}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest()[:16], "big")


def generate_credentials(
    config: ExperimentConfig,
    credential_count: int,
) -> tuple[CredentialRecord, ...]:
    """Generate ordered unique credentials using one domain-local PRNG."""

    if type(credential_count) is not int or not 3 <= credential_count <= 65536:
        raise ExperimentError("credential generation requires a count from 3 through 65536")
    generator = random.Random(
        _derived_seed(config.seed, credential_count, "CREDENTIALS")
    )
    indexes = list(range(credential_count))
    generator.shuffle(indexes)
    all_floor_count = max(1, credential_count * 40 // 100)
    zero_mask_count = max(1, credential_count * 30 // 100)
    if all_floor_count + zero_mask_count >= credential_count:
        zero_mask_count = 1
        all_floor_count = credential_count - 2
    category_by_index: dict[int, str] = {}
    for index in indexes[:all_floor_count]:
        category_by_index[index] = "all_floor"
    for index in indexes[all_floor_count : all_floor_count + zero_mask_count]:
        category_by_index[index] = "zero_mask"
    for index in indexes[all_floor_count + zero_mask_count :]:
        category_by_index[index] = "disabled"

    records = tuple(
        CredentialRecord(
            facility_code=0,
            credential_number=index,
            enabled=category_by_index[index] != "disabled",
            floor_mask=65535 if category_by_index[index] == "all_floor" else 0,
            label=f"credential-{index:05d}-{category_by_index[index]}",
        )
        for index in range(credential_count)
    )
    if len({(record.facility_code, record.credential_number) for record in records}) != credential_count:
        raise ExperimentError("generated credential keys are not unique")
    if not any(record.enabled and record.floor_mask == 65535 for record in records):
        raise ExperimentError("generated all-floor pool is empty")
    if not any(record.enabled and record.floor_mask == 0 for record in records):
        raise ExperimentError("generated zero-mask pool is empty")
    if not any(not record.enabled for record in records):
        raise ExperimentError("generated disabled pool is empty")
    return records


def _expected_category_counts(
    config: ExperimentConfig,
    request_count: int,
) -> dict[str, int]:
    expected: dict[str, int] = {}
    for category, percent in config.workload_mix_percent:
        numerator = request_count * percent
        if numerator % 100:
            raise ExperimentError("request count does not permit exact workload percentages")
        expected[category] = numerator // 100
    if sum(expected.values()) != request_count:
        raise ExperimentError("generated category counts do not reconcile")
    return expected


def generate_requests(
    config: ExperimentConfig,
    records: Sequence[CredentialRecord],
) -> tuple[GeneratedRequest, ...]:
    """Generate an immutable exact-mix request sequence for one size."""

    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ExperimentError("records must be a credential sequence")
    records_tuple = tuple(records)
    credential_count = len(records_tuple)
    if credential_count < 3:
        raise ExperimentError("request generation requires all three credential pools")
    keys = {(record.facility_code, record.credential_number) for record in records_tuple}
    if len(keys) != credential_count:
        raise ExperimentError("request generation received duplicate credential keys")
    all_floor = tuple(
        record for record in records_tuple if record.enabled and record.floor_mask == 65535
    )
    zero_mask = tuple(
        record for record in records_tuple if record.enabled and record.floor_mask == 0
    )
    disabled = tuple(record for record in records_tuple if not record.enabled)
    if not all_floor or not zero_mask or not disabled:
        raise ExperimentError("request generation requires nonempty category pools")

    request_count = max(config.minimum_request_count, credential_count)
    expected = _expected_category_counts(config, request_count)
    schedule = [
        category
        for category in CATEGORIES
        for _ in range(expected[category])
    ]
    generator = random.Random(
        _derived_seed(config.seed, credential_count, "REQUESTS")
    )
    generator.shuffle(schedule)

    requests: list[GeneratedRequest] = []
    pool_positions = {category: 0 for category in CATEGORIES}
    for position, category in enumerate(schedule):
        source = ReaderSource.LF if position % 2 == 0 else ReaderSource.HF
        floor = generator.randrange(1, 17)
        pool_position = pool_positions[category]
        pool_positions[category] += 1
        if category == "granted":
            record = all_floor[pool_position % len(all_floor)]
            frame: object = encode_frame(record.facility_code, record.credential_number)
        elif category == "unauthorized_floor":
            record = zero_mask[pool_position % len(zero_mask)]
            frame = encode_frame(record.facility_code, record.credential_number)
        elif category == "disabled_credential":
            record = disabled[pool_position % len(disabled)]
            frame = encode_frame(record.facility_code, record.credential_number)
        elif category == "unknown_credential":
            unknown_number = generator.randrange(0, 65536)
            unknown_key = (255, unknown_number)
            if unknown_key in keys:
                raise ExperimentError("unknown credential collided with generated records")
            frame = encode_frame(*unknown_key)
        elif category == "invalid_frame":
            record = all_floor[pool_position % len(all_floor)]
            frame = encode_frame(record.facility_code, record.credential_number)[:-1]
        else:
            raise ExperimentError("unknown generated workload category")
        requests.append(
            GeneratedRequest(
                category,
                CredentialRequest(source, frame, floor),
            )
        )
    generated = tuple(requests)
    if len(generated) != request_count:
        raise ExperimentError("generated request count is incorrect")
    if {item.request.reader_source for item in generated} != {
        ReaderSource.LF,
        ReaderSource.HF,
    }:
        raise ExperimentError("generated requests must contain LF and HF sources")
    return generated


def _canonical_json_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ExperimentError("value is not canonically serializable") from error


def canonical_checksum(value: object) -> str:
    """Return a SHA-256 digest over canonical UTF-8 JSON."""

    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def credential_checksum(records: Sequence[CredentialRecord]) -> str:
    canonical = [
        {
            "facility_code": record.facility_code,
            "credential_number": record.credential_number,
            "enabled": record.enabled,
            "floor_mask": record.floor_mask,
            "label": record.label,
        }
        for record in records
    ]
    return canonical_checksum(canonical)


def request_checksum(requests: Sequence[GeneratedRequest]) -> str:
    canonical = [
        {
            "category": generated.category,
            "reader_source": generated.request.reader_source.to_text()
            if isinstance(generated.request.reader_source, ReaderSource)
            else None,
            "frame": list(generated.request.frame)
            if isinstance(generated.request.frame, tuple)
            else generated.request.frame,
            "requested_floor": generated.request.requested_floor,
        }
        for generated in requests
    ]
    return canonical_checksum(canonical)


def nearest_rank_p95(samples: Sequence[int]) -> int:
    """Return the observed sample at ceil(0.95*n), without interpolation."""

    if not isinstance(samples, Sequence) or isinstance(samples, (str, bytes)) or not samples:
        raise ExperimentError("p95 samples must be a nonempty sequence")
    values = tuple(samples)
    if any(type(value) is not int or value < 0 for value in values):
        raise ExperimentError("p95 samples must be nonnegative integers")
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def _classify_response(generated: GeneratedRequest, response: object) -> str:
    if not hasattr(response, "result") or not hasattr(response, "reason"):
        raise ExperimentError("controller returned an invalid response")
    result = response.result
    reason = response.reason
    actual: str
    if result is Result.GRANTED and reason is Reason.AUTHORIZED:
        actual = "granted"
    elif result is Result.DENIED and reason is Reason.UNAUTHORIZED_FLOOR:
        actual = "unauthorized_floor"
    elif result is Result.DENIED and reason is Reason.DISABLED_CREDENTIAL:
        actual = "disabled_credential"
    elif result is Result.DENIED and reason is Reason.UNKNOWN_CREDENTIAL:
        actual = "unknown_credential"
    elif result is Result.ERROR and reason is Reason.INVALID_FRAME:
        actual = "invalid_frame"
    elif reason in (
        Reason.CONTROLLER_BUSY,
        Reason.WATCHDOG_TIMEOUT,
        Reason.LOGGING_ERROR,
    ):
        raise ExperimentError(f"unexpected experiment outcome: {reason.to_text()}")
    else:
        actual = "other"
    if actual != generated.category:
        raise ExperimentError(
            f"generated category {generated.category} produced {actual}"
        )
    return actual


def run_repetition(
    config: ExperimentConfig,
    records: Sequence[CredentialRecord],
    requests: Sequence[GeneratedRequest],
    repetition: int,
    *,
    timer: Callable[[], int] = time.perf_counter_ns,
) -> dict[str, object]:
    """Run one fresh graph and aggregate only Controller.submit host timings."""

    repetition = _exact_integer(repetition, "repetition", minimum=1)
    records_tuple = tuple(records)
    requests_tuple = tuple(requests)
    clock = SimulatedClock(0)
    event_log = EventLog()
    controller = Controller(clock, event_log)
    initialized = controller.initialize(config.simulator_config(), records_tuple)
    if initialized.state is not ControllerState.IDLE or initialized.reason is not None:
        raise ExperimentError("controller initialization failed")

    samples: list[int] = []
    counts = {category: 0 for category in CATEGORIES}
    other_outcomes = 0
    for generated in requests_tuple:
        start = timer()
        response = controller.submit(generated.request)
        end = timer()
        if type(start) is not int or type(end) is not int or end < start:
            raise ExperimentError("timer must return nondecreasing integer nanoseconds")
        samples.append(end - start)
        category = _classify_response(generated, response)
        if category == "other":
            other_outcomes += 1
        else:
            counts[category] += 1

        if category == "granted":
            cleanup = controller.advance_by(config.output_duration_ms)
            if (
                cleanup.result is not Result.COMPLETED
                or cleanup.reason is not Reason.OUTPUT_EXPIRED
                or cleanup.state is not ControllerState.IDLE
            ):
                raise ExperimentError("granted output did not expire cleanly")
        elif response.state is not ControllerState.IDLE or response.output_snapshot.active_floor is not None:
            raise ExperimentError("non-grant request left an active output")

    processed = len(samples)
    if processed != len(requests_tuple):
        raise ExperimentError("processed request count is incorrect")
    if processed != sum(counts.values()) + other_outcomes:
        raise ExperimentError("outcome counts do not reconcile")
    expected = _expected_category_counts(config, processed)
    if any(counts[category] != expected[category] for category in CATEGORIES):
        raise ExperimentError("observed workload mix differs from configuration")
    if other_outcomes:
        raise ExperimentError("official generated workload produced another outcome")
    total_ns = sum(samples)
    if total_ns <= 0:
        raise ExperimentError("total measured duration must be positive")
    if any(
        event.event_type in (EventType.WATCHDOG_RESET, EventType.LOGGING_ERROR)
        for event in event_log.records()
    ):
        raise ExperimentError("unexpected watchdog or logging event")

    return {
        "credential_count": len(records_tuple),
        "request_count": len(requests_tuple),
        "repetition": repetition,
        "processed": processed,
        "granted": counts["granted"],
        "denied_by_reason": {
            "unknown_credential": counts["unknown_credential"],
            "disabled_credential": counts["disabled_credential"],
            "unauthorized_floor": counts["unauthorized_floor"],
        },
        "validation_failures": counts["invalid_frame"],
        "validation_by_reason": {
            "invalid_frame": counts["invalid_frame"],
        },
        "other_outcomes": other_outcomes,
        "average_ns": statistics.fmean(samples),
        "median_ns": statistics.median(samples),
        "p95_ns": nearest_rank_p95(samples),
        "throughput_cases_per_second": processed * 1_000_000_000 / total_ns,
    }


def run_complete_experiment(
    config: ExperimentConfig,
    *,
    timer: Callable[[], int] = time.perf_counter_ns,
) -> list[dict[str, object]]:
    """Generate once per size, discard warm-up aggregates, and retain measured rows."""

    rows: list[dict[str, object]] = []
    for credential_count in config.credential_counts:
        records = generate_credentials(config, credential_count)
        requests = generate_requests(config, records)
        credentials_digest = credential_checksum(records)
        requests_digest = request_checksum(requests)
        for warmup in range(config.warmup_repetitions):
            run_repetition(
                config,
                records,
                requests,
                warmup + 1,
                timer=timer,
            )
        for repetition in range(1, config.measured_repetitions + 1):
            row = run_repetition(
                config,
                records,
                requests,
                repetition,
                timer=timer,
            )
            row["credential_checksum_sha256"] = credentials_digest
            row["request_checksum_sha256"] = requests_digest
            rows.append(row)
    validate_aggregate_rows(rows, config)
    return rows


def _finite_positive_number(value: object, field: str) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise ExperimentError(f"{field} must be finite and positive")


def validate_aggregate_rows(
    rows: Sequence[Mapping[str, object]],
    config: ExperimentConfig,
) -> None:
    """Validate measured aggregates before environment enrichment and export."""

    expected_row_count = len(config.credential_counts) * config.measured_repetitions
    if len(rows) != expected_row_count:
        raise ExperimentError("measured result row count is incorrect")
    by_size: dict[int, list[Mapping[str, object]]] = {
        count: [] for count in config.credential_counts
    }
    for row in rows:
        credential_count = row.get("credential_count")
        if credential_count not in by_size:
            raise ExperimentError("result contains an unexpected credential count")
        by_size[credential_count].append(row)  # type: ignore[index]
        request_count = max(config.minimum_request_count, credential_count)  # type: ignore[arg-type]
        expected = _expected_category_counts(config, request_count)
        denied = row.get("denied_by_reason")
        validation = row.get("validation_by_reason")
        if type(denied) is not dict or set(denied) != {
            "unknown_credential", "disabled_credential", "unauthorized_floor"
        }:
            raise ExperimentError("denied_by_reason schema is invalid")
        if type(validation) is not dict or set(validation) != {"invalid_frame"}:
            raise ExperimentError("validation_by_reason schema is invalid")
        actual_counts = (
            row.get("processed"),
            row.get("granted"),
            denied["unauthorized_floor"],
            denied["disabled_credential"],
            denied["unknown_credential"],
            row.get("validation_failures"),
            validation["invalid_frame"],
            row.get("other_outcomes"),
        )
        expected_counts = (
            request_count,
            expected["granted"],
            expected["unauthorized_floor"],
            expected["disabled_credential"],
            expected["unknown_credential"],
            expected["invalid_frame"],
            expected["invalid_frame"],
            0,
        )
        if actual_counts != expected_counts or row.get("request_count") != request_count:
            raise ExperimentError("result outcome counts do not match the exact workload")
        if row.get("processed") != (
            row.get("granted")
            + sum(denied.values())  # type: ignore[operator, union-attr]
            + row.get("validation_failures")
            + row.get("other_outcomes")
        ):
            raise ExperimentError("result outcome counts do not reconcile")
        for field in (
            "average_ns", "median_ns", "p95_ns", "throughput_cases_per_second"
        ):
            _finite_positive_number(row.get(field), field)
        if type(row.get("p95_ns")) is not int:
            raise ExperimentError("p95_ns must be an observed integer sample")
        for field in ("credential_checksum_sha256", "request_checksum_sha256"):
            digest = row.get(field)
            if type(digest) is not str or len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ExperimentError(f"{field} is invalid")

    for credential_count, size_rows in by_size.items():
        if len(size_rows) != config.measured_repetitions:
            raise ExperimentError("result repetitions per size are incorrect")
        if {row.get("repetition") for row in size_rows} != set(
            range(1, config.measured_repetitions + 1)
        ):
            raise ExperimentError("result repetition numbers are incorrect")
        for checksum_field in (
            "credential_checksum_sha256", "request_checksum_sha256"
        ):
            if len({row.get(checksum_field) for row in size_rows}) != 1:
                raise ExperimentError(
                    f"{checksum_field} changed across repetitions for {credential_count}"
                )


def collect_environment(config: ExperimentConfig) -> dict[str, object]:
    """Collect only bounded non-secret host metadata and a deterministic ID."""

    processor = platform.processor() or "unknown"
    document_without_id: dict[str, object] = {
        "schema_version": 1,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform_system": platform.system() or "unknown",
        "platform_release": platform.release() or "unknown",
        "platform_machine": platform.machine() or "unknown",
        "platform_processor": processor,
        "cpu_count": os.cpu_count() or 1,
        "timer": TIMER_NAME,
        "configuration_id": config.configuration_id,
        "workload_id": config.workload_id,
        "seed": config.seed,
        "credential_counts": list(config.credential_counts),
        "minimum_request_count": config.minimum_request_count,
        "warmup_repetitions": config.warmup_repetitions,
        "measured_repetitions": config.measured_repetitions,
        "interpretation_limits": list(INTERPRETATION_LIMITS),
    }
    environment_id = f"env-{canonical_checksum(document_without_id)[:16]}"
    document = {
        "schema_version": 1,
        "environment_id": environment_id,
        **{key: value for key, value in document_without_id.items() if key != "schema_version"},
    }
    validate_environment_document(document, config)
    return document


def build_results_document(
    config: ExperimentConfig,
    aggregate_rows: Sequence[Mapping[str, object]],
    environment: Mapping[str, object],
) -> dict[str, object]:
    """Enrich validated aggregates with one consistent environment reference."""

    validate_aggregate_rows(aggregate_rows, config)
    enriched: list[dict[str, object]] = []
    for aggregate in aggregate_rows:
        row = {
            "credential_count": aggregate["credential_count"],
            "request_count": aggregate["request_count"],
            "repetition": aggregate["repetition"],
            "processed": aggregate["processed"],
            "granted": aggregate["granted"],
            "denied_by_reason": aggregate["denied_by_reason"],
            "validation_failures": aggregate["validation_failures"],
            "validation_by_reason": aggregate["validation_by_reason"],
            "other_outcomes": aggregate["other_outcomes"],
            "average_ns": aggregate["average_ns"],
            "median_ns": aggregate["median_ns"],
            "p95_ns": aggregate["p95_ns"],
            "throughput_cases_per_second": aggregate["throughput_cases_per_second"],
            "credential_checksum_sha256": aggregate["credential_checksum_sha256"],
            "request_checksum_sha256": aggregate["request_checksum_sha256"],
            "environment_id": environment["environment_id"],
            "python_version": environment["python_version"],
            "python_implementation": environment["python_implementation"],
            "platform_system": environment["platform_system"],
            "platform_release": environment["platform_release"],
            "machine": environment["platform_machine"],
        }
        enriched.append(row)
    document = {
        "schema_version": 1,
        "configuration_id": config.configuration_id,
        "workload_id": config.workload_id,
        "seed": config.seed,
        "timer": TIMER_NAME,
        "results": enriched,
    }
    validate_results_document(document, config, environment)
    return document


def _contains_forbidden_raw_key(value: object) -> bool:
    forbidden = {
        "credentials", "requests", "events", "timing_samples", "samples",
        "username", "hostname", "home", "executable", "virtual_environment",
    }
    if isinstance(value, Mapping):
        return any(key in forbidden or _contains_forbidden_raw_key(member) for key, member in value.items())
    if isinstance(value, (list, tuple)):
        return any(_contains_forbidden_raw_key(member) for member in value)
    return False


def validate_results_document(
    document: Mapping[str, object],
    config: ExperimentConfig,
    environment: Mapping[str, object],
) -> None:
    if tuple(document) != (
        "schema_version", "configuration_id", "workload_id", "seed", "timer", "results"
    ):
        raise ExperimentError("results top-level schema or order is invalid")
    if (
        document["schema_version"] != 1
        or document["configuration_id"] != config.configuration_id
        or document["workload_id"] != config.workload_id
        or document["seed"] != config.seed
        or document["timer"] != TIMER_NAME
    ):
        raise ExperimentError("results metadata does not match configuration")
    rows = document["results"]
    if type(rows) is not list or any(type(row) is not dict for row in rows):
        raise ExperimentError("results must be an array of objects")
    validate_aggregate_rows(rows, config)
    for row in rows:
        if tuple(row) != RESULT_FIELDS:
            raise ExperimentError("result row field set or order is invalid")
        if (
            row["environment_id"] != environment["environment_id"]
            or row["python_version"] != environment["python_version"]
            or row["python_implementation"] != environment["python_implementation"]
            or row["platform_system"] != environment["platform_system"]
            or row["platform_release"] != environment["platform_release"]
            or row["machine"] != environment["platform_machine"]
        ):
            raise ExperimentError("result environment reference is inconsistent")
    if _contains_forbidden_raw_key(document):
        raise ExperimentError("results contain forbidden raw or identifying data")


def validate_environment_document(
    document: Mapping[str, object],
    config: ExperimentConfig,
) -> None:
    if tuple(document) != ENVIRONMENT_FIELDS:
        raise ExperimentError("environment field set or order is invalid")
    if (
        document["schema_version"] != 1
        or document["configuration_id"] != config.configuration_id
        or document["workload_id"] != config.workload_id
        or document["seed"] != config.seed
        or document["credential_counts"] != list(config.credential_counts)
        or document["minimum_request_count"] != config.minimum_request_count
        or document["warmup_repetitions"] != config.warmup_repetitions
        or document["measured_repetitions"] != config.measured_repetitions
        or document["timer"] != TIMER_NAME
    ):
        raise ExperimentError("environment metadata does not match configuration")
    if type(document["cpu_count"]) is not int or document["cpu_count"] < 1:
        raise ExperimentError("environment cpu_count is invalid")
    limits = document["interpretation_limits"]
    if limits != list(INTERPRETATION_LIMITS):
        raise ExperimentError("environment interpretation limits are incomplete")
    content = " ".join(limits).lower()
    for phrase in (
        "python software model",
        "recorded host environment",
        "not real-time guarantees",
        "rfid hardware",
        "electrical outputs",
        "elevator movement or safety",
        "commercial-controller equivalence",
        "across hosts",
        "controller.submit",
        "watchdog is disabled",
    ):
        if phrase not in content:
            raise ExperimentError(f"environment limitation is missing: {phrase}")
    if _contains_forbidden_raw_key(document):
        raise ExperimentError("environment contains forbidden identifying data")
    without_id = {
        key: value for key, value in document.items() if key != "environment_id"
    }
    expected_id = f"env-{canonical_checksum(without_id)[:16]}"
    if document["environment_id"] != expected_id:
        raise ExperimentError("environment_id does not match canonical metadata")


def _write_temporary_json(destination: Path, document: Mapping[str, object]) -> Path:
    if not destination.parent.is_dir():
        raise ExperimentError(f"output parent does not exist: {destination.parent}")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(
                document,
                stream,
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        return temporary
    except (OSError, TypeError, ValueError) as error:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise ExperimentError(f"could not prepare output: {destination.name}") from error


def export_documents(
    results_path: str | os.PathLike[str],
    environment_path: str | os.PathLike[str],
    results_document: Mapping[str, object],
    environment_document: Mapping[str, object],
) -> None:
    """Prepare both sibling temporaries before atomically replacing destinations."""

    results_destination = Path(results_path)
    environment_destination = Path(environment_path)
    try:
        if results_destination.resolve() == environment_destination.resolve():
            raise ExperimentError("results and environment paths must differ")
    except OSError as error:
        raise ExperimentError("could not resolve output paths") from error
    result_temporary: Path | None = None
    environment_temporary: Path | None = None
    try:
        result_temporary = _write_temporary_json(results_destination, results_document)
        environment_temporary = _write_temporary_json(
            environment_destination,
            environment_document,
        )
        os.replace(result_temporary, results_destination)
        result_temporary = None
        os.replace(environment_temporary, environment_destination)
        environment_temporary = None
    except ExperimentError:
        raise
    except OSError as error:
        raise ExperimentError("could not publish experiment outputs") from error
    finally:
        if result_temporary is not None:
            result_temporary.unlink(missing_ok=True)
        if environment_temporary is not None:
            environment_temporary.unlink(missing_ok=True)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_experiments.py",
        description="Run deterministic software-model scalability experiments.",
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--environment", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_argument_parser().parse_args(argv)
    try:
        config = load_experiment_config(arguments.config)
        aggregates = run_complete_experiment(config)
        environment = collect_environment(config)
        results = build_results_document(config, aggregates, environment)
        validate_results_document(results, config, environment)
        validate_environment_document(environment, config)
        export_documents(
            arguments.results,
            arguments.environment,
            results,
            environment,
        )
    except ExperimentError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"completed: sizes={len(config.credential_counts)} "
        f"measured_rows={len(results['results'])} timer={TIMER_NAME}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
