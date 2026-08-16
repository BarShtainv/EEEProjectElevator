"""SP-08.1 report-preparation and protected-boundary inspections."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "report/submission_requirements.md"
OUTLINE = ROOT / "report/report_outline.md"
CLAIMS = ROOT / "report/report_claim_source_matrix.csv"
ASSETS = ROOT / "report/report_asset_register.csv"
BIBLIOGRAPHY = ROOT / "report/bibliography_readiness.csv"
NEW_FILES = (SUBMISSION, OUTLINE, CLAIMS, ASSETS, BIBLIOGRAPHY)

SUBMISSION_COLUMNS = ("requirement_id", "input_or_decision", "current_value", "authority", "evidence", "status", "blocking_stage", "responsible_party", "notes")
CLAIM_COLUMNS = ("report_claim_id", "chapter_number", "claim_or_topic", "evidence_class", "source_ids", "source_paths", "validation_claim_ids", "required_qualifiers", "report_status", "blocking_input", "notes")
ASSET_COLUMNS = ("asset_id", "asset_type", "path", "intended_chapter", "source_artifacts", "caption_or_title", "interpretation_limit", "readiness_status", "required_action", "notes")
BIB_COLUMNS = ("source_id", "title", "author_or_organization", "year", "source_type", "canonical_path_or_url", "authority", "planned_report_use", "metadata_status", "access_status", "citation_ready", "missing_fields", "notes")
SECTION_NAMES = ("Abstract", "Introduction", "Product Under Study and Available Evidence", "Research Methodology and Limitations", "Literature Review", "Requirements and System Boundary", "Proposed Reference Architecture", "Software-Model Design and Implementation", "Verification and Experimental Method", "Results", "Discussion", "Limitations and Validity Threats", "Conclusions and Future Work", "References", "Appendices")
CANONICAL_MERMAID_PATHS = (
    "docs/figures/system_context.mmd",
    "docs/figures/top_level_architecture.mmd",
    "docs/figures/firmware_architecture.mmd",
    "docs/figures/controller_state_machine.mmd",
    "docs/figures/data_flow.mmd",
    "docs/figures/reset_sequence.mmd",
    "docs/figures/watchdog_sequence.mmd",
)
HISTORICAL_INPUT_HASHES = {
    "report/submission_requirements.md": "2f0d73021ed2453789234e9adcbb6806471cf17eff0b30a914580164299eefa8",
    "report/report_outline.md": "cece1ff5aed996350c4a2f2ba45dff59b7b2d1020b61dd6c108080476b5e05d0",
    "report/bibliography_readiness.csv": "53f01e1dd8010c7df713dcc029bc6ba1d6774902c6edaefd524adf87d7eeeffc",
}


def csv_rows(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    assert tuple(reader.fieldnames or ()) == columns
    assert rows and all(None not in row and all(value is not None for value in row.values()) for row in rows)
    return rows


def markdown_table(path: Path, first_header: str) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith(f"| {first_header} |"))
    headers = [cell.strip() for cell in lines[start].strip("|").split("|")]
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        values = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(values) == len(headers)
        rows.append(dict(zip(headers, values, strict=True)))
    return rows


def source_index_ids() -> set[str]:
    return set(re.findall(r"^\| (SRC-[A-Z0-9]+-\d{3}) \|", (ROOT / "evidence/source_index.md").read_text(encoding="utf-8"), re.MULTILINE))


def evidence_ids() -> set[str]:
    rows = csv_rows(ROOT / "evidence/claim_evidence_matrix.csv", ("claim_id", "claim_text", "evidence_class", "source_id", "source_path", "source_location", "status", "confidence", "notes"))
    return {row["source_id"] for row in rows}


def explicit_mermaid_paths(path: Path) -> set[str]:
    return set(re.findall(r"docs/figures/[A-Za-z0-9_./-]+\.mmd", path.read_text(encoding="utf-8")))


def validate_canonical_mermaid_rows(rows: list[dict[str, str]]) -> None:
    expected = set(CANONICAL_MERMAID_PATHS)
    architecture_paths = explicit_mermaid_paths(ROOT / "docs/architecture.md")
    outline_paths = explicit_mermaid_paths(OUTLINE)
    registered = [row["path"] for row in rows if row["path"].endswith(".mmd")]
    assert architecture_paths == expected
    assert set(registered) == expected and len(registered) == len(expected)
    assert architecture_paths <= set(registered)
    assert outline_paths <= set(registered)
    for canonical_path in CANONICAL_MERMAID_PATHS:
        assert registered.count(canonical_path) == 1

    diagram_rows = [row for row in rows if row["asset_type"] == "diagram"]
    assert len({row["path"] for row in diagram_rows}) == len(diagram_rows)
    for row in diagram_rows:
        path = Path(row["path"])
        assert not path.is_absolute() and (ROOT / path).is_file()
        assert row["readiness_status"] == "ready_with_limit"
        assert row["interpretation_limit"].strip()
        for source in row["source_artifacts"].split(";"):
            assert not Path(source).is_absolute() and (ROOT / source).is_file()
        if row["path"] in expected:
            assert (ROOT / path.with_suffix(".svg")).is_file()
            assert (ROOT / path.with_suffix(".png")).is_file()


def test_submission_requirements_gate_is_explicit_and_complete():
    text = SUBMISSION.read_text(encoding="utf-8")
    assert text.startswith("# Submission Requirements and Authoritative Inputs\n")
    rows = markdown_table(SUBMISSION, "requirement_id")
    assert len(rows) == 37 and tuple(rows[0]) == SUBMISSION_COLUMNS
    assert [row["requirement_id"] for row in rows] == [f"SUB-{index:03d}" for index in range(1, 38)]
    assert all(row["status"] in {"confirmed", "working_value", "pending_human", "not_available", "not_required", "conflict"} for row in rows)
    assert all(row["current_value"] and row["responsible_party"] and row["blocking_stage"] for row in rows)
    assert all("pending" in row["current_value"].lower() for row in rows if row["status"] == "pending_human")
    assert "internal project gate, not a university specification" in text and "no pending item may be silently invented" in text


def test_submission_identity_title_and_human_blockers_are_not_conflated():
    rows = {row["requirement_id"]: row for row in markdown_table(SUBMISSION, "requirement_id")}
    assert rows["SUB-001"]["status"] == rows["SUB-002"]["status"] == "confirmed"
    assert rows["SUB-011"]["status"] == "confirmed" and "authorizes report drafting" in rows["SUB-011"]["current_value"].lower()
    for key in ("SUB-003", "SUB-007", "SUB-009", "SUB-012", "SUB-013", "SUB-016"):
        assert rows[key]["status"] == "confirmed"
    for key in ("SUB-022", "SUB-028", "SUB-029", "SUB-030"):
        assert rows[key]["status"] == "pending_human"
    text = SUBMISSION.read_text(encoding="utf-8")
    assert all(heading in text for heading in ("## Blocking inputs for SP-08.2", "## Non-blocking inputs for early drafting", "## Human review checklist"))
    for value in ("no unresolved human decision", "deadline", "sp-08.4"):
        assert value in text.lower()
    assert "Codex cannot approve" in text


def test_report_outline_has_exact_order_and_complete_planning_fields():
    text = OUTLINE.read_text(encoding="utf-8")
    assert text.startswith("# Final Engineering Report Content Architecture\n")
    sections = re.findall(r"^## (\d+)\. (.+)$", text, re.MULTILINE)
    assert sections == [(str(index), name) for index, name in enumerate(SECTION_NAMES, 1)]
    required = ("Purpose", "Questions", "Canonical sources", "Evidence classes", "Claim IDs", "Proposed tables and figures", "Mandatory limitations", "Prohibited claims", "Unresolved inputs", "Drafting status")
    blocks = re.split(r"^## \d+\. .+$", text, flags=re.MULTILINE)[1:]
    assert len(blocks) == 15
    for block in blocks:
        assert all(f"**{label}:**" in block for label in required)
        status = re.search(r"\*\*Drafting status:\*\* `([^`]+)`", block)
        assert status and status.group(1) in {"ready_for_draft", "ready_with_limits", "blocked_by_human_input", "blocked_by_missing_evidence", "appendix_only"}
    assert "not final report prose" in text and "approved submission paragraphs" in text


def test_outline_preserves_product_literature_results_and_conclusion_boundaries():
    text = OUTLINE.read_text(encoding="utf-8")
    assert "Only URLs and limited owner-supplied evidence are preserved" in text
    assert "original capture, listing content, images" in text
    assert "ARM/STM32 sources are representative, not product evidence" in text
    assert "accepted 976-test SP-06 verification snapshot is historical" in text
    assert "mixed `Controller.submit`, direct lookup, and direct authorization boundaries differ" in text
    for phrase in ("Pooled statistics", "significance", "monotonic scaling", "constant-time", "hardware/field/commercial performance"):
        assert phrase in text
    assert "allow only conclusions" not in text.lower() or "authorized" in text.lower()


def test_claim_matrix_schema_ids_statuses_and_paths_resolve():
    rows = csv_rows(CLAIMS, CLAIM_COLUMNS)
    assert len(rows) == 27 and [row["report_claim_id"] for row in rows] == [f"RPT-{index:03d}" for index in range(1, 28)]
    assert all(row["chapter_number"].isdigit() and 1 <= int(row["chapter_number"]) <= 15 for row in rows)
    assert all(row["evidence_class"] in {"verified_product_evidence", "external_technical_evidence", "engineering_inference", "proposed_reference_design", "unknown_or_unresolved", "supported_quantitative_claim", "project_governance"} for row in rows)
    assert all(row["report_status"] in {"usable", "usable_with_limit", "unknown_only", "not_for_report", "pending_human", "superseded"} for row in rows)
    for row in rows:
        for source in row["source_paths"].split(";"):
            assert not Path(source).is_absolute() and (ROOT / source).exists(), (row["report_claim_id"], source)


def test_claim_matrix_source_and_validation_ids_resolve():
    rows = csv_rows(CLAIMS, CLAIM_COLUMNS)
    resolvable = source_index_ids() | evidence_ids() | set(re.findall(r"^\| (DEC-\d{3}) \|", (ROOT / "docs/decision_log.md").read_text(encoding="utf-8"), re.MULTILINE))
    with (ROOT / "audit/validation/subproject_07_final_validation_ledger.csv").open(encoding="utf-8", newline="") as handle:
        ledger_ids = {row["claim_id"] for row in csv.DictReader(handle)}
    for row in rows:
        assert set(row["source_ids"].split(";")) <= resolvable
        validation_ids = set(filter(None, row["validation_claim_ids"].split(";")))
        assert validation_ids <= ledger_ids
        if row["evidence_class"] == "supported_quantitative_claim":
            assert validation_ids


def test_timing_and_high_impact_claim_rules_are_enforced():
    rows = {row["report_claim_id"]: row for row in csv_rows(CLAIMS, CLAIM_COLUMNS)}
    for claim_id in ("RPT-016", "RPT-018", "RPT-020"):
        qualifiers = rows[claim_id]["required_qualifiers"].lower()
        assert all(value in qualifiers for value in ("one recorded host", "exactly three measured repetitions", "operation boundary", "no pooled statistic"))
    assert rows["RPT-002"]["report_status"] == rows["RPT-026"]["report_status"] == "usable_with_limit"
    assert rows["RPT-002"]["evidence_class"] == rows["RPT-026"]["evidence_class"] == "proposed_reference_design"
    assert rows["RPT-024"]["report_status"] == "not_for_report"
    assert "access-authorization layer" in rows["RPT-025"]["claim_or_topic"] and "safety" in rows["RPT-025"]["required_qualifiers"]
    for row in rows.values():
        if row["evidence_class"] == "proposed_reference_design":
            assert "project-specific" in (row["claim_or_topic"] + row["required_qualifiers"] + row["notes"]).lower()


def test_asset_register_schema_paths_and_required_assets():
    rows = csv_rows(ASSETS, ASSET_COLUMNS)
    assert len(rows) == 20 and [row["asset_id"] for row in rows] == [f"AST-{index:03d}" for index in range(1, 21)]
    assert all(row["asset_type"] in {"table", "figure", "diagram", "appendix_artifact", "external_product_image"} for row in rows)
    assert all(row["readiness_status"] in {"report_ready", "ready_with_limit", "needs_export", "needs_human_permission", "missing", "appendix_only", "not_for_report"} for row in rows)
    for row in rows:
        path = Path(row["path"])
        assert not path.is_absolute()
        if row["readiness_status"] != "missing":
            assert (ROOT / path).exists()
        for source in row["source_artifacts"].split(";"):
            assert not Path(source).is_absolute() and (ROOT / source).exists()
    required = {"data/results/sp07_table_experiment_coverage.csv", "data/results/sp07_table_correctness.csv", "data/results/sp07_table_timing_summary.csv", "docs/figures/sp07_mixed_controller_average_ns.svg", "docs/figures/sp07_lookup_average_ns.svg", "docs/figures/sp07_authorization_average_ns.svg"}
    assert required <= {row["path"] for row in rows}


def test_asset_register_preserves_sources_and_records_current_export_state():
    rows = csv_rows(ASSETS, ASSET_COLUMNS)
    diagram_rows = {row["asset_id"]: row for row in rows if row["asset_type"] == "diagram"}
    assert set(diagram_rows) == {"AST-012", "AST-013", "AST-014", "AST-017", "AST-018", "AST-019", "AST-020"}
    assert all(row["readiness_status"] == "ready_with_limit" for row in diagram_rows.values())
    assert all("generated SVG/PNG" in row["required_action"] for row in diagram_rows.values())
    for asset_id in ("AST-012", "AST-013", "AST-014", "AST-017", "AST-020"):
        assert "Included as Figure" in diagram_rows[asset_id]["notes"]
    for asset_id in ("AST-018", "AST-019"):
        assert "Rendered but omitted" in diagram_rows[asset_id]["notes"]


def test_canonical_mermaid_sources_reconcile_with_architecture_and_outline():
    rows = csv_rows(ASSETS, ASSET_COLUMNS)
    validate_canonical_mermaid_rows(rows)
    outline = OUTLINE.read_text(encoding="utf-8")
    assert all(value in outline for value in ("firmware architecture", "data flow", "state machine", "watchdog/reset sequences"))
    limits = {row["path"]: row["interpretation_limit"].lower() for row in rows}
    assert all(value in limits[CANONICAL_MERMAID_PATHS[0]] for value in ("logical labels", "abstract permission signals", "physical reader", "elevator interface", "safety behavior"))
    assert all(value in limits[CANONICAL_MERMAID_PATHS[2]] for value in ("project module responsibilities", "embedded firmware", "mcu selection", "hardware execution"))
    assert all(value in limits[CANONICAL_MERMAID_PATHS[5]] for value in ("startup", "manual-reset", "watchdog-reset", "simulated software behavior", "physical fail-safe", "safety-certification"))
    assert all(value in limits[CANONICAL_MERMAID_PATHS[6]] for value in ("simulated monotonic time", "mcu-watchdog equivalence", "real-time behavior", "reliability", "physical safety"))


def test_removing_any_canonical_mermaid_registration_fails_validation():
    rows = csv_rows(ASSETS, ASSET_COLUMNS)
    for missing_path in CANONICAL_MERMAID_PATHS:
        incomplete = [row for row in rows if row["path"] != missing_path]
        with pytest.raises(AssertionError):
            validate_canonical_mermaid_rows(incomplete)


def test_historical_inputs_and_current_human_gate_are_consistent():
    for path, expected in HISTORICAL_INPUT_HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    claims = {row["report_claim_id"]: row for row in csv_rows(CLAIMS, CLAIM_COLUMNS)}
    assert claims["RPT-027"]["report_status"] == "usable_with_limit"
    assert "IEEE style is confirmed" in claims["RPT-027"]["notes"]
    submission_rows = markdown_table(SUBMISSION, "requirement_id")
    assert sum(row["blocking_stage"] == "SP-08.2" and row["status"] in {"pending_human", "not_available", "conflict"} for row in submission_rows) == 2


def test_sp07_asset_hashes_match_manifest_and_timing_captions_keep_limits():
    rows = {row["path"]: row for row in csv_rows(ASSETS, ASSET_COLUMNS)}
    manifest = json.loads((ROOT / "data/results/sp07_report_artifact_manifest.json").read_text(encoding="utf-8"))
    generated = {entry["path"]: entry["sha256"] for entry in manifest["generated_artifacts"]}
    required = ("data/results/sp07_table_experiment_coverage.csv", "data/results/sp07_table_correctness.csv", "data/results/sp07_table_timing_summary.csv", "docs/figures/sp07_mixed_controller_average_ns.svg", "docs/figures/sp07_lookup_average_ns.svg", "docs/figures/sp07_authorization_average_ns.svg")
    assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == generated[path] for path in required)
    titles = {"docs/figures/sp07_mixed_controller_average_ns.svg": "Mixed controller request-processing timing", "docs/figures/sp07_lookup_average_ns.svg": "Credential repository lookup timing", "docs/figures/sp07_authorization_average_ns.svg": "Authorization decision timing"}
    for path, title in titles.items():
        row = rows[path]; limit = row["interpretation_limit"].lower()
        assert row["caption_or_title"] == title
        assert all(value in limit for value in ("points are repetition averages", "median of three repetition averages", "whiskers are repetition-average minima and maxima", "forbid cross-family ranking"))


def test_repurposed_asset_is_a_resolved_verification_inventory():
    row = next(row for row in csv_rows(ASSETS, ASSET_COLUMNS) if row["asset_id"] == "AST-016")
    assert row["asset_type"] == "appendix_artifact"
    assert row["readiness_status"] == "appendix_only" and (ROOT / row["path"]).is_file()
    assert row["path"] == "docs/test_case_inventory.csv"


def test_bibliography_schema_source_index_coverage_and_statuses():
    rows = csv_rows(BIBLIOGRAPHY, BIB_COLUMNS)
    assert len(rows) == 25 and len({row["source_id"] for row in rows}) == 25
    assert {row["source_id"] for row in rows} == source_index_ids()
    assert all(row["metadata_status"] in {"complete", "partial", "insufficient", "not_bibliographic"} for row in rows)
    assert all(row["citation_ready"] in {"yes", "no", "conditional"} for row in rows)
    assert all(row["citation_ready"] != "yes" for row in rows if row["metadata_status"] != "complete")
    assert all(row["author_or_organization"].strip() == "" and row["year"].strip() == "" for row in rows if row["source_id"].startswith("SRC-MISSING-"))


def test_bibliography_authority_and_known_gaps_remain_distinct():
    rows = {row["source_id"]: row for row in csv_rows(BIBLIOGRAPHY, BIB_COLUMNS)}
    assert rows["SRC-STM32-001"]["source_type"] == "manufacturer_manual" and rows["SRC-STM32-001"]["citation_ready"] == "yes"
    assert rows["SRC-RFID-001"]["source_type"] == "government_technical_publication"
    assert rows["SRC-PLAN-001"]["metadata_status"] == "not_bibliographic"
    assert rows["SRC-PRODUCT-001"]["source_type"] == "product_url" and rows["SRC-PRODUCT-001"]["citation_ready"] == "no"
    for source_id in ("SRC-ARM-003", "SRC-ARM-004", "SRC-ACADEMIC-001", "SRC-MISSING-009", "SRC-MISSING-010"):
        assert rows[source_id]["citation_ready"] == "no" and rows[source_id]["missing_fields"]


def test_new_files_are_strict_utf8_relative_and_nonidentifying():
    for path in NEW_FILES:
        text = path.read_bytes().decode("utf-8", errors="strict")
        assert not any(value in text for value in ("/home/", "/mnt/", "C:\\Users\\", "BarShtainv", "hostname"))
        assert not re.search(r"(?:^|[;,])\s*/", text)


def test_no_completion_or_unsupported_attribution_claim_is_introduced():
    text = "\n".join(path.read_text(encoding="utf-8") for path in NEW_FILES).lower()
    for phrase in ("commercial card uses arm", "commercial card uses stm32", "commercial card uses wiegand", "commercial card uses a relay", "physical elevator control was validated", "supervisor approval is complete", "university approval is complete", "report is complete", "pdf is complete", "presentation is complete", "ready for release preparation"):
        assert phrase not in text
    assert "no hardware or real-time" in text and "not product evidence" in text


def test_structural_boundary_and_dependency_file_are_preserved():
    forbidden = {".tex", ".docx", ".odt", ".pdf", ".pptx", ".zip", ".tar", ".gz", ".7z"}
    created_scope = [*NEW_FILES, ROOT / "tests/inspection/test_report_preparation.py", ROOT / "audit/baselines/subproject_08_01_baseline.md"]
    assert not any(path.suffix.lower() in forbidden for path in created_scope)
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["dependencies"] == []
    assert project["project"]["optional-dependencies"]["test"] == ["pytest>=7"]
    assert project["tool"]["pytest"]["ini_options"] == {
        "testpaths": ["tests"],
        "pythonpath": ["src"],
    }
    assert not (ROOT / "report/final_report.pdf").exists() and not (ROOT / "report/presentation.pptx").exists()


def test_principal_protected_inputs_match_baseline_hashes_except_finalized_pytest_path():
    rows = markdown_table(ROOT / "audit/baselines/subproject_08_01_baseline.md", "Path")
    assert len(rows) == 28
    for row in rows:
        path = row["Path"].strip("`"); expected = row["SHA-256"].strip("`")
        assert not Path(path).is_absolute() and (ROOT / path).is_file()
        if path == "pyproject.toml":
            assert expected == "08ee535e4deae72e81a98efe380c158f97ed9ecafa6f21ee27b26455e0397e67"
            continue
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
