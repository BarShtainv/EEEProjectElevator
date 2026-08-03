# SP-07.4R Validation — Final Review Provenance and Publication-Cleanup Repair

## Accepted state and baseline

- Repository `BarShtainv/EEEProjectElevator`, clean `main`, accepted starting commit `95ea1b34e44c4b387f50be52829ca8b041496ce2`.
- External environment: Python 3.13.13, pip 26.2, pytest 9.1.1; no install or network access.
- Accepted output hashes before repair: anomaly register `0f997c8e10f53fa104718acb2823b25e134309f0dd7ad201bc87be447392f7c9`, review summary `7d48384b258c1cd033efe84aa6aba1fa65cd1f23621ed382fd1df4f0c38c9b92`, final ledger `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745`, source notes `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6`.
- Generated caches were removed before the prescribed baseline. Baseline: 1132/1132 passed in 28.05s with zero failures, skips, and xfails.
- Existing SP-07.4 stage and validation reports remain unchanged historical execution records.

## Provenance corrections

The SP-07.4 baseline incorrectly labeled two canonical inputs with nonexistent `_repair_validation.md` names. Only the labels were corrected: `audit/validation/subproject_07_01_repair.md` retains SHA-256 `a4b14d0d7eed99c8049b2b2cf6b6ecfb2af9a1396db8b5016000f194c7dc6da6`, and `audit/validation/subproject_07_03_repair.md` retains SHA-256 `e0d00c7b948ffbb3836836807437ee610dd8f3f7d966baf4ec9723814c6b0b9b`. A new Markdown-table regression proves exact ordered equality with all 29 `SOURCES`/`EXPECTED_HASHES` entries, existence, and absence of both obsolete labels.

All 14 anomalies previously received one generic evidence pair. Each definition now carries its own category, observation, evidence, severity, disposition, implication, and follow-up. A semantic validator enforces exact IDs/order/status and observation-specific canonical evidence paths. The historical observation now says that the accepted 976-test SP-06 snapshot is historical and differs from later accepted Subproject-7 baselines; it cites the integrated summary and SP-07.3R validation without embedding a current test count. The 10,000-credential lookup spread is deterministically rendered as exactly `122.189 ns`, without changing source timing values.

## Publication cleanup state machine

The former `finally` cleanup allowed raw `OSError` to replace publication/rollback results. The repaired publisher tracks staged and backup temporaries, attempts bounded cleanup in output order, excludes failed-restoration recovery backups, and reports only artifact keys and temporary basenames. Successful publication plus cleanup failure preserves valid new outputs and raises a handled completion error. Failed publication plus complete rollback reports preserved outputs and any cleanup failure. Incomplete rollback retains recovery backups, preserves restoration details, and separately appends ordinary cleanup failures.

Regression coverage proves: successful publication with failed backup cleanup returns one CLI `error:` line and keeps new bytes; failed publication with complete rollback and failed staged cleanup restores old bytes; combined incomplete rollback and cleanup failure attempts every restoration, retains recovery material, and never deletes it prematurely. Each test restores destinations and removes injected temporary files before completion.

## Generation and independent review

The exact official four-output command ran twice; both runs exited 0 with 39 ledger rows, 14 anomalies, 12 timing rows, three figures, and zero blockers. Both generations produced identical hashes:

| Output | Before | After |
|---|---|---|
| `data/results/sp07_anomaly_register.csv` | `0f997c8e10f53fa104718acb2823b25e134309f0dd7ad201bc87be447392f7c9` | `cafaddaef88faeeedecca6d312a2c71ebdc0cae339ca1b66143e5de2f4ca5d88` |
| `data/results/sp07_independent_review_summary.json` | `7d48384b258c1cd033efe84aa6aba1fa65cd1f23621ed382fd1df4f0c38c9b92` | `52a2f9ca0b13945e2cdbf7327c7d81d53512beedfe2c998a6be0b4c7d2c4ae1a` |
| `audit/validation/subproject_07_final_validation_ledger.csv` | `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745` | byte-identical: `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745` |
| `docs/sp07_results_discussion_source_notes.md` | `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6` | byte-identical: `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6` |

The separate standard-library validator imported no review, analysis, benchmark, or simulator code and printed `INDEPENDENT_REPAIR_VALIDATION=PASS sources=29 anomalies=14 ledger=39 timing=12 figures=3 blocking=0`. It checked corrected baseline pairs, exact anomaly mappings and wording, source existence/hashes, ledger/notes preservation, reconciliation counts, and prohibited-claim boundaries.

## Validation results

- Initial repaired focused suite: 31/31 passed in 2.18s; zero failures, skips, and xfails.
- First repaired full suite: 1137/1137 passed in 25.02s; zero failures, skips, and xfails.
- Final focused suite: 31/31 passed in 2.15s; zero failures, skips, and xfails.
- Final full suite: 1137/1137 passed in 25.46s; zero failures, skips, and xfails.
- Compilation and imports: `compileall` and both prescribed package/controller imports exited 0.
- Git scope and cleanup: exactly seven authorized paths; protected tracked paths, including the byte-identical ledger and notes, are unchanged; caches, bytecode, test temporaries, comparison files, and recovery backups are absent.

Neither benchmark was executed. No accepted measurement, experiment configuration, correctness/timing/coverage table, SVG, manifest, catalog, integrated summary, simulator, requirements, inventory, traceability, verification record, report, presentation, release, or prior stage/validation report changed. Subproject 8 was not started. No commit or push occurred.

`READY FOR HUMAN REVIEW`
