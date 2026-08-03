"""Final documentation, reproducibility, and reconciliation inspections."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import tomllib
from types import MappingProxyType


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
REPRODUCIBILITY = ROOT / "docs" / "reproducibility.md"
INVENTORY = ROOT / "docs" / "test_case_inventory.csv"
TRACEABILITY = ROOT / "docs" / "requirements_to_test_traceability.csv"
VERIFICATION = ROOT / "audit" / "validation" / "subproject_06_11_verification_records.csv"
REPAIR = ROOT / "audit" / "validation" / "subproject_06_11_baseline_flake_repair.md"
TITLE = (
    "Literature-Based Engineering Analysis and Software Simulation of a 16-Floor "
    "Dual-Frequency RFID Elevator Access-Control Controller"
)
VERIFICATION_COLUMNS = [
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
]
OPTIONAL_IDS = {f"TST-OPT-{number:03d}" for number in range(1, 7)}
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
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
EXPERIMENT_IDS = {
    "TST-REP-001",
    "TST-REP-002",
    "TST-SCL-001",
    "TST-SCL-002",
    "TST-SCL-003",
}


def _csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or ()), list(reader)


def _references(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def _assert_relative_reference(reference: str) -> None:
    path_text, separator, node_text = reference.partition("::")
    path = Path(path_text)
    assert not path.is_absolute(), reference
    assert ".." not in path.parts, reference
    resolved = ROOT / path
    assert resolved.is_file() or resolved.is_dir(), reference
    if separator and node_text.startswith("test_"):
        tree = ast.parse(resolved.read_text(encoding="utf-8"), filename=path_text)
        functions = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert node_text in functions, reference


def test_readme_project_entry_point() -> None:
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert TITLE in text
    assert "deterministic Python software simulator" in text
    assert "supervisor approval remains pending" in lower
    assert "PYTHONPATH=src python -m pytest" in text
    for reference in (
        "docs/reproducibility.md",
        "src/elevator_access_sim/",
        "tests/",
        "experiments/scalability_config.json",
        "results/scalability_results.json",
        "results/scalability_environment.json",
    ):
        assert reference in text
    assert "LF and HF are logical reader-source labels" in text
    assert "no equivalence with a commercial controller" in lower
    assert "does not model" in lower and "physical rfid reader" in lower
    assert "does not claim those deliverables are finished" in lower
    for unsupported in (
        "commercial card uses",
        "commercial controller uses",
        "supervisor approval is complete",
        "presentation is complete",
        "release is complete",
    ):
        assert unsupported not in lower


def test_reproducibility_commands_temporary_files_and_variability() -> None:
    text = REPRODUCIBILITY.read_text(encoding="utf-8")
    for command in (
        "PYTHONPATH=src python -m pytest",
        'python -m pip install -e ".[test]"',
        "PYTHONPATH=src python -m pytest tests/unit",
        "PYTHONPATH=src python -m pytest tests/integration",
        "PYTHONPATH=src python -m pytest tests/end_to_end",
        "PYTHONPATH=src python -m pytest tests/inspection",
        "PYTHONPATH=src python -m pytest tests/experiment/test_run_experiments.py",
        'temporary_directory="$(mktemp -d)"',
        "PYTHONPATH=src python -m elevator_access_sim.cli",
        "PYTHONPATH=src python scripts/run_experiments.py",
        'rm -rf "$temporary_directory"',
    ):
        assert command in text
    for value in (
        '"facility_code": 1',
        '"credential_number": 100',
        '"floor_mask": 65535',
        '"label": "demo-user"',
        "10000000100000000011001000",
        "--source LF",
        "--floor 1",
        "--advance-to 3000",
    ):
        assert value in text
    lower = text.lower()
    assert "do not expect identical nanosecond values" in lower
    assert "stable values" in lower and "host-variable values" in lower
    for identifying in ("/mnt/", "/home/", "c:\\users\\", "hostname", ".venvs/"):
        assert identifying not in lower


def test_verification_records_schema_order_and_inventory_reconciliation() -> None:
    columns, records = _csv(VERIFICATION)
    _, inventory = _csv(INVENTORY)
    assert columns == VERIFICATION_COLUMNS
    assert len(records) == len(inventory) == 100
    assert [row["test_id"] for row in records] == [row["test_id"] for row in inventory]
    assert len({row["test_id"] for row in records}) == 100

    for record, source in zip(records, inventory, strict=True):
        assert record["requirements"] == source["requirements"]
        assert record["test_level"] == source["test_level"]
        assert record["category"] == source["module_or_flow"]
        assert record["input_or_configuration"] == source["inputs"]
        assert record["expected_result"] == source["expected_result"]
        assert record["expected_state"] == source["expected_state"]
        assert record["expected_events"] == source["expected_events"]
        assert record["actual_result"] != record["expected_result"]
        assert record["evidence"] and record["environment_reference"]
        if record["test_id"] in OPTIONAL_IDS:
            assert record["evaluation_status"] == "optional_deferred"
            assert record["actual_result"] == "not executed: optional post-MVP scope"
            assert "docs/requirements.md::Optional requirements" in record["evidence"]
            assert "docs/implementation_sequence.md::Task 11" in record["evidence"]
        else:
            assert record["evaluation_status"] == "passed"
            assert record["actual_result"].startswith("passed:")
        executable_paths: set[str] = set()
        for reference in _references(record["evidence"]):
            _assert_relative_reference(reference)
            path_text, separator, node_text = reference.partition("::")
            if separator and node_text.startswith("test_"):
                assert path_text in TEST_VALIDATION_PROVENANCE, reference
                executable_paths.add(path_text)
        environment_references = set(_references(record["environment_reference"]))
        for reference in environment_references:
            _assert_relative_reference(reference)

        originating_validations = {
            TEST_VALIDATION_PROVENANCE[path_text]
            for path_text in executable_paths
        }
        if record["test_id"] in OPTIONAL_IDS:
            assert environment_references == {
                "audit/validation/subproject_06_11_validation.md"
            }
        elif record["test_id"] in EXPERIMENT_IDS:
            assert originating_validations == {
                "audit/validation/subproject_06_10_validation.md"
            }
            assert environment_references == {
                "results/scalability_environment.json",
                "audit/validation/subproject_06_10_validation.md",
            }
        elif record["test_id"] == "TST-TRC-005":
            assert originating_validations == {
                "audit/validation/subproject_06_11_validation.md"
            }
            assert environment_references == {
                "audit/validation/subproject_06_11_validation.md"
            }
        else:
            assert executable_paths, record["test_id"]
            assert environment_references == originating_validations

    by_id = {row["test_id"]: row for row in records}
    for test_id in EXPERIMENT_IDS:
        evidence = by_id[test_id]["evidence"]
        assert "tests/experiment/test_run_experiments.py::test_" in evidence
        assert "results/scalability_results.json" in evidence
        assert "results/scalability_environment.json" in evidence
        assert "schema 1" in by_id[test_id]["actual_result"]
        assert "reconciliation" in by_id[test_id]["actual_result"]
    trace_record = by_id["TST-TRC-005"]
    assert "complete 13-column verification-record schema" in trace_record["actual_result"]
    assert "test_verification_records_schema_order_and_inventory_reconciliation" in trace_record["evidence"]
    assert by_id["TST-DAT-003"]["environment_reference"] == "audit/validation/subproject_06_07_validation.md"
    assert by_id["TST-CRD-006"]["environment_reference"] == "audit/validation/subproject_06_07_validation.md"
    assert by_id["TST-CFG-005"]["environment_reference"] == "audit/validation/subproject_06_07_validation.md"
    assert by_id["TST-E2E-001"]["environment_reference"] == "audit/validation/subproject_06_08_validation.md"
    assert by_id["TST-DAT-004"]["environment_reference"] == "audit/validation/subproject_06_03_validation.md"


def test_final_inventory_is_94_implemented_and_six_optional_designed() -> None:
    _, rows = _csv(INVENTORY)
    assert len(rows) == len({row["test_id"] for row in rows}) == 100
    assert sum(row["status"] == "implemented" for row in rows) == 94
    assert sum(row["status"] == "designed" for row in rows) == 6
    assert {row["test_id"] for row in rows if row["status"] == "designed"} == OPTIONAL_IDS
    assert next(row for row in rows if row["test_id"] == "TST-TRC-005")["status"] == "implemented"


def test_requirements_traceability_is_fully_reconciled() -> None:
    _, inventory = _csv(INVENTORY)
    _, rows = _csv(TRACEABILITY)
    inventory_status = {row["test_id"]: row["status"] for row in inventory}
    assert len(rows) == len({row["requirement_id"] for row in rows}) == 66
    assert sum(row["priority"] == "required" for row in rows) == 60
    assert sum(row["priority"] == "optional" for row in rows) == 6
    assert sum(row["status"] == "verified" for row in rows) == 60
    assert sum(row["status"] == "optional_deferred" for row in rows) == 6
    for row in rows:
        test_ids = _references(row["planned_test_id"])
        assert test_ids and set(test_ids) <= set(inventory_status)
        if row["priority"] == "required":
            assert row["status"] == "verified"
            assert any(inventory_status[test_id] == "implemented" for test_id in test_ids)
        else:
            assert row["status"] == "optional_deferred"
            assert all(test_id in OPTIONAL_IDS for test_id in test_ids)


def test_test_plan_separates_design_from_execution_evidence() -> None:
    text = (ROOT / "docs" / "test_plan.md").read_text(encoding="utf-8")
    assert "## SP-06 execution outcome and canonical evidence" in text
    assert "created before implementation" in text
    assert "SP-05 did not claim executed or passing results" in text
    assert "Actual outcomes are preserved separately" in text
    for reference in (
        "docs/test_case_inventory.csv",
        "docs/requirements_to_test_traceability.csv",
        "audit/validation/subproject_06_11_verification_records.csv",
        "results/scalability_results.json",
        "results/scalability_environment.json",
        "audit/validation/subproject_06_11_validation.md",
    ):
        assert reference in text
        _assert_relative_reference(reference)
    assert "do not provide hardware" in text.lower()
    assert "commercial-equivalence evidence" in text.lower()


def test_utf8_relative_paths_and_markdown_links() -> None:
    authored = [README, ROOT / "pyproject.toml"]
    for directory in (ROOT / "docs", ROOT / "src", ROOT / "tests", ROOT / "experiments", ROOT / "results", ROOT / "audit"):
        authored.extend(
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix in {".md", ".csv", ".toml", ".py", ".json"}
        )
    for path in authored:
        path.read_bytes().decode("utf-8", errors="strict")

    for document in (README, REPRODUCIBILITY):
        for target in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8")):
            path_text = target.split("#", 1)[0]
            if not path_text:
                continue
            candidate = Path(path_text)
            assert not candidate.is_absolute(), target
            assert (document.parent / candidate).exists(), target

    live_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (README, REPRODUCIBILITY, VERIFICATION, TRACEABILITY)
    ).lower()
    for identifying in ("/mnt/", "/home/", "c:\\users\\", ".venvs/", "hostname"):
        assert identifying not in live_text


def test_modified_documentation_preserves_protected_claim_boundaries() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (README, REPRODUCIBILITY, ROOT / "docs" / "test_plan.md")
    ).lower()
    for required in (
        "proposed project profile",
        "logical reader-source labels",
        "logical permission channels",
        "simulated time",
        "host timing is observational",
        "does not demonstrate physical rfid compatibility",
        "commercial-controller equivalence",
        "supervisor approval remains pending",
    ):
        assert required in text
    for unsupported in (
        "commercial card uses arm",
        "commercial card uses stm32",
        "commercial card uses wiegand",
        "commercial controller is production ready",
        "real-time guarantee is established",
        "safety certification is complete",
    ):
        assert unsupported not in text


def test_commands_match_unchanged_package_metadata() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["requires-python"] == ">=3.11"
    assert metadata["project"]["dependencies"] == []
    assert metadata["project"]["optional-dependencies"]["test"] == ["pytest>=7"]
    assert metadata["project"]["scripts"] == {"elevator-access-sim": "elevator_access_sim.cli:run"}
    assert metadata["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    for path in (README, REPRODUCIBILITY):
        text = path.read_text(encoding="utf-8")
        assert "PYTHONPATH=src python -m pytest" in text
        assert 'python -m pip install -e ".[test]"' in text


def test_baseline_flake_repair_is_preserved_exactly() -> None:
    test_text = (ROOT / "tests" / "unit" / "test_config_files.py").read_text(encoding="utf-8")
    assert 'os.fsencode(tmp_path / "bytes-config.json")' in test_text
    assert 'monkeypatch.setattr("builtins.open", unexpected_open)' in test_text
    assert 'assert type(error.value) is ConfigurationError' in test_text
    assert 'assert str(error.value) == "configuration file path must resolve to text"' in test_text
    assert "assert opened == []" in test_text
    assert hashlib.sha256(REPAIR.read_bytes()).hexdigest() == "aafcd53bd960a5ada73860625dfa8f4a3040f55e08ee634b868303388f43c318"


def test_official_scalability_artifacts_match_documented_stable_properties() -> None:
    config = json.loads((ROOT / "experiments" / "scalability_config.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results" / "scalability_results.json").read_text(encoding="utf-8"))
    environment = json.loads((ROOT / "results" / "scalability_environment.json").read_text(encoding="utf-8"))
    assert (config["schema_version"], config["configuration_id"], config["workload_id"], config["seed"]) == (1, "SP06_SCALABILITY_V1", "MIXED_REQUESTS_V1", 260516)
    assert config["credential_counts"] == [10, 100, 1000, 10000]
    assert len(results["results"]) == 12
    for size in config["credential_counts"]:
        rows = [row for row in results["results"] if row["credential_count"] == size]
        assert [row["repetition"] for row in rows] == [1, 2, 3]
        count = max(1000, size)
        unit = count // 100
        checksums = set()
        for row in rows:
            assert row["request_count"] == row["processed"] == count
            assert row["granted"] == 40 * unit
            assert row["denied_by_reason"] == {"unknown_credential": 15 * unit, "disabled_credential": 15 * unit, "unauthorized_floor": 20 * unit}
            assert row["validation_failures"] == 10 * unit
            assert row["other_outcomes"] == 0
            assert all(math.isfinite(row[key]) and row[key] > 0 for key in ("average_ns", "median_ns", "p95_ns", "throughput_cases_per_second"))
            assert isinstance(row["p95_ns"], int)
            assert row["environment_id"] == environment["environment_id"]
            checksums.add((row["credential_checksum_sha256"], row["request_checksum_sha256"]))
        assert len(checksums) == 1
    assert len(environment["interpretation_limits"]) == 7
