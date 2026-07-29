# SP-03 Baseline

## Stage identity

- Stage: `SP-03 — Requirements, scope freeze, and research methodology`
- Recorded: `2026-07-29T13:55:43+03:00`
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Current and accepted baseline commit: `88a646026c0bf468e28102bf80c00ef4cb3ea57f`
- Commit subject: `step2Repair`
- Initial `git status --short`: clean; no output

## Recent commits

```text
88a6460 (HEAD -> main, origin/main, origin/HEAD) step2Repair
4cba9bb step2Repair
fdad611 Step 2
3263466 Step1
9e46275 GeneralSources
d1643de Initial commit
```

The accepted commit contains the SP-02R baseline, repair report, validation record, four-source completion, prompt-file cleanup, corrected product URL, and non-blocking-gate decision. `git merge-base --is-ancestor` confirmed that the accepted commit is the current `HEAD`.

## Instructions and repository inventory

`README.md` is empty. No `AGENTS.md`, `WORKFLOW.md`, or `CONTRIBUTING.md` file was found in or above the repository. The applicable project instructions are:

- the SP-03 owner instruction supplied for this stage;
- `final_engineering_project_plan.md`;
- `general_purpose_evidence_gated_workflow_handbook_updated.md`.

Existing canonical files were inventoried under:

- `docs/`: decision log, literature-review outline, methodology;
- `audit/`: SP-01, SP-02, and SP-02R baselines, reports, validation, and the file-change ledger;
- `evidence/`: product evidence, assumptions/unknowns, claim matrix, source index, literature notes, and unresolved-source register.

## Prerequisite and readiness review

- SP-01: `READY FOR HUMAN REVIEW`; product images and listing captures remain unavailable.
- Original SP-02: blocked because core literature sources were absent.
- SP-02R: `READY FOR NEXT STAGE WITH NON-BLOCKING GATES`.
- SP-02R validation: passed.

The project-owner instruction for SP-03 authorizes the abstract software-only 16-floor scope in DEC-008. This is project-owner authorization, not supervisor approval. Supervisor confirmation remains required before final academic submission or expansion toward physical integration.

## SP-02R non-blocking gates carried forward

- Product images and listing captures are unavailable.
- Commercial processor, firmware, RFID frequency, credential protocol, Wiegand support, electrical outputs, and physical elevator interface remain unknown.
- Detailed RFID protocol coverage and exact commercial behavior are unresolved.
- Physical elevator integration is outside software scope and remains blocking for any physical wiring, installation, certification, or interface claim.
- Formal fail-safe/fail-secure terminology and university formatting requirements remain unresolved.

None of these gaps prevents an explicitly proposed, deterministic, software-only requirements model.

## Protected files

The following are protected from SP-03 edits:

- all PDFs under `literature/` and `referenceProject/`;
- `evidence/product_evidence.md` and its preserved URLs;
- `evidence/source_index.md`;
- `evidence/literature_notes.md`;
- `evidence/unresolved_sources.md`;
- `report/references.bib`;
- `final_engineering_project_plan.md`;
- `general_purpose_evidence_gated_workflow_handbook_updated.md`;
- prior audit reports and validations except the append-only canonical file-change ledger.

Baseline SHA-256 values for protected text files:

```text
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
```

Original and SP-02R source-PDF hashes are recorded in `audit/validation/subproject_02_repair_validation.md` and will be rechecked by status/path protection during SP-03 validation.

## Authorized SP-03 boundary

SP-03 may create requirements, traceability, a Mermaid context diagram, and stage audit records, and may narrowly update methodology, decisions, assumptions, the claim matrix, and the file-change ledger. It must not implement code, tests, experiments, detailed architecture, register maps, physical electronics, or commercial-product behavior.
