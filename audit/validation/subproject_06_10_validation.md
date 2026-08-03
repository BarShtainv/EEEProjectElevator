# SP-06.10 Validation

## Starting state and environment

- R2 root/branch/commit: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`, `main`, `1c746552f192302209fa7eb2e9bee34adbb30463`.
- Initial status: clean.
- History: SP-06.9 `a7ae9f0ec835150fd0b4a37809c93b2502b8d949`; incomplete SP-06.10 `d3679748096ed39d8e72996e203d06b0a9e3590f`; strict-mix repair `1c746552f192302209fa7eb2e9bee34adbb30463`.
- `python --version`: Python 3.13.13.
- `python -m pip --version`: pip 26.2.
- `python -m pytest --version`: pytest 9.1.1.
- Current R2 baseline `PYTHONPATH=src python -m pytest`: 965 collected/passed, 0 failed, 0 skipped, 0 xfailed in 3.63s.
- Previously recorded pre-repair baseline: 962/962 in 3.67s.

## Executed validation

| Command or gate | Exact result |
|---|---|
| `PYTHONPATH=src python -m pytest tests/experiment/test_run_experiments.py -v` | 94 collected/passed, 0 failed/skipped/xfailed in 0.62s. |
| strict official-mix nodes within the experiment module | Exact official configuration passed; 39/21/15/15/10 and 20/20/20/20/20 official substitutions both passed by raising the expected error; non-official bounded mix support passed. |
| `PYTHONPATH=src python scripts/run_experiments.py --config /tmp/eeeproject-elevator-sp0610r2-smoke/smoke_config.json --results /tmp/eeeproject-elevator-sp0610r2-smoke/smoke_results.json --environment /tmp/eeeproject-elevator-sp0610r2-smoke/smoke_environment.json` | Exit 0 with `completed: sizes=1 measured_rows=1 timer=time.perf_counter_ns`; one measured row; exact 40/20/15/15/10/0 outcomes; reconciliation passed; finite positive metrics; integer p95; environment parsed; no raw data; temporary directory removed; operational wall 0.123s. |
| `PYTHONPATH=src python scripts/run_experiments.py --config experiments/scalability_config.json --results results/scalability_results.json --environment results/scalability_environment.json` | Exit 0; `completed: sizes=4 measured_rows=12 timer=time.perf_counter_ns`; operational wall 0.691s. |
| standalone standard-library JSON validation | Exit 0; strict UTF-8, schemas, exact IDs/mix/sizes/repetitions/counts, equations, metrics, checksums, environment links/limits, and raw-data exclusions passed. |
| inventory validator | 100 unique IDs; 93 implemented and 7 designed; only the five owned statuses promoted. |
| first full regression after inventory promotion | 965 collected; 964 passed, 1 failed, 0 skipped, 0 xfailed in 3.32s; only stale SP-06.9 live-status assertion failed. |
| `PYTHONPATH=src python -m pytest tests/inspection/test_inventory_traceability.py -v` after correction | 2 collected/passed, 0 failed/skipped/xfailed in 0.49s. |
| corrected full regression | 965 collected/passed, 0 failed/skipped/xfailed in 3.21s. |
| final post-audit full regression | 965 collected/passed, 0 failed/skipped/xfailed in 3.16s. |
| `python -m compileall -q src tests scripts` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "import elevator_access_sim"` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "from elevator_access_sim import Controller"` | Exit 0 with no diagnostics. |
| final standalone JSON and inventory validator | Exit 0; 12 result rows passed exact configuration/outcome/reconciliation/metric/checksum/environment/raw-data checks; inventory was 93 implemented/7 designed with 100 unique IDs and exactly five changed status cells. |
| cleanup commands | Exit 0; `.pytest_cache`, `__pycache__`, bytecode, orphan `.tmp`, and smoke artifacts absent; no repository-local virtual environment found. |
| `git diff --check` | Exit 0 with no diagnostics. |
| `git diff --name-only` and `git status --short --untracked-files=all` | Reviewed six intended paths: ledger, inventory, generated aggregate results, narrow historical inspection correction, stage report, and validation record. |
| final branch, HEAD, and production scope checks | `main`; `1c746552f192302209fa7eb2e9bee34adbb30463`; `git diff --quiet -- src` exited 0. |

The stale assertion repair changed no historical CSV. It allows only historical `scheduled_sp06_10` rows to reflect subsequent live implementation, while `scheduled_sp06_11` remains required to be live-status `designed`.

## Official outcomes

Every repetition reconciled exactly:

| Credential size | Repetitions | Requests each | Granted | Unauthorized | Disabled | Unknown | Invalid frame | Other |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1, 2, 3 | 1,000 | 400 | 200 | 150 | 150 | 100 | 0 |
| 100 | 1, 2, 3 | 1,000 | 400 | 200 | 150 | 150 | 100 | 0 |
| 1,000 | 1, 2, 3 | 1,000 | 400 | 200 | 150 | 150 | 100 | 0 |
| 10,000 | 1, 2, 3 | 10,000 | 4,000 | 2,000 | 1,500 | 1,500 | 1,000 | 0 |

The 12 R2 rows all have finite positive average, median, observed integer nearest-rank p95, and throughput values. No threshold was evaluated. Environment ID is consistently `env-ffbfdbefc2f5ed62`. Same-size credential and request checksums are identical across repetitions:

- 10: `e6b71173d03d5aa5a6529afb86f62a0db1c39057a8cfc208bc90ff06330beaee`; `93dbc8c1f8fe624fad47c9e8a13d02f814bd6a0166777923719fb35456ab30b8`.
- 100: `2dbe74a204c5968756397ce3531a835f8f1a122e542048eb4ac8a1aba0077e3f`; `c08bf3b836778aede71c75ace428bc7de76fab0f31828cda40e8ff208313a0da`.
- 1,000: `decf95c5b5002df2d80219c5b5a0adcad49c4956f9476ac7ad5c363649e1f87d`; `625b9c80bdf6c2fd1ce0a2b45d8692ca347dc2e4377070cf7c7b7ba6be740d76`.
- 10,000: `2c859c5b59825058c02ac7d6ae98e05632d35318f08e1937317aa9ac85fb2b1d`; `c1ff8a6c7e6d63bfb50b323ee2d217ceddc7a2943927c88022464244f06eb55b`.

The result/environment documents contain no raw credentials, requests, events, timing arrays/samples, username, hostname, home path, executable path, or virtual-environment path. Interpretation text covers host-only `perf_counter_ns` around `Controller.submit`, excluded initialization/generation/cleanup/export, disabled watchdog, observational variability, no latency objective, no real-time guarantee, and no RFID/electrical/elevator/safety/reliability/commercial equivalence.

## Final boundary

The final command set passed all 94 experiment cases and all 965 repository tests, compiled `src tests scripts`, imported `elevator_access_sim` and `Controller`, and independently validated the JSON evidence and inventory after audit edits. Final whitespace, changed-path, status, scope, and cleanup results are recorded in the handoff. Production source remains byte-for-byte outside the diff. SP-06.11 README/reproducibility and `TST-TRC-005` were not performed. No commit or push occurred.

READY FOR HUMAN REVIEW
