"""SP-07.3 deterministic integrated-artifact generation tests."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "analysis/generate_figures.py"


@pytest.fixture(scope="module")
def generator():
    spec = importlib.util.spec_from_file_location("sp073_generator", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def inputs(generator):
    return {name: ROOT / path for name, path in generator.CANONICAL_INPUTS.items()}


@pytest.fixture(scope="module")
def artifacts(generator, inputs):
    return generator.build_artifacts(inputs)


def _csv(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))


def _json(data: bytes) -> dict[str, object]:
    return json.loads(data.decode("utf-8"))


def _output_paths(generator, directory: Path) -> dict[str, Path]:
    return {key: directory / Path(path).name for key, path in generator.GENERATED_PATHS.items()}


def _cli_arguments(generator, inputs: dict[str, Path], outputs: dict[str, Path]) -> list[str]:
    arguments: list[str] = []
    for name, path in inputs.items():
        arguments += ["--" + name.replace("_", "-"), str(path)]
    for name, path in outputs.items():
        option = "--" + name.replace("_", "-") + "-output"
        if name.endswith("_figure"):
            option = "--" + name.replace("_figure", "-figure").replace("_", "-") + "-output"
        arguments += [option, str(path)]
    return arguments


def test_accepted_canonical_inputs_parse_and_build_nine_artifacts(generator, inputs, artifacts) -> None:
    generator.validate_canonical_sources(inputs)
    assert set(artifacts) == set(generator.GENERATED_PATHS)


def test_strict_utf8_malformed_json_duplicate_json_and_wrong_csv_fail(generator, tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_bytes(b"\xff")
    with pytest.raises(generator.ArtifactError, match="strict UTF-8"):
        generator.load_json(invalid)
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(generator.ArtifactError, match="valid JSON"):
        generator.load_json(invalid)
    invalid.write_text('{"x":1,"x":2}', encoding="utf-8")
    with pytest.raises(generator.ArtifactError, match="duplicate JSON member"):
        generator.load_json(invalid)
    wrong = tmp_path / "wrong.csv"
    wrong.write_text("x\n1\n", encoding="utf-8")
    with pytest.raises(generator.ArtifactError, match="columns"):
        generator.load_csv(wrong, generator.CATALOG_COLUMNS)


def test_catalog_missing_row_and_wrong_exp05_status_fail(generator, inputs) -> None:
    rows = generator.load_csv(inputs["historical_catalog"], generator.CATALOG_COLUMNS)
    with pytest.raises(generator.ArtifactError, match="EXP-01 through EXP-07"):
        generator.validate_historical_catalog(rows[:-1])
    changed = copy.deepcopy(rows)
    changed[4]["evidence_status"] = "complete_existing"
    with pytest.raises(generator.ArtifactError, match="EXP-05"):
        generator.validate_historical_catalog(changed)


def test_altered_mixed_count_fails(generator, inputs) -> None:
    config = generator.load_json(inputs["mixed_config"])
    result = generator.load_json(inputs["mixed_results"])
    environment = generator.load_json(inputs["mixed_environment"])
    result["results"][0]["processed"] = 999
    with pytest.raises(generator.ArtifactError, match="processed"):
        generator.validate_mixed(config, result, environment)


@pytest.mark.parametrize("mutation,match", [
    (lambda result: result["results"].pop(), "24 ordered rows"),
    (lambda result: result["results"][0]["confusion_matrix"]["hit"].__setitem__("miss", 1), "diagonal"),
])
def test_altered_isolated_count_or_matrix_fails(generator, inputs, mutation, match: str) -> None:
    config = generator.load_json(inputs["isolated_config"])
    result = generator.load_json(inputs["isolated_results"])
    environment = generator.load_json(inputs["isolated_environment"])
    mutation(result)
    with pytest.raises(generator.ArtifactError, match=match):
        generator.validate_isolated(config, result, environment, generator.read_utf8(inputs["isolated_repair_validation"]))


def test_altered_timing_repair_identity_fails(generator, inputs) -> None:
    config = generator.load_json(inputs["isolated_config"])
    result = generator.load_json(inputs["isolated_results"])
    environment = generator.load_json(inputs["isolated_environment"])
    with pytest.raises(generator.ArtifactError, match="repair identity"):
        generator.validate_isolated(config, result, environment, "superseded READY FOR HUMAN REVIEW")


def test_substituted_and_copied_canonical_paths_fail(generator, inputs, tmp_path: Path) -> None:
    substituted = dict(inputs)
    substituted["historical_catalog"] = inputs["historical_summary"]
    with pytest.raises(generator.ArtifactError, match="canonical"):
        generator.validate_canonical_sources(substituted)
    copied = tmp_path / "catalog.csv"
    copied.write_bytes(inputs["historical_catalog"].read_bytes())
    substituted = dict(inputs)
    substituted["historical_catalog"] = copied
    with pytest.raises(generator.ArtifactError, match="canonical"):
        generator.validate_canonical_sources(substituted)


def test_integrated_catalog_exact_and_only_exp05_changes(generator, inputs, artifacts) -> None:
    historical = generator.load_csv(inputs["historical_catalog"], generator.CATALOG_COLUMNS)
    integrated = _csv(artifacts["integrated_catalog"])
    assert tuple(integrated[0]) == generator.CATALOG_COLUMNS
    assert [row["experiment_id"] for row in integrated] == [f"EXP-{number:02d}" for number in range(1, 8)]
    assert all(integrated[index] == historical[index] for index in (0, 1, 2, 3, 5, 6))
    exp05 = integrated[4]
    assert historical[4]["planned_question"] == (
        "What mixed controller request-processing host timing is present across 10, 100, "
        "1000, and 10000 credentials, and which isolated measurements are still absent?"
    )
    assert exp05["planned_question"] == generator.INTEGRATED_EXP05_QUESTION
    for phrase in (
        "Controller.submit", "CredentialRepository.lookup", "authorize", "10", "100",
        "1000", "10000", "operation boundaries", "limitations",
    ):
        assert phrase in exp05["planned_question"]
    lowered_question = exp05["planned_question"].lower()
    assert "still absent" not in lowered_question
    assert "isolated measurements are absent" not in lowered_question
    assert exp05["evidence_status"] == "complete_existing_with_limit"
    assert "results/scalability_results.json" in exp05["quantitative_artifacts"]
    assert "sp07_isolated_operation_results.json" in exp05["quantitative_artifacts"]
    for phrase in ("Controller.submit", "public repository method", "public authorization function", "host-software", "raw per-call", "constant-time", "asymptotic"):
        assert phrase in exp05["scope_limit"]
    assert "SP-07.4" in exp05["next_action"] and "optional" not in exp05["evidence_status"]
    generator.validate_integrated_catalog(historical, integrated)


def test_integrated_catalog_semantic_validator_rejects_stale_exp05_question(
    generator, inputs, artifacts
) -> None:
    historical = generator.load_csv(inputs["historical_catalog"], generator.CATALOG_COLUMNS)
    integrated = _csv(artifacts["integrated_catalog"])
    integrated[4]["planned_question"] = historical[4]["planned_question"]
    with pytest.raises(generator.ArtifactError, match="planned question"):
        generator.validate_integrated_catalog(historical, integrated)


def test_integrated_summary_identity_order_sources_and_snapshots(generator, artifacts) -> None:
    summary = _json(artifacts["integrated_summary"])
    assert tuple(summary) == generator.SUMMARY_FIELDS
    assert summary["schema_version"] == 1 and summary["analysis_id"] == "SP07_ANALYSIS_INTEGRATED_V1"
    assert {row["path"]: row["sha256"] for row in summary["source_artifacts"]} == generator.CANONICAL_HASHES
    assert (summary["verification_summary"]["collected_tests"], summary["verification_summary"]["passed"]) == (976, 976)
    assert "snapshot" in summary["verification_summary"]["snapshot_scope"].lower()
    assert (summary["requirements_summary"]["required_verified"], summary["requirements_summary"]["optional_deferred"]) == (60, 6)
    assert (summary["inventory_summary"]["implemented"], summary["inventory_summary"]["optional_designed"]) == (94, 6)
    assert len(summary["experiment_coverage"]) == 7 and summary["experiment_coverage"][4]["evidence_status"] == "complete_existing_with_limit"


def test_integrated_summary_mixed_isolated_and_correctness_totals(artifacts) -> None:
    summary = _json(artifacts["integrated_summary"])
    mixed = summary["mixed_controller_summary"]
    assert (mixed["total_measured_rows"], mixed["total_processed_requests"], mixed["total_granted"], mixed["total_denied"], mixed["total_validation_failures"], mixed["total_other_outcomes"]) == (12, 39000, 15600, 19500, 3900, 0)
    isolated = summary["isolated_operation_summary"]
    assert (isolated["total_measured_rows"], isolated["total_measured_calls"]) == (24, 24000)
    assert isolated["lookup_aggregate"] == {"processed": 12000, "correct_hits": 6000, "correct_misses": 6000, "mismatches": 0}
    assert isolated["authorization_aggregate"] == {"processed": 12000, "correct_grants": 4800, "correct_denials": 6000, "correct_errors": 1200, "incorrect_grants": 0, "incorrect_denials": 0, "other_mismatches": 0}
    assert summary["correctness_summary"]["authorization"]["incorrect_grants"] == 0
    assert summary["correctness_summary"]["authorization"]["incorrect_denials"] == 0


def test_metric_availability_and_claim_boundaries(artifacts) -> None:
    summary = _json(artifacts["integrated_summary"])
    available = {row["metric"]: row["value"] for row in summary["metric_availability"]["available"]}
    unavailable = {row["metric"]: row["value"] for row in summary["metric_availability"]["not_independently_available"]}
    assert available["incorrect_grant_count"] == available["incorrect_denial_count"] == 0
    assert all(value is None for value in unavailable.values())
    assert {"raw_per_call_timing_samples", "pooled_request_p95", "persistent_database_server_timing", "commercial_controller_timing"} <= set(unavailable)
    text = json.dumps(summary).lower()
    assert "constant-time behavior" in text and "not ranked" in text
    assert "pooled request statistic" in text


def test_coverage_and_correctness_tables_are_exact(generator, artifacts) -> None:
    coverage = _csv(artifacts["coverage_table"])
    correctness = _csv(artifacts["correctness_table"])
    assert tuple(coverage[0]) == generator.COVERAGE_COLUMNS and len(coverage) == 7
    assert coverage[4]["evidence_status"] == "complete_existing_with_limit"
    assert all(not Path(value).is_absolute() for row in coverage for field in ("primary_evidence", "quantitative_artifacts") for value in row[field].split(";"))
    assert tuple(correctness[0]) == generator.CORRECTNESS_COLUMNS and len(correctness) == 22
    values = {(row["measurement_group"], row["metric"]): row["value"] for row in correctness}
    assert values[("accepted_automated_verification", "pass_rate")] == "1.0"
    assert values[("mixed_controller", "processed")] == "39000"
    assert values[("mixed_controller", "other_outcomes")] == "0"
    assert values[("isolated_lookup", "correct_hits")] == "6000"
    assert values[("isolated_authorization", "correct_invalid_floor_errors")] == "1200"


def test_timing_table_order_counts_and_statistics(generator, inputs, artifacts) -> None:
    timing = _csv(artifacts["timing_table"])
    assert tuple(timing[0]) == generator.TIMING_COLUMNS and len(timing) == 12
    assert [(row["operation"], int(row["credential_count"])) for row in timing] == [(operation, size) for operation in generator.OPERATIONS for size in generator.SIZES]
    assert all(row["repetition_count"] == "3" for row in timing)
    assert [int(row["calls_per_repetition"]) for row in timing[:4]] == [1000, 1000, 1000, 10000]
    assert all(row["calls_per_repetition"] == "1000" for row in timing[4:])
    mixed = generator.load_json(inputs["mixed_results"])["results"]
    isolated = generator.load_json(inputs["isolated_results"])["results"]
    expected = generator.build_timing_rows(mixed, isolated, "time.perf_counter_ns")
    for actual, source in zip(timing, expected, strict=True):
        assert float(actual["average_ns_median"]) == source["average_ns_median"]
        assert float(actual["p95_ns_min"]) == source["p95_ns_min"]
        assert "repetition-level" in actual["interpretation"]
    assert "ranking" not in artifacts["timing_table"].decode("utf-8").lower()


@pytest.mark.parametrize("key,title,unit,scope", [
    ("mixed_figure", "Mixed controller request-processing timing", "ns/request", "Controller.submit"),
    ("lookup_figure", "Credential repository lookup timing", "ns/lookup", "CredentialRepository.lookup"),
    ("authorization_figure", "Authorization decision timing", "ns/decision", "direct authorize"),
])
def test_svg_accessibility_structure_counts_and_scope(artifacts, key: str, title: str, unit: str, scope: str) -> None:
    data = artifacts[key]
    text = data.decode("utf-8", errors="strict")
    root = ET.fromstring(data)
    ns = {"s": "http://www.w3.org/2000/svg"}
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.get("viewBox") == "0 0 960 600" and root.get("role") == "img" and root.get("aria-labelledby") == "title desc"
    assert root.find("s:title", ns).text == title and root.find("s:desc", ns).text
    assert len(root.findall(".//*[@class='repetition-point']")) == 12
    assert len(root.findall(".//*[@class='median-point']")) == 4
    assert len(root.findall(".//*[@class='whisker']")) == 4
    assert all(str(size) in text for size in (10, 100, 1000, 10000))
    for phrase in (unit, scope, "Three measured repetitions", "median of repetition-level average nanoseconds", "Host-software"):
        assert phrase in text
    assert "<script" not in text and "href=" not in text and "/home/" not in text and "/mnt/" not in text
    assert 'data-min="0"' not in text


def test_svg_values_match_sources_and_axis_is_zero_based(generator, inputs, artifacts) -> None:
    sources = {
        "mixed_figure": generator.load_json(inputs["mixed_results"])["results"],
        "lookup_figure": [row for row in generator.load_json(inputs["isolated_results"])["results"] if row["operation"] == generator.OPERATIONS[1]],
        "authorization_figure": [row for row in generator.load_json(inputs["isolated_results"])["results"] if row["operation"] == generator.OPERATIONS[2]],
    }
    for key, rows in sources.items():
        root = ET.fromstring(artifacts[key])
        points = {(int(node.get("data-size")), int(node.get("data-repetition"))): float(node.get("data-value")) for node in root.findall(".//*[@class='repetition-point']")}
        assert points == {(int(row["credential_count"]), int(row["repetition"])): float(row["average_ns"]) for row in rows}
        assert any(node.text == "0" for node in root.findall("{http://www.w3.org/2000/svg}text"))


def test_two_builds_and_serializations_are_byte_identical(generator, inputs, artifacts) -> None:
    second = generator.build_artifacts(inputs)
    assert artifacts == second
    assert generator.serialize_json(_json(artifacts["integrated_summary"])) == artifacts["integrated_summary"]


def test_two_complete_output_directories_have_identical_hashes(generator, artifacts, tmp_path: Path) -> None:
    first, second = _output_paths(generator, tmp_path / "one"), _output_paths(generator, tmp_path / "two")
    generator.publish_artifacts(first, artifacts)
    generator.publish_artifacts(second, artifacts)
    hashes = lambda paths: {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}
    assert hashes(first) == hashes(second)


def test_manifest_hashes_generated_bytes(generator, artifacts) -> None:
    manifest = _json(artifacts["manifest"])
    assert tuple(manifest) == ("schema_version", "artifact_set_id", "source_artifacts", "generated_artifacts", "generation_contract", "limitations")
    assert manifest["artifact_set_id"] == "SP07_REPORT_ARTIFACTS_V1" and len(manifest["generated_artifacts"]) == 8
    reverse = {path: key for key, path in generator.GENERATED_PATHS.items()}
    for row in manifest["generated_artifacts"]:
        assert row["sha256"] == hashlib.sha256(artifacts[reverse[row["path"]]]).hexdigest()
    assert generator.GENERATED_PATHS["manifest"] not in {row["path"] for row in manifest["generated_artifacts"]}


def test_successful_publication_writes_all_artifacts_and_removes_temps(generator, artifacts, tmp_path: Path) -> None:
    outputs = _output_paths(generator, tmp_path)
    generator.publish_artifacts(outputs, artifacts)
    assert all(path.read_bytes() == artifacts[key] for key, path in outputs.items())
    assert not list(tmp_path.rglob("*.tmp"))


def test_injected_publication_failure_restores_old_files(generator, artifacts, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    outputs = _output_paths(generator, tmp_path)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"old")
    original = generator.os.replace
    calls = 0
    def fail_once(source, destination):
        nonlocal calls
        calls += 1
        if calls == 5:
            raise OSError("injected")
        return original(source, destination)
    monkeypatch.setattr(generator.os, "replace", fail_once)
    with pytest.raises(generator.ArtifactError, match="preserved"):
        generator.publish_artifacts(outputs, artifacts)
    assert all(path.read_bytes() == b"old" for path in outputs.values())
    assert not list(tmp_path.rglob("*.tmp"))


def _inject_publication_and_restoration_failure(
    generator, outputs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> tuple[object, list[str]]:
    original = generator.os.replace
    destination_keys = {path: key for key, path in outputs.items()}
    restoration_attempts: list[str] = []

    def fail_publication_and_one_restoration(source, destination):
        source_path = Path(source)
        destination_path = Path(destination)
        key = destination_keys[destination_path]
        if ".backup." in source_path.name:
            restoration_attempts.append(key)
            if key == "integrated_catalog":
                raise OSError("injected restoration failure")
        elif key == "correctness_table":
            raise OSError("injected publication failure")
        return original(source, destination)

    monkeypatch.setattr(generator.os, "replace", fail_publication_and_one_restoration)
    return original, restoration_attempts


def test_rollback_incomplete_retains_recoverable_backup_and_attempts_all_restorations(
    generator, artifacts, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    outputs = _output_paths(generator, tmp_path)
    old_bytes = {key: f"old-{key}".encode() for key in outputs}
    for key, path in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(old_bytes[key])
    original, restoration_attempts = _inject_publication_and_restoration_failure(
        generator, outputs, monkeypatch
    )

    with pytest.raises(generator.ArtifactError) as raised:
        generator.publish_artifacts(outputs, artifacts)
    message = str(raised.value)
    assert message.startswith(
        "artifact publication failed; rollback incomplete; recovery backups retained: "
    )
    assert "integrated_catalog=" in message and str(tmp_path) not in message
    assert set(restoration_attempts) == {
        "integrated_catalog", "integrated_summary", "coverage_table"
    }
    assert outputs["integrated_catalog"].read_bytes() == artifacts["integrated_catalog"]
    for key in outputs:
        if key != "integrated_catalog":
            assert outputs[key].read_bytes() == old_bytes[key]
    retained = list(tmp_path.rglob("*.backup.*.tmp"))
    assert len(retained) == 1 and retained[0].read_bytes() == old_bytes["integrated_catalog"]
    assert set(tmp_path.rglob("*.tmp")) == set(retained)

    original(retained[0], outputs["integrated_catalog"])
    assert outputs["integrated_catalog"].read_bytes() == old_bytes["integrated_catalog"]
    assert not list(tmp_path.rglob("*.tmp"))


def test_cli_reports_rollback_incomplete_without_false_preservation_claim(
    generator, inputs, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    outputs = _output_paths(generator, tmp_path)
    for key, path in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"old-{key}".encode())
    original, restoration_attempts = _inject_publication_and_restoration_failure(
        generator, outputs, monkeypatch
    )

    assert generator.main(_cli_arguments(generator, inputs, outputs)) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(captured.err.splitlines()) == 1
    assert captured.err.startswith("error: artifact publication failed; rollback incomplete;")
    assert "existing outputs were preserved" not in captured.err
    assert "Traceback" not in captured.err and str(tmp_path) not in captured.err
    assert set(restoration_attempts) == {
        "integrated_catalog", "integrated_summary", "coverage_table"
    }
    retained = list(tmp_path.rglob("*.backup.*.tmp"))
    assert len(retained) == 1
    original(retained[0], outputs["integrated_catalog"])
    assert not list(tmp_path.rglob("*.tmp"))


def test_handled_cli_error_returns_one_line_and_preserves_outputs(generator, inputs, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    outputs = _output_paths(generator, tmp_path / "outputs")
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"old")
    bad = dict(inputs)
    bad["historical_catalog"] = tmp_path / "copy.csv"
    bad["historical_catalog"].write_bytes(inputs["historical_catalog"].read_bytes())
    assert generator.main(_cli_arguments(generator, bad, outputs)) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and len(captured.err.splitlines()) == 1 and captured.err.startswith("error: ")
    assert all(path.read_bytes() == b"old" for path in outputs.values())


def test_cli_success_and_all_arguments_required(generator, inputs, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    outputs = _output_paths(generator, tmp_path)
    assert generator.main(_cli_arguments(generator, inputs, outputs)) == 0
    assert capsys.readouterr().out == "completed: experiments=7 timing_groups=3 timing_rows=12 svg_figures=3 manifest_artifacts=8\n"
    with pytest.raises(SystemExit) as raised:
        generator.main([])
    assert raised.value.code == 2
    actions = [action for action in generator.build_argument_parser()._actions if action.option_strings]
    assert len([action for action in actions if action.required]) == 18


def test_ast_structural_boundary_uses_standard_library_and_executes_no_benchmark() -> None:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
    assert imports <= {"__future__", "argparse", "csv", "hashlib", "io", "json", "math", "os", "pathlib", "statistics", "sys", "tempfile", "xml"}
    forbidden = {"numpy", "pandas", "matplotlib", "seaborn", "plotly", "requests", "urllib", "socket", "sqlite3", "subprocess", "threading", "asyncio", "multiprocessing", "time", "elevator_access_sim"}
    assert imports.isdisjoint(forbidden)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert not any(isinstance(call.func, ast.Name) and call.func.id in {"run_complete_experiment", "run_lookup_repetition", "run_authorization_repetition", "authorize"} for call in calls)
    assert not any(isinstance(call.func, ast.Attribute) and call.func.attr in {"submit", "sleep"} for call in calls)
    source = SCRIPT.read_text(encoding="utf-8")
    assert "scripts.run_experiments" not in source and "analysis.run_experiments" not in source
