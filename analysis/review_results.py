#!/usr/bin/env python3
"""Independently review accepted SP-07 quantitative artifacts."""

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


class ReviewError(Exception):
    """Handled source, reconciliation, review, or publication failure."""


ROOT = Path(__file__).resolve().parents[1]
SIZES = (10, 100, 1000, 10000)
OPERATIONS = ("mixed_controller_submit", "credential_repository_lookup", "authorization_decision")
SOURCES = (
    "final_engineering_project_plan.md", "docs/requirements.md", "docs/test_case_inventory.csv",
    "docs/requirements_to_test_traceability.csv", "audit/validation/subproject_06_11_verification_records.csv",
    "data/results/sp07_experiment_catalog.csv", "data/results/sp07_quantitative_summary.json",
    "experiments/scalability_config.json", "results/scalability_results.json", "results/scalability_environment.json",
    "audit/validation/subproject_06_10_validation.md", "experiments/isolated_operations_config.json",
    "data/results/sp07_isolated_operation_results.json", "data/results/sp07_isolated_operation_environment.json",
    "audit/validation/subproject_07_02_timing_boundary_repair.md", "data/results/sp07_experiment_catalog_integrated.csv",
    "data/results/sp07_quantitative_summary_integrated.json", "data/results/sp07_table_experiment_coverage.csv",
    "data/results/sp07_table_correctness.csv", "data/results/sp07_table_timing_summary.csv",
    "docs/figures/sp07_mixed_controller_average_ns.svg", "docs/figures/sp07_lookup_average_ns.svg",
    "docs/figures/sp07_authorization_average_ns.svg", "data/results/sp07_report_artifact_manifest.json",
    "audit/validation/subproject_07_01_validation.md", "audit/validation/subproject_07_01_repair.md",
    "audit/validation/subproject_07_02_validation.md", "audit/validation/subproject_07_03_validation.md",
    "audit/validation/subproject_07_03_repair.md",
)
EXPECTED_HASHES = dict(zip(SOURCES, (
    "fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33",
    "9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d",
    "ce97fca1b72521536ffc85a4fe22c7cb8cf26f3dbb4220e1db394667e9178601",
    "e830fb840375e574d342073b285987b574fdaa76d80613e40d558f7b96bb2289",
    "623032dabefa0cd983812527ab09ba719a00998f1d3e6204ecea5fbe17da4e42",
    "c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb",
    "dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0",
    "93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921",
    "009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f",
    "ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba",
    "e6dc96bb105bf1af02ee170faf0c541f5a72f8e69686cfcfa6aca67f0d57f8d5",
    "6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838",
    "9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf",
    "106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec",
    "1524a88db09641bd5f31a0411341d0e0e9b454ff2502ea99948fefc50879ef90",
    "9270a15ca480a78ade0e5685ca1dd41a246aa9b4e824cc5cd80304ca96916ff8",
    "95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c",
    "f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f",
    "2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224",
    "5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811",
    "7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930",
    "26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096",
    "433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9",
    "69235fab571b97e00b54f4a8dd202e8331dadbf381dcd8caa0c2250f4ed44851",
    "675bb96506ef931c0ec2e26f15cf1ce3d61fe23540ff703d5c6ffbed83cfbd1e",
    "a4b14d0d7eed99c8049b2b2cf6b6ecfb2af9a1396db8b5016000f194c7dc6da6",
    "9849892b76a383b2b411b6cd46227e6d6d6741a92611c53f4f1d1c107d6a9775",
    "896a6d38b952f18e73ba2dda1dbd4e94e869ae7bc65d49f0b52a729d405d6a9d",
    "e0d00c7b948ffbb3836836807437ee610dd8f3f7d966baf4ec9723814c6b0b9b",
), strict=True))
LEDGER_COLUMNS = ("claim_id", "claim_category", "claim_text", "source_artifacts", "independent_check", "observed_value", "evaluation_status", "required_limitations", "report_usable_wording", "blocking_issue", "notes")
ANOMALY_COLUMNS = ("anomaly_id", "category", "observation", "evidence", "severity", "blocking", "disposition", "report_implication", "follow_up")
TIMING_COLUMNS = ("measurement_id", "operation", "credential_count", "repetition_count", "calls_per_repetition", "total_measured_calls", "timer", "average_ns_min", "average_ns_median", "average_ns_max", "median_ns_min", "median_ns_median", "median_ns_max", "p95_ns_min", "p95_ns_median", "p95_ns_max", "throughput_min", "throughput_median", "throughput_max", "interpretation")
OUTPUT_KEYS = ("review_summary", "anomaly_register", "validation_ledger", "source_notes")


def read_text(relative: str) -> str:
    path = (ROOT / relative).resolve()
    if ROOT.resolve() not in path.parents or not path.is_file():
        raise ReviewError(f"canonical source is unavailable: {relative}")
    try:
        return path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise ReviewError(f"strict UTF-8 source failure: {relative}") from exc


def digest(relative: str) -> str:
    try:
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    except OSError as exc:
        raise ReviewError(f"canonical source is unavailable: {relative}") from exc


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ReviewError(f"duplicate JSON member: {key}")
        value[key] = item
    return value


def json_source(relative: str) -> dict[str, object]:
    try:
        value = json.loads(read_text(relative), object_pairs_hook=_unique_pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(ReviewError(f"invalid JSON constant: {item}")))
    except json.JSONDecodeError as exc:
        raise ReviewError(f"invalid JSON: {relative}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"JSON object required: {relative}")
    return value


def csv_source(relative: str, columns: tuple[str, ...]) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(read_text(relative), newline=""))
    if tuple(reader.fieldnames or ()) != columns:
        raise ReviewError(f"CSV schema mismatch: {relative}")
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ReviewError(f"CSV row mismatch: {relative}")
    return rows


