# SP-06.5 Baseline

Clean `main` at accepted commit `510250c428ff5cad3155d7beca09d0987a739257` in `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`; Python 3.13.13, pip 26.2, pytest 9.1.1 in `/home/bar/.venvs/eeeproject-elevator`. Baseline: 425 collected/passed, 0 failed/skipped/xfailed in 1.16s. Existing SP-06.1–06.4 records and source/tests were present; no conflicting changes or repository instructions existed.

Frozen rules: exactly 16 Boolean channels; floor 1→index 0 and floor 16→index 15; zero/one active; inactive floor/expiry null; duration exact integer 100–30000; expiry `now+duration`; trusted misuse raises `StateInvariantError`. Reviewed API: `OutputManager()`, `activate`, `next_expiry_ms`, `expire_if_due`, `reset`, `snapshot`.

Authorized paths are new `outputs.py`, `test_outputs.py`, this baseline, SP-06.5 stage/validation, package export, and ledger section. Models/clock/config/Wiegand/credentials/authorization/event log, existing tests, engineering documents, prior audits, and Git history are protected. Watchdog/controller/CLI/experiments/physical behavior remain deferred.
