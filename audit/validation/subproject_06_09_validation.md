# SP-06.9 Validation

## Environment and baseline

- Accepted branch/commit: `main` at `9a6c448f71e887ac6c47d3a3436c0fe2a644e4e0`; initial status clean.
- `python --version`: Python 3.13.13.
- `python -m pip --version`: pip 26.2 from the external environment.
- `python -m pytest --version`: pytest 9.1.1.
- Prescribed baseline `PYTHONPATH=src python -m pytest`: 859 collected/passed, 0 failed, 0 skipped, 0 xfailed in 2.02 seconds.

An earlier invocation of `python -m pytest -q` without `PYTHONPATH=src` produced 17 collection import errors. It was an invocation deviation in the src-layout external environment, not a baseline failure; no file had been edited, and the exact prescribed command passed immediately afterward.

## Required commands

All commands used `/home/bar/.venvs/eeeproject-elevator` and ran from the repository root.

| Command | Result |
|---|---|
| `python --version` | Exit 0; Python 3.13.13. |
| `python -m pip --version` | Exit 0; pip 26.2. |
| `python -m pytest --version` | Exit 0; pytest 9.1.1. |
| `PYTHONPATH=src python -m pytest --collect-only -q` | Exit 0; 871 tests collected in 0.54s. |
| `PYTHONPATH=src python -m pytest tests/end_to_end -v` | Exit 0; 4 passed in 0.12s. |
| `PYTHONPATH=src python -m pytest tests/integration -v` | Exit 0; 192 passed in 0.55s. |
| `PYTHONPATH=src python -m pytest tests/inspection -v` | Exit 0; 8 passed in 0.81s. |
| `PYTHONPATH=src python -m pytest` | Exit 0; 871 passed in 2.68s. |
| `python -m compileall -q src tests` | Exit 0; no output. |
| `PYTHONPATH=src python -c "import elevator_access_sim"` | Exit 0. |
| `PYTHONPATH=src python -c "from elevator_access_sim import Controller, load_startup_files"` | Exit 0. |
| `PYTHONPATH=src python -c "from elevator_access_sim.cli import run"` | Exit 0. |
| standalone standard-library CSV validation | Exit 0; inventory 100, traceability 66, resolution 100, inventory statuses 88 implemented/12 designed. |
| focused result/reason/event/state/floor/vector pytest command | Exit 0; 97 passed in 0.40s. |
| `git diff --check` | Exit 0; no output. |
| `git diff --name-only` | Exit 0; only the two intended tracked modifications are listed; created files are reported by status. |
| `git status --short --untracked-files=all` | Exit 0; intended SP-06.9 files only, with no generated cache artifacts. |

The final suite reports 871 passed, 0 failed, 0 skipped, and 0 xfailed. New files contribute 12 collected cases through nine test functions: four invalid-recovery parameter cases and eight inspection cases.

## Inventory and requirement resolution

Standard-library CSV parsing and `test_sp06_09_resolution_is_complete_concrete_and_status_consistent` verified the exact nine-column resolution schema, original 100-ID order, uniqueness, concrete test/function references, later ownership, execution statuses, and canonical inventory-status consistency.

| Coverage class | Rows |
|---|---:|
| `implemented_existing` | 67 |
| `implemented_sp06_09` | 3 |
| `inspection_existing` | 0 |
| `inspection_sp06_09` | 18 |
| `scheduled_sp06_10` | 5 |
| `scheduled_sp06_11` | 1 |
| `optional_deferred` | 6 |
| `unresolved` | 0 |

The identifier resolver verified 66 requirements (60 required and six optional), 66 traceability rows, 100 inventory rows, nonempty planned test lists, valid range expansion, and no unknown or duplicate ID. Fifty-four required requirements have passing evidence; NFR-006, NFR-007, VER-005, VER-006, and VER-008 are SP-06.10-only; VER-007 is SP-06.11-only; the six optional requirements remain visibly deferred. No traceability correction was necessary.

## Execution matrices

- End-to-end: existing CLI/controller evidence maps LF grant and expiry, HF grant, three denial reasons, hostile busy handling, timeout recovery, manual-reset recovery, and watchdog recovery. The new four-case public flow proves invalid source, invalid frame, parity failure, and invalid floor each leave IDLE/inactive state, append one validation error, and permit a following HF floor-16 grant with sequence continuity.
- Logging faults: the passing 11-case matrix covers invalid source, invalid frame, unknown, disabled, invalid floor, unauthorized, grant, busy, output timeout, manual reset, and watchdog reset append failure. Grant stays inactive; required timeout/reset transitions remain applied; existing activation is preserved where required; failed append consumes no sequence; later success is contiguous. `LOGGING_ERROR` is serialization coverage only when append itself fails; no synthetic post-failure event is fabricated.
- Canonical values: the focused run covered five results, 17 reasons, six event types, and seven states. All members passed their direct serialization/state scenarios.
- Floors and frames: 16 authorization set-bit cases and 16 controller output-bit cases passed, including floor 1/bit 0 and floor 16/bit 15. Six frozen vectors and all 24 canonical single-bit parity corruptions passed; the full suite also covers invalid containers, lengths, members, and LF/HF source separation.
- Timing and replay: just-before/exact/after expiry, one-shot timeout, 3000/2000 and 30000/2000 heartbeat schedules, watchdog/output collision, two suppression epochs, large versus partitioned advances, and normalized JSON Lines replay all passed without wall-clock waits or per-millisecond scheduling.
- Startup/configuration: defaults, strict serialized fields, duration/watchdog endpoints, schema/type/member/malformed JSON failures, strict UTF-8 files, empty credentials, record/duplicate validation, repository infrastructure failure, corrected initialization, and atomic publication all passed.
- CLI: strict files, LF/HF, invalid source/frame/parity/floor, modeled denials, timeout, manual/watchdog reset, deterministic formatting, explicit nulls, exits 0/1/2, handled-error no-traceback behavior, and offline/thin structure map to the passing 192-case integration suite.

## Inspection and cleanup

AST and parsed-file inspections passed for the working title and pending supervisor approval; abstract access-only scope; change control; single owners for event sequence, output snapshot, credential index, and watchdog schedule; no duplicated CLI Wiegand/authorization policy; Python `>=3.11`; empty runtime dependencies; pytest-only test dependency; repository-root discovery; offline/device-free imports; absence of a repository-local virtual environment; UTF-8 authored files; repository-relative canonical CSV paths; proposed/logical/simulated/software-model terminology; and absence of physical adapter modules.

Development checks first exposed pytest 9's reserved `request` parametrization name and then two overly exact document phrase assertions. Both were corrected in test code and the resulting focused evidence passed before inventory promotion. No product defect, design deviation, skip, xfail, network access, hardware dependency, or user interaction was introduced.

Generated `.pytest_cache`, `__pycache__`, `.pyc`, `.pyo`, and coverage artifacts were removed after compilation/testing. Final scope contains no experiment generator, host performance timing, aggregate/scalability result, persistence, database, networking, GUI, hardware, physical reader/output, hardware watchdog, optional profile, or optional authorization implementation. SP-06.10 and SP-06.11 ownership remains explicit. Production source and all other protected content are unchanged. No commit or push occurred.

READY FOR HUMAN REVIEW

