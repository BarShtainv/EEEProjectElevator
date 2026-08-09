"""SP-08.2HR partial human-gate resolution inspections."""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESPONSE = ROOT / "report/human_input_response.md"
RESOLUTION = ROOT / "report/drafting_gate_resolution.csv"
AUTHORIZATION = ROOT / "report/drafting_authorization.md"
SNAPSHOT = ROOT / "report/drafting_gate_snapshot.csv"
SUBMISSION = ROOT / "report/submission_requirements.md"
FINAL = "REPORT DRAFTING NOT AUTHORIZED — supervisor drafting authorization and a final deadline or accepted interim drafting schedule remain unresolved"

def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_partial_resolution_records_are_sanitized_and_honest():
    assert text(RESPONSE).startswith("# Authoritative Human Drafting Decisions\n")
    assert not re.search(r"\b\d{9}\b", text(RESPONSE) + text(SUBMISSION) + text(RESOLUTION) + text(AUTHORIZATION))
    assert "title approval is present" in text(RESPONSE).lower()
    assert "drafting authorization is currently not granted" in text(RESPONSE).lower()
    assert "schedule exists" in text(RESPONSE).lower()
    assert text(AUTHORIZATION).rstrip().endswith(FINAL)

def test_six_gate_ledger_and_frozen_snapshot():
    with RESOLUTION.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["gate_group"] for r in rows] == ["GATE-TITLE", "GATE-IDENTITY", "GATE-LANGUAGE", "GATE-TEMPLATE", "GATE-CITATION", "GATE-SCHEDULE"]
    assert [r["resolution_status"] for r in rows] == ["partially_resolved", "resolved", "resolved", "resolved", "resolved", "unresolved"]
    assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == "947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863"
