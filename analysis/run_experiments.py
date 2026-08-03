#!/usr/bin/env python3
"""Run the isolated SP-07.2 lookup and authorization experiment."""

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

from elevator_access_sim.authorization import authorize
from elevator_access_sim.credentials import CredentialRepository
from elevator_access_sim.models import (
    AuthorizationDecision,
    CredentialKey,
    CredentialRecord,
    DecodedCredential,
    Reason,
    RepositoryLookup,
    Result,
)


CONFIGURATION_ID = "SP07_ISOLATED_OPERATIONS_V1"
WORKLOAD_ID = "LOOKUP_AUTHORIZATION_MATRIX_V1"
OFFICIAL_SEED = 270516
OFFICIAL_COUNTS = (10, 100, 1000, 10000)
TIMER_NAME = "time.perf_counter_ns"
OPERATIONS = ("credential_repository_lookup", "authorization_decision")
POOL_PERCENT = (
    ("enabled_all_floors", 60),
    ("enabled_no_floors", 20),
    ("disabled", 20),
)
LOOKUP_MIX = (("hit", 50), ("miss", 50))
AUTHORIZATION_MIX = (
    ("authorized", 40),
    ("unauthorized_floor", 20),
    ("disabled_credential", 15),
    ("unknown_credential", 15),
    ("invalid_floor", 10),
)
LOOKUP_LABELS = ("hit", "miss")
AUTHORIZATION_EXPECTED_LABELS = (
    "granted_authorized",
    "denied_unauthorized_floor",
    "denied_disabled_credential",
    "denied_unknown_credential",
    "error_invalid_floor",
)
AUTHORIZATION_ACTUAL_LABELS = AUTHORIZATION_EXPECTED_LABELS + ("other",)
CONFIG_FIELDS = (
    "schema_version",
    "configuration_id",
    "workload_id",
    "seed",
    "credential_counts",
    "case_count_per_repetition",
    "warmup_repetitions",
    "measured_repetitions",
    "credential_pool_percent",
    "lookup_mix_percent",
    "authorization_mix_percent",
)
RESULT_FIELDS = (
    "operation",
    "credential_count",
    "case_count",
    "repetition",
    "processed",
    "expected_outcomes",
    "actual_outcomes",
    "confusion_matrix",
    "correct_count",
    "mismatch_count",
    "correct_grant_count",
    "correct_denial_count",
    "correct_error_count",
    "incorrect_grant_count",
    "incorrect_denial_count",
    "other_mismatch_count",
    "average_ns",
    "median_ns",
    "p95_ns",
    "throughput_cases_per_second",
    "credential_checksum_sha256",
    "case_checksum_sha256",
    "environment_id",
)
RESULT_DOCUMENT_FIELDS = (
    "schema_version",
    "configuration_id",
    "workload_id",
    "seed",
    "timer",
    "operations",
    "results",
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
    "case_count_per_repetition",
    "warmup_repetitions",
    "measured_repetitions",
    "operation_definitions",
    "interpretation_limits",
)
OPERATION_DEFINITIONS = {
    "credential_repository_lookup": (
        "Times only CredentialRepository.lookup, including trusted-key validation, "
        "Python dictionary lookup, and RepositoryLookup construction."
    ),
    "authorization_decision": (
        "Times only authorize, including trusted decoded/record validation, precedence "
        "and floor-mask logic, and AuthorizationDecision construction; repository lookup is excluded."
    ),
}
INTERPRETATION_LIMITS = (
    "Results describe Python software operations observed on the recorded host environment.",
    "Timer overhead from time.perf_counter_ns is retained and is not subtracted.",
    "Credential generation, case generation, checksum calculation, and repository construction are excluded from timed regions.",
    "Lookup timing includes trusted-key validation, Python dictionary lookup, and RepositoryLookup construction.",
    "Authorization timing includes trusted-input validation, precedence and floor-mask logic, and AuthorizationDecision construction.",
    "Authorization rows exclude credential repository lookup.",
    "Both operations exclude controller coordination, Wiegand processing, event logging, output behavior, network access, database servers, and hardware behavior.",
    "Host timings may vary across hosts and runs; no real-time target or performance threshold exists.",
    "No physical RFID, electrical output, elevator movement, reliability, safety, certification, or commercial-equivalence result is established.",
)


class ExperimentError(Exception):
    """A handled configuration, generation, execution, validation, or output error."""


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    schema_version: int
    configuration_id: str
    workload_id: str
    seed: int
    credential_counts: tuple[int, ...]
    case_count_per_repetition: int
    warmup_repetitions: int
    measured_repetitions: int
    credential_pool_percent: tuple[tuple[str, int], ...]
    lookup_mix_percent: tuple[tuple[str, int], ...]
    authorization_mix_percent: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class LookupCase:
    key: CredentialKey
    expected_label: str


@dataclass(frozen=True, slots=True)
class AuthorizationCase:
    decoded: DecodedCredential
    record: CredentialRecord | None
    requested_floor: int
    expected_label: str


def _object_from_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, member in pairs:
        if key in value:
            raise ExperimentError(f"duplicate JSON member: {key}")
        value[key] = member
    return value


def _reject_constant(value: str) -> object:
    raise ExperimentError(f"non-finite JSON constant is not allowed: {value}")


