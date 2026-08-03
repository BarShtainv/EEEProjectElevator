# Python Software Model Design

## Status and scope

This SP-05 document freezes the proposed software contracts for the project-owner-approved abstract access-authorization model. It is a design for later Python 3.11+ implementation, not executable code and not evidence of commercial-controller behavior. Supervisor approval remains pending.

The model begins with complete logical requests and validated startup data. It ends at 16 abstract Boolean permission outputs, typed responses, and structured events. It does not model RF physics, reader electronics, pulse acquisition, electrical outputs, elevator wiring or motion, passenger-safety logic, certification, installation, or product equivalence.

The SP-03 requirements and SP-04 ownership, state, register, reset, event, failure, and busy-precedence rules remain frozen. SP-05 resolves only the internal logical heartbeat schedule required for deterministic watchdog behavior.

## Package layout

The later implementation will use this package; none of these paths is created in SP-05:

```text
src/elevator_access_sim/
├── __init__.py       # curated public re-exports only
├── models.py         # enums, immutable records, base exceptions
├── config.py         # atomic JSON configuration/credential loading
├── clock.py          # monotonic simulated integer-millisecond clock
├── wiegand.py        # stateless PROJECT_WIEGAND_26 validation/codec
├── credentials.py    # validated in-memory credential repository
├── authorization.py  # pure authorization decision
├── outputs.py        # sole output/active-floor/expiry owner
├── watchdog.py       # heartbeat/deadline/suppression state
├── event_log.py      # event sequence and in-memory records
├── controller.py     # state machine, precedence, scheduling, reset
└── cli.py            # thin demonstration adapter
```

The later experiment entry point is `scripts/run_experiments.py`; it is not part of the domain package and is not created in this stage.

Dependency direction is acyclic: `models` is the base; stateless/domain managers depend only on `models`; `config` depends on `models`; `controller` composes all managers; `cli` depends on `config` and `controller`. Managers never import `controller` or `cli`.

## Design principles

- Python 3.11+, standard library, and `pytest` are the required platform.
- Immutable dataclasses, enums, tuples, mappings, and protocols express boundaries.
- One manager owns each mutable category; snapshots are immutable copies.
- Expected external-input outcomes are returned as typed values.
- Exceptions are limited to startup data, infrastructure, invariant, and programmer-use failures.
- No global mutable state, network, database server, physical adapter, GUI, async framework, background thread, wall-clock sleep, or real-time test wait is used.
- A method either commits its whole logical update or leaves owned state unchanged.
- Text enum serialization is canonical lowercase; integer enum values match the logical register model.

## Shared types and enumerations

`models.py` will use integer-valued enums whose members serialize through an explicit lowercase value map, never through `str(enum)`.

| Enum | Members and fixed numeric values | Canonical text |
|---|---|---|
| `ReaderSource` | `LF = 1`, `HF = 2` | `lf`, `hf` |
| `ControllerState` | `RESETTING = 0`, `INITIALIZING = 1`, `IDLE = 2`, `VALIDATING = 3`, `LOOKUP = 4`, `AUTHORIZING = 5`, `OUTPUT_ACTIVE = 6` | lowercase member name |
| `EventType` | `ACCESS_DECISION = 1`, `VALIDATION_ERROR = 2`, `OUTPUT_TIMEOUT = 3`, `MANUAL_RESET = 4`, `WATCHDOG_RESET = 5`, `LOGGING_ERROR = 6` | lowercase member name |
| `Result` | `GRANTED = 1`, `DENIED = 2`, `ERROR = 3`, `COMPLETED = 4`, `RESET = 5` | lowercase member name |
| `Reason` | `AUTHORIZED = 1`, `UNKNOWN_CREDENTIAL = 2`, `DISABLED_CREDENTIAL = 3`, `UNAUTHORIZED_FLOOR = 4`, `INVALID_SOURCE = 5`, `INVALID_FRAME = 6`, `PARITY_FAILURE = 7`, `INVALID_FLOOR = 8`, `CONTROLLER_BUSY = 9`, `OUTPUT_EXPIRED = 10`, `MANUAL_REQUEST = 11`, `WATCHDOG_TIMEOUT = 12`, `INVALID_CONFIGURATION = 13`, `INVALID_CREDENTIAL_RECORD = 14`, `DUPLICATE_CREDENTIAL = 15`, `REPOSITORY_INITIALIZATION_FAILURE = 16`, `LOGGING_ERROR = 17` | lowercase member name |

