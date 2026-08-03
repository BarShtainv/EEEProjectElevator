"""SP-07.1 evidence-consolidation and deterministic-output tests."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import shutil
import sys
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "analysis" / "analyze_results.py"
SOURCE_ARGUMENTS = {
    "verification_records": ROOT / "audit/validation/subproject_06_11_verification_records.csv",
    "inventory": ROOT / "docs/test_case_inventory.csv",
    "traceability": ROOT / "docs/requirements_to_test_traceability.csv",
    "final_validation": ROOT / "audit/validation/subproject_06_11_validation.md",
    "scalability_config": ROOT / "experiments/scalability_config.json",
    "scalability_results": ROOT / "results/scalability_results.json",
    "scalability_environment": ROOT / "results/scalability_environment.json",
}


@pytest.fixture(scope="module")
def analysis_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("sp07_analyze_results", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _arguments(tmp_path: Path, **overrides: Path) -> argparse.Namespace:
    values = dict(SOURCE_ARGUMENTS)
    values.update(overrides)
    values["catalog_output"] = tmp_path / "catalog.csv"
    values["summary_output"] = tmp_path / "summary.json"
    return argparse.Namespace(**values)


def _copy(path: Path, tmp_path: Path) -> Path:
    target = tmp_path / path.name
    shutil.copyfile(path, target)
    return target


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or ()), list(reader)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _mutated_json(source: Path, tmp_path: Path, mutate: object) -> Path:
    value = json.loads(source.read_text(encoding="utf-8"))
    assert callable(mutate)
    mutate(value)
    target = tmp_path / source.name
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def _build(analysis_module: ModuleType, tmp_path: Path):
    return analysis_module.build_analysis(_arguments(tmp_path))


def _argv(arguments: argparse.Namespace) -> list[str]:
    result: list[str] = []
    for name, value in vars(arguments).items():
        result.extend((f"--{name.replace('_', '-')}", str(value)))
    return result


def test_exact_accepted_files_parse_and_reconcile(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, summary = _build(analysis_module, tmp_path)
    assert len(catalog) == 7
    assert summary["verification_summary"] == {
        "collected_tests": 976,
        "passed": 976,
        "failed": 0,
        "skipped": 0,
        "xfailed": 0,
        "pass_rate": 1.0,
    }


def test_malformed_utf8_fails(analysis_module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_bytes(b"\xff")
    with pytest.raises(analysis_module.AnalysisError, match="strict UTF-8"):
        analysis_module.read_utf8(path)


@pytest.mark.parametrize(
    "content,match",
    [
        ('{"schema_version":', "invalid JSON"),
        ('{"schema_version": 1, "schema_version": 1}', "duplicate JSON member"),
        ('{"value": NaN}', "non-finite JSON constant"),
    ],
)
def test_malformed_duplicate_and_nonfinite_json_fail(
    analysis_module: ModuleType, tmp_path: Path, content: str, match: str
) -> None:
    path = tmp_path / "bad.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(analysis_module.AnalysisError, match=match):
        analysis_module.load_json(path)


def test_wrong_csv_columns_fail(analysis_module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "wrong.csv"
    path.write_text("wrong\nvalue\n", encoding="utf-8")
    with pytest.raises(analysis_module.AnalysisError, match="wrong CSV columns"):
        analysis_module.load_csv(path, analysis_module.INVENTORY_COLUMNS)


@pytest.mark.parametrize(
    "mutation,match",
    [
        (lambda rows: rows.pop(), "exactly 100"),
        (lambda rows: rows.__setitem__(1, dict(rows[0])), "duplicate test IDs"),
        (lambda rows: rows[0].__setitem__("status", "unknown"), "unknown status"),
        (lambda rows: rows[0].__setitem__("status", "designed"), "94 implemented"),
    ],
)
def test_inventory_row_id_status_and_count_failures(
    analysis_module: ModuleType, tmp_path: Path, mutation: object, match: str
) -> None:
    fields, rows = _read_csv(SOURCE_ARGUMENTS["inventory"])
    assert callable(mutation)
    mutation(rows)
    path = tmp_path / "inventory.csv"
    _write_csv(path, fields, rows)
    with pytest.raises(analysis_module.AnalysisError, match=match):
        analysis_module.validate_inventory(
            analysis_module.load_csv(path, analysis_module.INVENTORY_COLUMNS)
        )


@pytest.mark.parametrize(
    "mutation,match",
    [
        (lambda rows: rows.pop(), "66 unique"),
        (lambda rows: rows[0].__setitem__("status", "planned"), "required requirement is unresolved"),
        (lambda rows: rows[0].__setitem__("planned_test_id", "TST-NOT-FOUND"), "does not resolve"),
    ],
)
def test_traceability_count_status_and_reference_failures(
    analysis_module: ModuleType, tmp_path: Path, mutation: object, match: str
) -> None:
    inventory = analysis_module.load_csv(
        SOURCE_ARGUMENTS["inventory"], analysis_module.INVENTORY_COLUMNS
    )
    fields, rows = _read_csv(SOURCE_ARGUMENTS["traceability"])
    assert callable(mutation)
    mutation(rows)
    path = tmp_path / "traceability.csv"
    _write_csv(path, fields, rows)
    with pytest.raises(analysis_module.AnalysisError, match=match):
        analysis_module.validate_traceability(
            analysis_module.load_csv(path, analysis_module.TRACEABILITY_COLUMNS), inventory
        )


def test_altered_final_pytest_result_fails(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    text = SOURCE_ARGUMENTS["final_validation"].read_text(encoding="utf-8")
    text = text.replace("976 collected/passed in 4.10s", "975 collected/passed in 4.10s")
    with pytest.raises(analysis_module.AnalysisError, match="976/976"):
        analysis_module.extract_final_pytest_result(text)


@pytest.mark.parametrize(
    "source_name,mutation,match",
    [
        ("scalability_config", lambda value: value.__setitem__("schema_version", 2), "frozen profile"),
        ("scalability_results", lambda value: value["results"].pop(), "exactly 12"),
        ("scalability_results", lambda value: value["results"][0].__setitem__("repetition", 2), "duplicate"),
        ("scalability_results", lambda value: value["results"][0].__setitem__("granted", 399), "outcome counts"),
        ("scalability_results", lambda value: value["results"][1].__setitem__("credential_checksum_sha256", "0" * 64), "checksums"),
        ("scalability_environment", lambda value: value.__setitem__("environment_id", "different"), "does not match"),
    ],
)
def test_scalability_schema_rows_repetitions_outcomes_checksums_and_environment_fail(
    analysis_module: ModuleType,
    tmp_path: Path,
    source_name: str,
    mutation: object,
    match: str,
) -> None:
    source = SOURCE_ARGUMENTS[source_name]
    changed = _mutated_json(source, tmp_path, mutation)
    with pytest.raises(analysis_module.AnalysisError, match=match):
        analysis_module.build_analysis(_arguments(tmp_path, **{source_name: changed}))


def test_catalog_has_exact_order_fields_resolved_evidence_and_bounded_gaps(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, _ = _build(analysis_module, tmp_path)
    assert [row["experiment_id"] for row in catalog] == [f"EXP-{number:02d}" for number in range(1, 8)]
    assert [row["experiment_name"] for row in catalog] == [
        "Protocol validation", "Authorization correctness", "Output timing",
        "Watchdog and fault recovery", "Database scalability",
        "End-to-end scenarios", "Robustness and malformed configuration",
    ]
    inventory_ids = {
        row["test_id"]
        for row in analysis_module.load_csv(
            SOURCE_ARGUMENTS["inventory"], analysis_module.INVENTORY_COLUMNS
        )
    }
    for row in catalog:
        assert set(row) == set(analysis_module.CATALOG_COLUMNS)
        assert all(row.values())
        assert set(row["mapped_test_ids"].split(";")) <= inventory_ids
        for reference in row["evidence_references"].split(";"):
            analysis_module._resolve_reference(reference)
        assert not set(row["mapped_test_ids"].split(";")) & analysis_module.OPTIONAL_IDS
        if row["evidence_status"] == "gap_identified":
            assert "SP-07.2" in row["next_action"]


def test_exp05_is_mixed_submit_timing_and_preserves_isolated_gap(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, _ = _build(analysis_module, tmp_path)
    row = next(item for item in catalog if item["experiment_id"] == "EXP-05")
    text = " ".join(row.values()).lower()
    assert row["evidence_status"] == "gap_identified"
    assert "mixed controller request-processing host timing" in text
    assert "isolated credential" in text and "not independently available" in text
    assert "lookup latency" not in text and "database query latency" not in text


def test_exp07_has_mandatory_direct_evidence_and_bounded_complete_claim(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, _ = _build(analysis_module, tmp_path)
    row = next(item for item in catalog if item["experiment_id"] == "EXP-07")
    evidence = row["evidence_references"].split(";")
    assert row["evidence_status"] == "complete_existing"
    assert all(reference in evidence for reference in analysis_module.EXP07_REQUIRED_EVIDENCE)
    assert "audit/validation/subproject_06_08_validation.md" in evidence
    assert "audit/validation/subproject_06_07_validation.md" in evidence
    inventory_status = {
        item["test_id"]: item["status"]
        for item in analysis_module.load_csv(
            SOURCE_ARGUMENTS["inventory"], analysis_module.INVENTORY_COLUMNS
        )
    }
    assert all(
        inventory_status[test_id] == "implemented"
        for test_id in row["mapped_test_ids"].split(";")
    )
    assert "specified software inputs" in row["scope_limit"]
    assert "not field-reliability" in row["scope_limit"]
    combined = " ".join(row.values()).lower()
    assert "hardware compatibility is established" not in combined
    assert "security is established" not in combined


def test_exp07_resolving_but_incomplete_evidence_is_rejected(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, _ = _build(analysis_module, tmp_path)
    incomplete = [dict(row) for row in catalog]
    row = next(item for item in incomplete if item["experiment_id"] == "EXP-07")
    references = row["evidence_references"].split(";")
    removed = analysis_module.EXP07_REQUIRED_EVIDENCE[0]
    assert removed in references
    row["evidence_references"] = ";".join(
        reference for reference in references if reference != removed
    )
    for reference in row["evidence_references"].split(";"):
        analysis_module._resolve_reference(reference)
    with pytest.raises(analysis_module.AnalysisError, match="mandatory direct evidence"):
        analysis_module.validate_experiment_evidence(incomplete)


def test_canonical_source_paths_accept_relative_and_absolute_identity(
    analysis_module: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    absolute = _arguments(tmp_path)
    analysis_module.validate_canonical_source_paths(absolute)
    _, summary = analysis_module.build_analysis(absolute)
    for argument_name, item in zip(
        analysis_module.CANONICAL_SOURCE_ARGUMENTS,
        summary["source_artifacts"],
        strict=True,
    ):
        supplied = getattr(absolute, argument_name).resolve(strict=True)
        recorded = (ROOT / item["path"]).resolve(strict=True)
        assert supplied == recorded
        assert item["sha256"] == hashlib.sha256(recorded.read_bytes()).hexdigest()

    monkeypatch.chdir(ROOT)
    relative = _arguments(tmp_path)
    for argument_name, canonical in zip(
        analysis_module.CANONICAL_SOURCE_ARGUMENTS,
        analysis_module.CANONICAL_SOURCES,
        strict=True,
    ):
        setattr(relative, argument_name, Path(canonical))
    analysis_module.validate_canonical_source_paths(relative)


def test_byte_identical_and_semantically_valid_substitute_sources_fail_identity(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    inventory_copy = _copy(SOURCE_ARGUMENTS["inventory"], tmp_path)
    copied_arguments = _arguments(tmp_path, inventory=inventory_copy)
    assert inventory_copy.read_bytes() == SOURCE_ARGUMENTS["inventory"].read_bytes()
    with pytest.raises(analysis_module.AnalysisError, match="canonical source path"):
        analysis_module.validate_canonical_source_paths(copied_arguments)

    final_copy = tmp_path / "alternate-final-validation.md"
    final_copy.write_text(
        SOURCE_ARGUMENTS["final_validation"].read_text(encoding="utf-8")
        + "\nSemantically irrelevant alternate-source fixture.\n",
        encoding="utf-8",
    )
    alternate_arguments = _arguments(tmp_path, final_validation=final_copy)
    analysis_module.build_analysis(alternate_arguments)
    with pytest.raises(analysis_module.AnalysisError, match="canonical source path"):
        analysis_module.validate_canonical_source_paths(alternate_arguments)


def test_cli_source_identity_failure_preserves_outputs_without_traceback(
    analysis_module: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory_copy = _copy(SOURCE_ARGUMENTS["inventory"], tmp_path)
    arguments = _arguments(tmp_path, inventory=inventory_copy)
    arguments.catalog_output.write_bytes(b"old catalog")
    arguments.summary_output.write_bytes(b"old summary")
    assert analysis_module.main(_argv(arguments)) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert len(output.err.splitlines()) == 1
    assert output.err.startswith("error: ") and "canonical source path" in output.err
    assert "Traceback" not in output.err
    assert arguments.catalog_output.read_bytes() == b"old catalog"
    assert arguments.summary_output.read_bytes() == b"old summary"


def test_summary_order_identity_hashes_and_reconciliation(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    _, summary = _build(analysis_module, tmp_path)
    assert tuple(summary) == analysis_module.SUMMARY_FIELDS
    assert summary["analysis_id"] == "SP07_ANALYSIS_BASELINE_V1"
    assert [item["path"] for item in summary["source_artifacts"]] == list(
        analysis_module.CANONICAL_SOURCES
    )
    for item in summary["source_artifacts"]:
        assert item["sha256"] == hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
    assert summary["requirements_summary"] == {
        "total": 66, "required": 60, "required_verified": 60,
        "optional": 6, "optional_deferred": 6, "unresolved": 0,
    }
    assert summary["inventory_summary"]["implemented"] == 94
    assert summary["inventory_summary"]["optional_designed"] == 6


def test_summary_scalability_totals_statistics_and_finite_values(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    _, summary = _build(analysis_module, tmp_path)
    scalability = summary["scalability_summary"]
    assert scalability["total_measured_rows"] == 12
    assert scalability["total_processed_requests"] == 39000
    assert scalability["total_granted"] == 15600
    assert scalability["total_denied"] == 19500
    assert scalability["total_denied_by_reason"] == {
        "unauthorized_floor": 7800,
        "disabled_credential": 5850,
        "unknown_credential": 5850,
    }
    assert scalability["total_validation_failures"] == 3900
    assert scalability["total_validation_by_reason"] == {"invalid_frame": 3900}
    assert scalability["total_other_outcomes"] == 0
    assert len(scalability["per_size_descriptive_summaries"]) == 4
    for item in scalability["per_size_descriptive_summaries"]:
        assert item["repetition_count"] == 3
        for name in (
            "repetition_average_ns", "repetition_median_ns",
            "repetition_nearest_rank_p95_ns", "throughput_cases_per_second",
        ):
            values = item[name]
            assert values["minimum"] <= values["median"] <= values["maximum"]
            assert all(math.isfinite(value) and value > 0 for value in values.values())


def test_unavailable_metrics_are_null_and_claims_are_bounded(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    _, summary = _build(analysis_module, tmp_path)
    unavailable = summary["metric_availability"]["not_independently_available"]
    assert unavailable
    assert all(item["value"] is None for item in unavailable)
    names = {item["metric"] for item in unavailable}
    for required in (
        "isolated_credential_lookup_timing", "isolated_authorization_timing",
        "raw_per_request_timing_samples", "pooled_request_median", "pooled_request_p95",
        "branch_coverage", "physical_reader_timing", "electrical_output_timing",
        "elevator_movement_timing", "field_reliability", "safety_or_certification_evidence",
    ):
        assert required in names
    text = json.dumps(summary).lower()
    assert "lookup latency" not in text and "database query latency" not in text
    assert "pooled request percentiles" in text
    assert "no performance threshold" in text
    assert "no performance threshold or real-time guarantee is established" in text
    assert "physical rfid" in text and "safety" in text


def test_two_builds_and_serializations_are_byte_deterministic(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog_one, summary_one = _build(analysis_module, tmp_path)
    catalog_two, summary_two = _build(analysis_module, tmp_path)
    assert catalog_one == catalog_two and summary_one == summary_two
    assert analysis_module.serialize_catalog(catalog_one) == analysis_module.serialize_catalog(catalog_two)
    first = analysis_module.serialize_summary(summary_one)
    second = analysis_module.serialize_summary(summary_two)
    assert first == second and first.endswith(b"\n")
    lower = first.decode("utf-8").lower()
    assert "timestamp" not in lower and "/mnt/" not in lower and "/home/" not in lower


def test_successful_atomic_replacement_writes_both_outputs(
    analysis_module: ModuleType, tmp_path: Path
) -> None:
    catalog, summary = _build(analysis_module, tmp_path)
    catalog_path = tmp_path / "catalog.csv"
    summary_path = tmp_path / "summary.json"
    catalog_hash, summary_hash = analysis_module.write_outputs_atomically(
        catalog_path, catalog, summary_path, summary
    )
    assert hashlib.sha256(catalog_path.read_bytes()).hexdigest() == catalog_hash
    assert hashlib.sha256(summary_path.read_bytes()).hexdigest() == summary_hash
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob(".*.tmp"))


def test_prepublication_failure_preserves_existing_outputs_and_removes_temporary_files(
    analysis_module: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    catalog, summary = _build(analysis_module, tmp_path)
    catalog_path = tmp_path / "catalog.csv"
    summary_path = tmp_path / "summary.json"
    catalog_path.write_bytes(b"old catalog")
    summary_path.write_bytes(b"old summary")
    original_replace = analysis_module.os.replace
    calls = 0

    def fail_second(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected publication failure")
        original_replace(source, target)

    monkeypatch.setattr(analysis_module.os, "replace", fail_second)
    with pytest.raises(analysis_module.AnalysisError, match="preserved"):
        analysis_module.write_outputs_atomically(catalog_path, catalog, summary_path, summary)
    assert catalog_path.read_bytes() == b"old catalog"
    assert summary_path.read_bytes() == b"old summary"
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob(".*.tmp"))


def test_cli_valid_and_handled_input_failure_contract(
    analysis_module: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    arguments = _arguments(tmp_path)
    argv = _argv(arguments)
    assert analysis_module.main(argv) == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out.startswith("completed: experiments=7 measured_rows=12 processed=39000 ")

    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    failure_argv = list(argv)
    index = failure_argv.index("--scalability-config") + 1
    failure_argv[index] = str(bad)
    old_catalog = arguments.catalog_output.read_bytes()
    old_summary = arguments.summary_output.read_bytes()
    assert analysis_module.main(failure_argv) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert len(output.err.splitlines()) == 1 and output.err.startswith("error: ")
    assert "Traceback" not in output.err
    assert arguments.catalog_output.read_bytes() == old_catalog
    assert arguments.summary_output.read_bytes() == old_summary


def test_cli_requires_all_paths_and_argparse_returns_two(
    analysis_module: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as raised:
        analysis_module.main([])
    assert raised.value.code == 2
    assert "required" in capsys.readouterr().err
    for action in analysis_module.build_parser()._actions:
        if action.option_strings:
            assert action.required or action.dest == "help"


def test_structural_boundary_is_standard_library_only_and_nonbenchmarking() -> None:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
    assert imports <= {
        "__future__", "argparse", "ast", "csv", "hashlib", "io", "json", "math", "os",
        "pathlib", "re", "statistics", "sys", "tempfile", "types", "typing",
    }
    assert imports.isdisjoint(
        {
            "matplotlib", "numpy", "pandas", "requests", "urllib", "socket", "sqlite3",
            "threading", "asyncio", "subprocess", "time",
        }
    )
    assert "src/elevator_access_sim" not in SCRIPT.read_text(encoding="utf-8").lower()
