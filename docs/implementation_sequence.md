# SP-06 Bounded Implementation Sequence

## Use and controls

These 11 tasks implement the reviewed SP-05 design incrementally. Each is sized for one focused Codex prompt and must begin from the accepted preceding commit, inspect local instructions/status, preserve user changes, implement only its listed scope, run its validation, and produce no pass claim without execution evidence. Frozen requirements, register semantics, enumerations, schemas, scheduler priority, safety boundary, and protected evidence may not be altered inside an implementation task.

## Task 1 — Package foundation, models, configuration, and clock

- **Objective:** Establish Python 3.11 package/test metadata, shared enums/immutable records/exceptions, strict configuration value validation, and simulated monotonic clock.
- **Files expected:** `pyproject.toml` and/or minimal dependency metadata selected at task start; `src/elevator_access_sim/__init__.py`, `models.py`, `config.py`, `clock.py`; focused tests and small inline JSON fixtures only.
- **Prerequisites:** Human-reviewed `docs/software_design.md`; clean accepted SP-05 commit; no conflicting package metadata.
- **Tests written:** enum names/numbers/text mapping; immutable records and 16-channel invariant; valid/default/invalid config values; monotonic now/advance-by/advance-to/backward rejection.
- **Requirements covered:** DAT-003–DAT-007, TIM-001–TIM-003, NFR-004, NFR-008–NFR-009.
- **Validation command:** `python -m pytest <task-1 test paths>` plus `python -m compileall src` and `git diff --check`.
- **Completion gate:** Fresh install/import works on Python 3.11+, scoped tests pass, no external runtime dependency exists, and enum/register checks match SP-04.
- **Prohibited unrelated work:** Wiegand behavior, repository/authorization, output, watchdog scheduling, controller, CLI, experiments, docs redesign.

## Task 2 — Wiegand profile and reference-vector tests

- **Objective:** Implement stateless `PROJECT_WIEGAND_26` validation, parity, decode, and trusted encode helper.
- **Files expected:** `src/elevator_access_sim/wiegand.py`; Wiegand test module and the six small canonical vectors.
- **Prerequisites:** Task 1 models/exceptions; verified SP-05 vector table.
- **Tests written:** six fixed vectors, field boundaries, length 0/25/27/concatenated, invalid container/value, leading/trailing parity flips, leading/trailing data flips, round trip, LF/HF separation at integration boundary.
- **Requirements covered:** FUN-001–FUN-006, DAT-001–DAT-003, VER-002, VER-004.
- **Validation command:** `python -m pytest <Wiegand test paths>` plus full existing suite and `git diff --check`.
- **Completion gate:** Fixed vectors independently match the document, all malformed cases return typed outcomes, and module has no credential/floor/controller dependency.
- **Prohibited unrelated work:** alternate profiles, pulse timing, physical reader support, credential lookup, output behavior.

## Task 3 — Credential repository and authorization

- **Objective:** Implement atomic validated in-memory repository construction, ordered-key lookup, stable observation, and pure authorization.
- **Files expected:** `src/elevator_access_sim/credentials.py`, `authorization.py`; focused repository/authorization tests.
- **Prerequisites:** Tasks 1–2 types and decoded value contracts.
- **Tests written:** empty/known/unknown/disabled, invalid records/labels/ranges/types, duplicates with no partial publication, colliding arithmetic sums, stable order/size, floor boundaries/types, all 16 mask bits, unauthorized/authorized outcomes.
- **Requirements covered:** FUN-007–FUN-010, DAT-004–DAT-006, NFR-002, NFR-009, VER-002.
- **Validation command:** `python -m pytest <credential and authorization test paths>` plus full suite and `git diff --check`.
- **Completion gate:** No silent replacement, every normal decision is typed, exhaustive mask mapping passes, and authorization has no output/log mutation.
- **Prohibited unrelated work:** persistence/database server, administrator/time rules, controller/output implementation.

## Task 4 — Event logger and failure injection

