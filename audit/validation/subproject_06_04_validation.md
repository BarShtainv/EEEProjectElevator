# SP-06.4 Validation

Repository `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`, branch `main`, HEAD `2677b8d03532733575460d6400fa2053ed5e539c`; Python 3.13.13, pip 26.2, pytest 9.1.1.

```text
$ PYTHONPATH=src python -m pytest
collected 367 items
============================= 367 passed in 1.01s ==============================
$ PYTHONPATH=src python -m pytest tests/unit/test_event_log.py -v
collecting ... collected 58 items
<58 verbose PASSED node results>
============================== 58 passed in 0.25s ==============================
$ PYTHONPATH=src python -m pytest
collected 425 items
============================= 425 passed in 0.94s ==============================
$ python -m compileall -q src tests
<no output; exit 0>
$ PYTHONPATH=src python -c "import elevator_access_sim"
<no output; exit 0>
$ PYTHONPATH=src python -c "from elevator_access_sim import EventLog"
<no output; exit 0>
```

All baseline/scoped/full failures, skips, and xfails: 0. Tests cover initial state, copied immutable records/order, contiguous allocation, equal/increasing/backward/invalid timestamps, atomic structural and injected failures, invalid flags, startup clear, all six event types, two sources plus null, five results, seventeen reasons, representative event kinds, exact nine-key order, explicit nulls, compact/repeatable JSONL, and prohibited-import inspection.

```text
API=EventLog signatures=matched INITIAL=empty
SEQUENCES=1,2,failure,3 contiguous EQUAL_TIMESTAMPS=accepted
JSON_KEYS=9 order=exact nulls=explicit enum_text=canonical
FAILURE=atomic no_synthetic_event STARTUP_CLEAR=complete
```

```text
$ find <cache/local-environment patterns>
<no output>
$ find src tests <later-module patterns>
<no output>
$ git diff --name-only -- <protected paths>
<no output>
$ git diff --check
<no output; exit 0>
$ git diff --name-only
audit/file_change_ledger.md
src/elevator_access_sim/__init__.py
$ git status --short --untracked-files=all
 M audit/file_change_ledger.md
 M src/elevator_access_sim/__init__.py
?? audit/baselines/subproject_06_04_baseline.md
?? audit/stage_reports/subproject_06_04.md
?? audit/validation/subproject_06_04_validation.md
?? src/elevator_access_sim/event_log.py
?? tests/unit/test_event_log.py
$ git rev-parse HEAD
2677b8d03532733575460d6400fa2053ed5e539c
$ git branch --show-current
main
```

Tracked diff names plus five authorized untracked paths total exactly seven allowed changes. Cleanup and protected-scope checks passed.

No later module, dependency/network action, commit, or push occurred.

READY FOR HUMAN REVIEW
