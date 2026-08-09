# SP-08.2D Report-Draft Baseline

## Starting state

- Stage: SP-08.2D, evidence-led final engineering report drafting.
- Repository: `BarShtainv/EEEProjectElevator`.
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`.
- Branch: `main`.
- Starting commit: `87004b22f49fd4c0c481f8a3128b663bb8f7fc83`.
- Initial worktree: clean under `git status --short --untracked-files=all`.
- Python: `Python 3.13.13`.
- pip: `pip 26.2` from the authorized virtual environment.
- pytest: `pytest 9.1.1`.
- Tracked Python/pytest cache artifacts: zero.

## Baseline execution

The cache-free command `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -p no:cacheprovider` collected 1176 tests and passed all 1176 in 25.61 seconds (25.83 seconds measured wall time), with zero failures, skips, or xfails. The additional test relative to the recorded 1175 count is the accepted SP-08.2IRR2 hygiene inspection at the starting commit.

## Drafting gates and protected hashes

The six gate groups in `report/drafting_gate_resolution.csv` were all `resolved`. Supervisor authorization was affirmative, and `report/drafting_authorization.md` ended exactly with `REPORT DRAFTING AUTHORIZED`. The frozen historical snapshot remained intact.

| Protected input | SHA-256 |
|---|---|
| `report/drafting_authorization.md` | `9e068de045547c64cc57c238f44fabd48c67b6d098a7b7459dffa0d9f1f7b1fa` |
| `report/authoritative_inputs/supervisor_drafting_authorization.md` | `c88e229ac3c02c28bbc288342cc9409e1be18c79dd1cbc98d9b08325d9f80b53` |
| `report/report_outline.md` | `cece1ff5aed996350c4a2f2ba45dff59b7b2d1020b61dd6c108080476b5e05d0` |
| `report/report_claim_source_matrix.csv` | `ca2cc6a0c0cb9b8158e62cae0dcb45b0dc1c9f8373cc5fac461f01aaeec9b5be` |
| `report/report_asset_register.csv` | `72f8b90a37bc47df3cc235e0807a847e8e3e68f9ec23310fb0c4b29aea4a4285` |
| `report/bibliography_readiness.csv` | `53f01e1dd8010c7df713dcc029bc6ba1d6774902c6edaefd524adf87d7eeeffc` |
| `report/references.bib` | `65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307` |
| `report/drafting_gate_snapshot.csv` | `947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863` |

## SP-07 quantitative sources

| Accepted artifact | SHA-256 |
|---|---|
| `data/results/sp07_table_experiment_coverage.csv` | `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f` |
| `data/results/sp07_table_correctness.csv` | `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224` |
| `data/results/sp07_table_timing_summary.csv` | `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811` |
| `data/results/sp07_anomaly_register.csv` | `cafaddaef88faeeedecca6d312a2c71ebdc0cae339ca1b66143e5de2f4ca5d88` |
| `data/results/sp07_independent_review_summary.json` | `52a2f9ca0b13945e2cdbf7327c7d81d53512beedfe2c998a6be0b4c7d2c4ae1a` |
| `data/results/sp07_quantitative_summary_integrated.json` | `95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c` |
| `data/results/sp07_report_artifact_manifest.json` | `69235fab571b97e00b54f4a8dd202e8331dadbf381dcd8caa0c2250f4ed44851` |

## Scope freeze

Authorized creation paths are `report/final_report.md`, `report/report_draft_traceability.csv`, `tests/inspection/test_final_report_draft.py`, this baseline, the SP-08.2D stage report, and the SP-08.2D validation report. The only authorized tracked update is a narrow appended section in `audit/file_change_ledger.md`.

All report gate inputs, evidence registers, requirements/design/test/reproducibility documents, production source, existing tests, experiment configurations, accepted SP-07 results/tables/figures/audits, literature, dependency metadata, `.gitignore`, `README.md`, and the project plan are protected. No DOCX, PDF, presentation, product image, Mermaid export, archive, release, commit, push, or history rewrite is authorized.
