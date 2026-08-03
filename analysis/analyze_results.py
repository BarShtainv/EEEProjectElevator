#!/usr/bin/env python3
"""Consolidate accepted SP-06 evidence into the deterministic SP-07 baseline."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import statistics
import sys
import tempfile
from types import MappingProxyType
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_ID = "SP07_ANALYSIS_BASELINE_V1"
CANONICAL_SOURCES = (
    "audit/validation/subproject_06_11_verification_records.csv",
    "docs/test_case_inventory.csv",
    "docs/requirements_to_test_traceability.csv",
    "audit/validation/subproject_06_11_validation.md",
    "experiments/scalability_config.json",
    "results/scalability_results.json",
    "results/scalability_environment.json",
)
CANONICAL_SOURCE_ARGUMENTS = (
    "verification_records",
    "inventory",
    "traceability",
    "final_validation",
    "scalability_config",
    "scalability_results",
    "scalability_environment",
)
INVENTORY_COLUMNS = (
    "test_id",
    "test_level",
    "module_or_flow",
    "requirements",
    "preconditions",
    "inputs",
    "steps",
    "expected_result",
    "expected_state",
    "expected_events",
    "fixture",
    "status",
    "notes",
)
TRACEABILITY_COLUMNS = (
    "requirement_id",
    "requirement_summary",
    "priority",
    "verification_method",
    "planned_test_id",
    "evidence_or_decision",
    "status",
    "notes",
)
VERIFICATION_COLUMNS = (
    "test_id",
    "requirements",
    "test_level",
    "category",
    "input_or_configuration",
    "expected_result",
    "expected_state",
    "expected_events",
    "actual_result",
    "evaluation_status",
    "evidence",
    "environment_reference",
    "notes",
)
CATALOG_COLUMNS = (
    "experiment_id",
    "experiment_name",
    "planned_question",
    "mapped_test_ids",
    "evidence_references",
    "evidence_status",
    "quantitative_artifacts",
    "scope_limit",
    "next_action",
)
SUMMARY_FIELDS = (
    "schema_version",
    "analysis_id",
    "source_artifacts",
    "verification_summary",
    "requirements_summary",
    "inventory_summary",
    "experiment_coverage",
    "scalability_summary",
    "metric_availability",
    "limitations",
    "deferred_work",
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
OFFICIAL_COUNTS = (10, 100, 1000, 10000)
OFFICIAL_REQUEST_COUNTS = MappingProxyType({10: 1000, 100: 1000, 1000: 1000, 10000: 10000})
OFFICIAL_MIX = MappingProxyType(
    {
        "granted": 40,
        "unauthorized_floor": 20,
        "disabled_credential": 15,
        "unknown_credential": 15,
        "invalid_frame": 10,
    }
)
OPTIONAL_IDS = frozenset(f"TST-OPT-{number:03d}" for number in range(1, 7))
EXPERIMENT_TEST_IDS = frozenset(
    {"TST-REP-001", "TST-REP-002", "TST-SCL-001", "TST-SCL-002", "TST-SCL-003"}
)
EXP07_REQUIRED_EVIDENCE = (
    "tests/unit/test_config_files.py::test_configuration_file_failures_keep_configuration_identity",
    "tests/unit/test_config_files.py::test_credential_file_failures_keep_credential_identity",
    "tests/unit/test_controller_initialization.py::test_corrected_initialization_after_failure_clears_error_event",
)
TEST_VALIDATION_PROVENANCE = MappingProxyType(
    {
        "tests/unit/test_models.py": "audit/validation/subproject_06_01_repair_validation.md",
        "tests/unit/test_clock.py": "audit/validation/subproject_06_01_repair_validation.md",
        "tests/unit/test_config.py": "audit/validation/subproject_06_01_repair_validation.md",
        "tests/unit/test_wiegand.py": "audit/validation/subproject_06_02_validation.md",
        "tests/unit/test_credentials.py": "audit/validation/subproject_06_03_validation.md",
        "tests/unit/test_credential_config.py": "audit/validation/subproject_06_03_validation.md",
        "tests/unit/test_authorization.py": "audit/validation/subproject_06_03_validation.md",
        "tests/unit/test_event_log.py": "audit/validation/subproject_06_04_validation.md",
        "tests/unit/test_outputs.py": "audit/validation/subproject_06_05_validation.md",
        "tests/unit/test_watchdog.py": "audit/validation/subproject_06_06_validation.md",
        "tests/unit/test_controller_initialization.py": "audit/validation/subproject_06_07_validation.md",
        "tests/integration/test_controller_requests.py": "audit/validation/subproject_06_07_validation.md",
        "tests/integration/test_controller_timing.py": "audit/validation/subproject_06_07_validation.md",
        "tests/integration/test_controller_resets.py": "audit/validation/subproject_06_07_validation.md",
        "tests/integration/test_controller_logging_faults.py": "audit/validation/subproject_06_07_validation.md",
        "tests/integration/test_cli.py": "audit/validation/subproject_06_08_validation.md",
        "tests/end_to_end/test_required_flows.py": "audit/validation/subproject_06_09_validation.md",
        "tests/inspection/test_scope_environment.py": "audit/validation/subproject_06_09_validation.md",
        "tests/inspection/test_inventory_traceability.py": "audit/validation/subproject_06_09_validation.md",
        "tests/experiment/test_run_experiments.py": "audit/validation/subproject_06_10_validation.md",
        "tests/inspection/test_documentation_reproducibility.py": "audit/validation/subproject_06_11_validation.md",
    }
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
FINAL_RESULT_PATTERN = re.compile(
    r"^\| `PYTHONPATH=src python -m pytest` \| "
    r"(?P<collected>\d+) collected/passed in [0-9.]+s; "
    r"(?P<failed>\d+) failed/skipped/xfailed\. \|$",
    re.MULTILINE,
)


class AnalysisError(Exception):
    """A handled source, reconciliation, or publication error."""


def read_utf8(path: Path) -> str:
    """Read strict UTF-8 without permitting a byte-order mark or NUL."""

    try:
        text = path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise AnalysisError(f"cannot read strict UTF-8 input: {path}") from error
    if text.startswith("\ufeff") or "\x00" in text:
        raise AnalysisError(f"input is not canonical UTF-8 text: {path}")
    return text


def _object_from_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AnalysisError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise AnalysisError(f"non-finite JSON constant: {value}")


def load_json(path: Path) -> dict[str, Any]:
    """Load one strict JSON object while rejecting duplicate members."""

    try:
        value = json.loads(
            read_utf8(path),
            object_pairs_hook=_object_from_pairs,
            parse_constant=_reject_constant,
        )
    except AnalysisError:
        raise
    except (json.JSONDecodeError, RecursionError) as error:
        raise AnalysisError(f"invalid JSON input: {path}") from error
    if type(value) is not dict:
        raise AnalysisError(f"JSON root must be an object: {path}")
    return value


def load_csv(path: Path, columns: Sequence[str]) -> list[dict[str, str]]:
    """Load a CSV document with one exact ordered schema."""

    try:
        reader = csv.DictReader(io.StringIO(read_utf8(path), newline=""))
        if tuple(reader.fieldnames or ()) != tuple(columns):
            raise AnalysisError(f"wrong CSV columns: {path}")
        rows = list(reader)
    except csv.Error as error:
        raise AnalysisError(f"invalid CSV input: {path}") from error
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise AnalysisError(f"malformed CSV row: {path}")
    return rows


def source_sha256(path: Path) -> str:
    """Return the SHA-256 digest of an accepted source artifact."""

    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise AnalysisError(f"cannot hash source: {path}") from error


def _references(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def _require_exact_keys(value: dict[str, Any], fields: Sequence[str], label: str) -> None:
    if tuple(value) != tuple(fields):
        raise AnalysisError(f"wrong {label} schema")


def _require_int(value: object, label: str, *, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise AnalysisError(f"invalid integer: {label}")
    return value


def _require_positive_number(value: object, label: str) -> int | float:
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise AnalysisError(f"invalid positive finite metric: {label}")
    return value


def _resolve_reference(reference: str) -> tuple[str, str]:
    path_text, separator, node = reference.partition("::")
    path = Path(path_text)
    if not path_text or path.is_absolute() or ".." in path.parts:
        raise AnalysisError(f"invalid repository-relative reference: {reference}")
    resolved = ROOT / path
    if not resolved.is_file():
        raise AnalysisError(f"unresolved evidence reference: {reference}")
    if separator and node.startswith("test_"):
        try:
            tree = ast.parse(read_utf8(resolved), filename=path_text)
        except SyntaxError as error:
            raise AnalysisError(f"invalid evidence test module: {path_text}") from error
        functions = {
            item.name
            for item in ast.walk(tree)
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if node not in functions:
            raise AnalysisError(f"unresolved pytest node: {reference}")
    return path_text, node


def validate_inventory(rows: list[dict[str, str]]) -> dict[str, Any]:
    """Validate and summarize the canonical test inventory."""

    if len(rows) != 100:
        raise AnalysisError("inventory must contain exactly 100 rows")
    ids = [row["test_id"] for row in rows]
    if len(set(ids)) != 100:
        raise AnalysisError("inventory contains duplicate test IDs")
    statuses = {row["status"] for row in rows}
    if not statuses <= {"implemented", "designed"}:
        raise AnalysisError("inventory contains an unknown status")
    implemented = sum(row["status"] == "implemented" for row in rows)
    designed_ids = {row["test_id"] for row in rows if row["status"] == "designed"}
    if implemented != 94 or designed_ids != OPTIONAL_IDS:
        raise AnalysisError("inventory does not reconcile to 94 implemented and six optional designed")
    return {
        "total": 100,
        "implemented": implemented,
        "designed": len(designed_ids),
        "optional_designed": len(designed_ids),
    }


def validate_traceability(
    rows: list[dict[str, str]], inventory_rows: list[dict[str, str]]
) -> dict[str, int]:
    """Validate requirements-to-test reconciliation."""

    if len(rows) != 66 or len({row["requirement_id"] for row in rows}) != 66:
        raise AnalysisError("traceability must contain 66 unique requirements")
    inventory_ids = {row["test_id"] for row in inventory_rows}
    for row in rows:
        ids = _references(row["planned_test_id"])
        if not ids or not set(ids) <= inventory_ids:
            raise AnalysisError(f"traceability test reference does not resolve: {row['requirement_id']}")
        if row["priority"] == "required" and row["status"] != "verified":
            raise AnalysisError(f"required requirement is unresolved: {row['requirement_id']}")
        if row["priority"] == "optional":
            if row["status"] != "optional_deferred" or not set(ids) <= OPTIONAL_IDS:
                raise AnalysisError(f"optional requirement is not deferred correctly: {row['requirement_id']}")
        elif row["priority"] != "required":
            raise AnalysisError(f"unknown requirement priority: {row['requirement_id']}")
    required = sum(row["priority"] == "required" for row in rows)
    optional = sum(row["priority"] == "optional" for row in rows)
    verified = sum(row["status"] == "verified" for row in rows)
    deferred = sum(row["status"] == "optional_deferred" for row in rows)
    if (required, optional, verified, deferred) != (60, 6, 60, 6):
        raise AnalysisError("traceability does not reconcile to 60 required and six optional")
    return {
        "total": 66,
        "required": required,
        "required_verified": verified,
        "optional": optional,
        "optional_deferred": deferred,
        "unresolved": 0,
    }


def validate_verification_records(
    rows: list[dict[str, str]], inventory_rows: list[dict[str, str]]
) -> dict[str, int]:
    """Validate final records, evidence resolution, and semantic provenance."""

    if len(rows) != 100:
        raise AnalysisError("verification records must contain exactly 100 rows")
    inventory_ids = [row["test_id"] for row in inventory_rows]
    if [row["test_id"] for row in rows] != inventory_ids:
        raise AnalysisError("verification records are not in inventory order")
    if len({row["test_id"] for row in rows}) != 100:
        raise AnalysisError("verification records contain duplicate test IDs")

    inventory_by_id = {row["test_id"]: row for row in inventory_rows}
    for row in rows:
        test_id = row["test_id"]
        source = inventory_by_id[test_id]
        for verification_field, inventory_field in (
            ("requirements", "requirements"),
            ("test_level", "test_level"),
            ("category", "module_or_flow"),
            ("input_or_configuration", "inputs"),
            ("expected_result", "expected_result"),
            ("expected_state", "expected_state"),
            ("expected_events", "expected_events"),
        ):
            if row[verification_field] != source[inventory_field]:
                raise AnalysisError(f"verification record does not match inventory: {test_id}")
        if row["actual_result"] == row["expected_result"]:
            raise AnalysisError(f"expected and actual result are not distinct: {test_id}")
        expected_status = "optional_deferred" if test_id in OPTIONAL_IDS else "passed"
        if row["evaluation_status"] != expected_status:
            raise AnalysisError(f"wrong verification status: {test_id}")
        if test_id in OPTIONAL_IDS:
            if row["actual_result"] != "not executed: optional post-MVP scope":
                raise AnalysisError(f"optional actual result changed: {test_id}")
        elif not row["actual_result"].startswith("passed:"):
            raise AnalysisError(f"passed record lacks an actual pass result: {test_id}")

        evidence_references = _references(row["evidence"])
        environment_references = set(_references(row["environment_reference"]))
        if not evidence_references or not environment_references:
            raise AnalysisError(f"missing verification reference: {test_id}")
        executable_paths: set[str] = set()
        for reference in evidence_references:
            path_text, node = _resolve_reference(reference)
            if node.startswith("test_"):
                if path_text not in TEST_VALIDATION_PROVENANCE:
                    raise AnalysisError(f"unmapped executable evidence: {reference}")
                executable_paths.add(path_text)
        for reference in environment_references:
            _resolve_reference(reference)

        originating = {TEST_VALIDATION_PROVENANCE[path] for path in executable_paths}
        if test_id in OPTIONAL_IDS:
            expected_environment = {"audit/validation/subproject_06_11_validation.md"}
        elif test_id in EXPERIMENT_TEST_IDS:
            expected_environment = {
                "audit/validation/subproject_06_10_validation.md",
                "results/scalability_environment.json",
            }
        elif test_id == "TST-TRC-005":
            expected_environment = {"audit/validation/subproject_06_11_validation.md"}
        else:
            if not executable_paths:
                raise AnalysisError(f"record has no executable evidence: {test_id}")
            expected_environment = originating
        if environment_references != expected_environment:
            raise AnalysisError(f"historically invalid environment provenance: {test_id}")

    passed = sum(row["evaluation_status"] == "passed" for row in rows)
    deferred = sum(row["evaluation_status"] == "optional_deferred" for row in rows)
    if (passed, deferred) != (94, 6):
        raise AnalysisError("verification records do not reconcile to 94 passed and six deferred")
    return {"passed": passed, "optional_deferred": deferred}


def extract_final_pytest_result(text: str) -> dict[str, int | float]:
    """Extract only the accepted final full-suite command result."""

    matches = list(FINAL_RESULT_PATTERN.finditer(text))
    if len(matches) != 1:
        raise AnalysisError("final validation must contain one canonical full-suite result")
    collected = int(matches[0].group("collected"))
    failed = int(matches[0].group("failed"))
    passed = collected - failed
    result: dict[str, int | float] = {
        "collected_tests": collected,
        "passed": passed,
        "failed": failed,
        "skipped": failed,
        "xfailed": failed,
        "pass_rate": passed / collected if collected else 0.0,
    }
    if result != {
        "collected_tests": 976,
        "passed": 976,
        "failed": 0,
        "skipped": 0,
        "xfailed": 0,
        "pass_rate": 1.0,
    }:
        raise AnalysisError("final full-suite result is not the accepted 976/976 result")
    return result


def validate_scalability_config(config: dict[str, Any]) -> dict[str, Any]:
    """Validate the complete frozen SP-06 scalability configuration."""

    _require_exact_keys(config, CONFIG_FIELDS, "scalability configuration")
    expected: dict[str, Any] = {
        "schema_version": 1,
        "configuration_id": "SP06_SCALABILITY_V1",
        "workload_id": "MIXED_REQUESTS_V1",
        "seed": 260516,
        "credential_counts": list(OFFICIAL_COUNTS),
        "minimum_request_count": 1000,
        "warmup_repetitions": 1,
        "measured_repetitions": 3,
        "profile": "PROJECT_WIEGAND_26",
        "output_duration_ms": 100,
        "watchdog_timeout_ms": 2000,
        "watchdog_enabled": False,
        "workload_mix_percent": dict(OFFICIAL_MIX),
    }
    if config != expected:
        raise AnalysisError("scalability configuration differs from the frozen profile")
    return config


def _hex_digest(value: object, label: str) -> str:
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise AnalysisError(f"invalid SHA-256 value: {label}")
    return value


def validate_scalability_results(
    document: dict[str, Any], config: dict[str, Any]
) -> list[dict[str, Any]]:
    """Validate all 12 accepted repetition-level aggregate rows."""

    _require_exact_keys(
        document,
        ("schema_version", "configuration_id", "workload_id", "seed", "timer", "results"),
        "scalability results",
    )
    if (
        document["schema_version"] != 1
        or document["configuration_id"] != config["configuration_id"]
        or document["workload_id"] != config["workload_id"]
        or document["seed"] != config["seed"]
        or document["timer"] != "time.perf_counter_ns"
    ):
        raise AnalysisError("scalability result metadata does not match configuration")
    rows = document["results"]
    if type(rows) is not list or len(rows) != 12:
        raise AnalysisError("scalability results must contain exactly 12 measured rows")

    seen: set[tuple[int, int]] = set()
    environment_ids: set[str] = set()
    checksums: dict[int, tuple[str, str]] = {}
    for index, row in enumerate(rows):
        if type(row) is not dict:
            raise AnalysisError(f"scalability row {index} must be an object")
        _require_exact_keys(row, RESULT_FIELDS, f"scalability row {index}")
        size = _require_int(row["credential_count"], "credential_count", minimum=1)
        repetition = _require_int(row["repetition"], "repetition", minimum=1)
        if size not in OFFICIAL_COUNTS or repetition not in (1, 2, 3):
            raise AnalysisError("scalability size or repetition is outside the frozen design")
        key = (size, repetition)
        if key in seen:
            raise AnalysisError("duplicate scalability size/repetition row")
        seen.add(key)
        request_count = OFFICIAL_REQUEST_COUNTS[size]
        if row["request_count"] != request_count or row["processed"] != request_count:
            raise AnalysisError("request and processed counts do not match the frozen workload")
        expected_granted = request_count * OFFICIAL_MIX["granted"] // 100
        expected_denied = {
            "unknown_credential": request_count * OFFICIAL_MIX["unknown_credential"] // 100,
            "disabled_credential": request_count * OFFICIAL_MIX["disabled_credential"] // 100,
            "unauthorized_floor": request_count * OFFICIAL_MIX["unauthorized_floor"] // 100,
        }
        expected_validation = {
            "invalid_frame": request_count * OFFICIAL_MIX["invalid_frame"] // 100
        }
        if row["granted"] != expected_granted or row["denied_by_reason"] != expected_denied:
            raise AnalysisError("scalability outcome counts do not match the frozen mix")
        if (
            row["validation_failures"] != expected_validation["invalid_frame"]
            or row["validation_by_reason"] != expected_validation
            or row["other_outcomes"] != 0
        ):
            raise AnalysisError("scalability validation or other outcome count is invalid")
        reconciled = (
            row["granted"]
            + sum(row["denied_by_reason"].values())
            + row["validation_failures"]
            + row["other_outcomes"]
        )
        if reconciled != row["processed"]:
            raise AnalysisError("scalability row outcomes do not reconcile")
        for metric in ("average_ns", "median_ns", "throughput_cases_per_second"):
            _require_positive_number(row[metric], metric)
        if type(row["p95_ns"]) is not int or row["p95_ns"] <= 0:
            raise AnalysisError("p95_ns must be a positive nearest-rank integer")
        pair = (
            _hex_digest(row["credential_checksum_sha256"], "credential checksum"),
            _hex_digest(row["request_checksum_sha256"], "request checksum"),
        )
        if size in checksums and checksums[size] != pair:
            raise AnalysisError("same-size generated-input checksums are inconsistent")
        checksums[size] = pair
        environment_id = row["environment_id"]
        if type(environment_id) is not str or not environment_id:
            raise AnalysisError("result environment ID is invalid")
        environment_ids.add(environment_id)
    expected_pairs = {(size, repetition) for size in OFFICIAL_COUNTS for repetition in (1, 2, 3)}
    if seen != expected_pairs:
        raise AnalysisError("scalability repetition set is incomplete")
    if len(environment_ids) != 1:
        raise AnalysisError("scalability rows must use one environment ID")
    return rows


def validate_environment(
    environment: dict[str, Any], config: dict[str, Any], result_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    """Validate the bounded, non-raw accepted environment record."""

    _require_exact_keys(environment, ENVIRONMENT_FIELDS, "scalability environment")
    environment_ids = {row["environment_id"] for row in result_rows}
    if (
        environment["schema_version"] != 1
        or {environment["environment_id"]} != environment_ids
        or environment["configuration_id"] != config["configuration_id"]
        or environment["workload_id"] != config["workload_id"]
        or environment["seed"] != config["seed"]
        or environment["credential_counts"] != list(OFFICIAL_COUNTS)
        or environment["minimum_request_count"] != 1000
        or environment["warmup_repetitions"] != 1
        or environment["measured_repetitions"] != 3
        or environment["timer"] != "time.perf_counter_ns"
        or environment["interpretation_limits"] != list(INTERPRETATION_LIMITS)
    ):
        raise AnalysisError("environment record does not match results and frozen configuration")
    if any(key in environment for key in ("hostname", "username", "cwd", "raw_samples", "requests")):
        raise AnalysisError("environment contains an unsupported identifying or raw-data field")
    return environment


EXPERIMENT_DEFINITIONS = (
    {
        "experiment_id": "EXP-01",
        "experiment_name": "Protocol validation",
        "planned_question": "Does the proposed PROJECT_WIEGAND_26 software profile preserve source metadata, field allocation, parity, fixed vectors, and corruption rejection?",
        "mapped_test_ids": (
            "TST-SRC-001", "TST-SRC-002", "TST-WIE-001", "TST-WIE-002", "TST-WIE-003",
            "TST-WIE-004", "TST-WIE-005", "TST-WIE-006", "TST-WIE-007", "TST-WIE-008",
            "TST-DAT-001", "TST-DAT-002", "TST-DAT-003",
        ),
        "evidence_status": "complete_existing",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "Software-only validation of the proposed 26-bit profile; it is not evidence of physical RFID reader or commercial-card compatibility.",
        "next_action": "Retain the accepted software evidence; no additional SP-07.1 measurement is authorized.",
    },
    {
        "experiment_id": "EXP-02",
        "experiment_name": "Authorization correctness",
        "planned_question": "Does the accepted software model distinguish repository identity and produce the specified enabled, disabled, unknown, floor-range, and floor-mask outcomes?",
        "mapped_test_ids": (
            "TST-CRD-001", "TST-CRD-002", "TST-CRD-003", "TST-CRD-004", "TST-CRD-005",
            "TST-AUT-001", "TST-AUT-002", "TST-AUT-003", "TST-AUT-004", "TST-AUT-005", "TST-DAT-004",
        ),
        "evidence_status": "complete_existing",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "Correctness applies to the deterministic in-memory repository and logical floors 1-16, not a deployed access database.",
        "next_action": "Retain the accepted correctness evidence; isolate timing only in the bounded SP-07.2 experiment.",
    },
    {
        "experiment_id": "EXP-03",
        "experiment_name": "Output timing",
        "planned_question": "Does simulated time enforce the one-output invariant, timeout boundaries, long output scheduling, and partition equivalence?",
        "mapped_test_ids": (
            "TST-OUT-001", "TST-OUT-002", "TST-OUT-003", "TST-OUT-004", "TST-OUT-005",
            "TST-TIM-001", "TST-TIM-002", "TST-TIM-003", "TST-TIM-004", "TST-TIM-005", "TST-INV-001",
        ),
        "evidence_status": "complete_existing_with_limit",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "The boundaries are deterministic simulated milliseconds and do not measure host, electrical-output, or elevator timing.",
        "next_action": "Keep simulated-time conclusions separate from later host-timing analysis; no physical measurement is planned in SP-07.1.",
    },
    {
        "experiment_id": "EXP-04",
        "experiment_name": "Watchdog and fault recovery",
        "planned_question": "Does the software model schedule watchdog actions, suppress service, resolve collisions, reset once, preserve owned data, and recover from logging faults?",
        "mapped_test_ids": (
            "TST-WDG-001", "TST-WDG-002", "TST-WDG-003", "TST-WDG-004", "TST-WDG-005", "TST-WDG-006",
            "TST-RST-001", "TST-RST-002", "TST-RST-003", "TST-RST-004", "TST-RST-005", "TST-RST-006",
            "TST-LOG-005", "TST-LOG-006", "TST-LOG-007",
        ),
        "evidence_status": "complete_existing_with_limit",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "Recovery evidence covers deterministic software state and injected logging failures, not hardware reliability, field reliability, or safety certification.",
        "next_action": "Retain the accepted verification status; do not infer a failure rate from scenario tests.",
    },
    {
        "experiment_id": "EXP-05",
        "experiment_name": "Database scalability",
        "planned_question": "What mixed controller request-processing host timing is present across 10, 100, 1000, and 10000 credentials, and which isolated measurements are still absent?",
        "mapped_test_ids": ("TST-REP-001", "TST-REP-002", "TST-SCL-001", "TST-SCL-002", "TST-SCL-003"),
        "evidence_status": "gap_identified",
        "quantitative_artifacts": (
            "experiments/scalability_config.json", "results/scalability_results.json", "results/scalability_environment.json"
        ),
        "scope_limit": "The accepted metrics time mixed Controller.submit request processing on one recorded host; isolated credential-repository and authorization timing are not independently available.",
        "next_action": "SP-07.2 will run the smallest controlled experiment for isolated credential lookup, isolated authorization, and an explicit expected-versus-actual outcome matrix.",
    },
    {
        "experiment_id": "EXP-06",
        "experiment_name": "End-to-end scenarios",
        "planned_question": "Do accepted LF/HF grant, denial, busy, invalid-input, timeout, watchdog-recovery, and state-transition scenarios produce the required software outcomes?",
        "mapped_test_ids": (
            "TST-E2E-001", "TST-E2E-002", "TST-E2E-003", "TST-E2E-004", "TST-E2E-005", "TST-E2E-006", "TST-E2E-007", "TST-STA-001"
        ),
        "evidence_status": "complete_existing",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "These are deterministic software scenarios with logical reader labels and outputs, not physical elevator journeys or operational trials.",
        "next_action": "Retain the accepted scenario evidence; no new end-to-end benchmark is authorized for SP-07.1.",
    },
    {
        "experiment_id": "EXP-07",
        "experiment_name": "Robustness and malformed configuration",
        "planned_question": "Does the software reject malformed frames, strict-UTF-8 and schema errors, invalid records, and duplicates while permitting corrected-startup recovery?",
        "mapped_test_ids": (
            "TST-WIE-001", "TST-WIE-002", "TST-WIE-003", "TST-WIE-004", "TST-WIE-005", "TST-WIE-007",
            "TST-CRD-002", "TST-CRD-003", "TST-CRD-005", "TST-CRD-006",
            "TST-CFG-001", "TST-CFG-002", "TST-CFG-003", "TST-CFG-004", "TST-CFG-005", "TST-RST-004",
        ),
        "additional_evidence_references": EXP07_REQUIRED_EVIDENCE
        + (
            "audit/validation/subproject_06_08_validation.md",
            "audit/validation/subproject_06_07_validation.md",
        ),
        "evidence_status": "complete_existing",
        "quantitative_artifacts": ("audit/validation/subproject_06_11_verification_records.csv",),
        "scope_limit": "Robustness is bounded to specified software inputs and failure injection; it is not field-reliability or adversarial-security evidence.",
        "next_action": "Retain the accepted malformed-input coverage; any broader security study requires separate authorization.",
    },
)


def build_experiment_catalog(
    inventory_rows: list[dict[str, str]], verification_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Build the ordered seven-experiment evidence catalog."""

    inventory = {row["test_id"]: row for row in inventory_rows}
    verification = {row["test_id"]: row for row in verification_rows}
    catalog: list[dict[str, str]] = []
    for definition in EXPERIMENT_DEFINITIONS:
        test_ids = definition["mapped_test_ids"]
        if not test_ids or not set(test_ids) <= set(inventory):
            raise AnalysisError(f"catalog test mapping does not resolve: {definition['experiment_id']}")
        if any(inventory[test_id]["status"] != "implemented" for test_id in test_ids):
            raise AnalysisError(f"catalog presents optional work as executed: {definition['experiment_id']}")
        evidence: list[str] = []
        for test_id in test_ids:
            for reference in _references(verification[test_id]["evidence"]):
                _resolve_reference(reference)
                if reference not in evidence:
                    evidence.append(reference)
        for reference in definition.get("additional_evidence_references", ()):
            _resolve_reference(reference)
            if reference not in evidence:
                evidence.append(reference)
        for reference in definition["quantitative_artifacts"]:
            _resolve_reference(reference)
        row = {
            "experiment_id": definition["experiment_id"],
            "experiment_name": definition["experiment_name"],
            "planned_question": definition["planned_question"],
            "mapped_test_ids": ";".join(test_ids),
            "evidence_references": ";".join(evidence),
            "evidence_status": definition["evidence_status"],
            "quantitative_artifacts": ";".join(definition["quantitative_artifacts"]),
            "scope_limit": definition["scope_limit"],
            "next_action": definition["next_action"],
        }
        if any(not value for value in row.values()):
            raise AnalysisError(f"catalog row contains an empty field: {definition['experiment_id']}")
        if row["evidence_status"] not in {
            "complete_existing", "complete_existing_with_limit", "gap_identified"
        }:
            raise AnalysisError(f"catalog evidence status is invalid: {definition['experiment_id']}")
        if row["evidence_status"] == "gap_identified" and "SP-07.2" not in row["next_action"]:
            raise AnalysisError(f"catalog gap lacks a bounded later action: {definition['experiment_id']}")
        catalog.append(row)
    validate_experiment_evidence(catalog)
    return catalog


