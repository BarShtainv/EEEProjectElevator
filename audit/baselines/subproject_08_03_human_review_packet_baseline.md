# SP-08.3H Human-Review Packet Baseline

## Starting state

- Stage: SP-08.3H, final report human technical review packet.
- Repository: `BarShtainv/EEEProjectElevator`.
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`.
- Branch: `main`.
- Starting commit: `e47e8ce537322a4ca20a921a11f2d8dd5c669bbc`.
- Initial worktree: clean under `git status --short --untracked-files=all`.
- Python: `Python 3.13.13`.
- pip: `pip 26.2` from the authorized virtual environment.
- pytest: `pytest 9.1.1`.
- Tracked Python/pytest cache artifacts: zero.

## Baseline execution

The cache-free command `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -p no:cacheprovider` collected 1,198 tests and passed all 1,198 in 26.35 seconds (26.57 seconds measured wall time), with zero failures, skips, or xfails.

## Protected report and gate hashes

| Protected input | SHA-256 |
|---|---|
| `report/final_report.md` | `db43c6f7f218d8d37f339d0d93420e2b819e022883ddc5cb357f07b9064ab170` |
| `report/report_draft_traceability.csv` | `957cac4b505154fc745d8a9b09dd96bb7fde6de4b26feb9f1b8f9f6e39489902` |
| `report/drafting_authorization.md` | `9e068de045547c64cc57c238f44fabd48c67b6d098a7b7459dffa0d9f1f7b1fa` |
| `report/authoritative_inputs/supervisor_drafting_authorization.md` | `c88e229ac3c02c28bbc288342cc9409e1be18c79dd1cbc98d9b08325d9f80b53` |
| `report/report_claim_source_matrix.csv` | `ca2cc6a0c0cb9b8158e62cae0dcb45b0dc1c9f8373cc5fac461f01aaeec9b5be` |
| `report/bibliography_readiness.csv` | `53f01e1dd8010c7df713dcc029bc6ba1d6774902c6edaefd524adf87d7eeeffc` |
| `report/references.bib` | `65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307` |
| `report/report_asset_register.csv` | `72f8b90a37bc47df3cc235e0807a847e8e3e68f9ec23310fb0c4b29aea4a4285` |

The accepted report contained exactly 15 main sections and 6,707 words. Its traceability file had the exact eight-column schema, 15 rows in report order, resolving sources/citations/assets and mapping all 27 RPT claim IDs. Supervisor drafting authorization remained affirmative, all six gate groups were resolved, and `report/drafting_authorization.md` ended exactly with `REPORT DRAFTING AUTHORIZED`.

## Accepted SP-07 result and figure hashes

| Artifact | SHA-256 |
|---|---|
| `data/results/sp07_table_experiment_coverage.csv` | `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f` |
| `data/results/sp07_table_correctness.csv` | `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224` |
| `data/results/sp07_table_timing_summary.csv` | `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811` |
| `docs/figures/sp07_mixed_controller_average_ns.svg` | `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930` |
| `docs/figures/sp07_lookup_average_ns.svg` | `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096` |
| `docs/figures/sp07_authorization_average_ns.svg` | `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9` |

## Authorized and protected scope

Authorized creation paths are `report/human_review_request.md`, `tests/inspection/test_report_human_review_packet.py`, this baseline, `audit/stage_reports/subproject_08_03_human_review_packet.md`, and `audit/validation/subproject_08_03_human_review_packet_validation.md`. The only authorized tracked update is the narrow SP-08.3H append to `audit/file_change_ledger.md`.

The report, traceability, report planning registers, drafting gates/authorizations, evidence, requirements/design, production source, existing tests, experiments, accepted SP-07 artifacts, prior audits, literature, README, project plan, dependencies, and `.gitignore` are protected. The human-supplied response path `report/authoritative_inputs/final_report_human_review.md` must not be created in this stage. No report revision, DOCX, PDF, PPTX, Mermaid rendering, product image, archive, release, history rewrite, commit, or push is authorized.
