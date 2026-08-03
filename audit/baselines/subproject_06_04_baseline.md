# SP-06.4 Baseline

- Repository: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator` (`BarShtainv/EEEProjectElevator`)
- Branch: `main`
- Accepted starting commit: `2677b8d03532733575460d6400fa2053ed5e539c` (`Step_6.3`)
- Initial status: clean
- Environment: `/home/bar/.venvs/eeeproject-elevator`; Python 3.13.13; pip 26.2; pytest 9.1.1
- Repository instructions: no `AGENTS.md`
- Baseline: 367 collected, 367 passed, 0 failed/skipped/xfailed in 1.01s

Existing source comprises models, configuration, clock, Wiegand, credentials, and authorization; seven existing unit-test modules passed. Accepted SP-06.1 through SP-06.3 records are present. No event-log or later module existed.

The frozen record order is `sequence_number`, `timestamp_ms`, `event_type`, `reader_source`, `facility_code`, `credential_number`, `requested_floor`, `result`, `reason`. Event/source/result/reason serialize through reviewed enum text: event/result/reason lowercase; source uppercase LF/HF or null. All nine fields remain present.

The reviewed API is `EventLog.__init__`, `append`, `set_append_failure`, `records`, `latest_sequence`, `clear_startup`, and `to_jsonl`. Owned state is successful records, next sequence, latest successful timestamp, and failure flag. Sequences begin at 1 and remain contiguous; timestamps are nonnegative/nondecreasing; injected failure precedes validation/allocation; startup clear resets all owned state.

Authorized changes are new `event_log.py`, `test_event_log.py`, this baseline, SP-06.4 stage/validation records, package-root `EventLog` export, and one ledger section. Models, all existing implementation/tests, frozen engineering documents, prior audit records, and Git history are protected. Outputs, timeout management, watchdog, controller, reset orchestration, CLI, experiments, persistence/database/network, and hardware remain deferred.
