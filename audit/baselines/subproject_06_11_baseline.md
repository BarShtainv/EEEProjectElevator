# SP-06.11 Baseline

## Accepted starting state

- Repository: `BarShtainv/EEEProjectElevator`.
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator` (recorded baseline context only).
- Branch: `main`.
- Accepted commit: `28a9dbebf23b0220ca87afdae143b7432ab0d8dc` (`Step_6.11`).
- Initial `git status --short --untracked-files=all`: empty.
- No conflicting user change, repository instruction file, or repository-local virtual environment was present.
- Python 3.13.13, pip 26.2, and pytest 9.1.1 were supplied by the accepted repository-external environment. No install or network access occurred.

## Prescribed baseline

Generated Python and pytest caches were removed before execution. The exact repository-root command `PYTHONPATH=src python -m pytest` collected and passed 965 tests in 3.58 seconds with zero failures, zero skips, and zero xfails. The hardened bytes-`PathLike` test remained collected and passing.

The accepted pre-stage repair is `audit/validation/subproject_06_11_baseline_flake_repair.md` (SHA-256 `aafcd53bd960a5ada73860625dfa8f4a3040f55e08ee634b868303388f43c318`). Its protected test file `tests/unit/test_config_files.py` began at SHA-256 `044fae7d87ee5583d2b570f8bf59fe0caaeb0802dcfeb01e36ffd0ab10cb3b92`.

## Documentation and reconciliation handoff

- `README.md` contains only `# EEEProjectElevator`; no useful entry point or reproducibility procedure exists yet.
- `docs/test_case_inventory.csv` has 100 unique rows: 93 `implemented` and seven `designed`.
- `TST-TRC-005` is the only remaining required designed row.
- The other six designed rows are exactly `TST-OPT-001` through `TST-OPT-006` and remain optional post-MVP work.
- `docs/requirements_to_test_traceability.csv` has 66 unique rows, all currently `planned`: 60 required and six optional requirements.
- The historical `audit/validation/subproject_06_09_inventory_resolution.csv` has 100 ordered rows and retains five `scheduled_sp06_10`, one `scheduled_sp06_11`, and six `optional_deferred` classifications.
- SP-06.1 through SP-06.10 baseline, stage, and validation records are present, together with the accepted pre-SP-06.11 repair record.

## Existing scalability evidence

- Official configuration: `experiments/scalability_config.json`; schema 1, configuration `SP06_SCALABILITY_V1`, workload `MIXED_REQUESTS_V1`, seed 260516, sizes 10/100/1,000/10,000, one warm-up, and three measured repetitions.
- Aggregate results: `results/scalability_results.json`; 12 rows, SHA-256 `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f`.
- Environment record: `results/scalability_environment.json`; environment `env-ffbfdbefc2f5ed62`, SHA-256 `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba`.
- Request counts are 1,000/1,000/1,000/10,000. Generated-input checksum pairs are stable within each size; timing remains host-observational.

## Authorized paths

Creation is limited to:

- `docs/reproducibility.md`;
- `tests/inspection/test_documentation_reproducibility.py`;
- this baseline;
- `audit/stage_reports/subproject_06_11.md`;
- `audit/validation/subproject_06_11_validation.md`;
- `audit/validation/subproject_06_11_verification_records.csv`.

Updates are limited to:

- `README.md`;
- `docs/test_plan.md`;
- `docs/test_case_inventory.csv`;
- `docs/requirements_to_test_traceability.csv`;
- `tests/inspection/test_inventory_traceability.py`;
- `audit/file_change_ledger.md`.

## Protected paths and boundaries

Production source, public APIs, `scripts/run_experiments.py`, official configuration/results/environment, existing unit/integration/end-to-end/experiment tests, the hardened PathLike test and its repair record, package metadata, frozen requirements/architecture/register/design/sequence/decisions/architecture traceability, historical SP-06.9 resolution, prior audits, evidence/literature/product/project/workflow material, and Git history are protected.

The stage may document and reconcile completed required software-model work only. It may not change simulator behavior, implement optional features, add dependencies or CI, regenerate tracked host measurements, create physical/commercial/safety/real-time/production-readiness claims, rewrite the engineering report or literature review, create the presentation, or create a release/submission package.

## Human approvals and later work

The exact working title is project-owner approved, while supervisor approval remains pending. Supervisor confirmation remains required for final submission and any physical-scope or commercial-equivalence expansion. Optional profiles, authorization policies, persistence, enhanced interface, physical adapters, and extra experiments remain deferred. The engineering report, presentation, release preparation, submission work, and all human approvals remain outside this Subproject-6 completion task.