- **Objective:** Implement nine-field immutable events, sequence ownership, explicit-null JSON Lines export, and pre-allocation append-failure injection.
- **Files expected:** `src/elevator_access_sim/event_log.py`; event-log/schema/fault tests.
- **Prerequisites:** Task 1 enum/record contracts.
- **Tests written:** append/retrieval immutability, all enum serialization, explicit nulls, deterministic field order, UTF-8 JSONL parse, monotonic sequences/timestamps, failed append consumes no number, startup clear/runtime-preserve primitives.
- **Requirements covered:** LOG-001–LOG-003, NFR-007–NFR-009, VER-003, VER-007.
- **Validation command:** `python -m pytest <event-log test paths>` plus full suite and `git diff --check`.
- **Completion gate:** Every successful append maps one-to-one to one record/line, injected failure is atomic, and no persistence/network feature is added.
- **Prohibited unrelated work:** controller-specific rollback, redundant/persistent logging, output/watchdog behavior.

## Task 5 — Output manager and simulated timeout

- **Objective:** Implement the sole owner of exactly 16 channels, active floor, and expiry with atomic activation/timeout/reset.
- **Files expected:** `src/elevator_access_sim/outputs.py`; focused output/timing tests.
- **Prerequisites:** Task 1 snapshots/exceptions/clock; frozen floor mapping/duration rules.
- **Tests written:** initial shape, floors 1/16 and all bits as applicable, one active bit, invalid/concurrent internal activation, exact expiry, before-expiry, one-shot timeout, reset, immutable snapshots.
- **Requirements covered:** SCP-004, FUN-011–FUN-015, DAT-006–DAT-007, TIM-001–TIM-002, RST-001–RST-002.
- **Validation command:** `python -m pytest <output test paths>` plus full suite and `git diff --check`.
- **Completion gate:** Output tuple/floor/expiry always change together, timeout is idempotent, and no real waiting exists.
- **Prohibited unrelated work:** busy orchestration, logging policy, watchdog, physical/relay output adapters.

## Task 6 — Watchdog heartbeat, suppression, and expiry

- **Objective:** Implement enabled state, `max(1, timeout // 2)` heartbeat, service/suppression, deadline, one expiry request per armed epoch, and reinitialization.
- **Files expected:** `src/elevator_access_sim/watchdog.py`; watchdog unit tests.
- **Prerequisites:** Task 1 clock/models; reviewed SP-05 scheduler contract.
- **Tests written:** default and boundary timeout, enabled/disabled, heartbeat service, suppressed skip without time stop, same-time heartbeat-before-expiry primitive behavior, exactly one request per epoch, rearm, long normal schedules.
- **Requirements covered:** TIM-002–TIM-003, RST-004, NFR-001, VER-003.
- **Validation command:** `python -m pytest <watchdog test paths>` plus full suite and `git diff --check`.
- **Completion gate:** 3000/2000 and 30000/2000 schedules are provable without a thread/sleep; watchdog never mutates controller/output directly.
- **Prohibited unrelated work:** controller reset, wall-clock timer, async/thread, MCU-specific behavior.

## Task 7 — Controller coordination and state transitions

- **Objective:** Compose managers into the seven-state controller with busy precedence, grant-log gate, chronological scheduler priority, reset, snapshots, and typed responses.
- **Files expected:** `src/elevator_access_sim/controller.py`; controller/state/timing/atomicity tests.
- **Prerequisites:** Tasks 1–6 complete and passing.
- **Tests written:** every state/transition; full processing order; every denial/error; busy not inspected/no extension; grant append failure; 3000 ms normal/no watchdog; suppression reset at 2000; 30000 ms normal; collision priority; large/small equivalence; no duplicate timeout/reset; reset from all states; preservation/recovery.
- **Requirements covered:** SCP-002–SCP-005, FUN-001–FUN-015, TIM-001–TIM-003, LOG-001–LOG-003, RST-001–RST-004, NFR-001–NFR-003, NFR-009, VER-002–VER-004.
- **Validation command:** `python -m pytest <controller/integration test paths>` plus full suite, `python -m compileall src`, and `git diff --check`.
- **Completion gate:** Every required state/event/atomicity invariant passes through public APIs; normal/fault timing proofs agree; no design rule is invented.
- **Prohibited unrelated work:** CLI, files beyond approved loaders, experiments, optional profiles/features, API redesign without review.

## Task 8 — JSON loaders and simple CLI demonstration

