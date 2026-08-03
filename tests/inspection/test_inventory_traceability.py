"""Automated inventory, requirement, and SP-06.9 resolution checks."""

from __future__ import annotations

import ast
import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "docs" / "test_case_inventory.csv"
TRACE_PATH = ROOT / "docs" / "requirements_to_test_traceability.csv"
REQUIREMENTS_PATH = ROOT / "docs" / "requirements.md"
RESOLUTION_PATH = ROOT / "audit" / "validation" / "subproject_06_09_inventory_resolution.csv"

RESOLUTION_COLUMNS = [
    "test_id",
    "requirements",
    "inventory_level",
    "owner_stage",
    "coverage_class",
    "implementation_reference",
    "execution_status",
    "evidence",
    "notes",
]
PASSING_CLASSES = {
    "implemented_existing",
    "implemented_sp06_09",
    "inspection_existing",
    "inspection_sp06_09",
}
SCHEDULED_CLASSES = {"scheduled_sp06_10", "scheduled_sp06_11"}
ALL_CLASSES = PASSING_CLASSES | SCHEDULED_CLASSES | {"optional_deferred", "unresolved"}
REQUIREMENT_PATTERN = re.compile(r"^[A-Z]+-\d{3}$")
TEST_ID_PATTERN = re.compile(r"^TST-[A-Z0-9]+-\d{3}$")
RANGE_PATTERN = re.compile(r"^([A-Z]+)-(\d{3})[–-](?:([A-Z]+)-)?(\d{3})$")


def _rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or ()), list(reader)


def _requirements() -> dict[str, str]:
    priorities: dict[str, str] = {}
    for line in REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 9 and REQUIREMENT_PATTERN.fullmatch(cells[0]) and cells[6] in {"required", "optional"}:
            priorities[cells[0]] = cells[6]
    return priorities


def _expand_requirement_cell(value: str) -> set[str]:
    resolved: set[str] = set()
    for raw in value.split(";"):
        token = raw.strip()
        match = RANGE_PATTERN.fullmatch(token)
        if match:
            start_prefix, start_text, end_prefix, end_text = match.groups()
            assert end_prefix in (None, start_prefix), token
            start, end = int(start_text), int(end_text)
            assert start <= end, token
            resolved.update(f"{start_prefix}-{number:03d}" for number in range(start, end + 1))
        else:
            assert REQUIREMENT_PATTERN.fullmatch(token), token
            resolved.add(token)
    return resolved


def _planned_test_ids(value: str) -> set[str]:
    return {token.strip() for token in value.split(";") if token.strip()}


def _assert_test_reference(reference: str) -> None:
    path_text, separator, node_text = reference.partition("::")
    assert separator and node_text.startswith("test_"), reference
    path = ROOT / path_text
    assert path.is_file(), reference
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path_text)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert node_text in functions, reference


def test_tst_trc_001_002_003_004_cross_file_identifiers() -> None:
    priorities = _requirements()
    inventory_columns, inventory = _rows(INVENTORY_PATH)
    trace_columns, trace = _rows(TRACE_PATH)

    assert len(priorities) == 66
    assert sum(value == "required" for value in priorities.values()) == 60
    assert sum(value == "optional" for value in priorities.values()) == 6
    assert inventory_columns == [
        "test_id", "test_level", "module_or_flow", "requirements", "preconditions", "inputs",
        "steps", "expected_result", "expected_state", "expected_events", "fixture", "status", "notes",
    ]
    assert len(inventory) == 100
    inventory_ids = [row["test_id"] for row in inventory]
    assert len(inventory_ids) == len(set(inventory_ids))
    assert all(TEST_ID_PATTERN.fullmatch(test_id) for test_id in inventory_ids)

    assert trace_columns[0] == "requirement_id"
    assert len(trace) == 66
    assert {row["requirement_id"] for row in trace} == set(priorities)
    for row in trace:
        planned = _planned_test_ids(row["planned_test_id"])
        assert planned
        assert planned <= set(inventory_ids)
    for row in inventory:
        assert _expand_requirement_cell(row["requirements"]) <= set(priorities)


def test_sp06_09_resolution_is_complete_concrete_and_status_consistent() -> None:
    priorities = _requirements()
    _, inventory = _rows(INVENTORY_PATH)
    resolution_columns, resolution = _rows(RESOLUTION_PATH)

    assert resolution_columns == RESOLUTION_COLUMNS
    assert len(resolution) == len(inventory) == 100
    assert [row["test_id"] for row in resolution] == [row["test_id"] for row in inventory]
    assert len({row["test_id"] for row in resolution}) == 100

    inventory_by_id = {row["test_id"]: row for row in inventory}
    for row in resolution:
        inventory_row = inventory_by_id[row["test_id"]]
        coverage_class = row["coverage_class"]
        status = row["execution_status"]
        assert coverage_class in ALL_CLASSES
        assert coverage_class != "unresolved"
        assert row["requirements"] == inventory_row["requirements"]
        assert row["inventory_level"] == inventory_row["test_level"]
        assert row["owner_stage"] and row["implementation_reference"] and row["evidence"]

        requirement_ids = _expand_requirement_cell(row["requirements"])
        optional = all(priorities[requirement_id] == "optional" for requirement_id in requirement_ids)
        if coverage_class in PASSING_CLASSES:
            assert status == "passed"
            assert inventory_row["status"] == "implemented"
            for reference in row["implementation_reference"].split(";"):
                _assert_test_reference(reference.strip())
        elif coverage_class in SCHEDULED_CLASSES:
            assert status == "scheduled"
            assert row["owner_stage"] in {"SP-06.10", "SP-06.11"}
            assert inventory_row["status"] in {"designed", "implemented"}
            assert row["implementation_reference"].startswith("docs/implementation_sequence.md::Task ")
        else:
            assert coverage_class == "optional_deferred"
            assert status == "optional_deferred"
            assert optional
            assert inventory_row["status"] == "designed"
            assert row["owner_stage"] == "Post-MVP"

    classes = [row["coverage_class"] for row in resolution]
    assert classes.count("implemented_existing") == 67
    assert classes.count("implemented_sp06_09") == 3
    assert classes.count("inspection_existing") == 0
    assert classes.count("inspection_sp06_09") == 18
    assert classes.count("scheduled_sp06_10") == 5
    assert classes.count("scheduled_sp06_11") == 1
    assert classes.count("optional_deferred") == 6
    assert classes.count("unresolved") == 0
