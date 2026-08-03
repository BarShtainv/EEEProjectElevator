# SP-07.1 Quantitative-Analysis Baseline

## Accepted starting state

- Stage: `SP-07.1` — Experiment evidence consolidation and quantitative-analysis baseline.
- Repository: `BarShtainv/EEEProjectElevator`; root name `EEEProjectElevator`.
- Branch and accepted commit: `main` at `a07ec409e01606913d3f20eef99a8d884263a658` (`Step_6.11R`).
- Initial `git status --short --untracked-files=all`: no output; the working tree was clean and no conflicting user change existed.
- Recent accepted history: `a07ec40 Step_6.11R`, `7b47e51 Step_6.11.2`, `28a9dbe Step_6.11`, `64cfabc Step_6.10R2`, `1c74655 Step_6.10R`.
- External environment: Python 3.13.13; pip 26.2; pytest 9.1.1 from the repository-external `eeeproject-elevator` environment. No install or network access occurred.
- Generated caches were removed before the baseline without deleting tracked or user-created files.

## Prescribed baseline

`PYTHONPATH=src python -m pytest` collected and passed 976 tests in 4.60s with zero failures, skips, and xfails. No implementation edit preceded this run.

Accepted reconciliation at the gate was:

- test inventory: 100 rows, 94 `implemented`, six optional `designed`;
- requirements traceability: 66 rows, 60 required `verified`, six optional `optional_deferred`;
- final verification records: 100 rows, 94 `passed`, six `optional_deferred`;
- final accepted full-suite evidence: 976 collected/passed, zero failed/skipped/xfailed.

All SP-06.1 through SP-06.11R baseline, stage, validation, repair, inventory, traceability, reproducibility, test, and experiment evidence required by the prompt was present.

## Canonical source artifacts

| Repository-relative path | SHA-256 |
|---|---|
| `audit/validation/subproject_06_11_verification_records.csv` | `623032dabefa0cd983812527ab09ba719a00998f1d3e6204ecea5fbe17da4e42` |
| `docs/test_case_inventory.csv` | `ce97fca1b72521536ffc85a4fe22c7cb8cf26f3dbb4220e1db394667e9178601` |
| `docs/requirements_to_test_traceability.csv` | `e830fb840375e574d342073b285987b574fdaa76d80613e40d558f7b96bb2289` |
| `audit/validation/subproject_06_11_validation.md` | `587e62db8799556a8c4b75aeb5adcb2c50cbdc1b67d804c0b288697452d8d1ab` |
| `experiments/scalability_config.json` | `93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921` |
| `results/scalability_results.json` | `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f` |
| `results/scalability_environment.json` | `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba` |

The frozen scalability evidence identifies schema 1, configuration `SP06_SCALABILITY_V1`, workload `MIXED_REQUESTS_V1`, seed 260516, environment `env-ffbfdbefc2f5ed62`, four sizes, three measured repetitions per size, and 12 aggregate result rows.

## Authorized and protected scope

Authorized creation paths were:

- `analysis/analyze_results.py`;
- `data/results/sp07_experiment_catalog.csv`;
- `data/results/sp07_quantitative_summary.json`;
- `tests/analysis/test_analyze_results.py`;
- this baseline;
- `audit/stage_reports/subproject_07_01.md`;
- `audit/validation/subproject_07_01_validation.md`.

Only `audit/file_change_ledger.md` was authorized for modification.

Protected content includes production source, the accepted experiment runner/configuration/results/environment, every Subproject-6 test and audit, README/reproducibility, requirements/design/architecture/register/test plan, inventory, traceability, final verification records and provenance repair, project plan, literature/evidence/product material, report, presentation, dependencies, and Git history.

## Known measurement limits and deferred work

The existing metrics are mixed `Controller.submit` request-processing host timing observed on one recorded environment. They do not isolate repository lookup or authorization, contain no raw per-request samples, support no pooled request percentiles, and establish no deterministic host timing, threshold, real-time guarantee, hardware/RFID/electrical/elevator behavior, field reliability, safety, certification, or commercial equivalence. Zero `other_outcomes` is exact reconciliation, not a separately measured false-grant or false-denial count.

SP-07.2 is deferred to the smallest independent lookup/authorization and explicit expected-versus-actual measurement. SP-07.3 figures/tables and SP-07.4 review/discussion notes remain deferred. No figure, final report prose, benchmark rerun, raw dataset, or Subproject-8 work is authorized here.
