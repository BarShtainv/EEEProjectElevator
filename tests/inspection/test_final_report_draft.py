"""SP-08.2D final-report draft, evidence, privacy, and artifact inspections."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "report/final_report.md"
TRACE = ROOT / "report/report_draft_traceability.csv"
CLAIMS = ROOT / "report/report_claim_source_matrix.csv"
ASSETS = ROOT / "report/report_asset_register.csv"
REFERENCES = ROOT / "report/references.bib"

TITLE = "Final Project Controlled Floor Elevator"
PENDING_DATE = "Submission date: Pending SP-08.4 human input"
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
TRACE_COLUMNS = (
    "section_number",
    "section_name",
    "report_claim_ids",
    "canonical_source_paths",
    "external_citation_keys",
    "asset_ids",
    "mandatory_limitations",
    "draft_review_status",
)
ALLOWED_REVIEW = {"drafted", "drafted_with_limit", "human_review_required"}
EXPECTED_REFERENCE_SNIPPETS = {
    1: "Guidelines for Securing Radio Frequency Identification (RFID) Systems",
    2: "Wiegand specification",
    3: "Security and Privacy Controls for Information Systems and Organizations",
    4: "NASA Software Engineering Handbook, Version D",
    5: "STM32F101xx, STM32F102xx, STM32F103xx, STM32F105xx and STM32F107xx",
    6: "ARM Developer Suite Developer Guide",
    7: "ARM Architecture Reference Manual: ARMv7-A and ARMv7-R Edition",
    8: "ARMADA 38x Family Functional Specifications",
}
ACCEPTED_ASSET_HASHES = {
    "data/results/sp07_table_experiment_coverage.csv": "f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f",
    "data/results/sp07_table_correctness.csv": "2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224",
    "data/results/sp07_table_timing_summary.csv": "5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811",
    "docs/figures/sp07_mixed_controller_average_ns.svg": "7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930",
    "docs/figures/sp07_lookup_average_ns.svg": "26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096",
    "docs/figures/sp07_authorization_average_ns.svg": "433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9",
}
MERMAID_PATHS = (
    "docs/figures/system_context.mmd",
    "docs/figures/top_level_architecture.mmd",
    "docs/figures/firmware_architecture.mmd",
    "docs/figures/controller_state_machine.mmd",
    "docs/figures/data_flow.mmd",
    "docs/figures/reset_sequence.mmd",
    "docs/figures/watchdog_sequence.mmd",
)


def read_csv(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return tuple(reader.fieldnames or ()), rows


def section_pairs(text: str) -> list[tuple[str, str]]:
    return re.findall(r"^## (\d+)\. (.+)$", text, re.MULTILINE)


def section_block(text: str, number: int) -> str:
    match = re.search(
        rf"^## {number}\. {re.escape(SECTIONS[number - 1])}\n(.*?)(?=^## \d+\.|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"missing section {number}"
    return match.group(1)


def reference_entries(text: str) -> dict[int, str]:
    block = section_block(text, 14)
    matches = list(re.finditer(r"^\[(\d+)\] (.+?)(?=\n\n\[\d+\]|\Z)", block, re.MULTILINE | re.DOTALL))
    return {int(match.group(1)): " ".join(match.group(2).split()) for match in matches}


def citation_numbers(text: str) -> list[int]:
    body = text[: text.index("## 14. References")]
    return [int(value) for value in re.findall(r"\[(\d+)\]", body)]


def bib_keys() -> set[str]:
    return set(re.findall(r"@\w+\{([^,]+),", REFERENCES.read_text(encoding="utf-8")))


def assert_number_present(text: str, value: int) -> None:
    forms = {str(value), f"{value:,}"}
    assert any(re.search(rf"(?<![\d,]){re.escape(form)}(?![\d,])", text) for form in forms), value


def validate_report_text(text: str) -> None:
    assert text.startswith(f"# {TITLE}\n")
    assert section_pairs(text) == [(str(index), name) for index, name in enumerate(SECTIONS, 1)]
    assert text.count(PENDING_DATE) == 1
    assert len(re.findall(r"^Submission date:", text, re.MULTILINE)) == 1
    for metadata in (
        "Bar Shtainvortzel",
        "Ariel University",
        "Faculty of Engineering",
        "Department of Electrical and Electronics",
        "B.Sc. program",
        "Professor Gadi Golan",
        "Academic year:** 4th year",
    ):
        assert metadata in text
    assert not re.search(r"\b\d{9}\b", text)

    lower = text.lower()
    for phrase in (
        "software-only",
        "commercial processor architecture and specific mcu remain unknown",
        "commercial frequencies, credential technologies, and smart-card protocols remain unknown",
        "commercial wiegand support",
        "armv7-a/r is therefore not cortex-m documentation",
        "stm32 material does not establish the commercial controller's mcu",
        "physical reader, elevator installation, commercial controller, real-time system, safety system",
        "absence of preserved evidence is not evidence",
    ):
        assert phrase in lower

    affirmative_forbidden = (
        r"^(?:the )?commercial (?:product|item|card|controller).{0,80}(?:uses|contains|implements|supports|provides).{0,80}stm32",
        r"^(?:the )?commercial (?:product|item|card|controller).{0,80}(?:uses|supports|operates at).{0,80}(?:125\s*k?hz|13\.56\s*mhz|nfc|mifare)",
        r"^(?:the )?commercial (?:product|item|card|controller).{0,80}(?:uses|supports|provides|implements).{0,80}(?:wiegand|relay|open collector)",
        r"(?:physically validated|physical validation (?:of|for)) (?:the )?elevator",
        r"(?:achieved|has|holds|received) safety certification",
        r"(?:is|was|demonstrates?|proved?) statistically significant",
        r"(?:is|was|demonstrates?|proved?) constant[- ]time",
    )
    assert not any(re.search(pattern, lower, re.DOTALL | re.MULTILINE) for pattern in affirmative_forbidden)

    references = reference_entries(text)
    citations = citation_numbers(text)
    assert citations and citations[0] == 1
    first_use = list(dict.fromkeys(citations))
    assert first_use == list(range(1, len(first_use) + 1))
    assert set(citations) == set(references)
    assert set(references) == set(EXPECTED_REFERENCE_SNIPPETS)
    for number, snippet in EXPECTED_REFERENCE_SNIPPETS.items():
        assert snippet in references[number]


def validate_trace_rows(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 15
    assert [(row["section_number"], row["section_name"]) for row in rows] == [
        (str(index), name) for index, name in enumerate(SECTIONS, 1)
    ]
    claim_headers, claim_rows = read_csv(CLAIMS)
    del claim_headers
    valid_claims = {row["report_claim_id"] for row in claim_rows}
    _, asset_rows = read_csv(ASSETS)
    valid_assets = {row["asset_id"] for row in asset_rows}
    valid_bib_keys = bib_keys()
    mapped_claims: set[str] = set()
    for row in rows:
        assert row["draft_review_status"] in ALLOWED_REVIEW
        assert row["mandatory_limitations"].strip()
        claims = set(filter(None, row["report_claim_ids"].split(";")))
        assert claims <= valid_claims
        mapped_claims |= claims
        for source in filter(None, row["canonical_source_paths"].split(";")):
            assert not Path(source).is_absolute() and (ROOT / source).exists(), source
        assert set(filter(None, row["external_citation_keys"].split(";"))) <= valid_bib_keys
        assert set(filter(None, row["asset_ids"].split(";"))) <= valid_assets
    assert mapped_claims == valid_claims


def canonical_correctness() -> dict[tuple[str, str], int]:
    _, rows = read_csv(ROOT / "data/results/sp07_table_correctness.csv")
    return {(row["measurement_group"], row["metric"]): int(float(row["value"])) for row in rows}


def test_report_exists_has_exact_structure_and_authorized_metadata() -> None:
    assert REPORT.is_file()
    validate_report_text(REPORT.read_text(encoding="utf-8"))


def test_quantitative_statements_match_accepted_sources() -> None:
    text = REPORT.read_text(encoding="utf-8")
    _, requirement_rows = read_csv(ROOT / "docs/requirements_to_test_traceability.csv")
    required = sum(row["priority"] == "required" for row in requirement_rows)
    optional = sum(row["priority"] == "optional" for row in requirement_rows)
    assert (len(requirement_rows), required, optional) == (66, 60, 6)
    for value in (66, 60, 6):
        assert_number_present(text, value)

    values = canonical_correctness()
    expected = {
        ("mixed_controller", "processed"): 39000,
        ("mixed_controller", "granted"): 15600,
        ("mixed_controller", "denied"): 19500,
        ("mixed_controller", "unauthorized_floor_denials"): 7800,
        ("mixed_controller", "disabled_credential_denials"): 5850,
        ("mixed_controller", "unknown_credential_denials"): 5850,
        ("mixed_controller", "invalid_frame_validation_failures"): 3900,
        ("mixed_controller", "other_outcomes"): 0,
        ("isolated_lookup", "processed"): 12000,
        ("isolated_lookup", "correct_hits"): 6000,
        ("isolated_lookup", "correct_misses"): 6000,
        ("isolated_lookup", "mismatches"): 0,
        ("isolated_authorization", "processed"): 12000,
        ("isolated_authorization", "correct_grants"): 4800,
        ("isolated_authorization", "correct_denials"): 6000,
        ("isolated_authorization", "correct_invalid_floor_errors"): 1200,
        ("isolated_authorization", "incorrect_grants"): 0,
        ("isolated_authorization", "incorrect_denials"): 0,
        ("isolated_authorization", "other_mismatches"): 0,
    }
    assert all(values[key] == value for key, value in expected.items())
    for value in set(expected.values()) | {24000}:
        assert_number_present(text, value)


def test_timing_semantics_and_boundaries_are_explicit() -> None:
    text = REPORT.read_text(encoding="utf-8").lower()
    _, timing = read_csv(ROOT / "data/results/sp07_table_timing_summary.csv")
    assert len(timing) == 12
    assert {row["operation"] for row in timing} == {
        "mixed_controller_submit",
        "credential_repository_lookup",
        "authorization_decision",
    }
    assert {int(row["repetition_count"]) for row in timing} == {3}
    assert {row["timer"] for row in timing} == {"time.perf_counter_ns"}
    for phrase in (
        "three repetition-level observations",
        "not pooled across individual calls",
        "raw per-call timing samples were not retained",
        "one recorded host",
        "operation boundaries differ",
        "must not be ranked against one another",
        "no statistical-significance claim is made",
        "do not establish monotonic scaling, constant-time behavior, asymptotic complexity",
        "or hardware performance",
    ):
        assert phrase in text


def test_traceability_schema_resolution_and_complete_rpt_coverage() -> None:
    headers, rows = read_csv(TRACE)
    assert headers == TRACE_COLUMNS
    validate_trace_rows(rows)


def test_accepted_assets_are_unchanged_and_planned_diagrams_are_deferred() -> None:
    text = REPORT.read_text(encoding="utf-8")
    for path, expected in ACCEPTED_ASSET_HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    linked_images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert linked_images == [
        "../docs/figures/sp07_mixed_controller_average_ns.svg",
        "../docs/figures/sp07_lookup_average_ns.svg",
        "../docs/figures/sp07_authorization_average_ns.svg",
    ]
    for path in MERMAID_PATHS:
        marker = f"Figure planned from {path}; rendering deferred to the controlled document-production stage."
        assert marker in text
        stem = ROOT / Path(path).with_suffix("")
        assert not any(stem.with_suffix(suffix).exists() for suffix in (".svg", ".png", ".pdf"))
    assert not (ROOT / "evidence/images/product_capture").exists()


def test_forbidden_final_outputs_are_absent() -> None:
    assert not list((ROOT / "report").glob("*.docx"))
    assert not list((ROOT / "report").glob("*.pdf"))
    assert not list(ROOT.glob("*.pptx"))
    assert not list(ROOT.glob("presentation/**/*"))
    assert not list(ROOT.glob("release/**/*"))
    assert not list(ROOT.glob("*.zip"))


@pytest.mark.parametrize(
    ("case", "mutate"),
    (
        ("missing_section", lambda value: re.sub(r"^## 11\. Discussion\n", "", value, count=1, flags=re.MULTILINE)),
        ("reordered_section", lambda value: value.replace("## 10. Results", "## SWAP. Results", 1).replace("## 11. Discussion", "## 10. Results", 1).replace("## SWAP. Results", "## 11. Discussion", 1)),
        ("student_identifier", lambda value: value + "\nStudent identifier: " + "1" * 9 + "\n"),
        ("invented_submission_date", lambda value: value.replace(PENDING_DATE, "Submission date: 2026-09-01")),
        ("commercial_stm32", lambda value: value + "\nThe commercial product uses an STM32 processor.\n"),
        ("commercial_frequency", lambda value: value + "\nThe commercial controller supports 125 kHz RFID.\n"),
        ("physical_elevator_validation", lambda value: value + "\nThe work physically validated the elevator.\n"),
        ("safety_certification", lambda value: value + "\nThe project achieved safety certification.\n"),
        ("constant_time", lambda value: value + "\nThe implementation is constant-time.\n"),
        ("statistical_significance", lambda value: value + "\nThe timing result is statistically significant.\n"),
        ("citation_without_reference", lambda value: value.replace("## 14. References", "Unsupported claim [9].\n\n## 14. References")),
        ("fabricated_reference", lambda value: value.replace("## 15. Appendices", "[9] Fabricated Author, *Fabricated Source*, 2026.\n\n## 15. Appendices")),
        ("unknown_only_rpt_promoted", lambda value: value + "\nThe commercial card implements Wiegand output.\n"),
    ),
)
def test_negative_report_fixtures_are_rejected(tmp_path: Path, case: str, mutate) -> None:
    fixture = tmp_path / f"{case}.md"
    fixture.write_text(mutate(REPORT.read_text(encoding="utf-8")), encoding="utf-8")
    with pytest.raises(AssertionError):
        validate_report_text(fixture.read_text(encoding="utf-8"))


def test_missing_traceability_source_fixture_is_rejected() -> None:
    _, rows = read_csv(TRACE)
    broken = deepcopy(rows)
    broken[0]["canonical_source_paths"] += ";does/not/exist.md"
    with pytest.raises(AssertionError):
        validate_trace_rows(broken)


def test_unregistered_asset_fixture_is_rejected() -> None:
    _, rows = read_csv(TRACE)
    broken = deepcopy(rows)
    broken[0]["asset_ids"] += ";AST-999"
    with pytest.raises(AssertionError):
        validate_trace_rows(broken)


def test_reference_keys_and_manifest_sources_resolve_without_fabrication() -> None:
    _, rows = read_csv(TRACE)
    used_keys = set().union(*(set(filter(None, row["external_citation_keys"].split(";"))) for row in rows))
    assert used_keys == bib_keys() - {"evidence_gated_workflow_handbook"}
    manifest = json.loads((ROOT / "data/results/sp07_report_artifact_manifest.json").read_text(encoding="utf-8"))
    generated = {entry["path"]: entry["sha256"] for entry in manifest["generated_artifacts"]}
    assert all(generated[path] == digest for path, digest in ACCEPTED_ASSET_HASHES.items())