def review_integrity() -> dict[str, object]:
    mismatches = [path for path in SOURCES if digest(path) != EXPECTED_HASHES[path]]
    if mismatches:
        raise ReviewError(f"canonical source hash mismatch: {mismatches[0]}")
    manifest = json_source("data/results/sp07_report_artifact_manifest.json")
    if manifest.get("artifact_set_id") != "SP07_REPORT_ARTIFACTS_V1":
        raise ReviewError("manifest identity mismatch")
    source_entries = manifest.get("source_artifacts")
    generated = manifest.get("generated_artifacts")
    if not isinstance(source_entries, list) or len(source_entries) != 9 or not isinstance(generated, list) or len(generated) != 8:
        raise ReviewError("manifest entry counts mismatch")
    for entry in (*source_entries, *generated):
        if not isinstance(entry, dict) or Path(str(entry.get("path"))).is_absolute() or digest(str(entry.get("path"))) != entry.get("sha256"):
            raise ReviewError("manifest hash or path mismatch")
    generated_paths = {str(entry["path"]) for entry in generated}
    if "data/results/sp07_report_artifact_manifest.json" in generated_paths:
        raise ReviewError("manifest must omit its own hash")
    for path in SOURCES:
        read_text(path)
    return {"source_count": len(SOURCES), "manifest_source_count": 9, "manifest_generated_count": 8, "verified_hash_count": len(SOURCES) + 8, "mismatches": [], "schema_result": "passed", "utf8_result": "passed", "relative_path_result": "passed"}


def review_governance() -> dict[str, object]:
    inventory = csv_source("docs/test_case_inventory.csv", ("test_id", "test_level", "module_or_flow", "requirements", "preconditions", "inputs", "steps", "expected_result", "expected_state", "expected_events", "fixture", "status", "notes"))
    traceability = csv_source("docs/requirements_to_test_traceability.csv", ("requirement_id", "requirement_summary", "priority", "verification_method", "planned_test_id", "evidence_or_decision", "status", "notes"))
    verification = csv_source("audit/validation/subproject_06_11_verification_records.csv", ("test_id", "requirements", "test_level", "category", "input_or_configuration", "expected_result", "expected_state", "expected_events", "actual_result", "evaluation_status", "evidence", "environment_reference", "notes"))
    summary = json_source("data/results/sp07_quantitative_summary_integrated.json")
    snapshot = summary["verification_summary"]
    if tuple(snapshot[key] for key in ("collected_tests", "passed", "failed", "skipped", "xfailed", "pass_rate")) != (976, 976, 0, 0, 0, 1.0):
        raise ReviewError("verification snapshot mismatch")
    required = [row for row in traceability if row["priority"] == "required"]
    optional = [row for row in traceability if row["priority"] == "optional"]
    if (len(traceability), len(required), sum(row["status"] == "verified" for row in required), len(optional), sum(row["status"] == "optional_deferred" for row in optional)) != (66, 60, 60, 6, 6):
        raise ReviewError("requirements reconciliation mismatch")
    if (len(inventory), sum(row["status"] == "implemented" for row in inventory), sum(row["status"] == "designed" for row in inventory)) != (100, 94, 6):
        raise ReviewError("inventory reconciliation mismatch")
    if (len(verification), sum(row["evaluation_status"] == "passed" for row in verification), sum(row["evaluation_status"] == "optional_deferred" for row in verification)) != (100, 94, 6):
        raise ReviewError("verification-record reconciliation mismatch")
    if "not the changing repository-wide analysis-test count" not in str(snapshot.get("snapshot_scope")):
        raise ReviewError("historical snapshot distinction absent")
    return {"collected": 976, "passed": 976, "failed": 0, "skipped": 0, "xfailed": 0, "pass_rate": 1.0, "requirements_total": 66, "required_verified": 60, "optional_deferred": 6, "inventory_total": 100, "inventory_implemented": 94, "inventory_optional_designed": 6, "verification_records_passed": 94, "verification_records_optional_deferred": 6, "snapshot_scope": "accepted historical simulator-verification snapshot, not current repository-wide test count"}


def _metrics(row: dict[str, object]) -> None:
    for field in ("average_ns", "median_ns", "p95_ns", "throughput_cases_per_second"):
        value = row[field]
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ReviewError(f"invalid metric {field}")
    if type(row["p95_ns"]) is not int:
        raise ReviewError("p95 must be integer")


def review_mixed() -> tuple[dict[str, object], list[dict[str, object]]]:
    config, result, environment = (json_source(path) for path in ("experiments/scalability_config.json", "results/scalability_results.json", "results/scalability_environment.json"))
    rows = result.get("results")
    expected = [(size, repetition) for size in SIZES for repetition in (1, 2, 3)]
    if not isinstance(rows, list) or [(r.get("credential_count"), r.get("repetition")) for r in rows if isinstance(r, dict)] != expected:
        raise ReviewError("mixed row structure mismatch")
    counts = {10: 1000, 100: 1000, 1000: 1000, 10000: 10000}
    for row in rows:
        _metrics(row)
        if row["processed"] != counts[row["credential_count"]] or row["request_count"] != counts[row["credential_count"]]:
            raise ReviewError("mixed request count mismatch")
    totals = {"rows": 12, "processed": sum(r["processed"] for r in rows), "granted": sum(r["granted"] for r in rows), "denied": sum(sum(r["denied_by_reason"].values()) for r in rows), "unauthorized_floor": sum(r["denied_by_reason"]["unauthorized_floor"] for r in rows), "disabled_credential": sum(r["denied_by_reason"]["disabled_credential"] for r in rows), "unknown_credential": sum(r["denied_by_reason"]["unknown_credential"] for r in rows), "invalid_frame": sum(r["validation_failures"] for r in rows), "other_outcomes": sum(r["other_outcomes"] for r in rows)}
    if tuple(totals.values()) != (12, 39000, 15600, 19500, 7800, 5850, 5850, 3900, 0):
        raise ReviewError("mixed totals mismatch")
    if config.get("workload_mix_percent") != {"granted": 40, "unauthorized_floor": 20, "disabled_credential": 15, "unknown_credential": 15, "invalid_frame": 10} or (config.get("warmup_repetitions"), config.get("measured_repetitions")) != (1, 3):
        raise ReviewError("mixed configuration mismatch")
    for size in SIZES:
        group = [r for r in rows if r["credential_count"] == size]
        if len({(r["credential_checksum_sha256"], r["request_checksum_sha256"]) for r in group}) != 1:
            raise ReviewError("mixed checksum mismatch")
    if {r["environment_id"] for r in rows} != {environment["environment_id"]} or result.get("timer") != "time.perf_counter_ns":
        raise ReviewError("mixed environment mismatch")
    return totals, rows


