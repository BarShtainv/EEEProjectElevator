# SP-01 File Change Ledger

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baseline.md` | new | Created baseline record. | Preserve initial repository and evidence state. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/file_change_ledger.md` | new | Created this ledger. | Audit all allowed changes. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/stage_reports/subproject_01.md` | new | Created stage report. | Durable SP-01 completion record. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/validation/subproject_01_validation.md` | new | Created validation record. | Record required checks and results. | No pre-existing file overwritten. | Required-file, CSV, Git, and content checks. |
| `evidence/product_evidence.md` | new | Preserved URLs and documented absence of local listing/product evidence. | Establish verified-evidence boundary. | No product files copied, altered, or replaced. | UTF-8/readability and assertion review. |
| `evidence/assumptions_and_unknowns.md` | new | Created inference, future-design, unknown, and missing-input register. | Prevent unsupported assumptions. | No pre-existing file overwritten. | UTF-8/readability and assertion review. |
| `evidence/claim_evidence_matrix.csv` | new | Created initial claim-evidence matrix. | Make claim status auditable. | No pre-existing file overwritten. | Parsed with Python `csv`; header and row widths checked. |
| `evidence/source_index.md` | new | Inventoried supplied URLs and available source documents. | Preserve source provenance without literature synthesis. | Existing sources only referenced, not modified. | UTF-8/readability check. |

No product image or listing snapshot was copied because none was available in the baseline workspace. No path outside the allowed SP-01 paths was modified.