Zero remains the logical register representation of null/not supplied; it is not a Python enum member.

The following records are frozen as `@dataclass(frozen=True, slots=True)` values. `object` on the raw request boundary is intentional: malformed source, frame, and floor values are normal validation cases, not constructor exceptions.

```python
CredentialRequest(
    reader_source: object,
    frame: object,
    requested_floor: object,
)

DecodedCredential(
    facility_code: int,
    credential_number: int,
)

CredentialKey(
    facility_code: int,
    credential_number: int,
)

CredentialRecord(
    facility_code: int,
    credential_number: int,
    enabled: bool,
    floor_mask: int,
    label: str | None = None,
)

AuthorizationDecision(
    result: Result,
    reason: Reason,
    decoded_credential: DecodedCredential | None = None,
    selected_record: CredentialRecord | None = None,
    selected_floor: int | None = None,
)

EventDraft(
    timestamp_ms: int,
    event_type: EventType,
    reader_source: ReaderSource | None,
    facility_code: int | None,
    credential_number: int | None,
    requested_floor: int | None,
    result: Result,
    reason: Reason,
)

EventRecord(
    sequence_number: int,
    timestamp_ms: int,
    event_type: EventType,
    reader_source: ReaderSource | None,
    facility_code: int | None,
    credential_number: int | None,
    requested_floor: int | None,
    result: Result,
    reason: Reason,
)

SimulatorConfig(
    schema_version: int,
    profile: str,
    output_duration_ms: int,
    watchdog_timeout_ms: int,
    watchdog_enabled: bool,
)

OutputSnapshot(
    channels: tuple[bool, ...],
    active_floor: int | None,
    expiry_ms: int | None,
)

ControllerResponse(
    result: Result | None,
    reason: Reason | None,
    state: ControllerState,
    latest_event_sequence: int | None,
    output_snapshot: OutputSnapshot,
    logging_fault: bool,
)

ControllerSnapshot(
    state: ControllerState,
    output_channels: tuple[bool, ...],
    active_floor: int | None,
    output_expiry_ms: int | None,
    watchdog_deadline_ms: int | None,
    initialized: bool,
    configuration_valid: bool,
    repository_ready: bool,
    latest_event_sequence: int | None,
)
```

`CredentialKey` is the ordered pair, with ordinary structural equality and hashing; it is never formed by arithmetic addition. `OutputSnapshot.channels` and `ControllerSnapshot.output_channels` are validated to contain exactly 16 actual `bool` values. Zero or one channel may be true; `active_floor` and `expiry_ms` are both `None` exactly when all are false.

Auxiliary immutable values make expected intermediate outcomes explicit:

```python
FrameValidation(ok: bool, reason: Reason | None, decoded: DecodedCredential | None)
RepositoryLookup(record: CredentialRecord | None)
LogAppendOutcome(record: EventRecord | None, logging_fault: bool)
StartupData(config: SimulatorConfig, credentials: tuple[CredentialRecord, ...])
```

Mutable classes—`SimulatedClock`, `CredentialRepository`, `OutputManager`, `Watchdog`, `EventLog`, and `Controller`—own only the state assigned below. They never expose a mutable collection.

## Domain-result and exception policy

Normal typed outcomes include invalid source/frame/parity/floor, unknown/disabled credential, unauthorized floor, busy, grant, output completion, manual reset, and watchdog reset. These use `Result` and `Reason`; callers do not catch exceptions to branch on access decisions.

```text
ElevatorAccessSimError
├── ConfigurationError
├── CredentialDataError
│   └── DuplicateCredentialError
├── ClockError
├── EventLogError
└── StateInvariantError
```

| Exception | May originate in | Meaning and controller treatment |
|---|---|---|
| `ConfigurationError` | `config` | Malformed JSON, wrong schema/type/range, unknown/missing field, or unsupported profile/version. Startup remains atomic and non-operational; the adapter reports `error/invalid_configuration`. |
| `CredentialDataError` | `config`, `credentials`, trusted Wiegand encoder | Invalid credential file/record or programmer misuse of fixture encoding. Startup remains unchanged; controller/adapter reports `error/invalid_credential_record` for startup data. |
| `DuplicateCredentialError` | `config`, `credentials` | Duplicate ordered key. No repository is published; report `error/duplicate_credential`. |
| `ClockError` | `clock`, `controller.advance_to` | Backward/negative advancement. This is API misuse and propagates so the calling test fails; controller state is unchanged. |
| `EventLogError` | `event_log` infrastructure injection | Append failed before sequence allocation. Controller converts it to `error/logging_error` and applies the frozen grant/denial/timeout/reset policy. Unexpected retrieval/serialization corruption propagates. |
| `StateInvariantError` | `outputs`, `watchdog`, `event_log`, `controller` | Impossible internal state or invalid manager call after validation. It is a programming defect, is not converted to a denial, and must fail the test. |

