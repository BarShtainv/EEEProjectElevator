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
