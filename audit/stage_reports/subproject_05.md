# SP-05 Stage Report

## Baseline and authority

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `08e7985f3d01303b9c28066d3693833fa3aa614e` (`Step_4`)
- Starting status: clean
- Baseline: `audit/baselines/subproject_05_baseline.md`

The current commit exactly matched the project-owner-specified baseline. The owner authorizes the SP-03 requirements and SP-04 architecture for this design stage; this is not supervisor approval. Supervisor confirmation remains pending.

## Watchdog timing clarification

The internal heartbeat interval is `max(1, watchdog_timeout_ms // 2)`. `Controller.advance_to` jumps between scheduled logical timestamps rather than iterating per millisecond. At the same timestamp the order is normal unsuppressed heartbeat service, watchdog expiry evaluation, then output expiry. Suppression skips service but not scheduling/time. Watchdog reset wins a fault collision, clears/cancels output expiry, clears transient suppression, and creates exactly one watchdog outcome for the armed deadline.

This resolves the frozen 3000 ms default output versus 2000 ms watchdog: normal heartbeats at 1000 ms keep the watchdog serviced until output timeout at 3000 ms; suppression resets at 2000 ms. Normal output durations through 30000 ms remain stable. No async framework, background thread, wall-clock sleep, physical watchdog, or real waiting is used. DEC-047 explicitly clarifies DEC-033 without rewriting it.

## Package, types, APIs, and ownership

The proposed `src/elevator_access_sim/` package contains `models.py`, `config.py`, `clock.py`, `wiegand.py`, `credentials.py`, `authorization.py`, `outputs.py`, `watchdog.py`, `event_log.py`, `controller.py`, and `cli.py`, plus a curated `__init__.py`. The later experiment runner is `scripts/run_experiments.py`. None was created in SP-05.

Dependencies are acyclic. Immutable enums/dataclasses/snapshots cross boundaries. Credential repository, clock, outputs, watchdog, event log, and controller each own one mutable state category. Enum numbers match the register model and text serialization is lowercase. The raw request permits malformed objects so invalid external values remain typed outcomes.

The public controller operations are initialize, submit, advance-to/by, manual reset, watchdog-service suppression, snapshot, and event retrieval. Busy detection precedes every read of the staged request. Grant append precedes output activation. A no-event advance returns null result/reason without fabricating an event.

## Schemas and outcome policy

Configuration is strict UTF-8 JSON schema version 1 with exactly five required fields: profile, output duration, watchdog timeout, and enabled flag plus version. The credential file is strict UTF-8 JSON schema version 1 with an ordered array of validated records. Unknown/missing/wrong-type/range/version data and duplicate keys are rejected; explicitly invalid values never receive defaults. Empty credentials are valid; publication is all-or-nothing; the required repository is in memory.

Events export as UTF-8 JSON Lines with deterministic practical field order, all nine fields, explicit JSON nulls, lowercase enums, and one object per successful append. The in-memory immutable event list is authoritative. Failed append consumes no sequence.

Expected invalid, denied, granted, timeout, and reset outcomes use typed `Result`/`Reason` values. `ConfigurationError`, `CredentialDataError`, `DuplicateCredentialError`, `ClockError`, `EventLogError`, and `StateInvariantError` derive from `ElevatorAccessSimError` and are reserved for startup data, infrastructure, invariants, or programmer misuse. Controller conversion and no-partial-update rules are explicit; no exception-per-denial hierarchy was designed.

## Test plan and fixed vectors

The pytest plan covers unit, integration, end-to-end, fault, inspection, replay, and scalability work with fresh mutable fixtures and no real wait, network, hardware, database service, or GUI. It covers all seven states and required transitions, all 16 mask bits, every canonical event/result/reason, strict file schemas, logging failure at every policy boundary, both source labels, reset preservation/recovery, and large/small advancement equivalence.

Six fixed `PROJECT_WIEGAND_26` vectors cover minimum, maximum, low, leading-sensitive, credential-sensitive, and demonstration values. An independent standard-library calculation confirmed all six exact 26-bit strings, binary values, both parity equations, and decoded fields. Twenty-four negative variants—leading/trailing parity and leading/trailing data flips for each vector—failed parity as expected. No validation implementation was retained.

## Inventory, traceability, and coverage

`docs/test_case_inventory.csv` contains 100 unique rows, all `designed`, with the exact 13-column header and explicit result/state/event expectations. All 69 unique existing test IDs referenced by the unchanged 66-row requirements traceability file resolve. All 60 required requirement rows remain `planned` with a planned test. The six optional rows remain planned inspection gates and do not block the MVP.

Automated/content checks found designed coverage for all 17 reasons, seven states, 16 floor bits, manual reset from every state, normal/suppressed/collision watchdog paths, one-shot timeout/reset behavior, configuration/repository initialization failures, and all required end-to-end categories. No passing implementation result is claimed.

## Scalability and generated data

The later runner uses credential counts 10, 100, 1000, and 10000; at least `max(1000, credential_count)` deterministic mixed requests; seed/config ID; one warm-up; and three measured repetitions. `time.perf_counter_ns` measures host execution. Aggregates include processed/granted/denied-by-reason/validation counts, average, median, nearest-rank p95, throughput, size, seed, Python version, host, and configuration ID.

Small canonical fixtures/vectors, configuration/seed, aggregates, and environment metadata are retained. Large generated credential/request sets are regenerated. No strict real-time target exists; results apply only to the Python model on the recorded host.

## Implementation sequence

`docs/implementation_sequence.md` divides SP-06 into 11 bounded tasks: foundation/models/config/clock; Wiegand; credentials/authorization; logger; outputs; watchdog; controller; loaders/CLI; integration/fault completion; scalability/export; and documentation/reproducibility. Every task identifies files, prerequisites, tests, requirements, a validation command, completion gate, and prohibited unrelated work.

## Human-review items

Review the package/API layout, raw request and null no-op response, immutable types/enums, exception conversion, strict schemas/label rule, JSON Lines format, heartbeat formula and priority, reset clearing of suppression, logging failure behavior, fixture isolation, fixed vectors, behavioral coverage, experiment workload/mix, generated-data paths, and 11-task sequence. All prior human/supervisor gates remain visible.

## Validation, scope, and deviations

Narrow validation passed for UTF-8 files, module responsibility/dependency/API documentation, enum/dataclass/schema consistency, JSON parsing, watchdog timing and priority, reference vectors/negative forms, CSV structure, trace resolution, reason/state/floor/category coverage, protected hashes, terminology, forbidden paths, and Git whitespace/scope. Details are in `audit/validation/subproject_05_validation.md`.

The independent scheduler validation harness was corrected during validation to handle an empty due queue after reset; it was an inline audit script only and caused no design or repository-code deviation. No frozen requirement, register model, architecture mapping, protected diagram/evidence/literature/bibliography/plan/workflow/prior audit, or Git history changed. The architecture edits are limited to the authorized watchdog clarification and software-design handoff.

No production code, automated test, package metadata, sample runtime configuration, experiment script, data, result, plot, or report chapter was created. No commit or push occurred. There were no scope deviations.

## Exact readiness state

READY FOR HUMAN REVIEW