Validation is completed before mutation. Candidate configuration, records, events, output snapshots, and deadlines are constructed in locals; owned state is swapped only after all checks succeed. Event append allocates the next number only after its injected failure point and record validation pass.

## Configuration schema

Configuration uses one UTF-8 JSON object:

```json
{
  "schema_version": 1,
  "profile": "PROJECT_WIEGAND_26",
  "output_duration_ms": 3000,
  "watchdog_timeout_ms": 2000,
  "watchdog_enabled": true
}
```

| Field | JSON type | Rule |
|---|---|---|
| `schema_version` | number interpreted as exact integer | required; exactly `1`; Boolean is rejected |
| `profile` | string | required; exactly `PROJECT_WIEGAND_26` |
| `output_duration_ms` | exact integer | required; 100–30000 inclusive; Boolean is rejected |
| `watchdog_timeout_ms` | exact integer | required; 1–4294967295 inclusive; default design value 2000; Boolean is rejected |
| `watchdog_enabled` | Boolean | required; no integer/string coercion |

All five serialized fields are required. Unknown fields and missing fields are rejected. The documented defaults belong to `default_config()` and example generation; a missing or explicitly invalid JSON value is never replaced with a default. Top-level arrays/scalars, duplicate JSON member names, malformed JSON, non-UTF-8 input, and non-finite/non-integer numbers are rejected. Loading produces one immutable `SimulatorConfig` only after every field validates.

## Credential schema

Credentials use a separate UTF-8 JSON object:

```json
{
  "schema_version": 1,
  "credentials": [
    {
      "facility_code": 1,
      "credential_number": 100,
      "enabled": true,
      "floor_mask": 65535,
      "label": "demo-user"
    }
  ]
}
```

The top-level object permits exactly `schema_version` and `credentials`; both are required. Version is exact integer `1`; `credentials` is an array. Each record permits exactly the four required fields `facility_code`, `credential_number`, `enabled`, `floor_mask` and optional `label`.

- `facility_code`: exact integer 0–255, not Boolean.
- `credential_number`: exact integer 0–65535, not Boolean.
- `enabled`: actual JSON Boolean.
- `floor_mask`: exact integer 0–65535, not Boolean.
- `label`: omitted or a non-empty UTF-8 string after validation; JSON null, empty/whitespace-only strings, and non-strings are rejected.
- Composite keys must be unique; silent replacement is prohibited.
- Empty `credentials` is valid and creates a ready repository in which every lookup is unknown.
- Input array order is retained for read-only iteration and reproducible experiments; lookup semantics do not depend on order.

Parsing and validation are all-or-nothing. No record is published until every record, label, unknown-field rule, and duplicate check passes. The required repository is in memory; a database server and persistence are outside the MVP.

## Event schema and serialization

The in-memory tuple of immutable `EventRecord` values is the source of truth. Preferred export is UTF-8 JSON Lines, one successful append per line, with fields in this deterministic order:

```json
{"sequence_number":1,"timestamp_ms":0,"event_type":"access_decision","reader_source":"lf","facility_code":1,"credential_number":100,"requested_floor":1,"result":"granted","reason":"authorized"}
```

Every object always has the nine fields `sequence_number`, `timestamp_ms`, `event_type`, `reader_source`, `facility_code`, `credential_number`, `requested_floor`, `result`, and `reason`. Conditional values serialize as JSON `null`, never omission. Enums serialize to canonical lowercase strings. Sequence begins at 1, increments once per successful append, and is strictly increasing. Timestamps are nonnegative simulated milliseconds and nondecreasing. A failed append creates no event and consumes no sequence. Rotation, persistent recovery, and redundant logs are deferred.

## Module contracts

