# Software Verification and Test Plan

## Purpose and scope

This SP-05 plan defines verification before implementation of the deterministic Python access-authorization model. It covers every required SP-03 requirement and SP-04 state, transition, event, result/reason, output/reset/watchdog policy, module contract, and startup rule. Designed cases are listed in `docs/test_case_inventory.csv`; no passing result is claimed here.

Verification applies only to the proposed software model and its recorded host environment. It cannot establish commercial-controller, physical RFID, electrical-output, elevator, safety, certification, or real-time performance.

## Test environment

- Python 3.11 or later.
- Supported local host with UTF-8 filesystem/text handling.
- No reader, controller board, GPIO, serial device, physical elevator, database server, network service, or GUI.
- A fresh `SimulatedClock` is injected into every time-dependent controller test.
- Host performance measurements use `time.perf_counter_ns`; domain tests never use wall-clock sleep.
- Later records state Python version, platform/host metadata, configuration ID, workload, seed, and interpretation limits.

## Test framework and dependency policy

`pytest` is the required runner. The standard library and pytest are sufficient; no dependency is added during SP-05. Required tests will later run from the repository root with one documented command equivalent to `python -m pytest`. `pytest-cov` is optional: if already available later, an 85% statement-coverage target for core modules may be reported, but coverage tooling may not block or complicate the MVP.

Tests use parametrization and fixtures rather than copied setup. No test may wait in real time, use async/thread scheduling, access the network/hardware, require an external database, or depend on test order.

## Test levels

| Level | Purpose | Principal scope |
|---|---|---|
| unit | one stateless function or owned manager | models, config, clock, Wiegand, credentials, authorization, outputs, watchdog, event log |
| integration | composed manager/controller behavior | processing precedence, state transitions, events, atomic activation, timeout/reset/recovery |
| end-to-end | public controller/CLI-controlled scenarios | LF/HF grants and every required denial/fault/recovery path |
| fault | deterministic injected failure | logging append failure and watchdog-service suppression |
| inspection | non-runtime scope/traceability/design rules | title, boundary, dependencies, files, API contracts, protected claims |
| experiment | reproducible host-software scalability observation | 10/100/1000/10000 credentials and fixed mixed workloads |

## Fixtures and deterministic data

| Fixture | Owner/setup | Isolation rule |
|---|---|---|
| `default_config` | immutable schema v1 config, profile `PROJECT_WIEGAND_26`, 3000/2000 ms, watchdog enabled | reused only because immutable |
| `clock_zero` | new `SimulatedClock(0)` | new instance per test; never shared |
| `event_log` | new normal `EventLog` | new list/sequence per test |
| `failing_event_log` | new logger with append failure enabled | new injection state per test |
| `empty_repository` | valid repository from zero records | immutable record view; new manager where mutation is possible |
| `enabled_repository` | record `(1,100)`, enabled, all floors | new repository per test |
| `disabled_repository` | record `(1,101)`, disabled | new repository per test |
| `all_floor_mask` | integer `0xFFFF` | immutable value |
| `floor_1_mask` / `floor_16_mask` | `0x0001` / `0x8000` | immutable values |
| `idle_controller` | initialized controller with fresh clock/logger/repository | factory fixture returns a new object graph |
| `active_controller` | idle controller granted floor 1 at time zero | no reuse between tests |
| `suppressed_controller` | initialized controller with watchdog service suppression enabled | fresh suppression epoch per test |
| `wiegand_frame_factory` | calls trusted encoder for fixtures and cross-checks fixed vectors | no mutable cache/global state |
| `lf_request` / `hf_request` | immutable canonical requests for `(1,100)`, floor 1 | reused only because immutable |
| `experiment_seed` | fixed integer `260516` | recorded with every generated workload |

Fixture ownership follows the component ownership model. Teardown needs no cleanup beyond ordinary object disposal. Tests that mutate time, output, watchdog, logger fault state, repository manager, or controller must receive fresh objects so no state leaks across cases.

## Wiegand reference vectors

The exact 26-bit strings below were independently calculated during SP-05. Bit 1 makes bits 1–13 even; bit 26 makes bits 14–26 odd. The decoded expectation repeats the input pair.