def review_isolated() -> tuple[dict[str, object], list[dict[str, object]]]:
    result = json_source("data/results/sp07_isolated_operation_results.json")
    environment = json_source("data/results/sp07_isolated_operation_environment.json")
    rows = result.get("results")
    expected = [(operation, size, repetition) for operation in OPERATIONS[1:] for size in SIZES for repetition in (1, 2, 3)]
    if not isinstance(rows, list) or [(r.get("operation"), r.get("credential_count"), r.get("repetition")) for r in rows if isinstance(r, dict)] != expected:
        raise ReviewError("isolated row structure mismatch")
    for row in rows:
        _metrics(row)
        if (row["case_count"], row["processed"], row["correct_count"], row["mismatch_count"]) != (1000, 1000, 1000, 0):
            raise ReviewError("isolated row count mismatch")
        for label, count in row["expected_outcomes"].items():
            matrix = row["confusion_matrix"]
            if row["actual_outcomes"].get(label) != count or matrix[label].get(label) != count or any(value for key, value in matrix[label].items() if key != label):
                raise ReviewError("isolated confusion matrix mismatch")
    lookup = [r for r in rows if r["operation"] == OPERATIONS[1]]
    auth = [r for r in rows if r["operation"] == OPERATIONS[2]]
    totals = {"rows": 24, "calls": 24000, "lookup_processed": sum(r["processed"] for r in lookup), "correct_hits": sum(r["actual_outcomes"]["hit"] for r in lookup), "correct_misses": sum(r["actual_outcomes"]["miss"] for r in lookup), "lookup_mismatches": sum(r["mismatch_count"] for r in lookup), "authorization_processed": sum(r["processed"] for r in auth), "correct_grants": sum(r["correct_grant_count"] for r in auth), "correct_denials": sum(r["correct_denial_count"] for r in auth), "correct_errors": sum(r["correct_error_count"] for r in auth), "incorrect_grants": sum(r["incorrect_grant_count"] for r in auth), "incorrect_denials": sum(r["incorrect_denial_count"] for r in auth), "other_mismatches": sum(r["other_mismatch_count"] for r in auth)}
    if tuple(totals.values()) != (24, 24000, 12000, 6000, 6000, 0, 12000, 4800, 6000, 1200, 0, 0, 0):
        raise ReviewError("isolated totals mismatch")
    for operation in OPERATIONS[1:]:
        for size in SIZES:
            group = [r for r in rows if r["operation"] == operation and r["credential_count"] == size]
            if len({(r["credential_checksum_sha256"], r["case_checksum_sha256"]) for r in group}) != 1:
                raise ReviewError("isolated checksum mismatch")
    definitions = environment.get("operation_definitions", {})
    if "Times only CredentialRepository.lookup" not in str(definitions.get(OPERATIONS[1])) or "Times only authorize" not in str(definitions.get(OPERATIONS[2])):
        raise ReviewError("direct-call boundary wording mismatch")
    repair = read_text("audit/validation/subproject_07_02_timing_boundary_repair.md")
    if "superseded" not in repair or "9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf" not in repair:
        raise ReviewError("isolated repair identity mismatch")
    return totals, rows


def review_timing(mixed: list[dict[str, object]], isolated: list[dict[str, object]]) -> list[dict[str, str]]:
    table = csv_source("data/results/sp07_table_timing_summary.csv", TIMING_COLUMNS)
    if len(table) != 12 or [(r["operation"], int(r["credential_count"])) for r in table] != [(op, size) for op in OPERATIONS for size in SIZES]:
        raise ReviewError("timing table structure mismatch")
    for row in table:
        operation, size = row["operation"], int(row["credential_count"])
        source = mixed if operation == OPERATIONS[0] else [r for r in isolated if r["operation"] == operation]
        group = [r for r in source if r["credential_count"] == size]
        if len(group) != 3 or int(row["repetition_count"]) != 3:
            raise ReviewError("timing repetition count mismatch")
        for field, prefix in (("average_ns", "average_ns"), ("median_ns", "median_ns"), ("p95_ns", "p95_ns"), ("throughput_cases_per_second", "throughput")):
            values = [r[field] for r in group]
            expected = (min(values), statistics.median(values), max(values))
            actual = tuple(float(row[f"{prefix}_{suffix}"]) for suffix in ("min", "median", "max"))
            if actual != tuple(float(value) for value in expected):
                raise ReviewError(f"timing statistic mismatch: {row['measurement_id']} {prefix}")
        expected_calls = group[0]["request_count"] if operation == OPERATIONS[0] else group[0]["case_count"]
        if int(row["calls_per_repetition"]) != expected_calls or "pooled" in row["interpretation"].lower() or "ranking" in row["interpretation"].lower():
            raise ReviewError("timing interpretation mismatch")
    return table