def validate_experiment_evidence(catalog: list[dict[str, str]]) -> None:
    """Require direct evidence that is semantically mandatory for EXP-07."""

    matches = [row for row in catalog if row.get("experiment_id") == "EXP-07"]
    if len(matches) != 1:
        raise AnalysisError("EXP-07 evidence sufficiency requires exactly one catalog row")
    row = matches[0]
    evidence = _references(row.get("evidence_references", ""))
    missing = [reference for reference in EXP07_REQUIRED_EVIDENCE if reference not in evidence]
    if missing:
        raise AnalysisError(f"EXP-07 mandatory direct evidence is missing: {missing[0]}")
    if row.get("evidence_status") != "complete_existing":
        raise AnalysisError("EXP-07 mandatory evidence requires complete_existing status")


def safe_descriptive_statistics(values: Sequence[int | float], label: str) -> dict[str, int | float]:
    """Summarize exactly three finite positive repetition-level aggregates."""

    if len(values) != 3:
        raise AnalysisError(f"{label} requires exactly three repetition aggregates")
    checked = [_require_positive_number(value, label) for value in values]
    return {
        "minimum": min(checked),
        "median": statistics.median(checked),
        "maximum": max(checked),
    }


def _sum_nested(rows: list[dict[str, Any]], field: str, member: str) -> int:
    return sum(row[field][member] for row in rows)


