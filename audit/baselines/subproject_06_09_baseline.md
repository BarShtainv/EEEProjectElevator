# SP-06.9 Baseline

## Accepted starting point

- Branch: `main`
- Commit: `9a6c448f71e887ac6c47d3a3436c0fe2a644e4e0`
- Initial Git status: clean
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`
- Baseline command: `PYTHONPATH=src python -m pytest`
- Baseline result: 859 collected, 859 passed, 0 failed, 0 skipped, 0 xfailed in 2.02 seconds

The external environment was activated equivalently by invoking its Python executable directly. An initial invocation without the required `PYTHONPATH=src` could not import the src-layout package; the prescribed command above then produced the accepted result without any repository edit.

## Reviewed repository state

Current source modules are `__init__.py`, `authorization.py`, `cli.py`, `clock.py`, `config.py`, `controller.py`, `credentials.py`, `event_log.py`, `models.py`, `outputs.py`, `watchdog.py`, and `wiegand.py` under `src/elevator_access_sim/`.

Current tests comprise five integration modules (`test_cli.py`, `test_controller_logging_faults.py`, `test_controller_requests.py`, `test_controller_resets.py`, and `test_controller_timing.py`) and twelve unit modules (`test_authorization.py`, `test_clock.py`, `test_config.py`, `test_config_files.py`, `test_controller_initialization.py`, `test_credential_config.py`, `test_credentials.py`, `test_event_log.py`, `test_models.py`, `test_outputs.py`, `test_watchdog.py`, and `test_wiegand.py`). There were no end-to-end or inspection test directories at baseline.

- Test-case inventory: 100 data rows; the only status value is `designed`.
- Requirements-to-test traceability: 66 data rows.
- Requirements: 60 required and 6 optional requirement rows.
- Accepted records: every SP-06.1 through SP-06.8 baseline, stage report, and validation record is present.

## Change boundary

Authorized paths are `tests/end_to_end/`, `tests/inspection/`, `docs/test_case_inventory.csv`, `audit/baselines/subproject_06_09_baseline.md`, `audit/stage_reports/subproject_06_09.md`, `audit/validation/subproject_06_09_validation.md`, `audit/validation/subproject_06_09_inventory_resolution.csv`, and `audit/file_change_ledger.md`. A production source or frozen traceability correction is authorized only if execution reveals a genuine defect; none is assumed.

Protected paths include production behavior unless a demonstrated defect requires the smallest correction; all frozen engineering documents; `docs/requirements_to_test_traceability.csv` unless a genuine broken identifier is found; `docs/architecture_to_requirements.csv`; prior tests and audit records; dependency and packaging policy; project/workflow, evidence, literature, and product artifacts; and Git history.

SP-06.10 retains ownership of reproducible generators, aggregate export, scalability execution at 10/100/1,000/10,000 credentials, host-timing metrics, and experiment reporting (`TST-REP-001`, `TST-REP-002`, and `TST-SCL-001` through `TST-SCL-003`). SP-06.11 retains ownership of final verification-record reconciliation and documentation (`TST-TRC-005`). Optional rows `TST-OPT-001` through `TST-OPT-006` remain explicitly deferred and cannot gate required completion.
