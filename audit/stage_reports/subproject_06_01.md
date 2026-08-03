# SP-06.1 Stage Report

## Baseline and toolchain

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `7a0b173724038aeac9f25f783a52a586a83619bf` (`Step_5`)
- Starting status: clean
- Python: `3.13.13`
- Pytest: unavailable (`/home/bar/miniforge3/bin/python: No module named pytest`)
- Baseline: `audit/baselines/subproject_06_01_baseline.md`

The commit and branch exactly matched the accepted task baseline. No package metadata, Python source, `src/`, or `tests/` path existed. Python satisfies the 3.11 minimum. Pytest was also absent from the available `python3` and `/usr/bin/python3` interpreters, and no pytest executable was present. Per task restrictions, no package was installed and no network was accessed.

## Mandatory specification corrections

`ReaderSource.LF/HF` now serialize as uppercase `LF`/`HF`, preserving numeric values 1/2. Controller state, event type, result, and reason serialize as lowercase. The software-design event example now uses `"reader_source":"LF"`; source expectations in the test plan/inventory are uppercase. DEC-059 records conformance to the already frozen requirements/register labels without changing semantics.

The undefined transition-observer/pause concept was removed. Later normal controller tests use public snapshots/events. Reset-from-every-state tests may construct internally valid states through a focused test-suite-only white-box fixture before invoking public reset. No production observer, state-forcing method, pause, reentrant callback, thread, or async task was added. Inventory entries TST-RST-005 and TST-STA-001 were updated accordingly.

## Package metadata and implementation

`pyproject.toml` uses setuptools with package discovery under `src`, project `elevator-access-sim` version `0.1.0`, Python `>=3.11`, zero runtime dependencies, optional pytest test dependency, and tests under `tests/`. No build, release, lockfile, environment, coverage, lint, format, type, or documentation tool was added.

Created only:

- `src/elevator_access_sim/__init__.py`;
- `src/elevator_access_sim/models.py`;
- `src/elevator_access_sim/config.py`;
- `src/elevator_access_sim/clock.py`.

The package root explicitly exports the five fixed enums, all 15 shared immutable record types, seven-class exception hierarchy, configuration API, clock protocol, and simulated clock through `__all__`.

## Models and enums

All register-aligned enum names/numbers are implemented. An explicit `to_text()` method returns uppercase source names and lowercase text for other enums; `str(enum)` is not the serialization contract. Zero remains absent from source/event/result/reason enums, while `ControllerState.RESETTING` retains its frozen value zero.

All reviewed records are frozen, slotted dataclasses. `CredentialRequest` accepts raw malformed objects without constructor validation. Credential records intentionally defer full validation to Task 3. Output/controller snapshots reject non-tuples, lengths other than 16, non-Boolean members, multiple active outputs, floor/bit mismatch, invalid floor/expiry, and Boolean-as-integer traps through `StateInvariantError`.

## Configuration

`default_config()` returns schema 1, `PROJECT_WIEGAND_26`, 3000 ms output duration, 2000 ms watchdog timeout, and enabled watchdog. `load_config_json()` accepts only a string containing exactly the five required fields. It rejects duplicate/unknown/missing fields, unsupported version/profile, wrong types, Boolean integers, out-of-range values, malformed/non-object JSON, and NaN/Infinity without coercion or fallback. Parsing has no mutable target and returns a new immutable config only after complete validation.

Credential JSON and combined startup loading are intentionally absent and deferred to Task 3.

## Simulated clock

`Clock` exposes only `now_ms()`. `SimulatedClock` accepts nonnegative exact integer time, permits zero/equal/forward advancement, rejects negative/backward/Boolean/non-integer operations before mutation, and owns only its current logical millisecond. It imports no wall-clock, sleep, thread, async, callback, or scheduler facility.

## Tests and requirements addressed

Created focused `test_models.py`, `test_config.py`, and `test_clock.py`. They cover enum/register behavior, uppercase/lowercase serialization, immutability, composite keys, raw request policy, snapshot invariants, exact configuration/defaults/endpoints/negative cases/atomicity, clock monotonicity/failure atomicity, and prohibited clock dependencies. Test names reference existing IDs where practical, including TST-SRC-001, TST-CRD-001, TST-OUT-004, TST-CFG-001–003/005, TST-TIM-002, and TST-TIM-003.

The implementation addresses the bounded foundation portions of DAT-003–DAT-007, TIM-001–TIM-003, NFR-001, NFR-004, NFR-008, and NFR-009. Inventory statuses remain `designed`; execution evidence belongs only in validation.

## Validation and blocker

Both source and tests compile, the package imports, `pyproject.toml` parses, no runtime dependency exists, and independent standard-library checks passed for enum values/serialization, dataclass immutability, snapshot invariants, strict configuration cases, and clock monotonicity/unchanged state after rejection. A temporary standard-library harness also directly exercised all 114 parameter-expanded test cases successfully, but it is explicitly not pytest and is not treated as the required test result.

The exact required pytest command could not start collection:

```text
/home/bar/miniforge3/bin/python: No module named pytest
```

Therefore there is no pytest pass/fail summary and no test-success claim. The implementation cannot satisfy SP-06.1's completion gate until pytest is made available by the project owner/environment and the scoped command passes. Details are in `audit/validation/subproject_06_01_validation.md`.

## Deferred work and scope

Task 2 retains all Wiegand work. Task 3 retains credential JSON loading, repository, and authorization. Event logging, outputs, watchdog, controller, CLI, and experiments remain in later tasks. No physical/network/database/GUI/async/thread behavior was added. Protected requirements, register model, architecture/mapping/diagrams, evidence, literature/PDFs, bibliography, plan/workflow, implementation sequence, and prior audit records remained unchanged.

No commit or push occurred. There were no scope deviations other than the environment blocker already required by the task's pytest policy.

## Exact readiness state

BLOCKED BEFORE NEXT STAGE — pytest is unavailable in the active Python environment