| Module | Primary responsibility and owned state | Dependencies | Requirements / architecture | Reset behavior | Principal designed tests |
|---|---|---|---|---|---|
| `models.py` | Define enums, immutable values, snapshots, and exception hierarchy; no mutable state. | standard library only | DAT-003–DAT-007, LOG-002; shared across ARC elements | none | enum encoding, immutability, snapshot invariants |
| `config.py` | Parse and atomically validate JSON configuration and credential data; no retained runtime state. | `json`, `models` | DAT-004–DAT-006, TIM-001, TIM-003, NFR-009; ARC-CFG-001 | none | schema, range, type, unknown/missing, malformed, duplicate, atomicity |
| `clock.py` | Own current nonnegative integer logical milliseconds. | `models` | TIM-002, NFR-001; ARC-TIM-001 | startup at caller value; runtime controller reset does not rewind time | now, advance by/to, backward rejection |
| `wiegand.py` | Stateless validation, parity, decode, and fixture/demo encoding for `PROJECT_WIEGAND_26`. | `models` | FUN-001–FUN-006, DAT-001–DAT-003; ARC-INP-001 | none | fixed/generated vectors and four corruption forms |
| `credentials.py` | Own validated ordered records and key index; deterministic lookup/iteration/size. | `models` | FUN-007–FUN-008, DAT-004–DAT-006; ARC-CRD-001 | startup publishes once; runtime reset preserves repository | empty/known/unknown/duplicate/colliding-sum/order |
| `authorization.py` | Pure decision over lookup, enabled flag, floor, and mask. | `models` | FUN-008–FUN-010; ARC-AUT-001 | none | every outcome, types/ranges, all 16 bits |
| `outputs.py` | Sole owner of 16 channels, active floor, and expiry. | `models` | FUN-011–FUN-015, DAT-007, TIM-001; ARC-OUT-001 | startup/runtime reset atomically clears all three values | activate, invalid/concurrent call, before/at expiry, reset |
| `watchdog.py` | Own enabled/timeout/heartbeat/last-service/next-heartbeat/deadline/suppression/epoch-emitted state and return expiry requests. | `models` | TIM-003, RST-004; ARC-WDG-001 | initialize/reinitialize deadlines; runtime reset starts a new armed epoch | normal/suppressed/disabled/collision/one request per epoch |
| `event_log.py` | Own immutable record list, next sequence, and injected append failure. | `json`, `models` | LOG-001–LOG-003, NFR-007; ARC-LOG-001 | startup clear; runtime reset preserves records/progression | schema/null/order/sequence/failure/no-consumption/export |
| `controller.py` | Own controller state/transients; compose managers, precedence, scheduling, reset, and responses. | all domain managers | FUN-001–FUN-015, RST-001–RST-004, NFR-001–NFR-002; ARC-CTL-001 | performs frozen startup/manual/watchdog sequences | states/transitions, precedence, atomicity, recovery, replay |
| `cli.py` | Thin parse/display/demo adapter; no domain state or duplicated rules. | `config`, `controller`, `models` | SCP-005, NFR-003–NFR-005, NFR-008–NFR-009; ARC-CLI-001 | delegates reset | controlled commands, formatting, errors, offline operation |

### Stateless and manager APIs

