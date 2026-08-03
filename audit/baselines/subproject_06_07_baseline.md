# SP-06.7 Baseline

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Accepted starting commit: `42f3bf47f2b2c696a903168b200c7b1705f8ea92`
- Initial status: clean (`git status --short --untracked-files=all` produced no output)
- Recent accepted stages: SP-06.1 through SP-06.6 are present in Git history and audit records.
- Environment: Python 3.13.13; pip 26.2; pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`.
- Baseline command: `PYTHONPATH=src python -m pytest`
- Baseline result: 562 collected, 562 passed, 0 failed, 0 skipped, 0 xfailed in 1.44s.

## Reviewed contracts

Available composition APIs are `SimulatedClock`, `validate_frame`, `CredentialRepository`, `authorize`, `OutputManager`, `Watchdog`, and `EventLog`, with the frozen shared models and exceptions in `models.py`. The controller contract is `Controller(clock, event_log=None)` plus `initialize`, `submit`, `advance_to`, `advance_by`, `manual_reset`, `set_watchdog_service_suppressed`, `snapshot`, and `events`.

The frozen seven states are `RESETTING`, `INITIALIZING`, `IDLE`, `VALIDATING`, `LOOKUP`, `AUTHORIZING`, and `OUTPUT_ACTIVE`. Busy handling precedes all request inspection. Idle processing is source, frame structure, parity/decode, lookup, enabled status, authorization, grant append, then output activation. Startup publishes validated configuration, repository, and watchdog atomically.

The scheduler jumps directly between due timestamps and processes heartbeat, watchdog expiry, then output expiry. Watchdog reset wins a collision. Manual and watchdog resets clear output/runtime transients and suppression while preserving configuration, repository, clock, event history, and sequence progression.

Only `EventLogError` is converted to `ERROR/LOGGING_ERROR`. Grant logging failure prevents activation; timeout/reset logging failures do not reverse completed safety transitions; busy logging failure preserves the existing activation. Successful later appends clear the controller logging-fault flag and failed appends consume no sequence.

## Scope controls

Authorized paths are the SP-06.7 controller, its five named controller test modules, the mandatory watchdog-test coverage closure, package export, this baseline, the SP-06.7 stage/validation records, and the file-change ledger. All other source modules, existing tests, frozen engineering documents, traceability files, prior audit records, requirements, dependency metadata, project/workflow records, literature/evidence/product artifacts, and Git history are protected.

Baseline SHA-256 values were recorded for every protected source collaborator and named frozen document before edits. SP-06.8 CLI and JSON file-adapter work, experiments, scalability, persistence, networking, GUI, hardware/physical behavior, optional profiles, and optional authorization features remain deferred.