| Vector ID | Facility | Credential | Exact 26-bit string | Leading parity | Trailing parity | Expected decoded | Example source | Notes |
|---|---:|---:|---|---:|---:|---|---|---|
| WV-001 | 0 | 0 | `00000000000000000000000001` | 0 | 1 | `(0, 0)` | LF | minimum fields; mostly-zero parity boundary |
| WV-002 | 255 | 65535 | `01111111111111111111111111` | 0 | 1 | `(255, 65535)` | HF | maximum fields; mostly-one boundary |
| WV-003 | 1 | 1 | `10000000100000000000000010` | 1 | 0 | `(1, 1)` | LF | low-value credential and both parity values reversed from WV-001 |
| WV-004 | 85 | 4660 | `10101010100010010001101001` | 1 | 1 | `(85, 4660)` | HF | alternating facility makes leading parity sensitive |
| WV-005 | 42 | 43690 | `10010101010101010101010101` | 1 | 1 | `(42, 43690)` | LF | alternating credential makes both data regions sensitive |
| WV-006 | 1 | 100 | `10000000100000000011001000` | 1 | 0 | `(1, 100)` | HF | normal demonstration credential |

For each vector, parameterized negative variants flip exactly one bit from the valid source: bit 1 (`leading_parity_flip`), bit 26 (`trailing_parity_flip`), bit 2 (`leading_data_flip`), and bit 14 (`trailing_data_flip`). A bit 1 or bit 2 flip makes the even leading region odd; a bit 26 or bit 14 flip makes the odd trailing region even. All four return `error/parity_failure`, never decode, and create no activation in controller integration.

The independent validation recalculates strings from field integers without importing production code, checks length/binary/parity, slices fields to decode, and verifies all four negative forms fail the intended region. The temporary script is not retained.

## Credential and authorization tests

Credential unit tests cover an empty but ready repository; known enabled, known disabled, and unknown keys; equal arithmetic sums with distinct ordered tuple keys; deterministic duplicate rejection; invalid/missing/wrong-type/range records; optional label validation; stable record order; and all-or-nothing construction.

Pure authorization tests cover unknown, disabled, floor values 1 and 16, zero/17/negative/non-integer/Boolean floors, unauthorized bits, and exhaustive mapping of floor `f` to bit `f-1` for all 16 floors. Decisions must have canonical pairs: `denied/unknown_credential`, `denied/disabled_credential`, `error/invalid_floor`, `denied/unauthorized_floor`, and `granted/authorized`. No authorization test may observe output/log mutation.

## Output and timing tests

Output-manager tests begin with 16 false channels and no floor/expiry. A grant sets exactly one correct bit, active floor, and `now + duration` atomically. Direct invalid/concurrent manager calls fail as invariant/programmer errors without partial state. Public busy handling returns `denied/controller_busy`, does not inspect deliberately malformed staged values, and preserves the exact output tuple and expiry.

At `expiry-1`, state remains active and no timeout event exists. At expiry, all three output values clear and exactly one `output_timeout/completed/output_expired` event is attempted. Repeated polling creates no duplicate. Durations 100, 3000, and 30000 ms are covered. One large time advance and parameterized smaller steps to the same target must yield the same snapshot and normalized event list.

## Controller state-machine tests

All seven states have designed entry/exit observation:

- startup `RESETTING → INITIALIZING → IDLE`;
- idle request `IDLE → VALIDATING`;
- invalid `VALIDATING → IDLE`;
- decoded `VALIDATING → LOOKUP`;
- unknown/disabled `LOOKUP → IDLE`;
- known enabled `LOOKUP → AUTHORIZING`;
- invalid/unauthorized `AUTHORIZING → IDLE`;
- grant `AUTHORIZING → OUTPUT_ACTIVE`;
- busy remains `OUTPUT_ACTIVE`;
- timeout `OUTPUT_ACTIVE → IDLE`;
- manual/watchdog reset interrupts each state via `RESETTING → IDLE`;
- invalid startup remains `INITIALIZING`, all inactive.