def _exact_integer(value: object, field: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise ExperimentError(f"{field} must be an integer")
    if minimum is not None and value < minimum:
        raise ExperimentError(f"{field} must be at least {minimum}")
    return value


def _parse_exact_percentages(
    value: object,
    expected: tuple[tuple[str, int], ...],
    field: str,
) -> tuple[tuple[str, int], ...]:
    if type(value) is not dict:
        raise ExperimentError(f"{field} must be an object")
    categories = tuple(category for category, _ in expected)
    if set(value) != set(categories):
        missing = sorted(set(categories) - set(value))
        unknown = sorted(set(value) - set(categories))
        if missing:
            raise ExperimentError(f"missing {field} category: {missing[0]}")
        raise ExperimentError(f"unknown {field} category: {unknown[0]}")
    parsed = tuple(
        (category, _exact_integer(value[category], f"{field} {category}", minimum=1))
        for category in categories
    )
    if sum(percent for _, percent in parsed) != 100:
        raise ExperimentError(f"{field} percentages must total exactly 100")
    if parsed != expected:
        raise ExperimentError(f"official {field} percentages must not be substituted")
    return parsed


def parse_experiment_config(text: str) -> ExperimentConfig:
    """Strictly parse the one official SP-07.2 configuration."""

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

    schema = _exact_integer(raw["schema_version"], "schema_version")
    seed = _exact_integer(raw["seed"], "seed", minimum=0)
    counts_value = raw["credential_counts"]
    if type(counts_value) is not list:
        raise ExperimentError("credential_counts must be an array")
    counts = tuple(_exact_integer(item, "credential_count", minimum=1) for item in counts_value)
    case_count = _exact_integer(
        raw["case_count_per_repetition"], "case_count_per_repetition", minimum=1
    )
    warmups = _exact_integer(raw["warmup_repetitions"], "warmup_repetitions", minimum=1)
    repetitions = _exact_integer(
        raw["measured_repetitions"], "measured_repetitions", minimum=1
    )
    pool = _parse_exact_percentages(raw["credential_pool_percent"], POOL_PERCENT, "credential_pool")
    lookup = _parse_exact_percentages(raw["lookup_mix_percent"], LOOKUP_MIX, "lookup_mix")
    authorization = _parse_exact_percentages(
        raw["authorization_mix_percent"], AUTHORIZATION_MIX, "authorization_mix"
    )
    official = (
        schema == 1,
        raw["configuration_id"] == CONFIGURATION_ID,
        raw["workload_id"] == WORKLOAD_ID,
        seed == OFFICIAL_SEED,
        counts == OFFICIAL_COUNTS,
        len(counts) == len(set(counts)),
        case_count == 1000,
        case_count % 100 == 0,
        warmups == 1,
        repetitions == 3,
    )
    if not all(official):
        raise ExperimentError("official configuration values must not be substituted")
    return ExperimentConfig(
        schema,
        CONFIGURATION_ID,
        WORKLOAD_ID,
        seed,
        counts,
        case_count,
        warmups,
        repetitions,
        pool,
        lookup,
        authorization,
    )


def load_experiment_config(path: str | os.PathLike[str]) -> ExperimentConfig:
    """Read the official configuration as strict UTF-8 without defaults."""

    try:
        text = Path(path).read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        raise ExperimentError("could not read experiment configuration as strict UTF-8") from error
    if text.startswith("\ufeff") or "\x00" in text:
        raise ExperimentError("experiment configuration is not canonical UTF-8")
    return parse_experiment_config(text)


def derive_domain_seed(seed: int, credential_count: int, domain: str) -> int:
    """Derive one local PRNG seed through canonical SHA-256 material."""

    seed = _exact_integer(seed, "seed", minimum=0)
    credential_count = _exact_integer(credential_count, "credential_count", minimum=1)
    if type(domain) is not str or not domain:
        raise ExperimentError("seed domain must be a nonempty string")
    material = f"SP07_ISOLATED_GENERATION_V1|{domain}|{seed}|{credential_count}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest()[:16], "big")


def _category_counts(total: int, percentages: tuple[tuple[str, int], ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for category, percent in percentages:
        numerator = total * percent
        if numerator % 100:
            raise ExperimentError("count does not permit exact configured percentages")
        counts[category] = numerator // 100
    if sum(counts.values()) != total or any(value <= 0 for value in counts.values()):
        raise ExperimentError("configured category counts are invalid")
    return counts


def generate_credentials(
    config: ExperimentConfig, credential_count: int
) -> tuple[CredentialRecord, ...]:
    """Generate exact 60/20/20 pools in ascending key order."""

    if credential_count not in config.credential_counts:
        raise ExperimentError("credential count is not configured")
    counts = _category_counts(credential_count, config.credential_pool_percent)
    indexes = list(range(credential_count))
    random.Random(
        derive_domain_seed(config.seed, credential_count, "CREDENTIAL_CATEGORY_ASSIGNMENT")
    ).shuffle(indexes)
    category: dict[int, str] = {}
    offset = 0
    for name, _ in config.credential_pool_percent:
        for index in indexes[offset : offset + counts[name]]:
            category[index] = name
        offset += counts[name]
    records = tuple(
        CredentialRecord(
            1,
            number,
            category[number] != "disabled",
            0 if category[number] == "enabled_no_floors" else 65535,
            None,
        )
        for number in range(credential_count)
    )
    repository = CredentialRepository.from_records(records)
    if repository.records() != records or len(repository) != credential_count:
        raise ExperimentError("generated credentials failed repository validation")
    return records


def _record_pools(
    records: Sequence[CredentialRecord],
) -> tuple[tuple[CredentialRecord, ...], tuple[CredentialRecord, ...], tuple[CredentialRecord, ...]]:
    records_tuple = tuple(records)
    all_floors = tuple(record for record in records_tuple if record.enabled and record.floor_mask == 65535)
    no_floors = tuple(record for record in records_tuple if record.enabled and record.floor_mask == 0)
    disabled = tuple(record for record in records_tuple if not record.enabled and record.floor_mask == 65535)
    if not all_floors or not no_floors or not disabled:
        raise ExperimentError("credential category pools must be nonempty")
    return all_floors, no_floors, disabled


def generate_lookup_cases(
    config: ExperimentConfig, records: Sequence[CredentialRecord]
) -> tuple[LookupCase, ...]:
    """Generate and shuffle the exact 500/500 lookup schedule."""

    records_tuple = tuple(records)
    if len(records_tuple) not in config.credential_counts:
        raise ExperimentError("lookup records have an unexpected size")
    case_counts = _category_counts(config.case_count_per_repetition, config.lookup_mix_percent)
    generator = random.Random(
        derive_domain_seed(config.seed, len(records_tuple), "LOOKUP_CASE_ORDER")
    )
    indexes = list(range(len(records_tuple)))
    generator.shuffle(indexes)
    cases: list[LookupCase] = []
    for position in range(case_counts["hit"]):
        record = records_tuple[indexes[position % len(indexes)]]
        cases.append(LookupCase(CredentialKey(1, record.credential_number), "hit"))
    for _ in range(case_counts["miss"]):
        cases.append(LookupCase(CredentialKey(255, generator.randrange(0, 65536)), "miss"))
    generator.shuffle(cases)
    generated = tuple(cases)
    if len(generated) != config.case_count_per_repetition:
        raise ExperimentError("lookup case count is incorrect")
    repository = CredentialRepository.from_records(records_tuple)
    for case in generated:
        lookup = repository.lookup(case.key)
        if case.expected_label == "hit":
            if lookup.record is None or (
                lookup.record.facility_code,
                lookup.record.credential_number,
            ) != (case.key.facility_code, case.key.credential_number):
                raise ExperimentError("generated lookup hit does not resolve")
        elif case.expected_label == "miss":
            if case.key.facility_code != 255 or lookup.record is not None:
                raise ExperimentError("generated lookup miss collides")
        else:
            raise ExperimentError("generated lookup label is invalid")
    return generated


def _decoded(record: CredentialRecord) -> DecodedCredential:
    return DecodedCredential(record.facility_code, record.credential_number)


def generate_authorization_cases(
    config: ExperimentConfig, records: Sequence[CredentialRecord]
) -> tuple[AuthorizationCase, ...]:
    """Generate and shuffle the exact five-category authorization schedule."""

    records_tuple = tuple(records)
    if len(records_tuple) not in config.credential_counts:
        raise ExperimentError("authorization records have an unexpected size")
    all_floors, no_floors, disabled = _record_pools(records_tuple)
    counts = _category_counts(
        config.case_count_per_repetition, config.authorization_mix_percent
    )
    generator = random.Random(
        derive_domain_seed(config.seed, len(records_tuple), "AUTHORIZATION_CASE_ORDER")
    )
    schedule = [
        category
        for category, _ in config.authorization_mix_percent
        for _ in range(counts[category])
    ]
    generator.shuffle(schedule)
    positions = {category: 0 for category, _ in config.authorization_mix_percent}
    cases: list[AuthorizationCase] = []
    for category in schedule:
        position = positions[category]
        positions[category] += 1
        floor = generator.randrange(1, 17)
        if category == "authorized":
            record = all_floors[position % len(all_floors)]
            case = AuthorizationCase(_decoded(record), record, floor, "granted_authorized")
        elif category == "unauthorized_floor":
            record = no_floors[position % len(no_floors)]
            case = AuthorizationCase(
                _decoded(record), record, floor, "denied_unauthorized_floor"
            )
        elif category == "disabled_credential":
            record = disabled[position % len(disabled)]
            case = AuthorizationCase(
                _decoded(record), record, floor, "denied_disabled_credential"
            )
        elif category == "unknown_credential":
            case = AuthorizationCase(
                DecodedCredential(255, generator.randrange(0, 65536)),
                None,
                floor,
                "denied_unknown_credential",
            )
        elif category == "invalid_floor":
            record = all_floors[position % len(all_floors)]
            case = AuthorizationCase(
                _decoded(record), record, 0 if position % 2 == 0 else 17, "error_invalid_floor"
            )
        else:
            raise ExperimentError("authorization category is invalid")
        cases.append(case)
    generated = tuple(cases)
    if len(generated) != config.case_count_per_repetition:
        raise ExperimentError("authorization case count is incorrect")
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
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def credential_checksum(records: Sequence[CredentialRecord]) -> str:
    return canonical_checksum(
        [
            {
                "facility_code": record.facility_code,
                "credential_number": record.credential_number,
                "enabled": record.enabled,
                "floor_mask": record.floor_mask,
                "label": record.label,
            }
            for record in records
        ]
    )


def lookup_case_checksum(cases: Sequence[LookupCase]) -> str:
    return canonical_checksum(
        [
            {
                "facility_code": case.key.facility_code,
                "credential_number": case.key.credential_number,
                "expected_label": case.expected_label,
            }
            for case in cases
        ]
    )


def _canonical_record(record: CredentialRecord | None) -> dict[str, object] | None:
    if record is None:
        return None
    return {
        "facility_code": record.facility_code,
        "credential_number": record.credential_number,
        "enabled": record.enabled,
        "floor_mask": record.floor_mask,
        "label": record.label,
    }


def authorization_case_checksum(cases: Sequence[AuthorizationCase]) -> str:
    return canonical_checksum(
        [
            {
                "decoded": {
                    "facility_code": case.decoded.facility_code,
                    "credential_number": case.decoded.credential_number,
                },
                "record": _canonical_record(case.record),
                "requested_floor": case.requested_floor,
                "expected_label": case.expected_label,
            }
            for case in cases
        ]
    )


def nearest_rank_p95(samples: Sequence[int]) -> int:
    """Return sorted_samples[ceil(0.95*n)-1] for integer nanoseconds."""

    if not isinstance(samples, Sequence) or isinstance(samples, (str, bytes)) or not samples:
        raise ExperimentError("p95 samples must be a nonempty sequence")
    values = tuple(samples)
    if any(type(value) is not int or value < 0 for value in values):
        raise ExperimentError("p95 samples must be nonnegative integer nanoseconds")
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def classify_lookup(outcome: RepositoryLookup, key: CredentialKey) -> str:
    if not isinstance(outcome, RepositoryLookup):
        raise ExperimentError("lookup returned an invalid public outcome")
    if outcome.record is None:
        return "miss"
    if (
        outcome.record.facility_code,
        outcome.record.credential_number,
    ) != (key.facility_code, key.credential_number):
        raise ExperimentError("lookup returned a record for a different key")
    return "hit"


def classify_authorization(decision: AuthorizationDecision) -> str:
    if not isinstance(decision, AuthorizationDecision):
        raise ExperimentError("authorize returned an invalid public decision")
    pair = (decision.result, decision.reason)
    mapping = {
        (Result.GRANTED, Reason.AUTHORIZED): "granted_authorized",
        (Result.DENIED, Reason.UNAUTHORIZED_FLOOR): "denied_unauthorized_floor",
        (Result.DENIED, Reason.DISABLED_CREDENTIAL): "denied_disabled_credential",
        (Result.DENIED, Reason.UNKNOWN_CREDENTIAL): "denied_unknown_credential",
        (Result.ERROR, Reason.INVALID_FLOOR): "error_invalid_floor",
    }
    return mapping.get(pair, "other")


def build_confusion_summary(
    expected: Sequence[str], actual: Sequence[str], operation: str
) -> dict[str, object]:
    """Build complete ordered matrices and correctness/mismatch counts."""

    expected_tuple = tuple(expected)
    actual_tuple = tuple(actual)
    if len(expected_tuple) != len(actual_tuple) or not expected_tuple:
        raise ExperimentError("expected and actual outcome sequences must align")
    if operation == OPERATIONS[0]:
        expected_labels = LOOKUP_LABELS
        actual_labels = LOOKUP_LABELS
    elif operation == OPERATIONS[1]:
        expected_labels = AUTHORIZATION_EXPECTED_LABELS
        actual_labels = AUTHORIZATION_ACTUAL_LABELS
    else:
        raise ExperimentError("confusion matrix operation is invalid")
    if any(label not in expected_labels for label in expected_tuple):
        raise ExperimentError("confusion matrix expected label is invalid")
    normalized_actual = tuple(label if label in actual_labels else "other" for label in actual_tuple)
    expected_counts = {label: expected_tuple.count(label) for label in expected_labels}
    actual_counts = {label: normalized_actual.count(label) for label in actual_labels}
    matrix = {
        expected_label: {
            actual_label: sum(
                expected_value == expected_label and actual_value == actual_label
                for expected_value, actual_value in zip(expected_tuple, normalized_actual, strict=True)
            )
            for actual_label in actual_labels
        }
        for expected_label in expected_labels
    }
    correct = sum(expected_value == actual_value for expected_value, actual_value in zip(expected_tuple, normalized_actual, strict=True))
    mismatch = len(expected_tuple) - correct
    if operation == OPERATIONS[0]:
        correct_grants = correct_denials = correct_errors = None
        incorrect_grants = incorrect_denials = other_mismatches = None
    else:
        correct_grants = matrix["granted_authorized"]["granted_authorized"]
        denial_labels = (
            "denied_unauthorized_floor",
            "denied_disabled_credential",
            "denied_unknown_credential",
        )
        correct_denials = sum(matrix[label][label] for label in denial_labels)
        correct_errors = matrix["error_invalid_floor"]["error_invalid_floor"]
        incorrect_grants = sum(
            matrix[label]["granted_authorized"]
            for label in expected_labels
            if label != "granted_authorized"
        )
        incorrect_denials = sum(
            matrix["granted_authorized"][label] for label in denial_labels
        )
        other_mismatches = mismatch - incorrect_grants - incorrect_denials
    return {
        "expected_outcomes": expected_counts,
        "actual_outcomes": actual_counts,
        "confusion_matrix": matrix,
        "correct_count": correct,
        "mismatch_count": mismatch,
        "correct_grant_count": correct_grants,
        "correct_denial_count": correct_denials,
        "correct_error_count": correct_errors,
        "incorrect_grant_count": incorrect_grants,
        "incorrect_denial_count": incorrect_denials,
        "other_mismatch_count": other_mismatches,
    }


def calculate_metrics(samples: Sequence[int]) -> dict[str, int | float]:
    values = tuple(samples)
    nearest = nearest_rank_p95(values)
    total = sum(values)
    if total <= 0:
        raise ExperimentError("total measured duration must be positive")
    throughput = len(values) * 1_000_000_000 / total
    if not math.isfinite(throughput) or throughput <= 0:
        raise ExperimentError("throughput must be finite and positive")
    return {
        "average_ns": statistics.fmean(values),
        "median_ns": statistics.median(values),
        "p95_ns": nearest,
        "throughput_cases_per_second": throughput,
    }


def _timer_sample(timer: Callable[[], int], operation: Callable[[], object]) -> tuple[int, object]:
    start = timer()
    outcome = operation()
    end = timer()
    if type(start) is not int or type(end) is not int or end < start:
        raise ExperimentError("timer must return nondecreasing integer nanoseconds")
    return end - start, outcome


def run_lookup_repetition(
    records: Sequence[CredentialRecord],
    cases: Sequence[LookupCase],
    repetition: int,
    *,
    timer: Callable[[], int] = time.perf_counter_ns,
) -> dict[str, object]:
    """Time exactly one repository lookup per immutable case."""

    repetition = _exact_integer(repetition, "repetition", minimum=1)
    records_tuple = tuple(records)
    cases_tuple = tuple(cases)
    repository = CredentialRepository.from_records(records_tuple)
    samples: list[int] = []
    expected: list[str] = []
    actual: list[str] = []
    for case in cases_tuple:
        if not isinstance(case, LookupCase):
            raise ExperimentError("lookup cases must be immutable LookupCase values")
        elapsed, outcome = _timer_sample(timer, lambda case=case: repository.lookup(case.key))
        samples.append(elapsed)
        expected.append(case.expected_label)
        actual.append(classify_lookup(outcome, case.key))  # type: ignore[arg-type]
    summary = build_confusion_summary(expected, actual, OPERATIONS[0])
    return {
        "operation": OPERATIONS[0],
        "credential_count": len(records_tuple),
        "case_count": len(cases_tuple),
        "repetition": repetition,
        "processed": len(samples),
        **summary,
        **calculate_metrics(samples),
    }


def run_authorization_repetition(
    cases: Sequence[AuthorizationCase],
    credential_count: int,
    repetition: int,
    *,
    timer: Callable[[], int] = time.perf_counter_ns,
) -> dict[str, object]:
    """Time exactly one pure authorization decision per immutable case."""

    credential_count = _exact_integer(credential_count, "credential_count", minimum=1)
    repetition = _exact_integer(repetition, "repetition", minimum=1)
    cases_tuple = tuple(cases)
    samples: list[int] = []
    expected: list[str] = []
    actual: list[str] = []
    for case in cases_tuple:
        if not isinstance(case, AuthorizationCase):
            raise ExperimentError("authorization cases must be immutable AuthorizationCase values")
        elapsed, decision = _timer_sample(
            timer,
            lambda case=case: authorize(case.decoded, case.record, case.requested_floor),
        )
        samples.append(elapsed)
        expected.append(case.expected_label)
        actual.append(classify_authorization(decision))  # type: ignore[arg-type]
    summary = build_confusion_summary(expected, actual, OPERATIONS[1])
    return {
        "operation": OPERATIONS[1],
        "credential_count": credential_count,
        "case_count": len(cases_tuple),
        "repetition": repetition,
        "processed": len(samples),
        **summary,
        **calculate_metrics(samples),
    }


def _hex_digest(value: object, field: str) -> str:
    if type(value) is not str or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ExperimentError(f"{field} is not a canonical SHA-256 value")
    return value


def _finite_positive(value: object, field: str) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise ExperimentError(f"{field} must be finite and positive")


def _expected_matrix(operation: str) -> tuple[dict[str, int], dict[str, int], dict[str, dict[str, int]]]:
    if operation == OPERATIONS[0]:
        counts = {"hit": 500, "miss": 500}
        matrix = {
            expected: {actual: counts[expected] if actual == expected else 0 for actual in LOOKUP_LABELS}
            for expected in LOOKUP_LABELS
        }
        return counts, counts, matrix
    expected = {
        "granted_authorized": 400,
        "denied_unauthorized_floor": 200,
        "denied_disabled_credential": 150,
        "denied_unknown_credential": 150,
        "error_invalid_floor": 100,
    }
    actual = {**expected, "other": 0}
    matrix = {
        expected_label: {
            actual_label: expected[expected_label] if actual_label == expected_label else 0
            for actual_label in AUTHORIZATION_ACTUAL_LABELS
        }
        for expected_label in AUTHORIZATION_EXPECTED_LABELS
    }
    return expected, actual, matrix


def validate_aggregate_rows(
    rows: Sequence[Mapping[str, object]], config: ExperimentConfig
) -> None:
    """Validate the exact 24-row order, matrices, metrics, and checksums."""

    rows_tuple = tuple(rows)
    expected_order = [
        (operation, count, repetition)
        for operation in OPERATIONS
        for count in config.credential_counts
        for repetition in range(1, config.measured_repetitions + 1)
    ]
    actual_order = [
        (row.get("operation"), row.get("credential_count"), row.get("repetition"))
        for row in rows_tuple
    ]
    if actual_order != expected_order:
        raise ExperimentError("measured result operation/size/repetition order is invalid")
    credential_digests: dict[int, set[object]] = {count: set() for count in config.credential_counts}
    case_digests: dict[tuple[str, int], set[object]] = {
        (operation, count): set() for operation in OPERATIONS for count in config.credential_counts
    }
    for row in rows_tuple:
        operation = row["operation"]
        expected_counts, actual_counts, matrix = _expected_matrix(operation)  # type: ignore[arg-type]
        if (
            row.get("case_count") != config.case_count_per_repetition
            or row.get("processed") != config.case_count_per_repetition
            or row.get("expected_outcomes") != expected_counts
            or row.get("actual_outcomes") != actual_counts
            or row.get("confusion_matrix") != matrix
            or row.get("correct_count") != 1000
            or row.get("mismatch_count") != 0
        ):
            raise ExperimentError("result counts or confusion matrix do not match the official workload")
        if operation == OPERATIONS[0]:
            if any(
                row.get(field) is not None
                for field in (
                    "correct_grant_count", "correct_denial_count", "correct_error_count",
                    "incorrect_grant_count", "incorrect_denial_count", "other_mismatch_count",
                )
            ):
                raise ExperimentError("lookup row authorization-specific counts must be null")
        elif operation == OPERATIONS[1]:
            counts = (
                row.get("correct_grant_count"),
                row.get("correct_denial_count"),
                row.get("correct_error_count"),
                row.get("incorrect_grant_count"),
                row.get("incorrect_denial_count"),
                row.get("other_mismatch_count"),
            )
            if counts != (400, 500, 100, 0, 0, 0):
                raise ExperimentError("authorization correctness counts are invalid")
        else:
            raise ExperimentError("result operation is invalid")
        for field in ("average_ns", "median_ns", "p95_ns", "throughput_cases_per_second"):
            _finite_positive(row.get(field), field)
        if type(row.get("p95_ns")) is not int:
            raise ExperimentError("p95_ns must be an observed integer sample")
        credential_digest = _hex_digest(row.get("credential_checksum_sha256"), "credential checksum")
        case_digest = _hex_digest(row.get("case_checksum_sha256"), "case checksum")
        count = row["credential_count"]
        credential_digests[count].add(credential_digest)  # type: ignore[index]
        case_digests[(operation, count)].add(case_digest)  # type: ignore[index]
    if any(len(values) != 1 for values in credential_digests.values()):
        raise ExperimentError("credential checksum changed across same-size rows")
    if any(len(values) != 1 for values in case_digests.values()):
        raise ExperimentError("case checksum changed across same-operation same-size rows")
    if len({next(iter(values)) for values in credential_digests.values()}) != len(config.credential_counts):
        raise ExperimentError("credential checksums must differ across sizes")
    for operation in OPERATIONS:
        if len({next(iter(case_digests[(operation, count)])) for count in config.credential_counts}) != len(config.credential_counts):
            raise ExperimentError("case checksums must differ across sizes")


def run_complete_experiment(
    config: ExperimentConfig,
    *,
    timer: Callable[[], int] = time.perf_counter_ns,
) -> list[dict[str, object]]:
    """Generate once, warm each operation once, then retain 24 measured rows."""

    lookup_rows: list[dict[str, object]] = []
    authorization_rows: list[dict[str, object]] = []
    for credential_count in config.credential_counts:
        records = generate_credentials(config, credential_count)
        lookup_cases = generate_lookup_cases(config, records)
        authorization_cases = generate_authorization_cases(config, records)
        credentials_digest = credential_checksum(records)
        lookup_digest = lookup_case_checksum(lookup_cases)
        authorization_digest = authorization_case_checksum(authorization_cases)
        for warmup in range(1, config.warmup_repetitions + 1):
            warm_lookup = run_lookup_repetition(records, lookup_cases, warmup, timer=timer)
            warm_authorization = run_authorization_repetition(
                authorization_cases, credential_count, warmup, timer=timer
            )
            if warm_lookup["mismatch_count"] or warm_authorization["mismatch_count"]:
                raise ExperimentError("warm-up outcome validation failed")
        for repetition in range(1, config.measured_repetitions + 1):
            lookup = run_lookup_repetition(records, lookup_cases, repetition, timer=timer)
            lookup["credential_checksum_sha256"] = credentials_digest
            lookup["case_checksum_sha256"] = lookup_digest
            lookup_rows.append(lookup)
            authorization = run_authorization_repetition(
                authorization_cases, credential_count, repetition, timer=timer
            )
            authorization["credential_checksum_sha256"] = credentials_digest
            authorization["case_checksum_sha256"] = authorization_digest
            authorization_rows.append(authorization)
    rows = lookup_rows + authorization_rows
    validate_aggregate_rows(rows, config)
    return rows


def collect_environment(config: ExperimentConfig) -> dict[str, object]:
    """Collect bounded host metadata and derive one deterministic environment ID."""

    without_id: dict[str, object] = {
        "schema_version": 1,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform_system": platform.system() or "unknown",
        "platform_release": platform.release() or "unknown",
        "platform_machine": platform.machine() or "unknown",
        "platform_processor": platform.processor() or "unknown",
        "cpu_count": os.cpu_count() or 1,
        "timer": TIMER_NAME,
        "configuration_id": config.configuration_id,
        "workload_id": config.workload_id,
        "seed": config.seed,
        "credential_counts": list(config.credential_counts),
        "case_count_per_repetition": config.case_count_per_repetition,
        "warmup_repetitions": config.warmup_repetitions,
        "measured_repetitions": config.measured_repetitions,
        "operation_definitions": dict(OPERATION_DEFINITIONS),
        "interpretation_limits": list(INTERPRETATION_LIMITS),
    }
    environment_id = f"env-{canonical_checksum(without_id)[:16]}"
    document = {
        "schema_version": 1,
        "environment_id": environment_id,
        **{key: value for key, value in without_id.items() if key != "schema_version"},
    }
    validate_environment_document(document, config)
    return document


def build_results_document(
    config: ExperimentConfig,
    aggregate_rows: Sequence[Mapping[str, object]],
    environment: Mapping[str, object],
) -> dict[str, object]:
    validate_aggregate_rows(aggregate_rows, config)
    rows: list[dict[str, object]] = []
    for aggregate in aggregate_rows:
        row = {
            "operation": aggregate["operation"],
            "credential_count": aggregate["credential_count"],
            "case_count": aggregate["case_count"],
            "repetition": aggregate["repetition"],
            "processed": aggregate["processed"],
            "expected_outcomes": aggregate["expected_outcomes"],
            "actual_outcomes": aggregate["actual_outcomes"],
            "confusion_matrix": aggregate["confusion_matrix"],
            "correct_count": aggregate["correct_count"],
            "mismatch_count": aggregate["mismatch_count"],
            "correct_grant_count": aggregate["correct_grant_count"],
            "correct_denial_count": aggregate["correct_denial_count"],
            "correct_error_count": aggregate["correct_error_count"],
            "incorrect_grant_count": aggregate["incorrect_grant_count"],
            "incorrect_denial_count": aggregate["incorrect_denial_count"],
            "other_mismatch_count": aggregate["other_mismatch_count"],
            "average_ns": aggregate["average_ns"],
            "median_ns": aggregate["median_ns"],
            "p95_ns": aggregate["p95_ns"],
            "throughput_cases_per_second": aggregate["throughput_cases_per_second"],
            "credential_checksum_sha256": aggregate["credential_checksum_sha256"],
            "case_checksum_sha256": aggregate["case_checksum_sha256"],
            "environment_id": environment["environment_id"],
        }
        rows.append(row)
    document = {
        "schema_version": 1,
        "configuration_id": config.configuration_id,
        "workload_id": config.workload_id,
        "seed": config.seed,
        "timer": TIMER_NAME,
        "operations": list(OPERATIONS),
        "results": rows,
    }
    validate_results_document(document, config, environment)
    return document


def _contains_forbidden_key(value: object) -> bool:
    forbidden = {
        "credentials",
        "records",
        "cases",
        "decoded_inputs",
        "selected_records",
        "samples",
        "timing_samples",
        "events",
        "controller_snapshots",
        "username",
        "hostname",
        "home",
        "repository_path",
        "virtual_environment",
        "executable",
    }
    if isinstance(value, Mapping):
        return any(
            key in forbidden or _contains_forbidden_key(member)
            for key, member in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(_contains_forbidden_key(member) for member in value)
    return False


def validate_results_document(
    document: Mapping[str, object],
    config: ExperimentConfig,
    environment: Mapping[str, object],
) -> None:
    if tuple(document) != RESULT_DOCUMENT_FIELDS:
        raise ExperimentError("results top-level field set or order is invalid")
    if (
        document["schema_version"] != 1
        or document["configuration_id"] != config.configuration_id
        or document["workload_id"] != config.workload_id
        or document["seed"] != config.seed
        or document["timer"] != TIMER_NAME
        or document["operations"] != list(OPERATIONS)
    ):
        raise ExperimentError("results metadata does not match configuration")
    rows = document["results"]
    if type(rows) is not list or any(type(row) is not dict for row in rows):
        raise ExperimentError("results must be an array of objects")
    if any(tuple(row) != RESULT_FIELDS for row in rows):
        raise ExperimentError("result row field set or order is invalid")
    validate_aggregate_rows(rows, config)
    if any(row["environment_id"] != environment["environment_id"] for row in rows):
        raise ExperimentError("result environment references are inconsistent")
    if _contains_forbidden_key(document):
        raise ExperimentError("results contain forbidden raw or identifying data")


def validate_environment_document(
    document: Mapping[str, object], config: ExperimentConfig
) -> None:
    if tuple(document) != ENVIRONMENT_FIELDS:
        raise ExperimentError("environment field set or order is invalid")
    if (
        document["schema_version"] != 1
        or document["timer"] != TIMER_NAME
        or document["configuration_id"] != config.configuration_id
        or document["workload_id"] != config.workload_id
        or document["seed"] != config.seed
        or document["credential_counts"] != list(config.credential_counts)
        or document["case_count_per_repetition"] != config.case_count_per_repetition
        or document["warmup_repetitions"] != config.warmup_repetitions
        or document["measured_repetitions"] != config.measured_repetitions
        or document["operation_definitions"] != OPERATION_DEFINITIONS
        or document["interpretation_limits"] != list(INTERPRETATION_LIMITS)
    ):
        raise ExperimentError("environment metadata is invalid")
    if type(document["cpu_count"]) is not int or document["cpu_count"] < 1:
        raise ExperimentError("environment cpu_count is invalid")
    for field in (
        "python_version", "python_implementation", "platform_system", "platform_release",
        "platform_machine", "platform_processor",
    ):
        if type(document[field]) is not str or not document[field]:
            raise ExperimentError(f"environment {field} is invalid")
    without_id = {key: value for key, value in document.items() if key != "environment_id"}
    if document["environment_id"] != f"env-{canonical_checksum(without_id)[:16]}":
        raise ExperimentError("environment_id does not match canonical metadata")
    if _contains_forbidden_key(document):
        raise ExperimentError("environment contains forbidden identifying or raw data")


def _json_bytes(document: Mapping[str, object]) -> bytes:
    try:
        return (
            json.dumps(document, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ExperimentError("output document is not serializable") from error


def _stage_bytes(destination: Path, content: bytes) -> Path:
    if not destination.parent.is_dir():
        raise ExperimentError(f"output parent does not exist: {destination.parent}")
    temporary: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
        )
        temporary = Path(name)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        return temporary
    except OSError as error:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise ExperimentError(f"could not prepare output: {destination.name}") from error


def _strict_published_json(path: Path) -> dict[str, object]:
    try:
        raw = json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=_object_from_pairs,
            parse_constant=_reject_constant,
        )
    except ExperimentError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ExperimentError(f"published output could not be parsed: {path.name}") from error
    if type(raw) is not dict:
        raise ExperimentError(f"published output is not an object: {path.name}")
    return raw


def publish_documents(
    results_path: str | os.PathLike[str],
    environment_path: str | os.PathLike[str],
    results_document: Mapping[str, object],
    environment_document: Mapping[str, object],
) -> None:
    """Publish both documents and restore both old files if either replacement fails."""

    results_destination = Path(results_path)
    environment_destination = Path(environment_path)
    try:
        if results_destination.resolve() == environment_destination.resolve():
            raise ExperimentError("results and environment paths must differ")
    except OSError as error:
        raise ExperimentError("could not resolve output paths") from error
    results_bytes = _json_bytes(results_document)
    environment_bytes = _json_bytes(environment_document)
    previous: dict[Path, bytes | None] = {}
    try:
        for path in (results_destination, environment_destination):
            previous[path] = path.read_bytes() if path.exists() else None
    except OSError as error:
        raise ExperimentError("could not preserve existing outputs") from error
    staged: list[Path | None] = []
    try:
        staged = [
            _stage_bytes(results_destination, results_bytes),
            _stage_bytes(environment_destination, environment_bytes),
        ]
        os.replace(staged[0], results_destination)
        staged[0] = None
        os.replace(staged[1], environment_destination)
        staged[1] = None
        if results_destination.read_bytes() != results_bytes or environment_destination.read_bytes() != environment_bytes:
            raise OSError("published bytes differ")
        _strict_published_json(results_destination)
        _strict_published_json(environment_destination)
    except (OSError, ExperimentError) as error:
        restore_failures: list[Exception] = []
        for path, old in previous.items():
            try:
                if old is None:
                    path.unlink(missing_ok=True)
                else:
                    restoration = _stage_bytes(path, old)
                    os.replace(restoration, path)
            except (OSError, ExperimentError) as restore_error:
                restore_failures.append(restore_error)
        if restore_failures:
            raise ExperimentError("output publication and rollback failed") from error
        raise ExperimentError("output publication failed; existing outputs were preserved") from error
    finally:
        for temporary in staged:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_experiments.py",
        description="Run isolated credential lookup and authorization experiments.",
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
        publish_documents(arguments.results, arguments.environment, results, environment)
        published_results = _strict_published_json(arguments.results)
        published_environment = _strict_published_json(arguments.environment)
        validate_results_document(published_results, config, published_environment)
        validate_environment_document(published_environment, config)
    except ExperimentError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"completed: sizes={len(config.credential_counts)} operations={len(OPERATIONS)} "
        f"measured_rows={len(results['results'])} timer={TIMER_NAME}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