def build_summary(
    *,
    source_paths: Sequence[tuple[str, Path]],
    verification_summary: dict[str, int | float],
    requirements_summary: dict[str, int],
    inventory_summary: dict[str, Any],
    verification_record_summary: dict[str, int],
    catalog: list[dict[str, str]],
    config: dict[str, Any],
    result_document: dict[str, Any],
    result_rows: list[dict[str, Any]],
    environment: dict[str, Any],
) -> dict[str, Any]:
    """Construct the ordered, deterministic quantitative baseline object."""

    per_size: list[dict[str, Any]] = []
    for size in OFFICIAL_COUNTS:
        rows = [row for row in result_rows if row["credential_count"] == size]
        rows.sort(key=lambda row: row["repetition"])
        per_size.append(
            {
                "credential_count": size,
                "request_count_per_repetition": OFFICIAL_REQUEST_COUNTS[size],
                "repetition_count": len(rows),
                "repetition_average_ns": safe_descriptive_statistics(
                    [row["average_ns"] for row in rows], "repetition average nanoseconds"
                ),
                "repetition_median_ns": safe_descriptive_statistics(
                    [row["median_ns"] for row in rows], "repetition median nanoseconds"
                ),
                "repetition_nearest_rank_p95_ns": safe_descriptive_statistics(
                    [row["p95_ns"] for row in rows], "repetition nearest-rank p95 nanoseconds"
                ),
                "throughput_cases_per_second": safe_descriptive_statistics(
                    [row["throughput_cases_per_second"] for row in rows], "throughput"
                ),
            }
        )

    total_processed = sum(row["processed"] for row in result_rows)
    total_granted = sum(row["granted"] for row in result_rows)
    total_denied_by_reason = {
        "unauthorized_floor": _sum_nested(result_rows, "denied_by_reason", "unauthorized_floor"),
        "disabled_credential": _sum_nested(result_rows, "denied_by_reason", "disabled_credential"),
        "unknown_credential": _sum_nested(result_rows, "denied_by_reason", "unknown_credential"),
    }
    total_validation_by_reason = {
        "invalid_frame": _sum_nested(result_rows, "validation_by_reason", "invalid_frame")
    }
    total_denied = sum(total_denied_by_reason.values())
    total_validation_failures = sum(row["validation_failures"] for row in result_rows)
    total_other = sum(row["other_outcomes"] for row in result_rows)
    if (
        total_processed,
        total_granted,
        total_denied,
        total_denied_by_reason["unauthorized_floor"],
        total_denied_by_reason["disabled_credential"],
        total_denied_by_reason["unknown_credential"],
        total_validation_failures,
        total_other,
    ) != (39000, 15600, 19500, 7800, 5850, 5850, 3900, 0):
        raise AnalysisError("derived scalability totals do not match the frozen workload")

    inventory = dict(inventory_summary)
    inventory["verification_records_passed"] = verification_record_summary["passed"]
    inventory["verification_records_optional_deferred"] = verification_record_summary[
        "optional_deferred"
    ]
    summary = {
        "schema_version": 1,
        "analysis_id": ANALYSIS_ID,
        "source_artifacts": [
            {"path": name, "sha256": source_sha256(path)} for name, path in source_paths
        ],
        "verification_summary": verification_summary,
        "requirements_summary": requirements_summary,
        "inventory_summary": inventory,
        "experiment_coverage": [
            {
                "experiment_id": row["experiment_id"],
                "experiment_name": row["experiment_name"],
                "evidence_status": row["evidence_status"],
                "mapped_test_count": len(_references(row["mapped_test_ids"])),
            }
            for row in catalog
        ],
        "scalability_summary": {
            "configuration_id": config["configuration_id"],
            "workload_id": config["workload_id"],
            "seed": config["seed"],
            "timer": result_document["timer"],
            "environment_id": environment["environment_id"],
            "credential_sizes": list(OFFICIAL_COUNTS),
            "request_counts": [OFFICIAL_REQUEST_COUNTS[size] for size in OFFICIAL_COUNTS],
            "measured_repetitions": config["measured_repetitions"],
            "total_measured_rows": len(result_rows),
            "total_processed_requests": total_processed,
            "total_granted": total_granted,
            "total_denied": total_denied,
            "total_denied_by_reason": total_denied_by_reason,
            "total_validation_failures": total_validation_failures,
            "total_validation_by_reason": total_validation_by_reason,
            "total_other_outcomes": total_other,
            "per_size_descriptive_summaries": per_size,
        },
        "metric_availability": {
            "available": [
                {"metric": "total_pytest_count", "value": verification_summary["collected_tests"]},
                {"metric": "automated_pass_rate", "value": verification_summary["pass_rate"]},
                {"metric": "required_requirement_verification_count", "value": requirements_summary["required_verified"]},
                {"metric": "inventory_evidence_count", "value": inventory_summary["implemented"]},
                {"metric": "grant_count_in_frozen_mixed_workload", "value": total_granted},
                {"metric": "denial_counts_by_reason", "value": total_denied_by_reason},
                {"metric": "validation_failure_count", "value": total_validation_failures},
                {"metric": "unexpected_outcomes", "value": total_other},
                {"metric": "repetition_level_average_ns", "value": "per_size_descriptive_summaries"},
                {"metric": "repetition_level_median_ns", "value": "per_size_descriptive_summaries"},
                {"metric": "repetition_level_nearest_rank_p95_ns", "value": "per_size_descriptive_summaries"},
                {"metric": "throughput_cases_per_second", "value": "per_size_descriptive_summaries"},
                {"metric": "watchdog_and_reset_verification_status", "value": "passed"},
                {"metric": "output_invariant_verification_status", "value": "passed"},
            ],
            "not_independently_available": [
                {"metric": "isolated_credential_lookup_timing", "value": None},
                {"metric": "isolated_authorization_timing", "value": None},
                {"metric": "raw_per_request_timing_samples", "value": None},
                {"metric": "pooled_request_median", "value": None},
                {"metric": "pooled_request_p95", "value": None},
                {"metric": "independently_measured_incorrect_grant_count", "value": None},
                {"metric": "independently_measured_incorrect_denial_count", "value": None},
                {"metric": "branch_coverage", "value": None},
                {"metric": "physical_reader_timing", "value": None},
                {"metric": "electrical_output_timing", "value": None},
                {"metric": "elevator_movement_timing", "value": None},
                {"metric": "field_reliability", "value": None},
                {"metric": "safety_or_certification_evidence", "value": None},
            ],
        },
        "limitations": [
            "The official observations are mixed Controller.submit request-processing host timing, not isolated credential-repository or authorization timing.",
            "Each per-size statistic summarizes three repetition-level aggregate rows; raw per-request timing samples are unavailable.",
            "A median of repetition medians and a median of repetition p95 values are not pooled request percentiles.",
            "Host timing is observational and variable; no performance threshold or real-time guarantee is established.",
            "Exact expected outcome reconciliation and zero other outcomes do not independently measure incorrect-grant or incorrect-denial counts.",
            "The evidence is software-only and does not establish physical RFID, electrical-output, elevator, field-reliability, safety, certification, or commercial performance.",
        ],
        "deferred_work": [
            {
                "stage": "SP-07.2",
                "work": "Measure isolated credential lookup and isolated authorization with controlled sizes and repetitions, and produce an explicit expected-versus-actual outcome matrix.",
            },
            {"stage": "SP-07.3", "work": "Generate tables and figures only from accepted machine-readable results."},
            {"stage": "SP-07.4", "work": "Perform independent review and prepare bounded results/discussion source notes."},
        ],
    }
    if tuple(summary) != SUMMARY_FIELDS:
        raise AnalysisError("internal summary field order is invalid")
    return summary


