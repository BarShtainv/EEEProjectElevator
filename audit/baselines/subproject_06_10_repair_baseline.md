# SP-06.10R Repair Baseline

## Accepted starting point

- Repository: `BarShtainv/EEEProjectElevator`
- Root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Branch: `main`
- Accepted commit: `d3679748096ed39d8e72996e203d06b0a9e3590f`
- Initial Git status: clean
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`
- Baseline command: `PYTHONPATH=src python -m pytest`
- Baseline result: 962 collected, 962 passed, 0 failed, 0 skipped, 0 xfailed in 3.67 seconds

## Incomplete SP-06.10 handoff

The incomplete commit contains exactly the six expected SP-06.10 artifacts: `audit/baselines/subproject_06_10_baseline.md`, `experiments/scalability_config.json`, `results/scalability_environment.json`, `results/scalability_results.json`, `scripts/run_experiments.py`, and `tests/experiment/test_run_experiments.py`.

The SP-06.10 stage report, SP-06.10 validation record, and SP-06.10 ledger entry are absent. Inventory rows `TST-REP-001`, `TST-REP-002`, `TST-SCL-001`, `TST-SCL-002`, and `TST-SCL-003` remain `designed`.

The runner validates official configuration identity, seed, sizes, repetition policy, simulator values, and merely positive workload percentages, but it does not compare the official workload mix with the exact frozen 40/20/15/15/10 values. Thus an all-positive, five-category, total-100 substituted mix can incorrectly parse under the official configuration ID.

## Repair boundary

Authorized changes are the smallest exact official-mix correction in `scripts/run_experiments.py`, direct substitution regressions in `tests/experiment/test_run_experiments.py`, status-only promotion of the five owned inventory rows after every gate, creation of the missing SP-06.10 stage and validation records, creation of this repair baseline, and an appended SP-06.10 ledger section.

Protected content includes all production modules, other tests, package metadata, requirements, register model, architecture/diagrams, software design, test plan, implementation sequence, decision log, traceability, historical SP-06.9 inventory resolution, earlier audit records including the original SP-06.10 baseline, project/workflow/evidence/literature/product material, and Git history. SP-06.11 documentation and `TST-TRC-005` remain deferred.
