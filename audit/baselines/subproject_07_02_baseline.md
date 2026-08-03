# SP-07.2 Isolated-Operation Experiment Baseline

## Accepted starting state

- Repository: `BarShtainv/EEEProjectElevator`; branch `main`.
- Accepted commit: `415fc24cfbc64d224f95474bc9fc9017a2e9fb01` (`Step_7.1R`).
- Initial `git status --short --untracked-files=all`: no output; no conflicting user change existed.
- Recent history: `415fc24 Step_7.1R`, `1bf26f8 Step_7.1`, `a07ec40 Step_6.11R`, `7b47e51 Step_6.11.2`, `28a9dbe Step_6.11`.
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from the accepted repository-external environment. No dependency installation or network access occurred.
- No repository instruction file was present.

Generated caches were removed without deleting tracked or user-created files. The untouched baseline `PYTHONPATH=src python -m pytest` collected and passed 1012 tests in 22.14s with zero failures, skips, and xfails.

## Accepted artifacts

| Artifact | SHA-256 |
|---|---|
| `data/results/sp07_experiment_catalog.csv` | `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb` |
| `data/results/sp07_quantitative_summary.json` | `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0` |
| `experiments/scalability_config.json` | `93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921` |
| `results/scalability_results.json` | `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f` |
| `results/scalability_environment.json` | `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba` |

The accepted EXP-05 row is `gap_identified`: mixed `Controller.submit` host timing does not independently measure `CredentialRepository.lookup`, `authorize`, or an expected-versus-actual outcome matrix. SP-07.2 is authorized only to close that gap with a separate experiment.

## Authorized and protected scope

Authorized creation paths are `analysis/run_experiments.py`, `experiments/isolated_operations_config.json`, two `sp07_isolated_operation_*` JSON outputs, `tests/analysis/test_run_isolated_experiments.py`, this baseline, `audit/stage_reports/subproject_07_02.md`, and `audit/validation/subproject_07_02_validation.md`. Only `audit/file_change_ledger.md` may be updated.

Protected content includes all production source; the accepted mixed runner/configuration/results/environment; `analysis/analyze_results.py`; SP-07.1 catalog/summary and all prior audits; existing tests; requirements/design/architecture/register/test plan/inventory/traceability/verification; README/reproducibility; project plan; literature/evidence/product files; report/presentation; dependencies; and Git history.

## Measurement boundaries and deferred work

Lookup timing includes only the public repository method call, its trusted-key validation, Python dictionary lookup, and result-wrapper construction. Authorization timing includes only the public pure function call, trusted-input validation, precedence/floor-mask logic, and decision construction. Generation, repository construction, checksums, classification, export, controller, Wiegand, logging, outputs, network/database servers, and hardware are excluded.

The results will be observational Python host timings with timer overhead retained, no threshold, no real-time/constant-time claim, no asymptotic inference, and no physical RFID/electrical/elevator/reliability/safety/certification/commercial conclusion. SP-07.3 integration/tables/figures and SP-07.4 independent review/source notes remain deferred.
