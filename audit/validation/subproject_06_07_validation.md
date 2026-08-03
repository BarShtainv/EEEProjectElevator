# SP-06.7 Validation

## Environment and executed test commands

```text
Repository: /mnt/c/Users/Bar/Desktop/EEEProjectElevator
Branch: main
Starting HEAD: 42f3bf47f2b2c696a903168b200c7b1705f8ea92
Python: 3.13.13
pip: 26.2
pytest: 9.1.1

Baseline `PYTHONPATH=src python -m pytest`: 562 collected/passed, 0 failed/skipped/xfailed in 1.44s
Output regression `tests/unit/test_outputs.py -q`: 71 passed in 0.27s
Watchdog closure `tests/unit/test_watchdog.py -v`: 68 passed in 0.26s
Initialization `tests/unit/test_controller_initialization.py -v`: 45 passed in 0.24s
Requests `tests/integration/test_controller_requests.py -v`: 94 passed in 0.28s
Timing `tests/integration/test_controller_timing.py -v`: 29 passed in 0.17s
Resets `tests/integration/test_controller_resets.py -v`: 12 passed in 0.14s
Logging faults `tests/integration/test_controller_logging_faults.py -v`: 15 passed in 0.15s
Aggregate controller paths: 195 passed in 0.54s
Full suite: 759 collected/passed, 0 failed/skipped/xfailed in 1.59s
```

## Behavioral evidence

- SP-06.6 closure: suppressed heartbeats at 1000/2000 and 3000/4000 produce one expiry per independently reinitialized/reinjected epoch; repeated checks are false. Disabled reinitialize retains interval, has no schedule/deadline, and clears suppression.
- Startup mapping: invalid configuration, record/sequence, duplicate key, and injected repository exception produce their four frozen reasons; no partial configuration/repository/watchdog publication occurs. Corrected restart succeeds and startup clear resets events/sequence.
- Request matrix: both LF/HF grant; identical frames decode identically; malformed container/length/member and both parity regions fail; unknown and disabled precede floor inspection; invalid floor errors; unauthorized floor denies; all 16 floors grant with their mapped mask bit; busy denies without inspection.
- State coverage: construction and startup plus validation, lookup, authorization, active, timeout, and reset transitions cover all seven states. Manual reset from every state observes `RESETTING` during append and finishes `IDLE`.
- Reason/result/event coverage: tests exercise all 17 `Reason` values, all five `Result` values, and controller production of `ACCESS_DECISION`, `VALIDATION_ERROR`, `OUTPUT_TIMEOUT`, `MANUAL_RESET`, and `WATCHDOG_RESET`. Explicit log serialization coverage for the sixth event type remains in the prior event-log suite.
- Busy proof: a hostile object recorded zero attribute reads; patched frame validation, repository lookup, authorization, and activation would fail if called. Original channels, floor, expiry, and active context remained unchanged.
- Grant gate: collaborator spies observed append then activation while state remained `AUTHORIZING`; injected append failure created no activation or sequence. Injected post-append activation invariant propagated and retained the successful grant event.
- Timing proof: normal 3000/2000 heartbeats at 1000, 2000, and 3000 prevent watchdog expiry and output times out once at timestamp 3000. Normal 30000/2000 services through all due heartbeats and times out once at 30000.
- Suppression/collision: suppressed watchdog resets at 2000 both idle and active, reinitializes deadline to 4000, and does not duplicate at repeated time. A shared 2000 watchdog/output deadline produces only watchdog reset and cancels output expiry.
- Scheduler: invalid/backward clock input is atomic; markers earlier than current raise `StateInvariantError`; due markers are selected from three managers and jumped to directly; priority is heartbeat, watchdog, output. No millisecond loop, wall-clock, callback, thread, or async path exists.
- Partition/replay: single versus partitioned advances produce equal final responses, snapshots, records, sequences, timestamps, JSON Lines, output/watchdog counts, and final logical time for normal timeout, suppressed reset, and long timeout. Two fresh deterministic replays are equal.
- Reset: manual/watchdog reset preserve config, repository, clock, events, and sequence while clearing output, expiry, ordinary/active transients, and suppression. Canceled timeout does not later fire, and subsequent valid requests grant.
- Logging matrix: invalid source, invalid frame, unknown, disabled, invalid floor, unauthorized floor, grant, busy, timeout, manual reset, and watchdog reset all return `ERROR/LOGGING_ERROR` on append failure with no consumed sequence. Grant stays inactive; busy preserves activation; timeout/reset remain cleared/completed. The next successful append uses the unconsumed number and clears the fault. No no-op or synthetic event clears/logs the failure.

## Final technical and scope checks

`python -m compileall -q src tests`, package import, `from elevator_access_sim import Controller`, exact signature/export inspection, programmatic state/timing/fault checks, `git diff --check`, changed-path/status inspection, protected SHA-256 comparison, cache cleanup, and repository-local virtual-environment inspection were executed after the final audit edits and passed. `Controller` imports only the eight approved project modules and standard-library sequence typing; the package import remains acyclic.

Only the 12 authorized paths in the SP-06.7 ledger changed. No CLI, JSON file adapter, experiment/scalability runner, storage/database/network/GUI/hardware/physical interface, extra profile, dependency, CI, or later-stage module was created. Requirements, register model, architecture, diagrams, software design, test plan/inventory, implementation sequence, traceability, evidence/literature/product records, prior audits, project/workflow records, and Git history remained unchanged. No virtual environment exists inside the repository. No commit or push occurred.

READY FOR HUMAN REVIEW