## SP-02 additions

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_02_baseline.md` | new | Recorded current, task, and reference baselines. | Preserve SP-02 starting-state comparison. | No prior file overwritten. | Git history/status and SP-01 prerequisite review. |
| `audit/file_change_ledger.md` | pre-existing | Added SP-02 ledger section. | Maintain canonical change audit. | Prior SP-01 content retained. | UTF-8/readability check. |
| `audit/stage_reports/subproject_02.md` | new | Created SP-02 report. | Record bounded-stage outcome and source gaps. | No prior file overwritten. | Required-file and scope checks. |
| `audit/validation/subproject_02_validation.md` | new | Created SP-02 validation record. | Preserve validation results. | No prior file overwritten. | CSV, source-ID, BibTeX, Git, and wording checks. |
| `evidence/source_index.md` | pre-existing | Expanded source metadata, scope, inspected locations, limitations, and availability. | Make source use auditable. | Existing IDs retained; original sources not changed. | Source-ID/path and UTF-8 checks. |
| `evidence/claim_evidence_matrix.csv` | pre-existing | Added traceable external, proposed, and unresolved claims. | Expand claim-evidence architecture. | Existing header and claims retained. | CSV/schema/ID/source checks. |
| `evidence/literature_notes.md` | new | Created topic-organized literature notes. | Preserve concise scoped paraphrases and source gaps. | No source text copied or source file changed. | Source-ID and manual scope review. |
| `evidence/unresolved_sources.md` | new | Created missing-source register. | Prevent unsupported technical claims. | No product unknown reclassified. | Coverage and blocking-effect review. |
| `evidence/assumptions_and_unknowns.md` | pre-existing | Added PRD-002 and PRD-003. | Label future simulator/reference choices. | Existing SP-01 entries retained. | Cross-reference and scope review. |
| `docs/methodology.md` | new | Created evidence-led research methodology. | Document citation, source, and limitation discipline. | No requirements or architecture design added. | Manual scope review. |
| `docs/literature_review_outline.md` | new | Created controlled literature outline. | Map sections, sources, and gaps. | No final prose or product claims added. | Source-ID review. |
| `docs/decision_log.md` | new | Created decision log. | Preserve evidence-scope decisions. | Product evidence remains intact. | Decision/cross-reference review. |
| `report/references.bib` | new | Created preliminary verified-metadata bibliography. | Support citation traceability. | No original source changed; uncertain metadata omitted. | Structural and unique-key checks. |

## SP-02R narrow completion

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `.gitignore` | new | Added `prompt*.txt`. | Keep local task prompts out of permanent engineering deliverables. | No prior ignore rules existed. | Prompt tracking/local-file checks. |
| `prompt.txt`, `prompt2.txt` | tracked local inputs | Removed from Git index with `git rm --cached`; local files retained. | Implement SP-02R prompt hygiene. | Contents retained locally and ignored. | `git ls-files` and `test -f`. |
| `audit/baselines/subproject_02_repair_baseline.md` | new | Recorded clean `fdad611` baseline, readiness, prompts, and defects. | Audit the narrow repair starting state. | No prior baseline overwritten. | Git and instruction-file inspection. |
| `audit/stage_reports/subproject_01.md` | pre-existing | Replaced custom readiness sentence with `READY FOR HUMAN REVIEW`. | Clarify that missing product captures limit claims but do not block literature/model planning. | Existing missing-evidence explanation retained. | Manual wording review. |
| `evidence/product_evidence.md` | pre-existing | Corrected the malformed original AliExpress URL. | Preserve the exact owner-supplied URL. | Canonical URL and all product limitations retained. | Exact/malformed URL searches. |
| `evidence/source_index.md` | pre-existing | Corrected URL; added four core sources and updated gap coverage. | Establish minimum credible literature coverage. | Existing IDs and source-scope qualifications retained. | Source metadata, IDs, paths, URLs, and hashes checked. |
| `literature/nist_sp_800_98_rfid.pdf` | new | Downloaded official NIST SP 800-98 PDF. | Preserve authoritative RFID source locally. | No existing PDF replaced. | PDF type, metadata, SHA-256, and path checks. |
| `literature/nist_sp_800_53_rev5_1.pdf` | new | Downloaded official NIST SP 800-53 Rev. 5 Release 5.1 derivative PDF. | Preserve authoritative access-authorization source locally. | No existing PDF replaced. | PDF type, metadata, SHA-256, and path checks. |
| `evidence/literature_notes.md` | pre-existing | Replaced core source gaps with concise RFID, Wiegand, authorization, and testing notes; scoped elevator integration. | Meet minimum note coverage without broad rewriting. | Product claims remain prohibited and unknowns retained. | Note/source-ID and manual qualification review. |
| `evidence/unresolved_sources.md` | pre-existing | Marked minimum core gaps resolved and remaining gaps non-blocking where authorized. | Permit SP-03 while retaining limitations. | No gap deleted. | Coverage/readiness review. |
| `evidence/assumptions_and_unknowns.md` | pre-existing | Aligned proposed Wiegand-26 status with the newly available general source while retaining the exact-field-allocation gate. | Remove a stale open-source statement without implying commercial support. | Existing product unknowns retained. | Cross-reference and scope review. |
| `evidence/claim_evidence_matrix.csv` | pre-existing | Updated claims, superseded duplicate CLM-014, and added CLM-021–CLM-026. | Trace future input, authorization, mask, test, and scope decisions. | Existing IDs retained; no wholesale renumbering. | Python CSV and reference validation. |
| `docs/literature_review_outline.md` | pre-existing | Mapped newly covered topics and controlled remaining gates. | Align outline with narrow completion. | Remains an outline, not final prose. | Source-ID review. |
| `docs/decision_log.md` | pre-existing | Added abstract elevator-output boundary and minimum-source-set decisions. | Make physical integration non-blocking for software work. | Safety boundary strengthened. | Decision/scope review. |
| `docs/methodology.md` | pre-existing | Added deadline-oriented literature sufficiency standard. | Explain why minimum authoritative coverage permits progress. | Evidence hierarchy unchanged. | Manual wording review. |
| `report/references.bib` | pre-existing | Added four verified core-source entries. | Support traceable citations. | Uncertain metadata omitted. | Unique-key and brace checks. |
| `audit/stage_reports/subproject_02_repair.md` | new | Recorded repair outcome and non-blocking gates. | Durable SP-02R report. | Historical SP-02 report retained. | Required-content review. |
| `audit/validation/subproject_02_repair_validation.md` | new | Recorded narrow validation. | Preserve audit evidence for readiness. | No earlier validation overwritten. | Required SP-02R checks. |