Normal transition tests use public snapshots and event records to observe externally visible state progression. Because intermediate states execute synchronously, manual-reset-from-every-state tests use a focused white-box fixture in the test suite to construct each internally valid controller state before invoking the public reset operation. The helper is test-only: no production state-forcing or transition-observer method, thread, asynchronous task, pause mechanism, reentrant callback, or test hook is added.

## Reset tests

Startup clears all runtime/log state before publication. Manual reset is parameterized from every state and explicitly tested while active. It immediately clears output/active floor/expiry/transients, preserves validated configuration and credentials, preserves prior events and next-sequence progression, attempts one `manual_reset/reset/manual_request`, and returns idle. The canceled timeout never fires later.

Watchdog reset receives the same preservation checks with `watchdog_reset/reset/watchdog_timeout`. Each reset path is followed by a valid request to prove recovery. Reset-event append failure still completes the state transition and reports `error/logging_error` without consuming an event sequence.

## Watchdog and scheduler tests

Heartbeat interval is `max(1, timeout_ms // 2)`. Tests cover enabled/disabled initialization, service, suppression, next heartbeat, deadline motion, and backward-time rejection. Required timing proofs are:

- default normal activation: heartbeats service at logical intervals and output times out at 3000 ms with no watchdog reset;
- default suppression: heartbeat is skipped and exactly one watchdog reset occurs at 2000 ms;
- normal long activation: 30000 ms completes without watchdog reset;
- collision: under suppression a watchdog deadline equal to output expiry yields watchdog reset only, cancels timeout, and logs no output timeout;
- same timestamp: normal heartbeat precedes expiry evaluation, which precedes output expiry;
- partition invariance: large versus small advances yield identical logical state/events;
- idempotence: repeated advance/poll at one timestamp yields no duplicate timeout/reset;
- per-epoch uniqueness: one armed suppressed deadline emits one reset; reset clears suppression, and a later deliberately reinjected fault belongs to a distinct epoch.

These are simulated chronological event tests. They use no loop per millisecond, thread, async task, `sleep`, or physical watchdog.

## Event-log tests

The six event types, five result values, and all 17 reasons have designed coverage. Records always contain nine fields; unavailable source/decoded/floor fields are explicit `None` and JSON `null`. Sequences start at 1 and strictly increase once per successful append; timestamps are nondecreasing under simulated time. Retrieval returns an immutable tuple, JSON Lines is UTF-8 parseable with uppercase `LF`/`HF` source labels, lowercase event/result/reason values, and deterministic field order; no duplicate timeout/reset is emitted.

Injected append failure is tested at grant, denial/validation, busy, timeout, manual reset, and watchdog reset. Grant failure prevents activation. Denial/busy failure leaves output unchanged. Timeout/reset failure never reverses required clearing/recovery. Failure occurs before sequence allocation; after the fault is disabled, the next successful append uses the unconsumed number.

## Configuration and credential-file tests

JSON tests cover valid documented values and programmatic defaults, output endpoints 100/30000, watchdog endpoints 1/4294967295, invalid duration/timeout values and Boolean-as-integer traps, unknown/missing fields, wrong top-level/field types, unsupported version/profile, malformed JSON, duplicate JSON members, invalid UTF-8 adapter input, valid empty credentials, invalid records/labels, duplicate keys, and deterministic order.

For every failure, no partially parsed `SimulatorConfig`, credential tuple, repository, or initialized controller becomes visible. Explicit invalid/missing values never trigger fallback defaults. Both example objects in `docs/software_design.md` must parse with Python's standard `json` library.

## End-to-end scenarios

Public-controller scenarios include successful LF and HF grants; unauthorized, disabled, and unknown denial; all frame-validation failures; invalid input followed by a valid recovery; active output followed by a deliberately malformed busy request; timeout followed by a later grant; manual reset followed by a later grant; and watchdog reset followed by a later grant. Each asserts canonical response, final state, 16-channel invariant, exact event delta, source metadata where available, and preservation rules.

## Fault-injection tests

