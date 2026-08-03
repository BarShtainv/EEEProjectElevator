#!/usr/bin/env python3
"""Generate deterministic SP-07.3 tables and SVG figures from accepted evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import statistics
import sys
import tempfile
import xml.etree.ElementTree as ET


class ArtifactError(Exception):
    """A handled source, schema, reconciliation, serialization, or publication error."""


ROOT = Path(__file__).resolve().parents[1]
SIZES = (10, 100, 1000, 10000)
OPERATIONS = ("mixed_controller_submit", "credential_repository_lookup", "authorization_decision")
CATALOG_COLUMNS = (
    "experiment_id", "experiment_name", "planned_question", "mapped_test_ids",
    "evidence_references", "evidence_status", "quantitative_artifacts", "scope_limit",
    "next_action",
)
COVERAGE_COLUMNS = (
    "experiment_id", "experiment_name", "evidence_status", "primary_evidence",
    "quantitative_artifacts", "scope_limit",
)
CORRECTNESS_COLUMNS = ("measurement_group", "metric", "value", "unit", "evidence", "scope_note")
TIMING_COLUMNS = (
    "measurement_id", "operation", "credential_count", "repetition_count",
    "calls_per_repetition", "total_measured_calls", "timer", "average_ns_min",
    "average_ns_median", "average_ns_max", "median_ns_min", "median_ns_median",
    "median_ns_max", "p95_ns_min", "p95_ns_median", "p95_ns_max",
    "throughput_min", "throughput_median", "throughput_max", "interpretation",
)
SUMMARY_FIELDS = (
    "schema_version", "analysis_id", "source_artifacts", "verification_summary",
    "requirements_summary", "inventory_summary", "experiment_coverage",
    "mixed_controller_summary", "isolated_operation_summary", "correctness_summary",
    "timing_summary", "metric_availability", "limitations", "deferred_work",
)
CANONICAL_INPUTS = {
    "historical_catalog": "data/results/sp07_experiment_catalog.csv",
    "historical_summary": "data/results/sp07_quantitative_summary.json",
    "mixed_config": "experiments/scalability_config.json",
    "mixed_results": "results/scalability_results.json",
    "mixed_environment": "results/scalability_environment.json",
    "isolated_config": "experiments/isolated_operations_config.json",
    "isolated_results": "data/results/sp07_isolated_operation_results.json",
    "isolated_environment": "data/results/sp07_isolated_operation_environment.json",
    "isolated_repair_validation": "audit/validation/subproject_07_02_timing_boundary_repair.md",
}
CANONICAL_HASHES = {
    "data/results/sp07_experiment_catalog.csv": "c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb",
    "data/results/sp07_quantitative_summary.json": "dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0",
    "experiments/scalability_config.json": "93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921",
    "results/scalability_results.json": "009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f",
    "results/scalability_environment.json": "ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba",
    "experiments/isolated_operations_config.json": "6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838",
    "data/results/sp07_isolated_operation_results.json": "9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf",
    "data/results/sp07_isolated_operation_environment.json": "106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec",
    "audit/validation/subproject_07_02_timing_boundary_repair.md": "1524a88db09641bd5f31a0411341d0e0e9b454ff2502ea99948fefc50879ef90",
}
GENERATED_PATHS = {
    "integrated_catalog": "data/results/sp07_experiment_catalog_integrated.csv",
    "integrated_summary": "data/results/sp07_quantitative_summary_integrated.json",
    "coverage_table": "data/results/sp07_table_experiment_coverage.csv",
    "correctness_table": "data/results/sp07_table_correctness.csv",
    "timing_table": "data/results/sp07_table_timing_summary.csv",
    "mixed_figure": "docs/figures/sp07_mixed_controller_average_ns.svg",
    "lookup_figure": "docs/figures/sp07_lookup_average_ns.svg",
    "authorization_figure": "docs/figures/sp07_authorization_average_ns.svg",
    "manifest": "data/results/sp07_report_artifact_manifest.json",
}


def read_utf8(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise ArtifactError(f"cannot read strict UTF-8 source {path}: {exc}") from exc


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ArtifactError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(
            read_utf8(path), object_pairs_hook=_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ArtifactError(f"invalid JSON constant: {value}")),
        )
    except json.JSONDecodeError as exc:
        raise ArtifactError(f"source is not valid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ArtifactError(f"JSON source must be an object: {path}")
    return value


def load_csv(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    try:
        reader = csv.DictReader(io.StringIO(read_utf8(path), newline=""))
        if tuple(reader.fieldnames or ()) != columns:
            raise ArtifactError(f"CSV columns do not match required schema: {path}")
        rows = list(reader)
    except csv.Error as exc:
        raise ArtifactError(f"source is not valid CSV: {path}") from exc
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ArtifactError(f"CSV row width is invalid: {path}")
    return rows


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as exc:
        raise ArtifactError(f"cannot hash source {path}: {exc}") from exc


def validate_canonical_sources(paths: dict[str, Path]) -> None:
    if set(paths) != set(CANONICAL_INPUTS):
        raise ArtifactError("canonical source argument set is incomplete")
    for name, relative in CANONICAL_INPUTS.items():
        expected = (ROOT / relative).resolve()
        try:
            supplied = paths[name].resolve(strict=True)
        except OSError as exc:
            raise ArtifactError(f"canonical source is unavailable: {relative}") from exc
        if supplied != expected:
            raise ArtifactError(f"source path is not the canonical repository file: {relative}")
        if sha256_path(supplied) != CANONICAL_HASHES[relative]:
            raise ArtifactError(f"canonical source hash mismatch: {relative}")


def validate_historical_catalog(rows: list[dict[str, str]]) -> None:
    if len(rows) != 7 or [row["experiment_id"] for row in rows] != [f"EXP-{n:02d}" for n in range(1, 8)]:
        raise ArtifactError("historical catalog must contain ordered EXP-01 through EXP-07")
    valid = {"complete_existing", "complete_existing_with_limit", "gap_identified"}
    if any(not all(row.values()) or row["evidence_status"] not in valid for row in rows):
        raise ArtifactError("historical catalog contains an invalid or empty field")
    if rows[4]["evidence_status"] != "gap_identified":
        raise ArtifactError("historical EXP-05 must remain gap_identified")
    required_exp07 = (
        "test_configuration_file_failures_keep_configuration_identity",
        "test_credential_file_failures_keep_credential_identity",
        "test_corrected_initialization_after_failure_clears_error_event",
    )
    if not all(value in rows[6]["evidence_references"] for value in required_exp07):
        raise ArtifactError("historical EXP-07 direct evidence is incomplete")
    for row in rows:
        for reference in (row["evidence_references"] + ";" + row["quantitative_artifacts"]).split(";"):
            path = reference.split("::", 1)[0]
            if not path or Path(path).is_absolute() or not (ROOT / path).is_file():
                raise ArtifactError(f"catalog reference does not resolve: {reference}")


def validate_historical_summary(summary: dict[str, object]) -> None:
    if summary.get("schema_version") != 1 or summary.get("analysis_id") != "SP07_ANALYSIS_BASELINE_V1":
        raise ArtifactError("historical summary identity is invalid")
    verification = summary.get("verification_summary")
    requirements = summary.get("requirements_summary")
    inventory = summary.get("inventory_summary")
    scalability = summary.get("scalability_summary")
    if not isinstance(verification, dict) or (verification.get("collected_tests"), verification.get("passed"), verification.get("pass_rate")) != (976, 976, 1.0):
        raise ArtifactError("historical verification snapshot is invalid")
    if not isinstance(requirements, dict) or (requirements.get("required_verified"), requirements.get("optional_deferred")) != (60, 6):
        raise ArtifactError("historical requirements summary is invalid")
    if not isinstance(inventory, dict) or (inventory.get("implemented"), inventory.get("optional_designed")) != (94, 6):
        raise ArtifactError("historical inventory summary is invalid")
    if not isinstance(summary.get("experiment_coverage"), list) or len(summary["experiment_coverage"]) != 7:
        raise ArtifactError("historical experiment coverage is invalid")
    if not isinstance(scalability, dict) or (scalability.get("total_measured_rows"), scalability.get("total_processed_requests")) != (12, 39000):
        raise ArtifactError("historical mixed-controller summary is invalid")
    unavailable = summary.get("metric_availability", {}).get("not_independently_available", [])  # type: ignore[union-attr]
    unavailable_map = {item["metric"]: item["value"] for item in unavailable if isinstance(item, dict)}
    if unavailable_map.get("isolated_credential_lookup_timing", object()) is not None or unavailable_map.get("isolated_authorization_timing", object()) is not None:
        raise ArtifactError("historical isolated timing must remain unavailable")
    actual_hashes = {item["path"]: item["sha256"] for item in summary.get("source_artifacts", []) if isinstance(item, dict)}
    for path in ("experiments/scalability_config.json", "results/scalability_results.json", "results/scalability_environment.json"):
        if actual_hashes.get(path) != CANONICAL_HASHES[path]:
            raise ArtifactError("historical summary source hashes are invalid")


def _positive_metrics(row: dict[str, object]) -> None:
    for field in ("average_ns", "median_ns", "p95_ns", "throughput_cases_per_second"):
        value = row.get(field)
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ArtifactError(f"invalid timing metric: {field}")


def validate_mixed(config: dict[str, object], result: dict[str, object], environment: dict[str, object]) -> list[dict[str, object]]:
    identity = ("SP06_SCALABILITY_V1", "MIXED_REQUESTS_V1", 260516)
    if (config.get("configuration_id"), config.get("workload_id"), config.get("seed")) != identity:
        raise ArtifactError("mixed configuration identity is invalid")
    if config.get("credential_counts") != list(SIZES) or (config.get("warmup_repetitions"), config.get("measured_repetitions")) != (1, 3):
        raise ArtifactError("mixed repetition policy is invalid")
    if config.get("workload_mix_percent") != {"granted": 40, "unauthorized_floor": 20, "disabled_credential": 15, "unknown_credential": 15, "invalid_frame": 10}:
        raise ArtifactError("mixed outcome percentages are invalid")
    if (result.get("configuration_id"), result.get("workload_id"), result.get("seed")) != identity:
        raise ArtifactError("mixed result identity is invalid")
    rows = result.get("results")
    if not isinstance(rows, list) or len(rows) != 12:
        raise ArtifactError("mixed results must contain 12 rows")
    expected_order = [(size, rep) for size in SIZES for rep in (1, 2, 3)]
    if [(row.get("credential_count"), row.get("repetition")) for row in rows if isinstance(row, dict)] != expected_order:
        raise ArtifactError("mixed result order is invalid")
    request_counts = {10: 1000, 100: 1000, 1000: 1000, 10000: 10000}
    for row in rows:
        if not isinstance(row, dict):
            raise ArtifactError("mixed result row is invalid")
        count = request_counts[row["credential_count"]]  # type: ignore[index]
        expected = {"granted": count * 40 // 100, "unauthorized_floor": count * 20 // 100, "disabled_credential": count * 15 // 100, "unknown_credential": count * 15 // 100, "invalid_frame": count * 10 // 100}
        if row.get("request_count") != count or row.get("processed") != count or row.get("granted") != expected["granted"]:
            raise ArtifactError("mixed processed or grant count is invalid")
        if row.get("denied_by_reason") != {"unknown_credential": expected["unknown_credential"], "disabled_credential": expected["disabled_credential"], "unauthorized_floor": expected["unauthorized_floor"]}:
            raise ArtifactError("mixed denial counts are invalid")
        if row.get("validation_by_reason") != {"invalid_frame": expected["invalid_frame"]} or row.get("validation_failures") != expected["invalid_frame"] or row.get("other_outcomes") != 0:
            raise ArtifactError("mixed validation reconciliation is invalid")
        _positive_metrics(row)
    if sum(int(row["processed"]) for row in rows) != 39000:
        raise ArtifactError("mixed processed aggregate is invalid")
    for size in SIZES:
        group = [row for row in rows if row["credential_count"] == size]
        if len({(row["credential_checksum_sha256"], row["request_checksum_sha256"]) for row in group}) != 1:
            raise ArtifactError("mixed same-size checksums differ")
    if (environment.get("configuration_id"), environment.get("workload_id"), environment.get("seed")) != identity or environment.get("timer") != "time.perf_counter_ns":
        raise ArtifactError("mixed environment identity is invalid")
    if {row["environment_id"] for row in rows} != {environment.get("environment_id")}:
        raise ArtifactError("mixed environment IDs differ")
    if "host" not in " ".join(environment.get("interpretation_limits", [])).lower():
        raise ArtifactError("mixed host-software limits are absent")
    return rows


def validate_isolated(config: dict[str, object], result: dict[str, object], environment: dict[str, object], repair_text: str) -> list[dict[str, object]]:
    identity = ("SP07_ISOLATED_OPERATIONS_V1", "LOOKUP_AUTHORIZATION_MATRIX_V1", 270516)
    if (config.get("configuration_id"), config.get("workload_id"), config.get("seed")) != identity or config.get("credential_counts") != list(SIZES):
        raise ArtifactError("isolated configuration identity is invalid")
    if (config.get("warmup_repetitions"), config.get("measured_repetitions"), config.get("case_count_per_repetition")) != (1, 3, 1000):
        raise ArtifactError("isolated repetition policy is invalid")
    if (result.get("configuration_id"), result.get("workload_id"), result.get("seed")) != identity or result.get("timer") != "time.perf_counter_ns":
        raise ArtifactError("isolated result identity or timer is invalid")
    rows = result.get("results")
    expected_order = [(operation, size, rep) for operation in OPERATIONS[1:] for size in SIZES for rep in (1, 2, 3)]
    if not isinstance(rows, list) or len(rows) != 24 or [(row.get("operation"), row.get("credential_count"), row.get("repetition")) for row in rows if isinstance(row, dict)] != expected_order:
        raise ArtifactError("isolated results must contain 24 ordered rows")
    for row in rows:
        if not isinstance(row, dict) or row.get("case_count") != 1000 or row.get("processed") != 1000 or row.get("correct_count") != 1000 or row.get("mismatch_count") != 0:
            raise ArtifactError("isolated row counts are invalid")
        expected, actual, matrix = row.get("expected_outcomes"), row.get("actual_outcomes"), row.get("confusion_matrix")
        if not isinstance(expected, dict) or not isinstance(actual, dict) or not isinstance(matrix, dict):
            raise ArtifactError("isolated confusion data is invalid")
        for label, count in expected.items():
            if actual.get(label) != count or not isinstance(matrix.get(label), dict) or matrix[label].get(label) != count or any(value for key, value in matrix[label].items() if key != label):
                raise ArtifactError("isolated confusion matrix is not complete and diagonal")
        if row["operation"] == "authorization_decision" and (row.get("correct_grant_count"), row.get("correct_denial_count"), row.get("correct_error_count"), row.get("incorrect_grant_count"), row.get("incorrect_denial_count"), row.get("other_mismatch_count")) != (400, 500, 100, 0, 0, 0):
            raise ArtifactError("isolated authorization counts are invalid")
        _positive_metrics(row)
        if type(row.get("p95_ns")) is not int:
            raise ArtifactError("isolated p95 must be an integer")
    for operation in OPERATIONS[1:]:
        for size in SIZES:
            group = [row for row in rows if row["operation"] == operation and row["credential_count"] == size]
            if len({(row["credential_checksum_sha256"], row["case_checksum_sha256"]) for row in group}) != 1:
                raise ArtifactError("isolated same-size checksums differ")
    auth = [row for row in rows if row["operation"] == "authorization_decision"]
    if tuple(sum(int(row[field]) for row in auth) for field in ("correct_grant_count", "correct_denial_count", "correct_error_count", "incorrect_grant_count", "incorrect_denial_count", "other_mismatch_count")) != (4800, 6000, 1200, 0, 0, 0):
        raise ArtifactError("isolated authorization aggregate is invalid")
    if (environment.get("configuration_id"), environment.get("workload_id"), environment.get("seed")) != identity or environment.get("timer") != "time.perf_counter_ns":
        raise ArtifactError("isolated environment identity is invalid")
    if {row["environment_id"] for row in rows} != {environment.get("environment_id")}:
        raise ArtifactError("isolated environment IDs differ")
    definitions = environment.get("operation_definitions")
    if not isinstance(definitions, dict) or "Times only CredentialRepository.lookup" not in str(definitions.get("credential_repository_lookup")) or "Times only authorize" not in str(definitions.get("authorization_decision")):
        raise ArtifactError("isolated direct-operation boundaries are absent")
    required_repair = (CANONICAL_HASHES["data/results/sp07_isolated_operation_results.json"], "superseded", "READY FOR HUMAN REVIEW")
    if not all(value in repair_text for value in required_repair):
        raise ArtifactError("timing-repair identity is invalid")
    return rows


def descriptive(rows: list[dict[str, object]]) -> dict[str, object]:
    if len(rows) != 3:
        raise ArtifactError("every descriptive group requires exactly three repetitions")
    def triple(field: str) -> dict[str, int | float]:
        values = [row[field] for row in rows]
        return {"minimum": min(values), "median": statistics.median(values), "maximum": max(values)}  # type: ignore[type-var]
    return {
        "repetition_count": 3,
        "repetition_average_ns": triple("average_ns"),
        "repetition_median_ns": triple("median_ns"),
        "repetition_nearest_rank_p95_ns": triple("p95_ns"),
        "throughput_cases_per_second": triple("throughput_cases_per_second"),
    }


def build_integrated_catalog(historical: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [dict(row) for row in historical]
    exp05 = rows[4]
    exp05["evidence_status"] = "complete_existing_with_limit"
    exp05["evidence_references"] += ";experiments/isolated_operations_config.json;data/results/sp07_isolated_operation_results.json;data/results/sp07_isolated_operation_environment.json;audit/validation/subproject_07_02_timing_boundary_repair.md"
    exp05["quantitative_artifacts"] = "experiments/scalability_config.json;results/scalability_results.json;results/scalability_environment.json;experiments/isolated_operations_config.json;data/results/sp07_isolated_operation_results.json;data/results/sp07_isolated_operation_environment.json"
    exp05["scope_limit"] = "Mixed timing measures Controller.submit; lookup timing measures the public repository method; authorization timing measures the public authorization function. All values are host-software observations; raw per-call samples are unavailable. No real-time, hardware, database-server, constant-time, or asymptotic result is established."
    exp05["next_action"] = "SP-07.4 independently reviews bounded claims; no additional MVP benchmark is required, and broader scalability questions remain outside this evidence."
    return rows


def build_timing_rows(mixed: list[dict[str, object]], isolated: list[dict[str, object]], timer: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    interpretations = {
        "mixed_controller_submit": "Mixed request processing through Controller.submit; not isolated lookup timing; median values summarize repetition-level aggregates.",
        "credential_repository_lookup": "Direct CredentialRepository.lookup host timing; repository construction excluded; median values summarize repetition-level aggregates.",
        "authorization_decision": "Direct authorize host timing; credential lookup excluded; median values summarize repetition-level aggregates.",
    }
    for operation in OPERATIONS:
        source = mixed if operation == OPERATIONS[0] else [row for row in isolated if row["operation"] == operation]
        for size in SIZES:
            group = [row for row in source if row["credential_count"] == size]
            stats = descriptive(group)
            calls = int(group[0]["request_count"] if operation == OPERATIONS[0] else group[0]["case_count"])
            average = stats["repetition_average_ns"]
            median = stats["repetition_median_ns"]
            p95 = stats["repetition_nearest_rank_p95_ns"]
            throughput = stats["throughput_cases_per_second"]
            rows.append({
                "measurement_id": f"{operation}_{size}", "operation": operation,
                "credential_count": size, "repetition_count": 3,
                "calls_per_repetition": calls, "total_measured_calls": calls * 3, "timer": timer,
                "average_ns_min": average["minimum"], "average_ns_median": average["median"], "average_ns_max": average["maximum"],
                "median_ns_min": median["minimum"], "median_ns_median": median["median"], "median_ns_max": median["maximum"],
                "p95_ns_min": p95["minimum"], "p95_ns_median": p95["median"], "p95_ns_max": p95["maximum"],
                "throughput_min": throughput["minimum"], "throughput_median": throughput["median"], "throughput_max": throughput["maximum"],
                "interpretation": interpretations[operation],
            })
    return rows


def build_coverage_table(catalog: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{
        "experiment_id": row["experiment_id"], "experiment_name": row["experiment_name"],
        "evidence_status": row["evidence_status"], "primary_evidence": row["evidence_references"],
        "quantitative_artifacts": row["quantitative_artifacts"], "scope_limit": row["scope_limit"],
    } for row in catalog]


def build_correctness_table(mixed: list[dict[str, object]], isolated: list[dict[str, object]]) -> list[dict[str, object]]:
    evidence_mixed = "results/scalability_results.json"
    evidence_isolated = "data/results/sp07_isolated_operation_results.json"
    rows: list[dict[str, object]] = []
    def add(group: str, metric: str, value: int | float, unit: str, evidence: str, note: str) -> None:
        rows.append({"measurement_group": group, "metric": metric, "value": value, "unit": unit, "evidence": evidence, "scope_note": note})
    verification_note = "Accepted SP-06 verification snapshot; not the changing repository-wide analysis-test count."
    add("accepted_automated_verification", "collected_tests", 976, "tests", "data/results/sp07_quantitative_summary.json", verification_note)
    add("accepted_automated_verification", "passed_tests", 976, "tests", "data/results/sp07_quantitative_summary.json", verification_note)
    add("accepted_automated_verification", "pass_rate", 1.0, "ratio", "data/results/sp07_quantitative_summary.json", verification_note)
    mixed_note = "Frozen mixed Controller.submit workload; other outcomes are not an independent false-positive/false-negative measure."
    mixed_metrics = (
        ("processed", sum(int(r["processed"]) for r in mixed)), ("granted", sum(int(r["granted"]) for r in mixed)),
        ("denied", sum(sum(int(v) for v in r["denied_by_reason"].values()) for r in mixed)),  # type: ignore[union-attr]
        ("unauthorized_floor_denials", sum(int(r["denied_by_reason"]["unauthorized_floor"]) for r in mixed)),  # type: ignore[index]
        ("disabled_credential_denials", sum(int(r["denied_by_reason"]["disabled_credential"]) for r in mixed)),  # type: ignore[index]
        ("unknown_credential_denials", sum(int(r["denied_by_reason"]["unknown_credential"]) for r in mixed)),  # type: ignore[index]
        ("invalid_frame_validation_failures", sum(int(r["validation_failures"]) for r in mixed)),
        ("other_outcomes", sum(int(r["other_outcomes"]) for r in mixed)),
    )
    for metric, value in mixed_metrics: add("mixed_controller", metric, value, "requests", evidence_mixed, mixed_note)
    lookup = [r for r in isolated if r["operation"] == "credential_repository_lookup"]
    auth = [r for r in isolated if r["operation"] == "authorization_decision"]
    lookup_metrics = (("processed", sum(int(r["processed"]) for r in lookup)), ("correct_hits", sum(int(r["actual_outcomes"]["hit"]) for r in lookup)), ("correct_misses", sum(int(r["actual_outcomes"]["miss"]) for r in lookup)), ("mismatches", sum(int(r["mismatch_count"]) for r in lookup)))  # type: ignore[index]
    for metric, value in lookup_metrics: add("isolated_lookup", metric, value, "calls", evidence_isolated, "Direct public repository lookup software outcomes.")
    auth_metrics = (("processed", sum(int(r["processed"]) for r in auth)), ("correct_grants", sum(int(r["correct_grant_count"]) for r in auth)), ("correct_denials", sum(int(r["correct_denial_count"]) for r in auth)), ("correct_invalid_floor_errors", sum(int(r["correct_error_count"]) for r in auth)), ("incorrect_grants", sum(int(r["incorrect_grant_count"]) for r in auth)), ("incorrect_denials", sum(int(r["incorrect_denial_count"]) for r in auth)), ("other_mismatches", sum(int(r["other_mismatch_count"]) for r in auth)))
    for metric, value in auth_metrics: add("isolated_authorization", metric, value, "calls", evidence_isolated, "Direct public authorization-function software outcomes.")
    return rows


def nice_ticks(maximum: float, count: int = 5) -> tuple[float, list[float]]:
    if not math.isfinite(maximum) or maximum <= 0:
        raise ArtifactError("SVG scale maximum must be finite and positive")
    rough = maximum / count
    magnitude = 10 ** math.floor(math.log10(rough))
    fraction = rough / magnitude
    nice = 1 if fraction <= 1 else 2 if fraction <= 2 else 5 if fraction <= 5 else 10
    step = nice * magnitude
    top = math.ceil(maximum / step) * step
    return top, [index * step for index in range(int(round(top / step)) + 1)]


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else format(value, ".12g")


def build_svg(operation: str, rows: list[dict[str, object]], title: str, y_label: str, scope_note: str) -> bytes:
    if len(rows) != 12:
        raise ArtifactError("SVG requires twelve source repetition rows")
    top, ticks = nice_ticks(max(float(row["average_ns"]) for row in rows))
    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    svg = ET.Element(f"{{{ns}}}svg", {"viewBox": "0 0 960 600", "role": "img", "aria-labelledby": "title desc", "font-family": "Arial, sans-serif"})
    ET.SubElement(svg, f"{{{ns}}}title", {"id": "title"}).text = title
    ET.SubElement(svg, f"{{{ns}}}desc", {"id": "desc"}).text = f"{title}. Three measured repetitions are shown for each credential size. The line is the median of repetition-level average nanoseconds. Whiskers show minimum and maximum repetition-level averages. Points are individual repetition averages. {scope_note} Host-software observations only; no hardware or real-time guarantee."
    ET.SubElement(svg, f"{{{ns}}}rect", {"x": "0", "y": "0", "width": "960", "height": "600", "fill": "white"})
    left, right, upper, lower = 105.0, 900.0, 75.0, 455.0
    plot_height = lower - upper
    x_positions = [180.0, 400.0, 620.0, 840.0]
    y = lambda value: lower - float(value) / top * plot_height
    for tick in ticks:
        yy = y(tick)
        ET.SubElement(svg, f"{{{ns}}}line", {"x1": _number(left), "y1": _number(yy), "x2": _number(right), "y2": _number(yy), "stroke": "#cccccc", "stroke-width": "1"})
        ET.SubElement(svg, f"{{{ns}}}text", {"x": "95", "y": _number(yy + 5), "text-anchor": "end", "font-size": "13", "fill": "black"}).text = _number(tick)
    ET.SubElement(svg, f"{{{ns}}}line", {"x1": _number(left), "y1": _number(upper), "x2": _number(left), "y2": _number(lower), "stroke": "black", "stroke-width": "2"})
    ET.SubElement(svg, f"{{{ns}}}line", {"x1": _number(left), "y1": _number(lower), "x2": _number(right), "y2": _number(lower), "stroke": "black", "stroke-width": "2"})
    medians: list[tuple[float, float]] = []
    for x, size in zip(x_positions, SIZES, strict=True):
        group = sorted((row for row in rows if row["credential_count"] == size), key=lambda row: int(row["repetition"]))
        values = [float(row["average_ns"]) for row in group]
        minimum, median, maximum = min(values), statistics.median(values), max(values)
        ET.SubElement(svg, f"{{{ns}}}line", {"class": "whisker", "data-size": str(size), "data-min": _number(minimum), "data-max": _number(maximum), "x1": _number(x), "y1": _number(y(minimum)), "x2": _number(x), "y2": _number(y(maximum)), "stroke": "black", "stroke-width": "2"})
        for offset, row, value in zip((-9, 0, 9), group, values, strict=True):
            ET.SubElement(svg, f"{{{ns}}}rect", {"class": "repetition-point", "data-size": str(size), "data-repetition": str(row["repetition"]), "data-value": _number(value), "x": _number(x + offset - 3), "y": _number(y(value) - 3), "width": "6", "height": "6", "fill": "white", "stroke": "black", "stroke-width": "1.5"})
        medians.append((x, y(median)))
        ET.SubElement(svg, f"{{{ns}}}circle", {"class": "median-point", "data-size": str(size), "data-value": _number(median), "cx": _number(x), "cy": _number(y(median)), "r": "5", "fill": "black"})
        ET.SubElement(svg, f"{{{ns}}}text", {"x": _number(x), "y": "478", "text-anchor": "middle", "font-size": "14", "fill": "black"}).text = str(size)
    ET.SubElement(svg, f"{{{ns}}}polyline", {"class": "median-line", "points": " ".join(f"{_number(x)},{_number(yy)}" for x, yy in medians), "fill": "none", "stroke": "black", "stroke-width": "2.5", "stroke-dasharray": "7 4"})
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "502", "y": "510", "text-anchor": "middle", "font-size": "15", "fill": "black"}).text = "Credential count"
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "28", "y": "270", "text-anchor": "middle", "font-size": "15", "fill": "black", "transform": "rotate(-90 28 270)"}).text = y_label
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "480", "y": "36", "text-anchor": "middle", "font-size": "22", "font-weight": "bold", "fill": "black"}).text = title
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "480", "y": "535", "text-anchor": "middle", "font-size": "12", "fill": "black"}).text = "Three measured repetitions; squares = repetition averages; dashed line/circles = median of repetition-level averages; whiskers = min/max."
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "480", "y": "558", "text-anchor": "middle", "font-size": "11", "fill": "black"}).text = scope_note
    ET.SubElement(svg, f"{{{ns}}}text", {"x": "480", "y": "578", "text-anchor": "middle", "font-size": "11", "fill": "black"}).text = "Host-software observation only; operation families are not ranked; no hardware or real-time guarantee."
    return ET.tostring(svg, encoding="utf-8", xml_declaration=True) + b"\n"


def serialize_csv(rows: list[dict[str, object]], columns: tuple[str, ...]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def serialize_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def build_summary(historical: dict[str, object], catalog: list[dict[str, str]], mixed: list[dict[str, object]], isolated: list[dict[str, object]], mixed_environment: dict[str, object], isolated_environment: dict[str, object], timing_rows: list[dict[str, object]], correctness_rows: list[dict[str, object]]) -> dict[str, object]:
    isolated_groups = []
    for operation in OPERATIONS[1:]:
        for size in SIZES:
            group = [row for row in isolated if row["operation"] == operation and row["credential_count"] == size]
            isolated_groups.append({"operation": operation, "credential_count": size, "calls_per_repetition": 1000, **descriptive(group)})
    available = [
        {"metric": "isolated_credential_repository_lookup_host_timing", "value": "isolated_operation_summary.per_operation_per_size_descriptive_summaries"},
        {"metric": "isolated_authorization_function_host_timing", "value": "isolated_operation_summary.per_operation_per_size_descriptive_summaries"},
        {"metric": "explicit_lookup_confusion_matrix", "value": "available"},
        {"metric": "explicit_authorization_confusion_matrix", "value": "available"},
        {"metric": "correct_grant_count", "value": 4800}, {"metric": "correct_denial_count", "value": 6000},
        {"metric": "correct_error_count", "value": 1200}, {"metric": "incorrect_grant_count", "value": 0},
        {"metric": "incorrect_denial_count", "value": 0},
    ]
    unavailable = [{"metric": name, "value": None} for name in (
        "raw_per_call_timing_samples", "pooled_request_median", "pooled_request_p95", "branch_coverage",
        "persistent_database_server_timing", "physical_reader_timing", "electrical_output_timing",
        "elevator_movement_timing", "field_reliability", "safety_or_certification_evidence",
        "commercial_controller_timing",
    )]
    mixed_summary = dict(historical["scalability_summary"])  # type: ignore[arg-type]
    mixed_summary["accepted_scope"] = "Mixed Controller.submit host-software request processing; not isolated lookup or authorization timing."
    lookup = [r for r in isolated if r["operation"] == OPERATIONS[1]]
    auth = [r for r in isolated if r["operation"] == OPERATIONS[2]]
    return {
        "schema_version": 1,
        "analysis_id": "SP07_ANALYSIS_INTEGRATED_V1",
        "source_artifacts": [{"path": path, "sha256": CANONICAL_HASHES[path]} for path in CANONICAL_INPUTS.values()],
        "verification_summary": {**historical["verification_summary"], "snapshot_scope": "Accepted SP-06 verification snapshot; not the changing repository-wide analysis-test count."},  # type: ignore[dict-item]
        "requirements_summary": historical["requirements_summary"],
        "inventory_summary": historical["inventory_summary"],
        "experiment_coverage": [{"experiment_id": row["experiment_id"], "experiment_name": row["experiment_name"], "evidence_status": row["evidence_status"], "mapped_test_count": len(row["mapped_test_ids"].split(";"))} for row in catalog],
        "mixed_controller_summary": mixed_summary,
        "isolated_operation_summary": {
            "configuration_id": "SP07_ISOLATED_OPERATIONS_V1", "workload_id": "LOOKUP_AUTHORIZATION_MATRIX_V1",
            "seed": 270516, "timer": "time.perf_counter_ns", "environment_id": isolated_environment["environment_id"],
            "credential_sizes": list(SIZES), "measured_repetitions": 3, "total_measured_rows": 24,
            "total_measured_calls": 24000,
            "lookup_aggregate": {"processed": 12000, "correct_hits": sum(int(r["actual_outcomes"]["hit"]) for r in lookup), "correct_misses": sum(int(r["actual_outcomes"]["miss"]) for r in lookup), "mismatches": 0},  # type: ignore[index]
            "authorization_aggregate": {"processed": 12000, "correct_grants": 4800, "correct_denials": 6000, "correct_errors": 1200, "incorrect_grants": 0, "incorrect_denials": 0, "other_mismatches": 0},
            "checksums": [{"operation": operation, "credential_count": size, "credential_checksum_sha256": next(r["credential_checksum_sha256"] for r in isolated if r["operation"] == operation and r["credential_count"] == size), "case_checksum_sha256": next(r["case_checksum_sha256"] for r in isolated if r["operation"] == operation and r["credential_count"] == size)} for operation in OPERATIONS[1:] for size in SIZES],
            "per_operation_per_size_descriptive_summaries": isolated_groups,
            "operation_definitions": isolated_environment["operation_definitions"],
        },
        "correctness_summary": {
            "mixed_controller": {row["metric"]: row["value"] for row in correctness_rows if row["measurement_group"] == "mixed_controller"},
            "lookup": {row["metric"]: row["value"] for row in correctness_rows if row["measurement_group"] == "isolated_lookup"},
            "authorization": {row["metric"]: row["value"] for row in correctness_rows if row["measurement_group"] == "isolated_authorization"},
            "mixed_other_outcomes_scope": "Zero other outcomes is frozen-workload reconciliation, not an independently measured false-positive or false-negative count.",
        },
        "timing_summary": {"statistical_semantics": "Minimum, median, and maximum across exactly three repetition-level aggregates per operation and credential size; the median of repetition averages is not a pooled request statistic.", "rows": timing_rows},
        "metric_availability": {"available": available, "not_independently_available": unavailable},
        "limitations": [
            "All timing values are observational host-software measurements and may vary across hosts and runs.",
            "Mixed Controller.submit, direct repository lookup, and direct authorization timings have different operation boundaries and are not ranked as comparable performance.",
            "Raw per-call samples are unavailable; pooled medians, pooled p95 values, confidence intervals, and statistical significance are not reconstructed.",
            "No performance threshold, constant-time behavior, asymptotic guarantee, hardware timing, real-time guarantee, reliability, safety, certification, or commercial equivalence is established.",
        ],
        "deferred_work": [
            {"stage": "SP-07.4", "work": "Independently review quantitative claims, source fidelity, validity threats, anomalies, and bounded results/discussion source notes."},
            {"stage": "Subproject 8", "work": "Prepare report, presentation, release, demonstration, defense, rendered-PDF review, and human approvals."},
        ],
    }


def build_manifest(generated: dict[str, bytes]) -> dict[str, object]:
    media = {"integrated_catalog": "text/csv", "integrated_summary": "application/json", "coverage_table": "text/csv", "correctness_table": "text/csv", "timing_table": "text/csv", "mixed_figure": "image/svg+xml", "lookup_figure": "image/svg+xml", "authorization_figure": "image/svg+xml"}
    counts = {"integrated_catalog": {"row_count": 7}, "integrated_summary": {}, "coverage_table": {"row_count": 7}, "correctness_table": {"row_count": 22}, "timing_table": {"row_count": 12}, "mixed_figure": {"svg_data_series_count": 1}, "lookup_figure": {"svg_data_series_count": 1}, "authorization_figure": {"svg_data_series_count": 1}}
    return {
        "schema_version": 1, "artifact_set_id": "SP07_REPORT_ARTIFACTS_V1",
        "source_artifacts": [{"path": path, "sha256": CANONICAL_HASHES[path]} for path in CANONICAL_INPUTS.values()],
        "generated_artifacts": [{"path": GENERATED_PATHS[key], "media_type": media[key], "sha256": sha256_bytes(generated[key]), **counts[key]} for key in media],
        "generation_contract": ["Standard-library-only deterministic generation.", "Unchanged canonical sources produce byte-identical artifacts.", "No benchmark execution and no manual result editing.", "Exactly three repetition-level aggregates per operation and size.", "No pooled percentile reconstruction."],
        "limitations": ["The manifest excludes its own SHA-256 to avoid a recursive identity.", "Artifacts describe bounded host-software evidence and do not establish hardware, real-time, safety, or commercial performance."],
    }


def build_artifacts(paths: dict[str, Path]) -> dict[str, bytes]:
    validate_canonical_sources(paths)
    catalog = load_csv(paths["historical_catalog"], CATALOG_COLUMNS)
    historical = load_json(paths["historical_summary"])
    validate_historical_catalog(catalog)
    validate_historical_summary(historical)
    mixed_config, mixed_result, mixed_environment = (load_json(paths[name]) for name in ("mixed_config", "mixed_results", "mixed_environment"))
    isolated_config, isolated_result, isolated_environment = (load_json(paths[name]) for name in ("isolated_config", "isolated_results", "isolated_environment"))
    mixed = validate_mixed(mixed_config, mixed_result, mixed_environment)
    isolated = validate_isolated(isolated_config, isolated_result, isolated_environment, read_utf8(paths["isolated_repair_validation"]))
    integrated = build_integrated_catalog(catalog)
    coverage = build_coverage_table(integrated)
    correctness = build_correctness_table(mixed, isolated)
    timing = build_timing_rows(mixed, isolated, "time.perf_counter_ns")
    summary = build_summary(historical, integrated, mixed, isolated, mixed_environment, isolated_environment, timing, correctness)
    artifacts = {
        "integrated_catalog": serialize_csv(integrated, CATALOG_COLUMNS),
        "integrated_summary": serialize_json(summary),
        "coverage_table": serialize_csv(coverage, COVERAGE_COLUMNS),
        "correctness_table": serialize_csv(correctness, CORRECTNESS_COLUMNS),
        "timing_table": serialize_csv(timing, TIMING_COLUMNS),
        "mixed_figure": build_svg(OPERATIONS[0], mixed, "Mixed controller request-processing timing", "Repetition average time (ns/request)", "Includes Controller.submit and mixed validation, lookup, authorization, and controller behavior according to the frozen workload; it is not isolated lookup timing."),
        "lookup_figure": build_svg(OPERATIONS[1], [row for row in isolated if row["operation"] == OPERATIONS[1]], "Credential repository lookup timing", "Repetition average time (ns/lookup)", "Measures direct CredentialRepository.lookup, including key validation, dictionary lookup, and result-wrapper construction; repository construction is excluded."),
        "authorization_figure": build_svg(OPERATIONS[2], [row for row in isolated if row["operation"] == OPERATIONS[2]], "Authorization decision timing", "Repetition average time (ns/decision)", "Measures direct authorize, including trusted-input validation and decision construction; credential lookup is excluded."),
    }
    artifacts["manifest"] = serialize_json(build_manifest(artifacts))
    validate_artifact_bytes(artifacts)
    return artifacts


def validate_artifact_bytes(artifacts: dict[str, bytes]) -> None:
    if set(artifacts) != set(GENERATED_PATHS):
        raise ArtifactError("generated artifact set is incomplete")
    for key, data in artifacts.items():
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ArtifactError(f"generated artifact is not strict UTF-8: {key}") from exc
        if not text.endswith("\n") or any(value in text for value in (str(ROOT), "/home/", "/mnt/", "C:\\Users\\")):
            raise ArtifactError(f"generated artifact contains nondeterministic or identifying content: {key}")
    loadable_json = ("integrated_summary", "manifest")
    for key in loadable_json:
        json.loads(artifacts[key].decode("utf-8"), object_pairs_hook=_pairs)
    for key, columns, count in (("integrated_catalog", CATALOG_COLUMNS, 7), ("coverage_table", COVERAGE_COLUMNS, 7), ("correctness_table", CORRECTNESS_COLUMNS, 22), ("timing_table", TIMING_COLUMNS, 12)):
        reader = csv.DictReader(io.StringIO(artifacts[key].decode("utf-8")))
        if tuple(reader.fieldnames or ()) != columns or len(list(reader)) != count:
            raise ArtifactError(f"generated CSV validation failed: {key}")
    for key in ("mixed_figure", "lookup_figure", "authorization_figure"):
        root = ET.fromstring(artifacts[key])
        if root.tag != "{http://www.w3.org/2000/svg}svg" or root.get("viewBox") != "0 0 960 600" or root.get("role") != "img":
            raise ArtifactError(f"generated SVG validation failed: {key}")


def publish_artifacts(destinations: dict[str, Path], artifacts: dict[str, bytes]) -> None:
    if set(destinations) != set(artifacts):
        raise ArtifactError("output destination set is incomplete")
    stages: dict[str, Path] = {}
    backups: dict[str, Path] = {}
    published: list[str] = []
    try:
        for key, destination in destinations.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
            stage = Path(name)
            with os.fdopen(fd, "wb") as handle:
                handle.write(artifacts[key])
                handle.flush()
                os.fsync(handle.fileno())
            stages[key] = stage
        for key, destination in destinations.items():
            if destination.exists():
                fd, backup_name = tempfile.mkstemp(prefix=f".{destination.name}.backup.", suffix=".tmp", dir=destination.parent)
                os.close(fd)
                backup = Path(backup_name)
                backup.write_bytes(destination.read_bytes())
                backups[key] = backup
            os.replace(stages[key], destination)
            published.append(key)
        for key, destination in destinations.items():
            if destination.read_bytes() != artifacts[key]:
                raise ArtifactError(f"post-write validation failed: {destination}")
        validate_artifact_bytes({key: destinations[key].read_bytes() for key in destinations})
    except Exception as exc:
        for key in reversed(published):
            destination = destinations[key]
            backup = backups.get(key)
            if backup and backup.exists():
                os.replace(backup, destination)
            elif destination.exists():
                destination.unlink()
        if isinstance(exc, ArtifactError):
            raise
        raise ArtifactError(f"artifact publication failed; existing outputs preserved: {exc}") from exc
    finally:
        for path in (*stages.values(), *backups.values()):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in CANONICAL_INPUTS:
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    for name in GENERATED_PATHS:
        option = "--" + name.replace("_", "-") + "-output"
        if name.endswith("_figure"):
            option = "--" + name.replace("_figure", "-figure").replace("_", "-") + "-output"
        parser.add_argument(option, type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    inputs = {name: getattr(args, name) for name in CANONICAL_INPUTS}
    outputs = {name: getattr(args, name + "_output") for name in GENERATED_PATHS}
    try:
        artifacts = build_artifacts(inputs)
        publish_artifacts(outputs, artifacts)
    except ArtifactError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("completed: experiments=7 timing_groups=3 timing_rows=12 svg_figures=3 manifest_artifacts=8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
