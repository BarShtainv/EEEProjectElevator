"""SP-08.2IR supervisor-authorization closure inspections."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "report/authoritative_inputs/supervisor_drafting_authorization.md"
RESPONSE = ROOT / "report/human_input_response.md"
AUTH = ROOT / "report/drafting_authorization.md"
SNAPSHOT = ROOT / "report/drafting_gate_snapshot.csv"

def test_affirmative_source_and_reconciled_response():
    source = SOURCE.read_text(encoding="utf-8")
    response = RESPONSE.read_text(encoding="utf-8").lower()
    assert source.startswith("# Supervisor Report-Drafting Authorization\n")
    assert "Gadi Golan" in source and "Authority:\nsupervisor" in source
    assert "The supervisor authorizes report drafting to begin." in source
    assert "Decision date or version:" in source and "Recorded in the repository by:" in source
    assert "supervisor report-drafting authorization is granted" in response
    assert "currently not granted" not in response
    assert "report/authoritative_inputs/supervisor_drafting_authorization.md" in response
    assert not re.search(r"\b\d{9}\b", source + response)

def test_frozen_snapshot_and_authorization_terminal_state():
    assert not (ROOT / "prompt4").exists()
    assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == "947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863"
    assert AUTH.read_text(encoding="utf-8").rstrip().endswith("REPORT DRAFTING AUTHORIZED")