```python
# config.py
def default_config() -> SimulatorConfig: ...
def load_config_json(text: str) -> SimulatorConfig: ...
def load_credentials_json(text: str) -> tuple[CredentialRecord, ...]: ...
def load_startup_json(config_text: str, credentials_text: str) -> StartupData: ...

# clock.py
class Clock(Protocol):
    def now_ms(self) -> int: ...
class SimulatedClock:
    def __init__(self, start_ms: int = 0) -> None: ...
    def now_ms(self) -> int: ...
    def advance_by(self, delta_ms: int) -> int: ...
    def advance_to(self, target_ms: int) -> int: ...

# wiegand.py
def validate_frame(frame: object) -> FrameValidation: ...
def decode_frame(frame: tuple[int, ...]) -> DecodedCredential: ...
def encode_frame(facility_code: int, credential_number: int) -> tuple[int, ...]: ...
def has_valid_parity(frame: tuple[int, ...]) -> bool: ...

# credentials.py
class CredentialRepository:
    @classmethod
    def from_records(cls, records: Sequence[CredentialRecord]) -> CredentialRepository: ...
    def lookup(self, key: CredentialKey) -> RepositoryLookup: ...
    def records(self) -> tuple[CredentialRecord, ...]: ...
    def __len__(self) -> int: ...

# authorization.py
def authorize(
    decoded: DecodedCredential,
    record: CredentialRecord | None,
    requested_floor: object,
) -> AuthorizationDecision: ...

# outputs.py
class OutputManager:
    def __init__(self) -> None: ...
    def activate(self, floor: int, now_ms: int, duration_ms: int) -> OutputSnapshot: ...
    def next_expiry_ms(self) -> int | None: ...
    def expire_if_due(self, now_ms: int) -> bool: ...
    def reset(self) -> OutputSnapshot: ...
    def snapshot(self) -> OutputSnapshot: ...

# watchdog.py
class Watchdog:
    def __init__(self, enabled: bool, timeout_ms: int, now_ms: int) -> None: ...
    def heartbeat_interval_ms(self) -> int: ...
    def next_heartbeat_ms(self) -> int | None: ...
    def expiry_deadline_ms(self) -> int | None: ...
    def set_service_suppressed(self, suppressed: bool) -> None: ...
    def service(self, now_ms: int) -> bool: ...
    def process_heartbeat(self, now_ms: int) -> bool: ...
    def expiry_request_if_due(self, now_ms: int) -> bool: ...
    def reinitialize(self, now_ms: int) -> None: ...

# event_log.py
class EventLog:
    def __init__(self) -> None: ...
    def append(self, draft: EventDraft) -> EventRecord: ...
    def set_append_failure(self, enabled: bool) -> None: ...
    def records(self) -> tuple[EventRecord, ...]: ...
    def latest_sequence(self) -> int | None: ...
    def clear_startup(self) -> None: ...
    def to_jsonl(self) -> str: ...
```

`validate_frame` returns `error/invalid_frame` semantics for an invalid container, wrong length, or non-binary member, and `error/parity_failure` for either parity region. `decode_frame` is called only after validation; misuse raises `StateInvariantError`. Encoding is a trusted fixture/demo helper and rejects invalid numeric inputs with `CredentialDataError`.

Repository construction may raise `CredentialDataError`/`DuplicateCredentialError`; lookup itself does not raise for absence. `authorize` returns `denied/unknown_credential`, `denied/disabled_credential`, `error/invalid_floor`, `denied/unauthorized_floor`, or `granted/authorized` without mutation.

`OutputManager.activate` is called only after authorization and a successful grant append. Invalid/concurrent internal calls raise `StateInvariantError`. `expire_if_due` changes all three output values together and returns true once. The watchdog returns a Boolean expiry request and never resets other managers. `service` returns false and leaves its deadline unchanged when suppressed; otherwise it moves both the expiry and next-heartbeat schedule. `process_heartbeat` consumes the due heartbeat and applies the same service rule, so a suppressed heartbeat advances its next-heartbeat marker but not its expiry deadline. `EventLog.append` raises injected `EventLogError` before consuming a sequence.

## Public API contracts

The public domain boundary is `Controller`; callers do not mutate component managers:

```python
class Controller:
    def __init__(self, clock: SimulatedClock, event_log: EventLog | None = None) -> None: ...
    def initialize(
        self,
        config: SimulatorConfig,
        credentials: Sequence[CredentialRecord],
    ) -> ControllerResponse: ...
    def submit(self, request: CredentialRequest) -> ControllerResponse: ...
    def advance_to(self, target_ms: int) -> ControllerResponse: ...
    def advance_by(self, delta_ms: int) -> ControllerResponse: ...
    def manual_reset(self) -> ControllerResponse: ...
    def set_watchdog_service_suppressed(self, suppressed: bool) -> ControllerResponse: ...
    def snapshot(self) -> ControllerSnapshot: ...
    def events(self) -> tuple[EventRecord, ...]: ...
```

Construction starts in `RESETTING` with inactive outputs. `initialize` validates and constructs candidate configuration/repository/watchdog objects before publishing them. Success traverses `INITIALIZING` to `IDLE` and returns `result=None, reason=None`; startup exceptions map to the canonical startup error response while state remains `INITIALIZING`, flags false as applicable, and outputs inactive. A `StateInvariantError` and backward-time `ClockError` propagate.

Every operation returns a fresh immutable response/snapshot. `advance_to` returns the final scheduled domain outcome; if no domain event occurs by the target, it returns `result=None, reason=None` and appends no synthetic event. This uses the logical register model's existing null outcome rather than inventing a result or reason. Tests also assert state and event deltas. The SP-06 task may add an explicit immutable scheduler summary only if it does not add an enum value or change event semantics; otherwise human review is required.