def serialize_catalog(rows: list[dict[str, str]]) -> bytes:
    """Serialize catalog rows as deterministic UTF-8 CSV."""

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=CATALOG_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def serialize_summary(summary: dict[str, Any]) -> bytes:
    """Serialize the summary as stable, readable UTF-8 JSON."""

    return (json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _stage_bytes(path: Path, content: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return temporary


def _validate_serialized_outputs(catalog_bytes: bytes, summary_bytes: bytes) -> None:
    try:
        catalog_text = catalog_bytes.decode("utf-8", errors="strict")
        reader = csv.DictReader(io.StringIO(catalog_text, newline=""))
        rows = list(reader)
        if tuple(reader.fieldnames or ()) != CATALOG_COLUMNS or len(rows) != 7:
            raise AnalysisError("serialized catalog failed post-write parsing")
        summary = json.loads(
            summary_bytes.decode("utf-8", errors="strict"),
            object_pairs_hook=_object_from_pairs,
            parse_constant=_reject_constant,
        )
        if type(summary) is not dict or tuple(summary) != SUMMARY_FIELDS:
            raise AnalysisError("serialized summary failed post-write parsing")
    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as error:
        raise AnalysisError("serialized output failed post-write parsing") from error


def write_outputs_atomically(
    catalog_path: Path,
    catalog_rows: list[dict[str, str]],
    summary_path: Path,
    summary: dict[str, Any],
) -> tuple[str, str]:
    """Publish two validated outputs, rolling both back on a handled failure."""

    if catalog_path.resolve() == summary_path.resolve():
        raise AnalysisError("catalog and summary outputs must be different paths")
    catalog_bytes = serialize_catalog(catalog_rows)
    summary_bytes = serialize_summary(summary)
    _validate_serialized_outputs(catalog_bytes, summary_bytes)
    previous: dict[Path, bytes | None] = {}
    for path in (catalog_path, summary_path):
        try:
            previous[path] = path.read_bytes() if path.exists() else None
        except OSError as error:
            raise AnalysisError(f"cannot preserve existing output: {path}") from error
    staged: list[Path] = []
    try:
        staged = [_stage_bytes(catalog_path, catalog_bytes), _stage_bytes(summary_path, summary_bytes)]
        os.replace(staged[0], catalog_path)
        staged[0] = Path()
        os.replace(staged[1], summary_path)
        staged[1] = Path()
        if catalog_path.read_bytes() != catalog_bytes or summary_path.read_bytes() != summary_bytes:
            raise OSError("published output verification failed")
        _validate_serialized_outputs(catalog_path.read_bytes(), summary_path.read_bytes())
    except (OSError, AnalysisError) as error:
        restore_errors: list[OSError] = []
        for path, content in previous.items():
            try:
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    restoration = _stage_bytes(path, content)
                    os.replace(restoration, path)
            except OSError as restore_error:
                restore_errors.append(restore_error)
        if restore_errors:
            raise AnalysisError("output publication and rollback failed") from error
        raise AnalysisError("output publication failed; existing outputs were preserved") from error
    finally:
        for temporary in staged:
            if temporary != Path():
                temporary.unlink(missing_ok=True)
    return hashlib.sha256(catalog_bytes).hexdigest(), hashlib.sha256(summary_bytes).hexdigest()


def build_analysis(arguments: argparse.Namespace) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Validate all canonical inputs and construct both complete output objects."""

    source_paths = (
        (CANONICAL_SOURCES[0], arguments.verification_records),
        (CANONICAL_SOURCES[1], arguments.inventory),
        (CANONICAL_SOURCES[2], arguments.traceability),
        (CANONICAL_SOURCES[3], arguments.final_validation),
        (CANONICAL_SOURCES[4], arguments.scalability_config),
        (CANONICAL_SOURCES[5], arguments.scalability_results),
        (CANONICAL_SOURCES[6], arguments.scalability_environment),
    )
    inventory_rows = load_csv(arguments.inventory, INVENTORY_COLUMNS)
    inventory_summary = validate_inventory(inventory_rows)
    traceability_rows = load_csv(arguments.traceability, TRACEABILITY_COLUMNS)
    requirements_summary = validate_traceability(traceability_rows, inventory_rows)
    verification_rows = load_csv(arguments.verification_records, VERIFICATION_COLUMNS)
    record_summary = validate_verification_records(verification_rows, inventory_rows)
    final_result = extract_final_pytest_result(read_utf8(arguments.final_validation))
    config = validate_scalability_config(load_json(arguments.scalability_config))
    result_document = load_json(arguments.scalability_results)
    result_rows = validate_scalability_results(result_document, config)
    environment = validate_environment(
        load_json(arguments.scalability_environment), config, result_rows
    )
    catalog = build_experiment_catalog(inventory_rows, verification_rows)
    summary = build_summary(
        source_paths=source_paths,
        verification_summary=final_result,
        requirements_summary=requirements_summary,
        inventory_summary=inventory_summary,
        verification_record_summary=record_summary,
        catalog=catalog,
        config=config,
        result_document=result_document,
        result_rows=result_rows,
        environment=environment,
    )
    return catalog, summary


def validate_canonical_source_paths(arguments: argparse.Namespace) -> None:
    """Prevent CLI inputs from being labeled as different canonical sources."""

    for argument_name, relative_path in zip(
        CANONICAL_SOURCE_ARGUMENTS, CANONICAL_SOURCES, strict=True
    ):
        supplied = getattr(arguments, argument_name)
        try:
            supplied_path = supplied.resolve(strict=True)
            canonical_path = (ROOT / relative_path).resolve(strict=True)
        except OSError as error:
            raise AnalysisError(
                f"canonical source path cannot be resolved: --{argument_name.replace('_', '-')}"
            ) from error
        if supplied_path != canonical_path:
            raise AnalysisError(
                f"canonical source path mismatch: --{argument_name.replace('_', '-')}"
            )


def build_parser() -> argparse.ArgumentParser:
    """Build the required-path command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    for option in (
        "verification-records", "inventory", "traceability", "final-validation",
        "scalability-config", "scalability-results", "scalability-environment",
        "catalog-output", "summary-output",
    ):
        parser.add_argument(f"--{option}", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate, consolidate, and atomically publish the SP-07.1 baseline."""

    arguments = build_parser().parse_args(argv)
    try:
        validate_canonical_source_paths(arguments)
        catalog, summary = build_analysis(arguments)
        catalog_hash, summary_hash = write_outputs_atomically(
            arguments.catalog_output, catalog, arguments.summary_output, summary
        )
    except (AnalysisError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        "completed: experiments=7 measured_rows=12 processed=39000 "
        f"catalog_sha256={catalog_hash} summary_sha256={summary_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
