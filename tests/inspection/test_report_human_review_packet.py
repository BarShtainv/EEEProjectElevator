"""SP-08.3H final-report human technical review packet inspections."""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "report/final_report.md"
TRACE = ROOT / "report/report_draft_traceability.csv"
REQUEST = ROOT / "report/human_review_request.md"
RESPONSE = ROOT / "report/authoritative_inputs/final_report_human_review.md"

REPORT_HASH = "db43c6f7f218d8d37f339d0d93420e2b819e022883ddc5cb357f07b9064ab170"
TRACE_HASH = "957cac4b505154fc745d8a9b09dd96bb7fde6de4b26feb9f1b8f9f6e39489902"
TITLE = "Final Project Controlled Floor Elevator"
STARTING_COMMIT = "e47e8ce537322a4ca20a921a11f2d8dd5c669bbc"
RESPONSE_PATH = "report/authoritative_inputs/final_report_human_review.md"
SECTIONS = (
    "Abstract",
    "Introduction",
    "Product Under Study and Available Evidence",
    "Research Methodology and Limitations",
    "Literature Review",
    "Requirements and System Boundary",
    "Proposed Reference Architecture",
    "Software-Model Design and Implementation",
    "Verification and Experimental Method",
    "Results",
    "Discussion",
    "Limitations and Validity Threats",
    "Conclusions and Future Work",
    "References",
    "Appendices",
)
CHECKLIST_HEADINGS = (
    "## A. Overall engineering accuracy",
    "## B. Abstract and introduction",
    "## C. Product evidence",
    "## D. Literature review",
    "## E. Requirements and system boundary",
    "## F. Architecture",
    "## G. Software design",
    "## H. Verification methodology",
    "## I. Results",
    "## J. Results interpretation",
    "## K. Limitations",
    "## L. Conclusions and future work",
    "## M. References",
    "## N. Appendices",
    "## O. Readability and balance",
    "## P. Final document preparation",
)
MERMAID_PATHS = (
    "docs/figures/system_context.mmd",
    "docs/figures/top_level_architecture.mmd",
    "docs/figures/firmware_architecture.mmd",
    "docs/figures/controller_state_machine.mmd",
    "docs/figures/data_flow.mmd",
    "docs/figures/reset_sequence.mmd",
    "docs/figures/watchdog_sequence.mmd",
)
DECISIONS = (
    "approved_for_revision_closure",
    "approved_with_required_revisions",
    "major_revision_required",
    "not_approved",
)
RESPONSE_FIELDS = (
    "Draft commit:",
    "Reviewer 1 name:",
    "Reviewer 1 role:",
    "Reviewer 2 name:",
    "Reviewer 2 role:",
    "Review date or version:",
    "Overall review decision:",
)
RESPONSE_HEADINGS = (
    "## Required revisions",
    "## Recommended revisions",
    "## Technical corrections",
    "## Literature and citation feedback",
    "## Architecture and figure decisions",
    "## Results and discussion feedback",
    "## Limitations feedback",
    "## Conclusions feedback",
    "## Formatting and DOCX guidance",
    "## Items explicitly approved without change",
    "## Reviewer confirmation",
)
SP07_HASHES = {
    "data/results/sp07_table_experiment_coverage.csv": "f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f",
    "data/results/sp07_table_correctness.csv": "2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224",
    "data/results/sp07_table_timing_summary.csv": "5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811",
    "docs/figures/sp07_mixed_controller_average_ns.svg": "7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930",
    "docs/figures/sp07_lookup_average_ns.svg": "26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096",
    "docs/figures/sp07_authorization_average_ns.svg": "433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_packet(text: str) -> None:
    assert text.startswith("# Final Engineering Report Human Review Request\n")
    for value in (TITLE, STARTING_COMMIT, "report/final_report.md", "6,707", "exactly fifteen numbered main sections"):
        assert value in text
    for heading in CHECKLIST_HEADINGS:
        assert heading in text
    for path in MERMAID_PATHS:
        assert f"`{path}`" in text
    for value in DECISIONS:
        assert value in text
    assert RESPONSE_PATH in text
    assert "# Final Engineering Report Human Review" in text
    for field in RESPONSE_FIELDS:
        assert field in text
    for heading in RESPONSE_HEADINGS:
        assert heading in text

    lower = text.lower()
    for phrase in (
        "software-only",
        "not an approved final submission",
        "not being asked to rerun",
        "39,000 mixed requests",
        "15,600 grants",
        "19,500 denials",
        "3,900 invalid frames",
        "24,000 isolated operations",
        "zero lookup mismatches",
        "zero incorrect authorization outcomes",
        "three accepted sp-07 figures",
        "one-host scope",
        "exactly three measured repetitions",
        "lack of raw per-call data",
        "statistical significance",
        "constant-time or asymptotic behavior",
        "rpt-027",
        "older `pending_human` status",
        "ieee citation style",
        "absence of the response is not approval",
        "final submission due date is not a prerequisite",
        "separate sp-08.4 administrative input",
        "genuine human-supplied review decisions",
        "student identification numbers",
        "private email addresses",
        "private portal information",
    ):
        assert phrase in lower
    assert "`none` is acceptable" in lower
    assert not re.search(r"\b\d{9}\b", text)
    for forbidden in (
        "the report is finally approved",
        "human review has already occurred",
        "human review was completed",
        "the submission due date is a prerequisite for review",
    ):
        assert forbidden not in lower


def test_accepted_report_and_traceability_are_byte_identical() -> None:
    assert REPORT.is_file() and sha256(REPORT) == REPORT_HASH
    assert TRACE.is_file() and sha256(TRACE) == TRACE_HASH
    report_sections = re.findall(r"^## (\d+)\. (.+)$", REPORT.read_text(encoding="utf-8"), re.MULTILINE)
    assert report_sections == [(str(index), name) for index, name in enumerate(SECTIONS, 1)]


def test_traceability_still_resolves_all_sections_sources_keys_assets_and_claims() -> None:
    with TRACE.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    assert tuple(reader.fieldnames or ()) == (
        "section_number", "section_name", "report_claim_ids", "canonical_source_paths",
        "external_citation_keys", "asset_ids", "mandatory_limitations", "draft_review_status",
    )
    assert len(rows) == 15
    assert [(row["section_number"], row["section_name"]) for row in rows] == [
        (str(index), name) for index, name in enumerate(SECTIONS, 1)
    ]
    for row in rows:
        for source in filter(None, row["canonical_source_paths"].split(";")):
            assert (ROOT / source).exists()
    with (ROOT / "report/references.bib").open(encoding="utf-8") as handle:
        citation_keys = set(re.findall(r"@\w+\{([^,]+),", handle.read()))
    with (ROOT / "report/report_asset_register.csv").open(encoding="utf-8", newline="") as handle:
        asset_ids = {row["asset_id"] for row in csv.DictReader(handle)}
    with (ROOT / "report/report_claim_source_matrix.csv").open(encoding="utf-8", newline="") as handle:
        claim_ids = {row["report_claim_id"] for row in csv.DictReader(handle)}
    assert set().union(*(set(filter(None, row["external_citation_keys"].split(";"))) for row in rows)) <= citation_keys
    assert set().union(*(set(filter(None, row["asset_ids"].split(";"))) for row in rows)) <= asset_ids
    assert set().union(*(set(filter(None, row["report_claim_ids"].split(";"))) for row in rows)) == claim_ids
    assert len(claim_ids) == 27


def test_review_request_is_complete_and_does_not_fabricate_response() -> None:
    assert REQUEST.is_file()
    validate_packet(REQUEST.read_text(encoding="utf-8"))
    assert not RESPONSE.exists()


def test_accepted_sp07_assets_and_deferred_mermaid_state_are_unchanged() -> None:
    for path, digest in SP07_HASHES.items():
        assert sha256(ROOT / path) == digest
    for path in MERMAID_PATHS:
        stem = ROOT / Path(path).with_suffix("")
        assert not any(stem.with_suffix(suffix).exists() for suffix in (".svg", ".png", ".pdf"))


@pytest.mark.parametrize(
    ("case", "mutate"),
    (
        ("missing_response_path", lambda text: text.replace(RESPONSE_PATH, "report/authoritative_inputs/RESPONSE_PATH_MISSING.md")),
        ("missing_decision", lambda text: text.replace("approved_with_required_revisions", "DECISION_VALUE_REMOVED")),
        ("false_final_approval", lambda text: text + "\nThe report is finally approved.\n"),
        ("false_review_occurrence", lambda text: text + "\nHuman review has already occurred.\n"),
        ("due_date_prerequisite", lambda text: text + "\nThe submission due date is a prerequisite for review.\n"),
        ("student_identifier", lambda text: text + "\nStudent identification number: " + "1" * 9 + "\n"),
        ("removed_category", lambda text: text.replace("## K. Limitations", "## CATEGORY REMOVED")),
    ),
)
def test_negative_packet_fixtures_are_rejected(tmp_path: Path, case: str, mutate) -> None:
    fixture = tmp_path / f"{case}.md"
    fixture.write_text(mutate(REQUEST.read_text(encoding="utf-8")), encoding="utf-8")
    with pytest.raises(AssertionError):
        validate_packet(fixture.read_text(encoding="utf-8"))


def test_authorization_privacy_and_forbidden_outputs_remain_bounded() -> None:
    assert (ROOT / "report/drafting_authorization.md").read_text(encoding="utf-8").rstrip().endswith(
        "REPORT DRAFTING AUTHORIZED"
    )
    assert not re.search(r"\b\d{9}\b", REQUEST.read_text(encoding="utf-8"))
    assert not list((ROOT / "report").glob("*.docx"))
    assert not list((ROOT / "report").glob("*.pdf"))
    assert not list(ROOT.glob("*.pptx"))
    assert not list(ROOT.glob("release/**/*"))
