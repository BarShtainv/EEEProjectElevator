# SP-06.10 Baseline

## Accepted starting point

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Commit: `a7ae9f0ec835150fd0b4a37809c93b2502b8d949`
- Initial Git status: clean
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`
- Baseline command: `PYTHONPATH=src python -m pytest`
- Baseline result: 871 collected, 871 passed, 0 failed, 0 skipped, 0 xfailed in 3.13 seconds
- Accepted records: SP-06.1 through SP-06.9 baseline, stage, and validation records are present.

## Inventory handoff

The test inventory contains 100 rows: 88 `implemented` and 12 `designed`. The SP-06.9 resolution contains 100 rows: 67 existing executable, 3 SP-06.9 executable, 18 SP-06.9 inspection, 5 scheduled SP-06.10, 1 scheduled SP-06.11, 6 optional deferred, and 0 unresolved.

SP-06.10 owns the five still-designed rows `TST-REP-001`, `TST-REP-002`, `TST-SCL-001`, `TST-SCL-002`, and `TST-SCL-003`. SP-06.11 retains still-designed `TST-TRC-005`. Optional rows `TST-OPT-001` through `TST-OPT-006` remain designed and deferred.

## Change boundary

Authorized created paths are `scripts/run_experiments.py`, `experiments/scalability_config.json`, `results/scalability_results.json`, `results/scalability_environment.json`, `tests/experiment/test_run_experiments.py`, this baseline, `audit/stage_reports/subproject_06_10.md`, and `audit/validation/subproject_06_10_validation.md`. Authorized modifications are limited to the status field of the five SP-06.10 inventory rows in `docs/test_case_inventory.csv` after all execution gates pass, plus the new SP-06.10 section in `audit/file_change_ledger.md`.

Protected paths include every production module under `src/elevator_access_sim/`, all existing tests, `pyproject.toml`, requirements, register model, architecture/diagrams, software design, test plan, implementation sequence, decision log, both traceability CSVs, the historical SP-06.9 resolution, all prior audit records, project/workflow material, and evidence/literature/bibliography/product artifacts. A simulator defect requiring production change must be reported before scope expands.

## Interpretation and deferred work

SP-06.10 measurements are observational host measurements from `time.perf_counter_ns` around only `Controller.submit`. Generation, initialization, output-expiry cleanup, environment collection, validation, and export are excluded. The frozen experiment disables the simulated watchdog. No latency objective, real-time guarantee, hardware/RFID/electrical/elevator/safety/reliability inference, commercial equivalence, or cross-host equality is authorized.

SP-06.11 retains final README/reproducibility instructions, final verification-record reconciliation, documentation-command review, and `TST-TRC-005`. None is authorized in this stage.
