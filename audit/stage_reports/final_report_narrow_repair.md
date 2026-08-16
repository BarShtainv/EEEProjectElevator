# Final Report Narrow Repair Pass

## Baseline

- Date: 2026-08-16
- Repository: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Branch: `main`
- Starting commit: `3f0e0e0e412afd80c31bb61612ce7a615add8fe7`
- Starting status: clean
- Starting repository-wide result: 1,197 passed and 13 failed. The failures were confined to historical report-stage inspection invariants; no implementation or quantitative-evidence test failed.

## Authorized repairs

The report narrative was not broadly rewritten. One verification paragraph now distinguishes the frozen 976-test implementation milestone from later report, artifact, and inspection validation. Accepted experiment values, architecture content, citations, software-only scope, safety limitations, and the commercial-product evidence boundary remain unchanged.

The document builder now applies Word's `TOC Heading` style to the Table of Contents label. The TOC field remains `TOC \\o "1-2" \\h \\z \\u`; Lists of Figures and Tables retain `Heading 1`, so they remain visible in the chapter-level TOC while the TOC does not list itself.

The project title remains **Final Project Controlled Floor Elevator**. It is confirmed for report use by `report/human_input_response.md`, `report/submission_requirements.md`, and `report/drafting_authorization.md`. That authority does not constitute final supervisor approval of the completed report.

Pytest configuration now declares `pythonpath = ["src"]`, allowing the requested ordinary `python -m pytest -q` command to collect the src-layout package without external environment variables. Runtime dependencies remain empty and the existing optional test dependency remains `pytest>=7`.

## Resolution of the 13 historical failures

| Historical failing inspection | Principled current-state replacement |
|---|---|
| Drafting packet: exact protected report/register hashes | Retain exact hashes only for immutable packet inputs; verify accepted SP-07 hashes independently. |
| Drafting packet: exports and final outputs forbidden | Verify all canonical Mermaid source/SVG/PNG triplets and grading DOCX/PDF exist; continue forbidding release and presentation outputs. |
| Draft report: exact old section title and cover metadata | Verify the current 15-section report, authorized metadata, unresolved-date boundary, references, and claim limitations. |
| Draft report: traceability used old section title | Verify the current section name and complete claim/source/citation/asset resolution. |
| Draft report: only three SVGs allowed and Mermaid export deferred | Preserve accepted SVG hashes while verifying the eight intended PNG links and all seven rendered diagram pairs. |
| Draft report: DOCX/PDF forbidden | Require valid grading DOCX/PDF, an updateable chapter-level TOC field, `TOC Heading`, and continued absence of release outputs. |
| Human-review packet: report and traceability fixed to old bytes | Verify current report/traceability structure and the human-supplied title authority instead of obsolete hashes. |
| Human-review packet: traceability used old section title | Verify current 15-section traceability and complete path/key/asset/claim resolution. |
| Human-review packet: Mermaid exports forbidden | Preserve accepted SP-07 hashes and require current SVG/PNG exports. |
| Human-review packet: final documents forbidden | Preserve privacy and authorization checks while requiring the grading DOCX/PDF and continuing to forbid release/presentation output. |
| Report preparation: original asset rows fixed to pre-export bytes | Verify canonical sources, statuses, actions, selected figures, and deliberately omitted redundant diagrams semantically. |
| Report preparation: every diagram required `needs_export` | Require `ready_with_limit`, interpretation limits, source resolution, and corresponding SVG/PNG files. |
| Report preparation: current registers fixed to preparation-stage hashes | Preserve immutable preparation inputs while verifying the current IEEE-ready claim status and unresolved human gate. |

The archived preparation baseline retains the former `pyproject.toml` hash as historical evidence. The live test validates current configuration semantics rather than rewriting that historical record.

## Document outputs

- `report/final_report_grading_draft.docx`: 874,283 bytes; SHA-256 `f2b4deecafe60647797d7aa162f43e47f574e3b03b49c8fb9553038089f83631`
- `report/final_report_grading_draft.pdf`: 1,149,890 bytes; 26 A4 pages; SHA-256 `2798fcb5923ddbaf6064e5239f3f6ac53fb6c1a7ea325d04a89496ee2393bfb5`

## Validation

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/unit tests/integration tests/end_to_end tests/experiment tests/analysis
```

Result: 1,118 passed in 23.83 seconds.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

Final result: 1,210 passed in 25.97 seconds.

```sh
python -m pytest -q
```

Final result: 1,210 passed in 26.31 seconds.

Focused current-state report inspections passed 67 of 67. DOCX ZIP integrity, ten populated tables, eight embedded figures, the TOC field/style, PDF A4 geometry, text extraction on all pages, references [1]–[8], title authority, accepted-result hashes, and reader-facing placeholder scans were also checked.

## Visual inspection

All 26 regenerated PDF pages were inspected as contact sheets, with targeted full-page review of the cover, TOC, lists, introduction, architecture pages, state/watchdog diagrams, results graphs, dense tables, references, appendices, and final page. The TOC does not list itself. Lists of Figures and Tables remain present. No clipping, overlap, missing figure, unresolved field text, raw Markdown, excessive blank page, or broken table was observed.

## Readiness

The narrow technical repair is complete. Final submission date, final supervisor approval, signature requirements, and submission/defense logistics remain authoritative human decisions.

READY FOR SUPERVISOR / GRADING REVIEW