- **Objective:** Complete strict UTF-8 JSON text/file adapters and a thin offline CLI for controlled request/time/reset/watchdog demonstrations.
- **Files expected:** narrow additions to `config.py`; `src/elevator_access_sim/cli.py`; CLI entry metadata if reviewed; small sample input only if separately authorized; loader/CLI tests.
- **Prerequisites:** Tasks 1–7; reviewed JSON and CLI contracts.
- **Tests written:** exact examples, unknown/missing/malformed/version/profile/type/range/duplicate JSON cases, all-or-nothing startup, LF/HF command, time advance, reset/fault demo, formatting, exit statuses, offline/no-device behavior.
- **Requirements covered:** DAT-004–DAT-005, TIM-001–TIM-003, NFR-003–NFR-005, NFR-007–NFR-009.
- **Validation command:** `python -m pytest <config/CLI test paths>` plus full suite, one documented CLI smoke invocation using temporary data, and `git diff --check`.
- **Completion gate:** CLI delegates all behavior, invalid explicit input never defaults, no external service/device is touched, and examples are reproducible.
- **Prohibited unrelated work:** GUI, network/database, persistent credential mutation, domain-rule duplication, physical adapter.

## Task 9 — Integration and fault test completion

- **Objective:** Close the complete inventory for required end-to-end, recovery, log-failure, deterministic replay, traceability, and state coverage.
- **Files expected:** integration/end-to-end/fault test modules and only narrowly necessary implementation fixes.
- **Prerequisites:** Tasks 1–8; inventory-to-test naming convention agreed.
- **Tests written:** every still-designed required inventory row, all six event types/five results/17 reasons, logger failure at grant/denial/busy/timeout/resets, LF/HF, invalid-then-valid, timeout/reset-then-grant, replay, environment isolation.
- **Requirements covered:** all 60 required requirements, especially VER-001–VER-004, VER-007, LIM-001–LIM-004.
- **Validation command:** single clean `python -m pytest`; automated inventory/traceability resolver; `git diff --check`.
- **Completion gate:** Every required inventory ID maps to an implemented test or explicit inspection, one documented pytest command passes, and no required behavior is skipped/xfail.
- **Prohibited unrelated work:** optional features, broad refactor, experiment optimization, claim changes.

## Task 10 — Scalability runner and result export

- **Objective:** Implement deterministic workload generation, warm-up/three repetitions, host timing aggregation, validation, and machine-readable export for four sizes.
- **Files expected:** `scripts/run_experiments.py`; small experiment-schema/workload tests; later generated aggregate/environment output paths defined by project convention.
- **Prerequisites:** Tasks 1–9 passing; reviewed workload mix/config ID and storage paths.
- **Tests written:** deterministic seed regeneration, 10/100/1000/10000 sizes, at least `max(1000,n)` cases, required outcome mix, count reconciliation, average/median/nearest-rank p95/throughput, schema/environment/config fields, no storage of large inputs.
- **Requirements covered:** NFR-006–NFR-008, VER-005–VER-008, LIM-004.
- **Validation command:** unit-test runner tests; a bounded smoke experiment; schema/count validation; full pytest; `git diff --check`.
- **Completion gate:** Runner can reproduce all four aggregate records from seed/config, metrics reconcile, environment/limits are recorded, and large generated sets are absent from Git.
- **Prohibited unrelated work:** performance optimization, strict latency target, extra sizes replacing required sizes, product/hardware interpretation.

## Task 11 — Documentation and reproducibility check

- **Objective:** Reconcile implementation, commands, test/experiment evidence, README/reproducibility instructions, and traceability without changing behavior.
- **Files expected:** narrow updates to canonical design/test/traceability/README/audit/reproducibility records; no duplicate manuals.
- **Prerequisites:** Tasks 1–10 implemented and evidence available.
- **Tests written:** documentation command smoke tests, clean-environment setup/run check, artifact schema/path/UTF-8 checks, protected-claim scan, inventory/requirements reconciliation.
- **Requirements covered:** SCP-001–SCP-007, NFR-004–NFR-008, VER-001, VER-007–VER-008, LIM-001–LIM-004.
- **Validation command:** documented clean setup, single pytest command, required experiments/result validation, link/path/CSV/JSON checks, `git diff --check`, and final `git status --short` review.
- **Completion gate:** A new reviewer can reproduce tests and aggregate experiments from repository-relative instructions; actual results are distinguished from expectations; all limitations and human approvals remain visible.
- **Prohibited unrelated work:** behavioral refactor, new feature, broad literature/report rewrite, physical/commercial claim, release/commit/push unless separately authorized.