CLI adapter signatures are intentionally narrow:

```python
def build_parser() -> argparse.ArgumentParser: ...
def run(argv: Sequence[str] | None = None) -> int: ...
def format_snapshot(snapshot: ControllerSnapshot) -> str: ...
def format_event(event: EventRecord) -> str: ...
```

Configuration/data errors yield a stable nonzero CLI exit and message. Access denials are displayed domain outcomes, not process failures. The CLI contains no parser, authorization, output, timing, watchdog, or log policy.

## Controller orchestration

When active, `submit` performs busy detection before reading any request field, tries exactly one `access_decision/denied/controller_busy` append, preserves output/expiry, and stays `OUTPUT_ACTIVE`. Append failure changes the response to `error/logging_error` with `logging_fault=true` without changing the activation.

When idle, `submit` transitions through the frozen order: source → container/length → bits → parity → decode → lookup → enabled → floor → mask → prepare output/expiry → append grant → activate. Validation/denial results append their canonical event and return to `IDLE`. Failed validation/denial logging returns `error/logging_error`, outputs unchanged. Successful grant append is followed immediately by one atomic output activation and transition to `OUTPUT_ACTIVE`.

The controller alone changes controller state and transient request/decision references. It services normal coordinator checkpoints through the watchdog API, but the scheduled logical heartbeat is what guarantees progress during an otherwise quiet long activation.

## Simulated clock and scheduler

`advance_to(target_ms)` rejects `target_ms < clock.now_ms()` with `ClockError` before mutation. It repeatedly chooses the minimum non-null due timestamp among watchdog heartbeat, watchdog expiry, and output expiry, bounded by `target_ms`. It jumps the clock directly to that timestamp, processes all due work in this priority, then recomputes due times:

1. normal heartbeat service when the watchdog is enabled and service is not suppressed;
2. watchdog expiry evaluation;
3. output expiry.

A suppressed heartbeat is processed/skipped at priority 1 so it cannot be reconsidered forever. If priority 2 returns an expiry request, the controller completes watchdog reset and does not process a formerly due output expiry at priority 3. Stale due markers are invalidated by reset. If no due internal event is at or before the target, the clock jumps directly to the target and returns. Each event carries a processed marker through manager state, so polling at an unchanged timestamp cannot duplicate it.

The algorithm is event-driven, not a loop over elapsed milliseconds. For identical initial state, a single `advance_to(T)` and any monotonic partition ending at `T` produce identical controller state and normalized events.

## Watchdog heartbeat and expiry

For enabled timeout `W`, heartbeat interval `H = max(1, W // 2)`. Initialization/service at time `t` sets expiry deadline `t + W` and schedules the next heartbeat according to the watchdog epoch. A normal due heartbeat services at its scheduled timestamp, sets a later expiry deadline, and schedules the next heartbeat. Fault injection suppresses only service: scheduled heartbeat timestamps are still consumed, simulated time continues, and the existing deadline is unchanged.

Expiry is evaluated after the heartbeat at the same timestamp. Therefore normal service prevents ordinary expiry, including `W = 1`; suppression permits it. An armed deadline emits at most one request. Controller reset clears outputs/expiry/transients, logs exactly one watchdog outcome if possible, and reinitializes a new watchdog epoch with service suppression cleared. A later deliberately reinjected suppression may produce one reset at its own later deadline; it is never a duplicate of the first expiry.

With defaults, normal heartbeats at 1000 ms intervals keep a 3000 ms output alive until its own timeout. Under suppression, no service occurs and watchdog reset is processed at 2000 ms. At a collision between watchdog and output expiry under suppression, watchdog reset wins and cancels the output timeout, yielding one watchdog outcome and no `output_timeout` event.

## Output atomicity

- Invalid request handling never modifies configuration or credentials.
- Denial never creates a new activation.
- Busy never reads/validates the staged request and never changes activation/expiry.
- Grant activation follows successful grant-event append only.
- The 16-channel tuple, active floor, and expiry update together.
- Timeout clears those three values together before attempting its event.
- Failed grant append prevents activation.
- Failed timeout append leaves the completed timeout transition in effect and exposes `logging_error`.
- Startup configuration and credentials publish together only after full validation.

## Reset and preservation behavior

