"""SP-08.2HR partial human-gate resolution inspections."""
from __future__ import annotations

import csv
import hashlib
import re
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESPONSE = ROOT / "report/human_input_response.md"
RESOLUTION = ROOT / "report/drafting_gate_resolution.csv"
AUTHORIZATION = ROOT / "report/drafting_authorization.md"
SNAPSHOT = ROOT / "report/drafting_gate_snapshot.csv"
SUBMISSION = ROOT / "report/submission_requirements.md"
FINAL = "REPORT DRAFTING AUTHORIZED"
LEDGER_COLUMNS = ("gate_group", "requirement_ids", "resolution_status", "authoritative_decision", "authority", "evidence", "privacy_handling", "drafting_effect", "remaining_issue", "notes")

def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_partial_resolution_records_are_sanitized_and_honest():
    assert text(RESPONSE).startswith("# Authoritative Human Drafting Decisions\n")
    assert not re.search(r"\b\d{9}\b", text(RESPONSE) + text(SUBMISSION) + text(RESOLUTION) + text(AUTHORIZATION))
    assert "title approval is present" in text(RESPONSE).lower()
    assert "drafting authorization is currently not granted" in text(RESPONSE).lower()
    response = text(RESPONSE).lower()
    assert "final submission due date is not yet established" in response
    assert "not required to begin report drafting" in response
    assert "student identification number: not stored in the repository" in response
    assert text(AUTHORIZATION).rstrip().endswith(FINAL)

def test_six_gate_ledger_and_frozen_snapshot():
    with RESOLUTION.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader)
    assert tuple(reader.fieldnames or ()) == LEDGER_COLUMNS
    assert [r["gate_group"] for r in rows] == ["GATE-TITLE", "GATE-IDENTITY", "GATE-LANGUAGE", "GATE-TEMPLATE", "GATE-CITATION", "GATE-SCHEDULE"]
    assert [r["resolution_status"] for r in rows] == ["resolved"] * 6
    assert rows[0]["evidence"] == "report/human_input_response.md;report/authoritative_inputs/supervisor_drafting_authorization.md"
    assert rows[0]["drafting_effect"] == "No report-drafting blocker"
    assert rows[-1]["drafting_effect"] == "No report-drafting blocker"
    assert rows[-1]["remaining_issue"] == "Final submission due date remains pending for SP-08.4"
    assert not any(re.search(r"\b\d{9}\b", ",".join(row.values())) for row in rows)
    assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == "947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863"

def test_submission_authorization_and_negative_fixtures():
    submission = text(SUBMISSION)
    sub008 = next(line for line in submission.splitlines() if line.startswith("| SUB-008"))
    assert "| confirmed |" in sub008 and "Private-handling policy confirmed" in sub008
    assert "| confirmed |" in next(line for line in submission.splitlines() if line.startswith("| SUB-011"))
    sub022 = next(line for line in submission.splitlines() if line.startswith("| SUB-022"))
    assert "| pending_human | SP-08.4 |" in sub022
    assert not re.search(r"\b\d{9}\b", submission)
    identifier_fixture = text(RESPONSE) + "\n" + "1" * 9 + "\n"
    authorization_fixture = text(AUTHORIZATION).replace("REPORT DRAFTING AUTHORIZED", "REPORT DRAFTING NOT AUTHORIZED")
    deadline_fixture = text(RESPONSE).replace("not yet established", "established")
    assert re.search(r"\b\d{9}\b", identifier_fixture)
    assert not authorization_fixture.rstrip().endswith(FINAL)
    assert "not required to begin report drafting" not in (text(RESPONSE).replace("not required to begin report drafting", "required before report drafting")).lower()
