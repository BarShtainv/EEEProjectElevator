"""SP-08.2IR supervisor-authorization closure inspections."""
from __future__ import annotations

import hashlib
import re
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "report/authoritative_inputs/supervisor_drafting_authorization.md"
RESPONSE = ROOT / "report/human_input_response.md"
AUTH = ROOT / "report/drafting_authorization.md"
SNAPSHOT = ROOT / "report/drafting_gate_snapshot.csv"
SUBMISSION = ROOT / "report/submission_requirements.md"
LEDGER = ROOT / "report/drafting_gate_resolution.csv"

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

def test_final_gate_register_ledger_and_hygiene_contract():
    lines = SUBMISSION.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("| requirement_id |"))
    headers = [v.strip() for v in lines[start].strip("|").split("|")]
    rows = [dict(zip(headers, [v.strip() for v in line.strip("|").split("|")], strict=True)) for line in lines[start + 2:] if line.startswith("|")]
    assert len(rows) == 37 and [r["requirement_id"] for r in rows] == [f"SUB-{i:03d}" for i in range(1, 38)]
    by_id = {row["requirement_id"]: row for row in rows}
    assert by_id["SUB-008"]["status"] == by_id["SUB-011"]["status"] == "confirmed"
    assert "supervisor_drafting_authorization.md" in by_id["SUB-011"]["evidence"]
    assert by_id["SUB-022"]["status"] == "pending_human" and by_id["SUB-022"]["blocking_stage"] == "SP-08.4"
    assert "software simulation" in by_id["SUB-036"]["current_value"].lower()
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        ledger = list(csv.DictReader(handle))
    assert [r["gate_group"] for r in ledger] == ["GATE-TITLE", "GATE-IDENTITY", "GATE-LANGUAGE", "GATE-TEMPLATE", "GATE-CITATION", "GATE-SCHEDULE"]
    assert all(r["resolution_status"] == "resolved" for r in ledger)
    assert "supervisor_drafting_authorization.md" in ledger[0]["evidence"]
    assert ledger[-1]["remaining_issue"] == "Final submission due date remains pending for SP-08.4"
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    assert not any("/__pycache__/" in path or path.endswith((".pyc", ".pyo")) or path.startswith(".pytest_cache/") for path in tracked)
    assert all(rule in (ROOT / ".gitignore").read_text(encoding="utf-8") for rule in ("__pycache__/", "*.py[cod]", ".pytest_cache/"))
