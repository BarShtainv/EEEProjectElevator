"""SP-08.2G human drafting-input packet inspections."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "report/submission_requirements.md"
REQUEST = ROOT / "report/human_input_request.md"
SNAPSHOT = ROOT / "report/drafting_gate_snapshot.csv"

SNAPSHOT_COLUMNS = (
    "gate_row_id", "requirement_id", "input_or_decision", "current_value",
    "current_status", "blocking_stage", "minimum_gate_group",
    "minimum_for_sp08_2", "authority", "responsible_party",
    "privacy_classification", "requested_human_response", "evidence", "notes",
)
REQUEST_SECTIONS = (
    "Minimum decisions required for SP-08.2",
    "Sensitive identity information",
    "Later formatting and submission decisions",
    "Product image and physical-component decisions",
    "Paste-back response template",
    "Evidence to attach",
    "Decision-handling rules",
    "Current readiness",
)
MINIMUM_GROUPS = (
    "GATE-TITLE", "GATE-IDENTITY", "GATE-LANGUAGE", "GATE-TEMPLATE",
    "GATE-CITATION", "GATE-SCHEDULE",
)
GROUP_MEMBERS = {
    "GATE-TITLE": {"SUB-001", "SUB-002", "SUB-011"},
    "GATE-IDENTITY": {f"SUB-{number:03d}" for number in range(3, 11)},
    "GATE-LANGUAGE": {"SUB-012", "SUB-018", "SUB-019"},
    "GATE-TEMPLATE": {"SUB-013", "SUB-014", "SUB-015", "SUB-020"},
    "GATE-CITATION": {"SUB-016", "SUB-017"},
    "GATE-SCHEDULE": {"SUB-021", "SUB-022"},
}
PASTE_BACK_FIELDS = (
    "Title decision", "Supervisor title approval", "Student names", "Institution",
    "Faculty or school", "Department", "Degree or program", "Supervisor name",
    "Supervisor title", "Report language",
    "Template file or template-neutral authorization", "Required output format",
    "Page or word range", "Citation style", "Reference-count rule",
    "Abstract-language rule", "RTL or bilingual rule", "Academic year",
    "Deadline or interim schedule", "Confidentiality decision",
    "Product-image decision", "Physical-component expectation",
)
PROTECTED_HASHES = {
    "report/submission_requirements.md": "698de2a26919d3acb9184d13cbc3fe7ff6681b49dd1af42ef5aedbcd81c19e1c",
    "report/report_outline.md": "cece1ff5aed996350c4a2f2ba45dff59b7b2d1020b61dd6c108080476b5e05d0",
    "report/report_claim_source_matrix.csv": "ca2cc6a0c0cb9b8158e62cae0dcb45b0dc1c9f8373cc5fac461f01aaeec9b5be",
    "report/report_asset_register.csv": "72f8b90a37bc47df3cc235e0807a847e8e3e68f9ec23310fb0c4b29aea4a4285",
    "report/bibliography_readiness.csv": "53f01e1dd8010c7df713dcc029bc6ba1d6774902c6edaefd524adf87d7eeeffc",
}


def markdown_rows(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("| requirement_id |"))
    headers = [cell.strip() for cell in lines[start].strip("|").split("|")]
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        values = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(values) == len(headers)
        rows.append(dict(zip(headers, values, strict=True)))
    return rows


def snapshot_rows(path: Path = SNAPSHOT) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    assert tuple(reader.fieldnames or ()) == SNAPSHOT_COLUMNS
    assert all(None not in row and all(value is not None for value in row.values()) for row in rows)
    return rows


def validate_snapshot(rows: list[dict[str, str]], canonical: list[dict[str, str]] | None = None) -> None:
    assert len(rows) == 37
    assert [row["requirement_id"] for row in rows] == [f"SUB-{index:03d}" for index in range(1, 38)]
    assert [row["gate_row_id"] for row in rows] == [f"DGT-{index:03d}" for index in range(1, 38)]
    assert len({row["requirement_id"] for row in rows}) == len({row["gate_row_id"] for row in rows}) == 37
    assert rows[0]["current_value"] == "Pending human decision"

    actual_groups = {group: {row["requirement_id"] for row in rows if row["minimum_gate_group"] == group} for group in MINIMUM_GROUPS}
    assert actual_groups == GROUP_MEMBERS
    assert {row["minimum_gate_group"] for row in rows if row["minimum_gate_group"]} == set(MINIMUM_GROUPS)
    grouped_ids = set().union(*GROUP_MEMBERS.values())
    assert all(row["minimum_gate_group"] == "" for row in rows if row["requirement_id"] not in grouped_ids)
    assert all(any(row["requested_human_response"].strip() for row in rows if row["minimum_gate_group"] == group) for group in MINIMUM_GROUPS)

    assert {row["minimum_for_sp08_2"] for row in rows} <= {"yes", "conditional", "no"}
    conditional = {"SUB-001", "SUB-002", "SUB-003", "SUB-004", "SUB-005", "SUB-006", "SUB-008", "SUB-010", "SUB-013", "SUB-014", "SUB-015", "SUB-017", "SUB-018", "SUB-019", "SUB-020", "SUB-021", "SUB-022"}
    assert all(row["minimum_for_sp08_2"] == "conditional" for row in rows if row["requirement_id"] in conditional)
    assert all(row["minimum_for_sp08_2"] == "no" for row in rows if row["requirement_id"] not in grouped_ids)
    assert all(row["current_status"] not in {"resolved", "approved"} for row in rows if row["minimum_gate_group"])

    allowed_privacy = {"public_project_decision", "personal_information", "sensitive_personal_information", "restricted_document", "external_rights_decision"}
    assert {row["privacy_classification"] for row in rows} <= allowed_privacy
    by_id = {row["requirement_id"]: row for row in rows}
    assert by_id["SUB-007"]["privacy_classification"] == "personal_information"
    assert by_id["SUB-008"]["privacy_classification"] == "sensitive_personal_information"
    assert by_id["SUB-009"]["privacy_classification"] == by_id["SUB-010"]["privacy_classification"] == "personal_information"
    assert by_id["SUB-013"]["privacy_classification"] == "restricted_document"
    assert by_id["SUB-026"]["privacy_classification"] == "external_rights_decision"
    assert "do not provide identification numbers in public paste-back" in by_id["SUB-008"]["requested_human_response"].lower()
    assert all(row["requested_human_response"].strip() for row in rows if row["current_status"] in {"pending_human", "not_available"})


def paste_back_block(text: str) -> str:
    match = re.search(r"## Paste-back response template\n.*?```text\n(.*?)```", text, re.DOTALL)
    assert match
    return match.group(1)


def validate_request(text: str) -> None:
    assert text.startswith("# Human Inputs Required Before Report Drafting\n")
    assert tuple(re.findall(r"^## (.+)$", text, re.MULTILINE)) == REQUEST_SECTIONS
    assert tuple(re.findall(r"^### (GATE-[A-Z]+)$", text, re.MULTILINE)) == MINIMUM_GROUPS
    assert "project-owner approval is not supervisor approval" in text.lower()
    assert "final-report drafting has not begun" in text
    assert "missing values must not be inferred" in text.lower()
    assert "this packet is not approval by itself" in text.lower()

    block = paste_back_block(text)
    expected_lines = tuple(f"{field}: [human response required]" for field in PASTE_BACK_FIELDS)
    assert tuple(block.strip().splitlines()) == expected_lines
    assert "identification number" not in block.lower()
    assert not re.search(r"\b\d{7,10}\b", block)
    assert "Report language: [human response required]" in block
    assert "Deadline or interim schedule: [human response required]" in block
    assert "Student names: [human response required]" in block

    assert "do not place them in a public issue, ordinary chat transcript, or commit" in text
    assert "approved restricted channel" in text
    assert "URLs alone do not prove template content, product content, or permission" in text
    assert "Codex cannot answer, select, or approve any human decision" in text
    assert "Human drafting authorization: pending." in text
    assert "Report drafting: blocked." in text
    assert "PDF and presentation: not started." in text
    assert "Report drafting: approved" not in text
    assert not re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text)


def validate_packet(text: str, rows: list[dict[str, str]], canonical: list[dict[str, str]]) -> None:
    validate_request(text)
    validate_snapshot(rows, canonical)


def test_snapshot_is_frozen_pre_resolution_evidence():
    assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == "947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863"
    validate_snapshot(snapshot_rows())


def test_human_request_has_complete_unresolved_six_group_gate():
    validate_request(REQUEST.read_text(encoding="utf-8"))


def test_packet_is_strict_utf8_nonidentifying_and_private_by_default():
    text = REQUEST.read_bytes().decode("utf-8", errors="strict")
    snapshot_text = SNAPSHOT.read_bytes().decode("utf-8", errors="strict")
    combined = text + snapshot_text
    assert not any(value in combined for value in ("/home/", "/mnt/", "C:\\Users\\", "hostname"))
    assert not re.search(r"\b\d{7,10}\b", paste_back_block(text))
    student_id = next(row for row in snapshot_rows() if row["requirement_id"] == "SUB-008")
    assert student_id["current_value"] == "Pending human input"


def test_protected_report_and_sp07_assets_are_unchanged():
    for path, expected in PROTECTED_HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    manifest = json.loads((ROOT / "data/results/sp07_report_artifact_manifest.json").read_text(encoding="utf-8"))
    generated = {entry["path"]: entry["sha256"] for entry in manifest["generated_artifacts"]}
    accepted = (
        "data/results/sp07_table_experiment_coverage.csv",
        "data/results/sp07_table_correctness.csv",
        "data/results/sp07_table_timing_summary.csv",
        "docs/figures/sp07_mixed_controller_average_ns.svg",
        "docs/figures/sp07_lookup_average_ns.svg",
        "docs/figures/sp07_authorization_average_ns.svg",
    )
    assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == generated[path] for path in accepted)


def test_stage_boundary_dependencies_and_forbidden_outputs():
    assert hashlib.sha256((ROOT / "pyproject.toml").read_bytes()).hexdigest() == "08ee535e4deae72e81a98efe380c158f97ed9ecafa6f21ee27b26455e0397e67"
    forbidden_suffixes = {".tex", ".docx", ".odt", ".pdf", ".pptx", ".zip", ".tar", ".gz", ".7z"}
    assert not any(path.suffix.lower() in forbidden_suffixes for path in (REQUEST, SNAPSHOT))
    for stem in ("system_context", "top_level_architecture", "firmware_architecture", "controller_state_machine", "data_flow", "reset_sequence", "watchdog_sequence"):
        assert not any((ROOT / "docs/figures" / f"{stem}{suffix}").exists() for suffix in (".svg", ".png", ".pdf", ".jpg", ".jpeg", ".webp"))
    assert not any((ROOT / path).exists() for path in ("report/main.tex", "report/final_report.pdf", "report/presentation.pptx", "report/human_decisions.csv", ".venv", "venv"))


@pytest.mark.parametrize(
    "mutation",
    (
        "omit_sub", "alter_copy", "remove_group", "fabricate_identity",
        "preselect_language", "invent_deadline", "request_public_id", "approve_drafting",
    ),
)
def test_negative_packet_mutations_fail_validation(mutation: str, tmp_path: Path):
    canonical = markdown_rows(SUBMISSION)
    rows = copy.deepcopy(snapshot_rows())
    text = REQUEST.read_text(encoding="utf-8")
    if mutation == "omit_sub":
        rows.pop(6)
    elif mutation == "alter_copy":
        rows[0]["current_value"] = "Invented title"
    elif mutation == "remove_group":
        for row in rows:
            if row["minimum_gate_group"] == "GATE-CITATION":
                row["minimum_gate_group"] = ""
    elif mutation == "fabricate_identity":
        text = text.replace("Student names: [human response required]", "Student names: Alice Example")
    elif mutation == "preselect_language":
        text = text.replace("Report language: [human response required]", "Report language: English")
    elif mutation == "invent_deadline":
        text = text.replace("Deadline or interim schedule: [human response required]", "Deadline or interim schedule: 2026-09-01")
    elif mutation == "request_public_id":
        text = text.replace("Student names: [human response required]", "Student identification numbers: [human response required]")
    elif mutation == "approve_drafting":
        text = text.replace("Report drafting: blocked.", "Report drafting: approved.")
    request_fixture = tmp_path / "human_input_request.md"
    snapshot_fixture = tmp_path / "drafting_gate_snapshot.csv"
    request_fixture.write_text(text, encoding="utf-8")
    with snapshot_fixture.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SNAPSHOT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(AssertionError):
        validate_packet(request_fixture.read_text(encoding="utf-8"), snapshot_rows(snapshot_fixture), canonical)
