# Final Report Grading-Readiness and Document-Production Pass

## Baseline

- Repository: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Branch: `main`
- Starting commit: `2272470b8f2f03b53ef51f1e827554d30a405daf`
- Starting status: untracked `report/final_report_draft.docx` and `report/~$nal_report_draft.docx`; both were treated as user-owned. The lock file later disappeared outside this work, and the pre-existing draft was not modified.
- Initial active Python: 3.13.13. The declared test dependency was absent, so pytest 9.1.1 and document-production libraries were installed in the active environment without changing project dependencies.
- Initial repository-wide test result after dependency setup: 1,210 collected; 1,208 passed and two prior-stage inspection tests failed because the pre-existing DOCX files violated their historical no-DOCX rule. No implementation, integration, experiment, or analysis test failed.

## Academic revision

`report/final_report.md` was revised into a reader-facing B.Sc. engineering report. Internal stage markers, draft-status narration, and seven figure placeholders were removed. The abstract and introduction now identify the implemented engineering contribution directly. Requirements, architecture, implementation, verification, results, discussion, limitations, conclusions, future work, references, and appendices were tightened without changing accepted numerical results or the commercial-product evidence boundary.

The report contains eight numbered figures, ten numbered tables, eight IEEE-style references, and explicit separation between the motivating commercial listing and the project-defined software reference model. All references [1]–[8] are cited and all eight bibliography entries are present.

## Figures

All seven Mermaid sources were rendered as SVG and high-resolution PNG files. Five were selected for the report:

1. System context and engineering boundary.
2. Conceptual top-level architecture and implemented software boundary.
3. Authorization data flow.
4. Controller state machine.
5. Simulated watchdog and recovery sequence.

The firmware-responsibility and reset-sequence diagrams were rendered but omitted as redundant. The three accepted timing graphs were preserved numerically, converted to high-resolution PNG for reliable DOCX/PDF rendering, and included as Figures 6–8.

## Document production

Primary commands:

```sh
for f in docs/figures/*.mmd; do npx -y @mermaid-js/mermaid-cli -i "$f" -o "${f%.mmd}.svg" -b white -t neutral; done
for f in docs/figures/*.mmd; do npx -y @mermaid-js/mermaid-cli -i "$f" -o "${f%.mmd}.png" -b white -t neutral -s 2; done
python scripts/build_grading_report.py
libreoffice -env:UserInstallation="file://<temporary-profile>" --headless --accept='socket,host=localhost,port=<port>;urp;StarOffice.ServiceManager' --norestore --nodefault --nofirststartwizard
/usr/bin/python3 scripts/update_docx_indexes.py report/final_report_grading_draft.docx --port <port> --pdf-output <temporary-pdf> --no-store
```

The build script creates an A4 Word document with a cover page, updateable TOC field, lists of figures and tables, heading hierarchy, headers, page numbers, styled captions, professional margins, and controlled figure sizing. LibreOffice updates the TOC in memory and exports the validation PDF without round-tripping the DOCX, preserving Word-table compatibility.

- DOCX: `report/final_report_grading_draft.docx`, 854 KiB, SHA-256 `69c5f36a4444db482de0b6d4fe75b8372ff51cfca807156201de9019105918ad`
- PDF: `report/final_report_grading_draft.pdf`, 26 A4 pages, SHA-256 `6f9fd518337f8304b484add9bf8b53c1c3255922367a0ef5e368e2b134dda944`

## Visual inspection and repairs

All 26 PDF pages were inspected through full contact sheets. The cover, abstract, TOC, lists, each architecture figure, every results graph, all ten tables, references, appendices, and final page received targeted checks; dense figure/table pages were also inspected at full-page resolution.

Repairs made after rendered inspection:

- separated cover metadata into centered paragraphs;
- replaced Mermaid SVG embeddings with high-resolution PNGs after LibreOffice exposed SVG text-box defects;
- corrected a Mermaid state-label parsing issue;
- changed several diagrams to document-friendly aspect ratios;
- reduced TOC depth and refreshed page numbers;
- compacted wide timing and experiment tables;
- preserved automatic table row sizing for LibreOffice/Word compatibility;
- resized the watchdog figure so its caption remains on the same page;
- shortened appendix artifact narration to eliminate a nearly blank final page.

No clipping, overlap, missing image, placeholder, raw Markdown, empty table, or unresolved TOC text remains in the validation PDF. DOCX structure checks confirmed ten populated tables and eight embedded figures; ZIP integrity passed.

## Technical validation

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -p no:cacheprovider tests/unit tests/integration tests/end_to_end tests/experiment tests/analysis
```

Result: 1,118 passed in 23.83 seconds.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

Result: 1,210 collected; 1,197 passed and 13 historical report-stage inspection tests failed. Every failure enforces the superseded draft freeze: exact old report/register text or hashes, deferred Mermaid exports, or absence of DOCX/PDF. These assertions directly conflict with this authorized grading-readiness task. No controller, unit, integration, end-to-end, experiment, analysis, or general reproducibility test failed. The historical tests were not weakened or rewritten.

Compilation of `src`, `tests`, `scripts`, and `analysis`, both required imports, document-builder compilation, DOCX ZIP integrity, table/figure counts, PDF metadata, and all-page text extraction also passed.

## Remaining authoritative human inputs

- Final submission date/deadline.
- Submission portal or delivery method.
- Whether a student identification field is formally required; any value must be handled privately.
- Signature/approval-page requirement and final sign-off workflow.
- Supervisor decision on whether a physical component is required beyond the accepted software-only project.
- Final supervisor technical approval of the report and generated document.
- Presentation format and timing, if defense logistics are to be finalized.

## Readiness

The grading draft is technically and visually ready for human examination. It does not claim supervisor approval, university approval, release approval, or submission.

READY FOR SUPERVISOR / GRADING REVIEW