Startup clears controller/output/watchdog/log/transient state, validates candidate configuration and records, initializes the watchdog, and reaches `IDLE` only if all are valid. A startup failure remains all-inactive and non-operational in `INITIALIZING`.

Manual and watchdog reset may interrupt every one of the seven states. They enter `RESETTING`, clear output/active-floor/expiry, request/decision transients, and watchdog service suppression before attempting a reset event; preserve validated configuration, credential repository, existing events, and next-sequence progression; reinitialize the watchdog; and return to `IDLE`. Reset completes despite an event append failure and returns `error/logging_error` with the fault visible. The simulated clock never rewinds. Manual reset returns `reset/manual_request`; watchdog reset returns `reset/watchdog_timeout` when logging succeeds.

## Fault-injection interfaces

Only two required deterministic fault controls exist:

- `Controller.set_watchdog_service_suppressed(bool)` delegates to the watchdog and suppresses service, not time or scheduling.
- `EventLog.set_append_failure(bool)` makes every attempted append fail before mutation/sequence allocation until disabled.

The harness receives the logger as an injected dependency so it can configure append failure; production callers see it only through controller responses and snapshots. Invalid frames/records/configuration are data cases, not hidden fault hooks. Tests restore each injected dependency through fresh fixtures; no fault state is global.

## CLI adapter boundary

The CLI may load the two JSON documents, initialize a controller, submit a complete controlled request, advance logical time, print snapshots/events, request manual reset, and demonstrate watchdog suppression. It must call the same public APIs as tests and must not infer source labels, modify masks, sleep, access a network/device/database, or recover from invalid startup data by silently substituting defaults.

## Experiment interfaces

`scripts/run_experiments.py` will later use only `CredentialRepository`, `Controller`, immutable request/record types, and public snapshots/events. A seed-driven generator creates credential sets and request workloads; `time.perf_counter_ns()` measures host processing around controlled request batches, while the simulated clock remains logical domain time. Results are aggregated before export. Large generated inputs are regenerated rather than stored.

## Requirements and architecture mapping

| Design area | Requirements | Architecture elements |
|---|---|---|
| Boundary/package/dependencies | SCP-002–SCP-006, NFR-002–NFR-005, LIM-001–LIM-004 | ARC-BND-001, ARC-GOV-001, ARC-LIM-001 |
| Request/profile/source | FUN-001–FUN-006, DAT-001–DAT-003 | ARC-INP-001, ARC-CTL-001 |
| Credentials/authorization | FUN-007–FUN-010, DAT-004–DAT-006 | ARC-CRD-001, ARC-AUT-001 |
| Outputs/timing | FUN-011–FUN-015, DAT-007, TIM-001–TIM-002 | ARC-OUT-001, ARC-TIM-001, ARC-CTL-001 |
| Watchdog/reset | TIM-003, RST-001–RST-004 | ARC-WDG-001, ARC-CTL-001 |
| Events/failure behavior | LOG-001–LOG-003, NFR-009 | ARC-LOG-001, ARC-CTL-001 |
| Configuration/reproducibility | NFR-001, NFR-006–NFR-008 | ARC-CFG-001, ARC-TST-001 |
| Verification/experiments | VER-001–VER-008 | ARC-VER-001, ARC-TST-001 |

The detailed test linkage remains in `docs/requirements_to_test_traceability.csv` and `docs/test_case_inventory.csv`. Optional requirements FUN-016–FUN-017, NFR-010–NFR-012, and VER-009 stay deferred and cannot gate the MVP.

## Implementation constraints

SP-06 must not alter canonical enum names/values, the seven states, all-nine-field event schema, floor/mask mapping, timing defaults/range, watchdog default/formula/priority, busy precedence, logging gate, reset preservation, or physical boundary without a reviewed decision. It must use no Pydantic, ORM, database/network service, async/thread scheduling, GUI, hardware adapter, real sleep, or hidden mutable singleton. Dependencies remain standard library plus `pytest`; `pytest-cov` is optional and non-blocking.

## Human-review items

Review the package/dependency layout, raw-request boundary typing, immutable records, enum encodings, exception conversion policy, strict JSON schemas, label rule, JSON Lines order/nulls, public controller signatures, null no-op `advance_to` response, heartbeat formula, same-timestamp priority, reset clearing of service suppression, logging-failure behavior, fault hooks, experiment boundary, and implementation constraints. Owner authorization permits later implementation within this abstract boundary; supervisor approval is still pending.
