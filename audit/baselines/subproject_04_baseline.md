# SP-04 Baseline

## Stage identity

- Stage: `SP-04 — Conceptual hardware and firmware architecture`
- Recorded: `2026-08-03T11:18:37+03:00`
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Current and accepted starting commit: `94b051cfeebed08db8aec9b590fb99d60c87aee3`
- Commit subject: `step3`
- Initial `git status --short`: clean; no output

## Recent history

```text
94b051c (HEAD -> main, origin/main, origin/HEAD) step3
88a6460 step2Repair
4cba9bb step2Repair
fdad611 Step 2
3263466 Step1
9e46275 GeneralSources
d1643de Initial commit
```

The accepted SP-03 commit is the current `HEAD`. `git merge-base --is-ancestor` confirmed it is present, and its commit diff contains the frozen requirements, traceability matrix, context diagram, decisions, methodology, and SP-03 audit records. No later or conflicting work is present.

## Applicable instructions

`README.md` is empty. No `AGENTS.md`, `WORKFLOW.md`, or `CONTRIBUTING.md` was found in the repository. Applicable instructions are:

- the SP-04 project-owner instruction supplied for this stage;
- `final_engineering_project_plan.md`;
- `general_purpose_evidence_gated_workflow_handbook_updated.md`.

The project owner authorizes conceptual-design work using the SP-03 frozen requirements and defaults. This is not supervisor approval. Supervisor confirmation remains pending before final academic submission or physical-scope expansion.

## Required architecture outputs

SP-04 must create:

- `docs/architecture.md`;
- `docs/register_model.md`;
- `docs/architecture_to_requirements.csv`;
- six focused Mermaid diagrams for top-level architecture, firmware responsibilities, controller states, data flow, reset, and watchdog behavior;
- the SP-04 baseline, stage report, and validation record.

It may update only the decision log, a short methodology architecture-method note if needed, and the canonical file-change ledger.

## Frozen SP-03 decisions

- Exact working title is project-owner approved; supervisor approval is pending.
- The implemented system is a deterministic Python software simulator of an access-authorization layer.
- `LF` and `HF` are logical reader-source labels only.
- `PROJECT_WIEGAND_26` is the proposed input profile.
- Floors are 1–16; floor 1 maps to bit 0 and floor 16 to bit 15.
- The credential key is `(facility_code, credential_number)` and duplicates are rejected.
- At most one abstract output is active.
- A request while active is rejected as `controller_busy` without changing expiry.
- Output duration defaults to 3000 ms with a 100–30000 ms valid range.
- Watchdog timeout defaults to 2000 ms and reset returns all outputs inactive.
- Events use the frozen minimum fields.
- Required experiment sizes are 10, 100, 1,000, and 10,000 credentials.
- Required work precedes optional work.

The SP-03 requirement set contains 60 required and six optional requirements. SP-04 must map every required requirement without modifying it.

## Pending human-review items

- conceptual hardware boundary;
- state enumeration;
- busy-before-validation precedence;
- reset preservation rules;
- explicit-null event schema and enumerations;
- logical memory/register organization;
- initialization failure policy;
- event-log append failure policy;
- watchdog service checkpoints;
- architecture-to-requirements coverage;
- all previously pending SP-03 defaults and supervisor approval.

## Protected material

Protected from SP-04 modification:

- `docs/requirements.md`;
- `docs/requirements_to_test_traceability.csv`;
- `docs/figures/system_context.mmd`;
- all evidence files;
- all source PDFs and product material;
- `report/references.bib`;
- the project plan and workflow handbook;
- all prior audit reports and validations;
- Git history.

Baseline SHA-256 values:

```text
9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d  docs/requirements.md
059388cae0320965a3ee38ac7d6ac488e968d51aceba1eb3c694802490e8b294  docs/requirements_to_test_traceability.csv
2f15218127660b422c578c6da1e5ca0c6cb72d336edb0f613fad49f6fe7a47e0  docs/figures/system_context.mmd
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
```

Source-PDF hashes remain protected by the prior validation records and Git path checks.

## Scope boundary

SP-04 documents a proposed reference architecture. Conceptual power, reader, isolation, driver, and elevator-interface blocks are not implemented by the simulator. No voltage, rating, component, connector, relay, PCB, physical memory capacity, physical wiring, processor selection, or commercial equivalence may be introduced. No code, tests, detailed test plan, experiment data, or final report prose is authorized.