The only required injected infrastructure faults are event append failure and watchdog-service suppression. Cases assert that fault state is explicit, deterministic, reset-isolated, and reversible. Invalid data drives ordinary validation paths rather than a private bypass. A fault test records pre-state, injection action, expected response, output effect, event effect, post-state, and recovery action.

## Deterministic replay tests

For a fixed configuration, credential order, request list, seed, initial time, advancement partition, and fault schedule, two fresh controller graphs must produce identical responses, snapshots, and normalized JSON Lines. Host timing fields are excluded. A separate partition test proves that logically equivalent large/small time advancement yields identical normalized results.

## Scalability experiments

Required credential counts are 10, 100, 1000, and 10000. Seed `260516` (or another explicitly versioned seed recorded by the runner) deterministically generates credentials and at least `max(1000, credential_count)` requests at each size. Each workload contains grants, unauthorized floors, disabled credentials, and unknown credentials under one documented mix; validation-failure count remains a required metric and may be zero only if the frozen workload configuration explicitly selects zero malformed cases.

Each size has one unmeasured warm-up and three measured repetitions. `time.perf_counter_ns()` brackets host processing; simulated time is never a performance timer. Each repetition records processed count, grants, denials by reason, validation failures, average/median/nearest-rank p95 nanoseconds, throughput cases/second, credential count, seed, Python version, host environment, and configuration identifier. Nearest-rank p95 sorts `n` samples and selects one-based rank `ceil(0.95*n)`.

Later storage retains the small generator configuration, seed, workload mix/configuration identifier, aggregate records, and environment metadata. Large generated credential/request sets are regenerated and are not committed. Only small canonical fixtures and the fixed Wiegand vectors are permanent. No strict real-time threshold exists; results describe only the Python model on the recorded host.

## Result recording

Automated test reports retain test ID, controlled input/configuration, expected result/state/events, actual result/state/events, and pass/fail evaluation. Experiment aggregate rows retain repetition and all frozen metrics. Counts must reconcile:

`processed = granted + sum(denied_by_reason) + validation_failures + other_explicit_error_outcomes`.

Machine-readable export is CSV or JSON with UTF-8, repository-relative paths, schema/config identifiers, and no large embedded generated datasets. SP-05 records only designed expectations, never actual/pass results.

## Coverage expectations

Mandatory behavioral coverage is 100% of the 60 required requirements; every canonical denial/error reason; every public API positive and negative boundary; all seven state entries/exits and required transitions; all 16 mask bits; all manual/watchdog/reset/logging policies; all external-input boundaries; both LF/HF labels; deterministic replay; and the four scalability sizes. All 69 pre-existing planned test IDs resolve in the inventory. Optional tests remain designed/deferred where their feature is not implemented.

Source percentage is secondary. Later optional `pytest-cov` reporting may target at least 85% statement coverage for core modules if available, without adding a blocking dependency or encouraging tests of incidental lines instead of behavior.

## Entry and exit criteria

SP-06 task entry requires human review of APIs/types/schemas/priority, exact fixed vectors, complete resolvable inventory, no major undefined behavior, and an unchanged frozen baseline. Each implementation task exits only when its scoped tests pass, its requirements are traceable, no earlier tests regress, validation commands are recorded, and prohibited unrelated work is absent.

The full verification stage exits only when every required test has an actual result, expected/actual/evaluation records are preserved, one documented pytest command passes in a clean supported environment, experiment results reconcile, and limitations are stated. Test design alone does not meet those later criteria.

## Deferred optional testing

Additional Wiegand profiles, administrative/time-based authorization, persistent local storage, GUI/enhanced CLI, physical adapters, and extra experiment sizes remain optional. Their inventory inspection entries preserve traceability but cannot fail or delay the required MVP until a separate scope decision authorizes implementation. Database-server, network, physical, and commercial-equivalence tests remain prohibited.

## Interpretation limitations

Passing later software tests would demonstrate conformance of one Python implementation to this proposed model under controlled inputs. It would not demonstrate real-reader compatibility, commercial-card behavior, electrical correctness, elevator response, safety, certification, reliability in service, or a real-time guarantee. Host timing is observational and comparable only with its recorded workload/environment.