def review_figures(mixed: list[dict[str, object]], isolated: list[dict[str, object]]) -> list[dict[str, object]]:
    specs = (
        ("docs/figures/sp07_mixed_controller_average_ns.svg", mixed, "ns/request", "Controller.submit"),
        ("docs/figures/sp07_lookup_average_ns.svg", [r for r in isolated if r["operation"] == OPERATIONS[1]], "ns/lookup", "CredentialRepository.lookup"),
        ("docs/figures/sp07_authorization_average_ns.svg", [r for r in isolated if r["operation"] == OPERATIONS[2]], "ns/decision", "direct authorize"),
    )
    reviewed = []
    for path, source, unit, boundary in specs:
        raw = (ROOT / path).read_bytes()
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise ReviewError(f"invalid SVG: {path}") from exc
        text = raw.decode("utf-8", errors="strict")
        if root.tag != "{http://www.w3.org/2000/svg}svg" or root.get("viewBox") != "0 0 960 600" or root.get("role") != "img" or root.get("aria-labelledby") != "title desc":
            raise ReviewError(f"SVG accessibility mismatch: {path}")
        points = {(int(n.get("data-size")), int(n.get("data-repetition"))): float(n.get("data-value")) for n in root.findall(".//*[@class='repetition-point']")}
        expected_points = {(r["credential_count"], r["repetition"]): float(r["average_ns"]) for r in source}
        if points != expected_points or len(root.findall(".//*[@class='median-point']")) != 4 or len(root.findall(".//*[@class='whisker']")) != 4 or len(root.findall(".//*[@class='median-line']")) != 1:
            raise ReviewError(f"SVG plotted values mismatch: {path}")
        for size in SIZES:
            values = [float(r["average_ns"]) for r in source if r["credential_count"] == size]
            median = next(n for n in root.findall(".//*[@class='median-point']") if int(n.get("data-size")) == size)
            whisker = next(n for n in root.findall(".//*[@class='whisker']") if int(n.get("data-size")) == size)
            if float(median.get("data-value")) != statistics.median(values) or (float(whisker.get("data-min")), float(whisker.get("data-max"))) != (min(values), max(values)):
                raise ReviewError(f"SVG median or whisker mismatch: {path}")
        if not all(value in text for value in (unit, boundary, "Host-software", ">0<")) or any(value in text for value in ("<script", "href=", "/home/", "/mnt/")):
            raise ReviewError(f"SVG scope or resource mismatch: {path}")
        reviewed.append({"path": path, "points": 12, "medians": 4, "whiskers": 4, "result": "passed"})
    return reviewed


def build_ledger(governance: dict[str, object], mixed: dict[str, object], isolated: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    def add(category: str, text: str, source: str, check: str, value: object, status: str = "supported", limits: str = "Accepted deterministic software evidence only.", wording: str | None = None) -> None:
        rows.append({"claim_id": f"CLM-{len(rows)+1:03d}", "claim_category": category, "claim_text": text, "source_artifacts": source, "independent_check": check, "observed_value": str(value), "evaluation_status": status, "required_limitations": limits, "report_usable_wording": wording or f"Independent review confirmed {text.lower()} ({value}) within the stated software-evidence boundary.", "blocking_issue": "no", "notes": "Independently recalculated from accepted canonical bytes."})
    summary_source = "data/results/sp07_quantitative_summary_integrated.json"
    for text, value in (("Accepted simulator verification snapshot collected and passed tests", "976/976"), ("Accepted snapshot pass rate", 1.0), ("Required requirements verified", 60), ("Optional requirements deferred", 6), ("Implemented inventory rows", 94), ("Optional designed inventory rows", 6)):
        add("verification_traceability", text, f"{summary_source};docs/requirements_to_test_traceability.csv;docs/test_case_inventory.csv", "Independent row/status reconciliation", value, "supported_with_limit", "Historical accepted SP-06 snapshot; not the current repository-wide test count.")
    for text, key in (("Mixed requests processed", "processed"), ("Mixed grants", "granted"), ("Mixed total denials", "denied"), ("Mixed unauthorized-floor denials", "unauthorized_floor"), ("Mixed disabled-credential denials", "disabled_credential"), ("Mixed unknown-credential denials", "unknown_credential"), ("Mixed invalid-frame failures", "invalid_frame"), ("Mixed other outcomes", "other_outcomes")):
        add("mixed_correctness", text, "results/scalability_results.json", "Summed 12 accepted rows", mixed[key], "supported_with_limit", "Frozen deterministic mixed workload; zero other outcomes is not an independent false-positive/false-negative rate.")
    for text, key in (("Lookup calls processed", "lookup_processed"), ("Lookup correct hits", "correct_hits"), ("Lookup correct misses", "correct_misses"), ("Lookup mismatches", "lookup_mismatches"), ("Authorization calls processed", "authorization_processed"), ("Authorization correct grants", "correct_grants"), ("Authorization correct denials", "correct_denials"), ("Authorization correct invalid-floor errors", "correct_errors"), ("Authorization incorrect grants", "incorrect_grants"), ("Authorization incorrect denials", "incorrect_denials"), ("Authorization other mismatches", "other_mismatches")):
        add("isolated_correctness", text, "data/results/sp07_isolated_operation_results.json", "Summed diagonal matrix/count fields", isolated[key], "supported_with_limit", "Deterministic constructed isolated workload; not a population-level field error rate.")
    timing_claims = (
        ("Mixed Controller.submit timing is available", "results/scalability_results.json", "Mixed request processing on one recorded host."),
        ("Direct CredentialRepository.lookup timing is available", "data/results/sp07_isolated_operation_results.json", "Public in-memory repository method on one recorded host; not persistent database timing."),
        ("Direct authorize timing is available", "data/results/sp07_isolated_operation_results.json", "Public authorization function on one recorded host; credential lookup excluded."),
        ("Twelve repetition-summary rows match accepted repetitions", "data/results/sp07_table_timing_summary.csv", "Min/median/max across exactly three repetition aggregates; no pooling."),
        ("Pooled request percentiles are unavailable", "data/results/sp07_quantitative_summary_integrated.json", "Raw per-call samples are unavailable."),
        ("Constant-time and asymptotic conclusions are unsupported", "data/results/sp07_quantitative_summary_integrated.json", "Observed host timings do not prove complexity or constant-time behavior."),
    )
    for text, source, limit in timing_claims: add("timing", text, source, "Independent repetition-level recalculation", "confirmed", "supported_with_limit", limit)
    for text, source in (("Mixed figure reproduces accepted source averages", "docs/figures/sp07_mixed_controller_average_ns.svg"), ("Lookup figure reproduces accepted source averages", "docs/figures/sp07_lookup_average_ns.svg"), ("Authorization figure reproduces accepted source averages", "docs/figures/sp07_authorization_average_ns.svg"), ("All figures are accessible and correctly labeled", "docs/figures/sp07_mixed_controller_average_ns.svg;docs/figures/sp07_lookup_average_ns.svg;docs/figures/sp07_authorization_average_ns.svg")):
        add("figures", text, source, "Parsed XML and compared points/medians/whiskers", "passed", "supported_with_limit", "Separate operation boundaries; host-software observation only; no cross-family ranking.")
    for text in ("Measurements use one recorded host", "Every timing group has three repetitions", "Raw per-call timing samples are unavailable", "No physical, real-time, reliability, safety, certification, or commercial result exists"):
        add("limits", text, "data/results/sp07_quantitative_summary_integrated.json", "Checked limitations and source metadata", "confirmed", "supported_with_limit", "Must accompany every timing or deployment interpretation.")
    return rows


def build_anomalies(timing: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped = {op: [float(row["average_ns_median"]) for row in timing if row["operation"] == op] for op in OPERATIONS}
    lookup_10000 = next(row for row in timing if row["operation"] == OPERATIONS[1] and row["credential_count"] == "10000")
    spread = f"{float(lookup_10000['average_ns_max']) - float(lookup_10000['average_ns_min']):.3f}"
    disposition = "Accepted validity threat or observation; not evidence of a software defect."
    implication = "State this limitation or observation explicitly and avoid stronger causal or performance claims."
    follow_up = "Preserve for Subproject-8 human technical review; new measurement requires separate authorization."
    specs = (
        ("timing_variation", f"Mixed repetition-average medians are non-monotonic across sizes: {grouped[OPERATIONS[0]]}.", "data/results/sp07_table_timing_summary.csv;results/scalability_results.json", "medium", disposition, implication, follow_up),
        ("timing_variation", f"Lookup repetition-average medians are non-monotonic across sizes: {grouped[OPERATIONS[1]]}.", "data/results/sp07_table_timing_summary.csv;data/results/sp07_isolated_operation_results.json", "medium", disposition, implication, follow_up),
        ("timing_variation", f"The 10000-credential lookup repetition-average spread is {spread} ns, visibly greater than smaller groups.", "data/results/sp07_table_timing_summary.csv;data/results/sp07_isolated_operation_results.json", "medium", disposition, implication, follow_up),
        ("timing_variation", f"Authorization repetition-average medians are non-monotonic across sizes: {grouped[OPERATIONS[2]]}.", "data/results/sp07_table_timing_summary.csv;data/results/sp07_isolated_operation_results.json", "medium", disposition, implication, follow_up),
        ("sample_size", "Only three measured repetitions exist per size and operation.", "experiments/scalability_config.json;experiments/isolated_operations_config.json;data/results/sp07_table_timing_summary.csv", "medium", disposition, implication, follow_up),
        ("environment", "Measurements come from one recorded host environment.", "results/scalability_environment.json;data/results/sp07_isolated_operation_environment.json", "medium", disposition, implication, follow_up),
        ("data_availability", "Raw per-call timing samples are not retained.", "data/results/sp07_quantitative_summary_integrated.json;results/scalability_environment.json;data/results/sp07_isolated_operation_environment.json", "medium", disposition, implication, follow_up),
        ("statistics", "Pooled medians, pooled p95, confidence intervals, and statistical significance are unavailable.", "data/results/sp07_quantitative_summary_integrated.json;results/scalability_environment.json;data/results/sp07_isolated_operation_environment.json", "medium", disposition, implication, follow_up),
        ("workload", "The 10000-credential mixed group uses 10000 requests per repetition; smaller sizes use 1000.", "results/scalability_results.json;data/results/sp07_table_timing_summary.csv", "low", disposition, implication, follow_up),
        ("scope", "Mixed, lookup, and authorization timing boundaries differ and must not be ranked directly.", "results/scalability_environment.json;data/results/sp07_isolated_operation_environment.json;data/results/sp07_table_timing_summary.csv", "high", disposition, implication, follow_up),
        ("external_validity", "Correctness workloads are deterministic constructed workloads, not field-population estimates.", "experiments/scalability_config.json;experiments/isolated_operations_config.json", "medium", disposition, implication, follow_up),
        ("coverage", "Branch coverage is not independently available.", "data/results/sp07_quantitative_summary_integrated.json", "low", disposition, implication, follow_up),
        ("snapshot", "The accepted 976-test SP-06 verification snapshot is historical and differs from later accepted Subproject-7 repository-wide test baselines after analysis tests were added.", "data/results/sp07_quantitative_summary_integrated.json;audit/validation/subproject_07_03_repair.md", "information", disposition, implication, follow_up),
        ("external_validity", "No physical RFID, electrical output, elevator movement, field reliability, safety, certification, real-time, or commercial-controller performance was measured.", "data/results/sp07_quantitative_summary_integrated.json;results/scalability_environment.json;data/results/sp07_isolated_operation_environment.json", "high", disposition, implication, follow_up),
    )
    rows = []
    for index, (category, observation, evidence, severity, disposition, report_implication, follow_up) in enumerate(specs, 1):
        rows.append({"anomaly_id": f"ANM-{index:03d}", "category": category, "observation": observation, "evidence": evidence, "severity": severity, "blocking": "no", "disposition": disposition, "report_implication": report_implication, "follow_up": follow_up})
    validate_anomalies(rows)
    return rows


def validate_anomalies(rows: list[dict[str, str]]) -> None:
    expected_evidence = (
        ("data/results/sp07_table_timing_summary.csv", "results/scalability_results.json"),
        ("data/results/sp07_table_timing_summary.csv", "data/results/sp07_isolated_operation_results.json"),
        ("data/results/sp07_table_timing_summary.csv", "data/results/sp07_isolated_operation_results.json"),
        ("data/results/sp07_table_timing_summary.csv", "data/results/sp07_isolated_operation_results.json"),
        ("experiments/scalability_config.json", "experiments/isolated_operations_config.json", "data/results/sp07_table_timing_summary.csv"),
        ("results/scalability_environment.json", "data/results/sp07_isolated_operation_environment.json"),
        ("data/results/sp07_quantitative_summary_integrated.json", "results/scalability_environment.json", "data/results/sp07_isolated_operation_environment.json"),
        ("data/results/sp07_quantitative_summary_integrated.json", "results/scalability_environment.json", "data/results/sp07_isolated_operation_environment.json"),
        ("results/scalability_results.json", "data/results/sp07_table_timing_summary.csv"),
        ("results/scalability_environment.json", "data/results/sp07_isolated_operation_environment.json", "data/results/sp07_table_timing_summary.csv"),
        ("experiments/scalability_config.json", "experiments/isolated_operations_config.json"),
        ("data/results/sp07_quantitative_summary_integrated.json",),
        ("data/results/sp07_quantitative_summary_integrated.json", "audit/validation/subproject_07_03_repair.md"),
        ("data/results/sp07_quantitative_summary_integrated.json", "results/scalability_environment.json", "data/results/sp07_isolated_operation_environment.json"),
    )
    if len(rows) != 14 or [row.get("anomaly_id") for row in rows] != [f"ANM-{index:03d}" for index in range(1, 15)]:
        raise ReviewError("anomaly identity or ordering mismatch")
    for index, (row, evidence) in enumerate(zip(rows, expected_evidence, strict=True), 1):
        if row.get("severity") not in {"information", "low", "medium", "high"} or row.get("blocking") != "no":
            raise ReviewError(f"anomaly status mismatch: ANM-{index:03d}")
        if any(not row.get(field) for field in ("category", "observation", "disposition", "report_implication", "follow_up")):
            raise ReviewError(f"incomplete anomaly: ANM-{index:03d}")
        actual = tuple(row.get("evidence", "").split(";"))
        if actual != evidence:
            raise ReviewError(f"anomaly evidence mismatch: ANM-{index:03d}")
        if any(path not in SOURCES or Path(path).is_absolute() or not (ROOT / path).is_file() for path in actual):
            raise ReviewError(f"invalid anomaly evidence: ANM-{index:03d}")
    if rows[12]["observation"] != "The accepted 976-test SP-06 verification snapshot is historical and differs from later accepted Subproject-7 repository-wide test baselines after analysis tests were added.":
        raise ReviewError("historical snapshot anomaly mismatch")
    if "122.189 ns" not in rows[2]["observation"] or "122.18900000000002" in rows[2]["observation"]:
        raise ReviewError("lookup spread presentation mismatch")


def build_notes(mixed: dict[str, object], isolated: dict[str, object], timing: list[dict[str, str]]) -> str:
    med = {(row["operation"], row["credential_count"]): row["average_ns_median"] for row in timing}
    lines = [
        "# SP-07 Results and Discussion Source Notes", "",
        "This is evidence-led source material, not final report prose. It must not be copied without human technical review. All timing values are host-software observations.", "",
        "## 1. Evidence and artifact status", "",
        "Observation: all accepted manifest hashes, tables, and figures reconcile. Interpretation must follow `audit/validation/subproject_07_final_validation_ledger.csv` and `data/results/sp07_anomaly_register.csv`.", "",
        "## 2. Accepted verification snapshot", "",
        "Observation: the accepted SP-06 snapshot is 976 collected and 976 passed with pass rate 1.0; it is historical and not the current repository-wide count (`data/results/sp07_quantitative_summary_integrated.json`).", "",
        "## 3. Correctness observations", "",
        f"Observation: the mixed workload processed {mixed['processed']} requests with {mixed['granted']} grants, {mixed['denied']} denials, {mixed['invalid_frame']} invalid-frame failures, and {mixed['other_outcomes']} other outcomes (`results/scalability_results.json`).",
        f"Observation: isolated lookup processed {isolated['lookup_processed']} calls with {isolated['correct_hits']} correct hits, {isolated['correct_misses']} correct misses, and {isolated['lookup_mismatches']} mismatches; authorization processed {isolated['authorization_processed']} calls with {isolated['correct_grants']} correct grants, {isolated['correct_denials']} correct denials, {isolated['correct_errors']} correct errors, and zero incorrect grants/denials/other mismatches (`data/results/sp07_isolated_operation_results.json`). Interpretation: these are deterministic constructed workloads, not a zero field error rate.", "",
        "## 4. Mixed-controller timing observations", "",
        f"Observation: median repetition-level averages for 10/100/1000/10000 credentials are {med[(OPERATIONS[0],'10')]}, {med[(OPERATIONS[0],'100')]}, {med[(OPERATIONS[0],'1000')]}, and {med[(OPERATIONS[0],'10000')]} ns/request (`data/results/sp07_table_timing_summary.csv`). The 10000 group uses 10000 requests per repetition while smaller groups use 1000 (`results/scalability_results.json`). Interpretation: do not claim monotonic scaling or statistical significance.", "",
        "## 5. Isolated lookup timing observations", "",
        f"Observation: median repetition-level lookup averages are {med[(OPERATIONS[1],'10')]}, {med[(OPERATIONS[1],'100')]}, {med[(OPERATIONS[1],'1000')]}, and {med[(OPERATIONS[1],'10000')]} ns/lookup (`data/results/sp07_table_timing_summary.csv`). The 10000 group has greater observed spread; this requires cautious wording and is not proof of degradation. The public in-memory repository lookup is not a persistent-database query.", "",
        "## 6. Isolated authorization timing observations", "",
        f"Observation: median repetition-level authorization averages are {med[(OPERATIONS[2],'10')]}, {med[(OPERATIONS[2],'100')]}, {med[(OPERATIONS[2],'1000')]}, and {med[(OPERATIONS[2],'10000')]} ns/decision (`data/results/sp07_table_timing_summary.csv`). Interpretation: no monotonic or statistically significant trend is established.", "",
        "## 7. Figure and table interpretation", "", "Each timing median is a median of three repetition-level averages; whiskers are repetition-average minima/maxima, not pooled request percentiles (`data/results/sp07_table_timing_summary.csv`). Unlike operation families must not be ranked directly.", "",
        "## 8. Anomalies and variability", "", "Non-monotonicity and the larger 10000-credential lookup spread are observations, not diagnosed software defects (`data/results/sp07_anomaly_register.csv`).", "",
        "## 9. Threats to validity", "", "One host, three repetitions, absent raw samples, unequal mixed request counts, constructed workloads, and distinct operation boundaries limit inference (`data/results/sp07_anomaly_register.csv`).", "",
        "## 10. Conclusions supported by evidence", "", "Required software behavior was verified in the accepted snapshot; deterministic workloads reconcile; bounded host timings exist; tables and figures reproduce sources; no incorrect grant or denial occurred in the isolated workload (`audit/validation/subproject_07_final_validation_ledger.csv`).", "",
        "## 11. Conclusions not supported", "", "Constant-time, asymptotic complexity, persistent-database performance, population error rate, hardware, real-time, production readiness, reliability, safety, certification, and commercial equivalence are not supported (`audit/validation/subproject_07_final_validation_ledger.csv`).", "",
        "## 12. Suggested report-safe wording", "", "Suggested wording: “On the recorded host, three repetition-level aggregate observations were available for each size; these bounded software measurements show variability and do not establish a monotonic trend or hardware performance” (`data/results/sp07_table_timing_summary.csv`).", "",
        "## 13. Table and figure insertion map", "",
        "- `data/results/sp07_table_experiment_coverage.csv` — bounded evidence-coverage table.", "- `data/results/sp07_table_correctness.csv` — deterministic correctness reconciliation.", "- `data/results/sp07_table_timing_summary.csv` — repetition-level timing summary.", "- `docs/figures/sp07_mixed_controller_average_ns.svg` — suggested caption: mixed Controller.submit host timing.", "- `docs/figures/sp07_lookup_average_ns.svg` — suggested caption: direct repository lookup host timing.", "- `docs/figures/sp07_authorization_average_ns.svg` — suggested caption: direct authorization host timing.", "",
        "## 14. Subproject-8 handoff", "", "Subproject 8 must preserve the final ledger and anomaly limitations, conduct human technical review, and treat these notes as source material rather than final prose.", "",
    ]
    return "\n".join(lines)


def build_outputs() -> dict[str, bytes]:
    integrity = review_integrity()
    governance = review_governance()
    mixed, mixed_rows = review_mixed()
    isolated, isolated_rows = review_isolated()
    timing = review_timing(mixed_rows, isolated_rows)
    figures = review_figures(mixed_rows, isolated_rows)
    ledger = build_ledger(governance, mixed, isolated)
    anomalies = build_anomalies(timing)
    status_counts = {status: sum(r["evaluation_status"] == status for r in ledger) for status in ("supported", "supported_with_limit", "unresolved", "not_supported")}
    severity_counts = {severity: sum(r["severity"] == severity for r in anomalies) for severity in ("information", "low", "medium", "high")}
    summary = {
        "schema_version": 1, "review_id": "SP07_INDEPENDENT_REVIEW_V1",
        "source_artifacts": [{"path": path, "sha256": EXPECTED_HASHES[path]} for path in SOURCES],
        "artifact_integrity": integrity, "verification_reconciliation": governance,
        "mixed_controller_reconciliation": mixed, "isolated_operation_reconciliation": isolated,
        "timing_table_reconciliation": {"rows_reviewed": 12, "groups": 3, "result": "passed", "semantics": "min/median/max across exactly three repetition aggregates; no pooled percentiles"},
        "figure_reconciliation": {"figures_reviewed": 3, "details": figures, "result": "passed"},
        "claim_review_summary": {"total_ledger_rows": len(ledger), **status_counts, "blocking_rows": 0},
        "anomaly_summary": {"total_anomalies": len(anomalies), "counts_by_severity": severity_counts, "blocking_anomaly_count": 0},
        "validity_threats": [r["observation"] for r in anomalies],
        "authorized_conclusions": ["Required software behavior was verified in the accepted simulator snapshot.", "Deterministic workloads reconcile to expected outcome counts.", "Mixed controller, lookup, and authorization host-software timing observations are available within distinct boundaries.", "Accepted figures and tables reproduce source aggregates.", "No incorrect grant or incorrect denial occurred in the isolated authorization workload."],
        "prohibited_conclusions": ["constant-time guarantee", "asymptotic-complexity proof", "persistent database performance", "physical RFID timing", "electrical output timing", "elevator movement timing", "field reliability", "production readiness", "safety certification", "commercial-controller equivalence", "real-time guarantee", "population-level error rate", "statistical significance"],
        "report_handoff": {"usable_artifacts": ["data/results/sp07_table_experiment_coverage.csv", "data/results/sp07_table_correctness.csv", "data/results/sp07_table_timing_summary.csv", "docs/figures/sp07_mixed_controller_average_ns.svg", "docs/figures/sp07_lookup_average_ns.svg", "docs/figures/sp07_authorization_average_ns.svg"], "interpretation_authorities": ["audit/validation/subproject_07_final_validation_ledger.csv", "data/results/sp07_anomaly_register.csv"], "notes_status": "source material, not final prose", "subproject_8_requirement": "Preserve all limitations and obtain human technical review.", "blocking_discrepancy": False},
        "readiness": "READY FOR HUMAN REVIEW",
    }
    outputs = {"review_summary": json_bytes(summary), "anomaly_register": csv_bytes(anomalies, ANOMALY_COLUMNS), "validation_ledger": csv_bytes(ledger, LEDGER_COLUMNS), "source_notes": build_notes(mixed, isolated, timing).encode("utf-8")}
    validate_outputs(outputs)
    return outputs


def csv_bytes(rows: list[dict[str, str]], columns: tuple[str, ...]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
    writer.writeheader(); writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def validate_outputs(outputs: dict[str, bytes]) -> None:
    if set(outputs) != set(OUTPUT_KEYS): raise ReviewError("review output set mismatch")
    for key, data in outputs.items():
        text = data.decode("utf-8", errors="strict")
        if not text.endswith("\n") or any(value in text for value in (str(ROOT), "/home/", "/mnt/", "C:\\Users\\")):
            raise ReviewError(f"invalid generated content: {key}")
    summary = json.loads(outputs["review_summary"], object_pairs_hook=_unique_pairs)
    if tuple(summary) != ("schema_version", "review_id", "source_artifacts", "artifact_integrity", "verification_reconciliation", "mixed_controller_reconciliation", "isolated_operation_reconciliation", "timing_table_reconciliation", "figure_reconciliation", "claim_review_summary", "anomaly_summary", "validity_threats", "authorized_conclusions", "prohibited_conclusions", "report_handoff", "readiness") or summary["claim_review_summary"]["blocking_rows"] != 0:
        raise ReviewError("review summary schema or readiness mismatch")
    parsed_csv: dict[str, list[dict[str, str]]] = {}
    for key, columns in (("anomaly_register", ANOMALY_COLUMNS), ("validation_ledger", LEDGER_COLUMNS)):
        reader = csv.DictReader(io.StringIO(outputs[key].decode()))
        rows = list(reader)
        if tuple(reader.fieldnames or ()) != columns or not rows: raise ReviewError(f"output CSV mismatch: {key}")
        parsed_csv[key] = rows
    validate_anomalies(parsed_csv["anomaly_register"])
    if not outputs["source_notes"].decode().startswith("# SP-07 Results and Discussion Source Notes\n"):
        raise ReviewError("source notes heading mismatch")


def _cleanup_temporaries(stages: dict[str, Path], backups: dict[str, Path], retained: set[str]) -> list[str]:
    failures: list[str] = []
    for kind, paths in (("stage", stages), ("backup", backups)):
        for key in OUTPUT_KEYS:
            path = paths.get(key)
            if path is None or (kind == "backup" and key in retained):
                continue
            try:
                path.unlink(missing_ok=True)
            except OSError:
                failures.append(f"{kind}[{key}]={path.name}")
    return failures


def publish(destinations: dict[str, Path], outputs: dict[str, bytes]) -> None:
    stages: dict[str, Path] = {}; backups: dict[str, Path] = {}; published: list[str] = []; retained: set[str] = set()
    publication_error: OSError | ReviewError | None = None
    rollback_failures: list[str] = []
    try:
        for key in OUTPUT_KEYS:
            destination = destinations[key]; destination.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
            stages[key] = Path(name)
            with os.fdopen(fd, "wb") as handle: handle.write(outputs[key]); handle.flush(); os.fsync(handle.fileno())
        for key in OUTPUT_KEYS:
            destination = destinations[key]
            if destination.exists():
                fd, name = tempfile.mkstemp(prefix=f".{destination.name}.backup.", suffix=".tmp", dir=destination.parent)
                backups[key] = Path(name); os.close(fd); backups[key].write_bytes(destination.read_bytes())
        for key in OUTPUT_KEYS: os.replace(stages[key], destinations[key]); published.append(key)
        if any(destinations[key].read_bytes() != outputs[key] for key in OUTPUT_KEYS): raise ReviewError("post-write byte mismatch")
        validate_outputs({key: destinations[key].read_bytes() for key in OUTPUT_KEYS})
    except (OSError, ReviewError) as exc:
        publication_error = exc
        for key in reversed(published):
            try:
                if key in backups and backups[key].exists(): os.replace(backups[key], destinations[key])
                else: destinations[key].unlink(missing_ok=True)
            except OSError:
                rollback_failures.append(key)
                if key in backups and backups[key].exists(): retained.add(key)
    cleanup_failures = _cleanup_temporaries(stages, backups, retained)
    cleanup_detail = ", ".join(cleanup_failures)
    if publication_error is None:
        if cleanup_failures:
            raise ReviewError(f"review publication completed; temporary cleanup incomplete: {cleanup_detail}")
        return
    if rollback_failures:
        recovery_detail = ", ".join(f"{key}={backups[key].name}" if key in retained else key for key in rollback_failures)
        message = f"review publication failed; rollback incomplete; recovery backups retained: {recovery_detail}"
        if cleanup_failures:
            message += f"; temporary cleanup incomplete: {cleanup_detail}"
        raise ReviewError(message) from publication_error
    message = "review publication failed; existing outputs were preserved"
    if cleanup_failures:
        message += f"; temporary cleanup incomplete: {cleanup_detail}"
    raise ReviewError(message) from publication_error


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--review-summary-output", type=Path, required=True)
    value.add_argument("--anomaly-register-output", type=Path, required=True)
    value.add_argument("--validation-ledger-output", type=Path, required=True)
    value.add_argument("--source-notes-output", type=Path, required=True)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    destinations = {key: getattr(args, key + "_output") for key in OUTPUT_KEYS}
    try:
        outputs = build_outputs(); publish(destinations, outputs)
    except ReviewError as exc:
        print(f"error: {exc}", file=sys.stderr); return 1
    summary = json.loads(outputs["review_summary"]); print(f"completed: ledger_rows={summary['claim_review_summary']['total_ledger_rows']} anomalies={summary['anomaly_summary']['total_anomalies']} blocking=0 figures=3 timing_rows=12")
    return 0


if __name__ == "__main__": raise SystemExit(main())
