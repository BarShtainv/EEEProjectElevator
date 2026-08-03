# Conceptual Hardware and Firmware Architecture

## Document status and evidence boundary

This is the proposed SP-04 reference architecture for the project-owner-approved working title, “Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller.” Supervisor approval remains pending.

Every architecture choice is a project decision unless an external source is named. Nothing here identifies the commercial controller's processor, protocol support, electrical behavior, memory, outputs, or elevator interface. The implemented project remains a deterministic Python software simulator.

## Frozen requirements and owner approval

The owner approved proceeding from the 60 required and six optional SP-03 requirements at commit `94b051cfeebed08db8aec9b590fb99d60c87aee3`. SP-04 does not alter them. Key frozen values are `PROJECT_WIEGAND_26`, logical `LF`/`HF` labels, floors 1–16, bit 0–15 floor mapping, one active output, busy rejection, 3000 ms output default, 2000 ms watchdog default, and software-only verification.

## System boundary

The simulator begins with a complete credential frame, logical reader-source label, and requested floor. It ends at 16 abstract Boolean permission outputs and structured event records. It models validation, lookup, authorization, logical timing, reset, watchdog recovery, and test observation.

It excludes RF propagation, antennas, modulation, pulse acquisition, reader electronics, voltage/current behavior, mains power, relays, wiring, movement, motors, brakes, doors, passenger-safety logic, installation, certification, compliance, and commercial-controller equivalence. The preserved context is `docs/figures/system_context.mmd`.

## Architecture principles

- One owner exists for each mutable state category.
- The controller coordinator owns transition and request-precedence policy, not component data.
- Busy detection precedes all input validation while an output is active.
- Decisions are deterministic for controlled inputs and simulated time.
- A grant is committed only after its required event can be appended.
- Denial or invalid input creates no new output activation.
- Initialization/configuration failure remains all-inactive and non-operational.
- Logical registers are observation/control documentation, not a processor model.
- Required behavior is designed before any optional extension.

## Conceptual hardware reference architecture

The following blocks describe a controller class only. Blocks marked conceptual-only are not part of the Python simulator.

| Block ID | Conceptual block | Architectural role | Simulator treatment | Boundary and limitation | Requirements |
|---|---|---|---|---|---|
| HWR-PWR-001 | Power input, regulation, protection | Supplies a hypothetical controller. | conceptual-only | No voltage, topology, component, rating, or protection claim. | SCP-002, SCP-005, LIM-003 |
| HWR-RDR-001 | External RFID-reader interface | Conceptual source of reader data. | conceptual-only | D0/D1 may illustrate literature context; no physical interface or product support is claimed. | SCP-003, LIM-002 |
| HWR-ISO-001 | Input conditioning/isolation | Conceptual separation before acquisition. | conceptual-only | No circuit, threshold, timing, or isolation rating. | SCP-005, LIM-003 |
| HWR-ACQ-001 | Frame-acquisition boundary | Converts a conceptual reader transfer into a complete frame. | simulator starts after this boundary | Pulse timing is not acquired or reconstructed. | FUN-001, FUN-003 |
| HWR-CTL-001 | Embedded-controller core | Coordinates validation, authorization, timing, logging, and reset. | modeled by ARC-CTL-001 | No MCU or instruction set selected. | SCP-002, NFR-002 |
| HWR-PGM-001 | Program-memory concept | Holds hypothetical control logic/config defaults. | host software artifact only | No physical technology or capacity assigned. | NFR-004, LIM-001 |
| HWR-RAM-001 | Working-data-memory concept | Holds transient request and controller state. | logical regions only | No SRAM claim or capacity. | DAT-007, RST-003 |
| HWR-CRD-001 | Credential-storage concept | Holds logical credential records. | ARC-CRD-001 | Persistence is optional; no product storage claim. | DAT-004, DAT-005 |
| HWR-TIM-001 | Timer function | Provides output deadlines. | ARC-TIM-001 | Logical monotonic milliseconds only. | TIM-001, TIM-002 |
| HWR-WDG-001 | Watchdog function | Requests reset after missed service. | ARC-WDG-001 | Simulated behavior; no MCU equivalence. | TIM-003, RST-004 |
| HWR-LOG-001 | Event-log storage | Retains structured project events. | ARC-LOG-001 | In-memory MVP; capacity/persistence unspecified. | LOG-001, LOG-002 |
| HWR-SVC-001 | Service/configuration interface | Supplies validated configuration and credentials. | ARC-CFG-001 and ARC-CLI-001 | No connector or physical service protocol. | TIM-001, NFR-009 |
| HWR-OUT-001 | 16 floor-output channels | Represents abstract permission state. | ARC-OUT-001 | Exactly 16 logical Booleans. | SCP-004, FUN-011 |
| HWR-DRV-001 | Output driver/isolation boundary | Conceptual boundary after logical outputs. | conceptual-only | No relay, transistor, voltage, current, or isolation design. | SCP-005, LIM-003 |
| HWR-ELV-001 | Elevator access-interface boundary | Terminates the conceptual architecture. | conceptual-only/outside implemented boundary | No electrical command, wiring, motion, or safety control. | SCP-002, SCP-007, LIM-003 |

Diagram: `docs/figures/top_level_architecture.mmd`.

## Simulator and firmware architecture

The proposed responsibilities below are contracts for SP-05 design, not final Python classes or signatures.

| Element ID | Responsibility | Inputs | Outputs | Owned state | Dependencies | Requirements served | Failure behavior | SP-05 handoff |
|---|---|---|---|---|---|---|---|---|
| ARC-INP-001 | Validate source, frame container, length, bits, parity; decode fields. | source label, complete frame | decoded key or validation result/reason | no cross-request state | ARC-CFG-001 | SCP-003; FUN-001–FUN-006; DAT-001–DAT-003 | returns one deterministic error; never activates output | define immutable request/result types and profile API |
| ARC-CRD-001 | Own records, composite lookup, validation, duplicate rejection. | validated record or composite key | record, not-found, or repository error | credential records | ARC-CFG-001 | FUN-007–FUN-008; DAT-004–DAT-006 | fail closed; invalid repository blocks normal operation | define repository contract and record schema |
| ARC-AUT-001 | Evaluate enabled state, floor validity, and permission bit. | record/not-found, floor | grant/deny decision and reason | none | ARC-CRD-001 | FUN-008–FUN-010; DAT-006 | deterministic denial; no output mutation | define decision value model |
| ARC-OUT-001 | Own 16 outputs, active floor, and single expiry. | committed grant, clock, reset, timeout | output state and timeout indication | output vector, active floor, expiry | ARC-TIM-001 | SCP-004; FUN-011–FUN-015; DAT-007; TIM-001 | invalid activation rejected; reset clears synchronously | define output state operations/invariants |
| ARC-CTL-001 | Own state-machine transitions, busy precedence, orchestration, and reset sequencing. | request, component results, timeout/reset/watchdog requests | controller state and response | controller state and transient request/decision | all runtime elements | SCP-002; FUN-001–FUN-015; RST-001–RST-004 | fail closed; logging gate precedes grant activation | define coordinator contract from transition table |
| ARC-WDG-001 | Own enabled flag, last-service deadline, suppression fault, expiry request. | clock and service checkpoints | watchdog-reset request | enabled, last service, deadline, suppression | ARC-TIM-001, ARC-CTL-001 | TIM-003; RST-004 | exactly one expiry request per deadline | define service/expire/fault-injection contract |
| ARC-LOG-001 | Own event records and sequence generation; enforce schema. | canonical event fields | append success/failure and records | event list, next sequence, logging-fault indication | ARC-TIM-001 | LOG-001–LOG-003; NFR-007 | proposed logging policy in Event architecture | define event/enumeration/append contract |
| ARC-TIM-001 | Supply injectable monotonic milliseconds and deterministic advancement. | harness advancement | current time and due-deadline checks | logical time | none | TIM-002; NFR-001 | rejects backward time; no wall-clock wait | define clock protocol and fake clock |
| ARC-CFG-001 | Validate output/watchdog values and runtime policy/profile selection. | configuration data | immutable validated configuration or error | active valid configuration | none | TIM-001; TIM-003; NFR-004; NFR-009 | invalid configuration blocks initialization | define configuration schema and validation |
| ARC-CLI-001 | Adapt a simple demonstration to controller requests/results. | user/demo values | presentation only | no controller state | ARC-CTL-001 | NFR-003; NFR-005; NFR-008 | reports canonical errors without changing them | define adapter boundary after core APIs |
| ARC-TST-001 | Drive time, requests, faults, scales, and observation. | fixtures, seed/config ID | test/experiment records | harness scenario state only | all public architecture boundaries | SCP-005–SCP-006; VER-001–VER-008; NFR-005–NFR-007 | exposes component faults; never repairs hidden state | define fixtures, observation points, result schema |

Architecture governance elements used in traceability are ARC-BND-001 (system boundary), ARC-HWR-001 (conceptual hardware view), ARC-MEM-001 (logical memory), ARC-REG-001 (logical registers), ARC-VER-001 (verification/experiment design), ARC-GOV-001 (scope/approval), and ARC-LIM-001 (interpretation limits). Diagram: `docs/figures/firmware_architecture.mmd`.

## Architecture-element catalog

State ownership is acyclic: ARC-CTL-001 references component results but does not own repository, output, watchdog, clock, or log state. ARC-OUT-001 alone mutates outputs/expiry; ARC-WDG-001 alone mutates watchdog deadline; ARC-LOG-001 alone allocates sequence numbers; ARC-CRD-001 alone mutates records.

All runtime and governance IDs, plus every HWR block, appear in `docs/architecture_to_requirements.csv`.

## Request-processing order

When `IDLE`, ARC-CTL-001 applies this exact order:

1. validate source label;
2. validate frame container and length;
3. validate binary values;
4. validate leading and trailing parity;
5. decode facility code and credential number;
6. look up `(facility_code, credential_number)`;
7. check enabled state;
8. validate floor 1–16;
9. evaluate the mapped floor-mask bit;
10. prepare the selected output activation;
11. prepare its expiry;
12. append the grant event, then atomically commit activation only if append succeeds.

For denial or validation failure, append the corresponding event and return to `IDLE`. If that append fails, return explicit `error/logging_error`, keep outputs unchanged, expose the fault, and return to `IDLE`.

When `OUTPUT_ACTIVE`, ARC-CTL-001 first detects busy state, does not inspect the new source/frame/floor, leaves activation and expiry unchanged, attempts exactly one busy-denial event, and remains `OUTPUT_ACTIVE`. Logging failure changes the response to `error/logging_error` but not the existing output.

## Controller state machine

States are `RESETTING`, `INITIALIZING`, `IDLE`, `VALIDATING`, `LOOKUP`, `AUTHORIZING`, and `OUTPUT_ACTIVE`.

| Source | Condition | Entry/transition action | Event generated | Output invariant | Destination |
|---|---|---|---|---|---|
| startup | process starts | force outputs inactive; clear startup-transient state | none | all inactive | RESETTING |
| RESETTING | startup reset actions complete | initialize event/time references; validate config/repository/watchdog | none | all inactive | INITIALIZING |
| RESETTING | manual/watchdog reset actions complete and preserved state remains valid | reinitialize watchdog; retain config/repository/history | manual_reset, watchdog_reset, or logging_error | all inactive | IDLE |
| INITIALIZING | config and repository valid | service watchdog; commit initialized state | none | all inactive | IDLE |
| INITIALIZING | config/repository invalid | expose deterministic initialization error; accept only corrective service/reset | logging error if available | all inactive | INITIALIZING |
| IDLE | request accepted | capture request; service watchdog | none | all inactive | VALIDATING |
| VALIDATING | frame/source invalid | append validation error; clear transient request | validation_error | all inactive | IDLE |
| VALIDATING | frame valid and decoded | service watchdog; retain decoded key | none | all inactive | LOOKUP |
| LOOKUP | unknown or disabled | append denial; clear transient request | access_decision | all inactive | IDLE |
| LOOKUP | known enabled | service watchdog; retain record | none | all inactive | AUTHORIZING |
| AUTHORIZING | invalid/unauthorized floor | append denial; clear transient request | validation_error or access_decision | all inactive | IDLE |
| AUTHORIZING | authorized and grant event append succeeds | activate one output; set one expiry; service watchdog | access_decision | exactly one active | OUTPUT_ACTIVE |
| AUTHORIZING | grant event append fails | expose logging error; clear pending activation | logging_error | all inactive | IDLE |
| OUTPUT_ACTIVE | new request | skip validation; append busy result if possible | access_decision or logging_error | original one active, original expiry | OUTPUT_ACTIVE |
| OUTPUT_ACTIVE | expiry reached | deactivate output, cancel expiry, append timeout if possible | output_timeout or logging_error | all inactive | IDLE |
| any state | manual reset | execute manual reset sequence | manual_reset or logging_error | all inactive before transition completes | RESETTING then IDLE |
| any state | watchdog expiry | execute watchdog reset sequence | watchdog_reset or logging_error | all inactive before transition completes | RESETTING then IDLE |

Exiting `VALIDATING`, `LOOKUP`, or `AUTHORIZING` clears only state no longer required by the destination. `RESETTING` clears every transient request/decision field. Diagram: `docs/figures/controller_state_machine.mmd`.

Invariants: zero or one output is active; an active output has exactly one expiry; `IDLE`, `RESETTING`, and `INITIALIZING` have no active output; failure creates no new activation; reset clears outputs before idle.

## Input/output interfaces

| Interface ID | Producer | Consumer | Logical data/direction | Validation | Failure behavior | Requirements | Simulator status |
|---|---|---|---|---|---|---|---|
| IF-REQ-001 | CLI/harness | ARC-CTL-001 | complete request inbound | atomic request container | explicit invalid-frame error | FUN-001 | later |
| IF-SRC-001 | request | ARC-INP-001 | `LF`/`HF` inbound | exact enumeration | invalid_source, no activation | FUN-002; DAT-003 | later |
| IF-FRM-001 | request | ARC-INP-001 | 26 ordered bits inbound | length, binary, parity | invalid_frame/parity_failure | FUN-003–FUN-006 | later |
| IF-FLR-001 | request | ARC-AUT-001 | floor inbound | integer 1–16 | invalid_floor | FUN-009–FUN-010 | later |
| IF-CFG-001 | service/harness | ARC-CFG-001 | timing/policy/profile inbound | complete range/type validation | non-operational all-inactive | TIM-001; TIM-003 | later |
| IF-CRD-001 | config/harness | ARC-CRD-001 | records/lookup bidirectional | schema, ranges, duplicates | fail closed/not-found | DAT-004–DAT-006 | later |
| IF-TIM-001 | harness | ARC-TIM-001 | logical monotonic ms inbound/read | no backward advancement | explicit clock error | TIM-002 | later |
| IF-WDG-001 | harness | ARC-WDG-001 | service-suppression control inbound | Boolean fault control | deterministic config error | RST-004 | later |
| IF-OUT-001 | ARC-OUT-001 | CLI/harness | 16 Boolean states outbound | state invariant | expose invariant error, no new activation | DAT-007 | later |
| IF-LOG-001 | ARC-LOG-001 | CLI/harness | event records outbound | fixed schema/enumerations | explicit logging fault | LOG-001–LOG-003 | later |
| IF-CLI-001 | person/demo script | ARC-CLI-001 | textual presentation bidirectional | adapter parsing only | report core error | NFR-008–NFR-009 | later |
| IF-TST-001 | harness | runtime elements | observations/faults/scenarios bidirectional | fixture/config schema | fail test explicitly | VER-001–VER-008 | later |
| IF-PHY-IN-001 | physical reader concept | HWR-ACQ-001 | conceptual D0/D1-to-frame direction | not specified | outside simulator | SCP-005; LIM-002 | conceptual-only |
| IF-PHY-OUT-001 | HWR-OUT-001 | physical elevator boundary | abstract permission direction only | no electrical definition | outside simulator | SCP-002; LIM-003 | conceptual-only |

No interface defines a connector, voltage, current, relay, or elevator wire.

## Data flow

Source, frame, and floor enter ARC-CTL-001 as one request. ARC-INP-001 validates/decodes, ARC-CRD-001 returns a record or not-found result, ARC-AUT-001 decides, ARC-LOG-001 records, and ARC-OUT-001 activates only after a grant event succeeds. ARC-TIM-001 drives output/watchdog deadlines; ARC-TST-001 observes and injects faults. Invalid input exits before lookup or authorization. Manual/watchdog reset interrupts every flow. No modeled electrical command crosses HWR-ELV-001. Diagram: `docs/figures/data_flow.mmd`.

## Configuration model

Required configuration is profile name `PROJECT_WIEGAND_26`, output duration 100–30000 ms (default 3000), watchdog timeout positive with default 2000 ms, watchdog enabled state, and the credential record set. Values are validated as one initialization transaction. Invalid configuration or invalid repository initialization leaves the controller in `INITIALIZING`, all outputs inactive, and normal requests rejected until corrected and reset/reinitialized. Configuration serialization is deferred to SP-05.

## Timing and output behavior

ARC-TIM-001 is monotonic and injectable. A grant event is appended before ARC-OUT-001 atomically sets the selected bit and one expiry equal to current logical time plus duration. At expiry, outputs clear even if timeout logging fails. Busy requests do not extend expiry. Register timestamps expose a 32-bit logical view; internal time representation is deferred.

## Reset architecture

Startup sequence: (1) clear outputs, (2) clear transient request/decode/decision/timer state, (3) initialize event sequence and logical time references, (4) validate configuration, (5) load/initialize repository, (6) initialize watchdog, (7) enter idle only if valid.

Manual/watchdog sequence: (1) clear outputs, (2) cancel expiry, (3) clear transient request/decision, (4) preserve valid configuration, (5) preserve repository, (6) preserve prior events and sequence progression, (7) append one reset event if possible, (8) reinitialize watchdog, (9) return idle. Causes are `manual_request` and `watchdog_timeout`. State transition occurs even if logging fails, and the logging fault is exposed. Diagram: `docs/figures/reset_sequence.mmd`.

## Watchdog architecture

ARC-WDG-001 holds timeout, enabled state, last-service time/deadline, and service-suppression control. Normal checkpoints are successful initialization, entry to `VALIDATING`, `LOOKUP`, `AUTHORIZING`, committed `OUTPUT_ACTIVE`, timeout completion, and return to `IDLE`. Fault injection suppresses service but never clock advancement.

At the deadline exactly one reset request is emitted. Reset clears outputs/expiry/transients, preserves valid configuration/repository/event history, appends one `watchdog_reset` with reason `watchdog_timeout` if possible, reinitializes watchdog, and returns to idle. Later processing remains possible. This is not an MCU watchdog reproduction. Diagram: `docs/figures/watchdog_sequence.mmd`.

## Event architecture

Every event contains all fields: `sequence_number`, `timestamp_ms`, `event_type`, `reader_source`, `facility_code`, `credential_number`, `requested_floor`, `result`, `reason`. Unavailable conditional values are explicit `null`. Sequence numbers begin at 1 and increase only on successful append; timestamps are logical monotonic milliseconds.

Canonical event types are `access_decision`, `validation_error`, `output_timeout`, `manual_reset`, `watchdog_reset`, and `logging_error`. Results are `granted`, `denied`, `error`, `completed`, and `reset`. Reasons are `authorized`, `unknown_credential`, `disabled_credential`, `unauthorized_floor`, `invalid_source`, `invalid_frame`, `parity_failure`, `invalid_floor`, `controller_busy`, `output_expired`, `manual_request`, `watchdog_timeout`, `invalid_configuration`, `invalid_credential_record`, `duplicate_credential`, `repository_initialization_failure`, and `logging_error`. Numerical register encodings are in `docs/register_model.md`; textual values are canonical.

Proposed logging-failure policy:

- a decision is never changed retroactively;
- a grant event is precommitted, so append failure denies before activation with `error/logging_error`;
- denial/validation append failure returns `error/logging_error` and leaves outputs unchanged;
- busy append failure leaves the prior activation/expiry unchanged;
- timeout/reset state changes occur even if their event append fails;
- every logging fault is exposed to ARC-TST-001;
- persistent recovery and redundant logging are outside SP-04.

An optional human-readable message may be derived but is not canonical state.

## Failure modes and safe logical state

“All inactive” is a software invariant, not a physical safety certification.

| Failure ID | Initiating condition | Detection/state | Result/reason | Output effect | Logged event | Recovery | Requirements | Residual limitation |
|---|---|---|---|---|---|---|---|---|
| FLT-INP-001 | invalid source label (not LF/HF) | ARC-INP-001 / VALIDATING | error/invalid_source | no new activation | validation_error | clear request, IDLE | FUN-002 | input transport deferred |
| FLT-INP-002 | invalid frame container | ARC-INP-001 / VALIDATING | error/invalid_frame | no new activation | validation_error | clear request, IDLE | FUN-001 | container type deferred |
| FLT-INP-003 | length not 26 | ARC-INP-001 / VALIDATING | error/invalid_frame | no new activation | validation_error | clear request, IDLE | FUN-003 | other formats optional |
| FLT-INP-004 | non-binary bit | ARC-INP-001 / VALIDATING | error/invalid_frame | no new activation | validation_error | clear request, IDLE | FUN-004 | representation deferred |
| FLT-INP-005 | leading parity fails | ARC-INP-001 / VALIDATING | error/parity_failure | no new activation | validation_error | clear request, IDLE | FUN-005 | common reason value |
| FLT-INP-006 | trailing parity fails | ARC-INP-001 / VALIDATING | error/parity_failure | no new activation | validation_error | clear request, IDLE | FUN-005 | common reason value |
| FLT-CRD-001 | key not found | ARC-CRD-001 / LOOKUP | denied/unknown_credential | no new activation | access_decision | IDLE | FUN-007–FUN-008 | commercial behavior unknown |
| FLT-CRD-002 | record disabled | ARC-AUT-001 / LOOKUP | denied/disabled_credential | no new activation | access_decision | IDLE | FUN-008 | project policy |
| FLT-CRD-003 | invalid record | ARC-CRD-001 / INITIALIZING | error/invalid_credential_record | all inactive, non-operational | validation_error if logger available | correct repository; reinitialize | DAT-004 | storage format deferred |
| FLT-CRD-004 | duplicate key | ARC-CRD-001 / INITIALIZING | error/duplicate_credential | all inactive, non-operational | validation_error if logger available | remove duplicate; reinitialize | DAT-005 | no silent replacement |
| FLT-AUT-001 | invalid floor | ARC-AUT-001 / AUTHORIZING | error/invalid_floor | no new activation | validation_error | IDLE | FUN-009 | type representation deferred |
| FLT-AUT-002 | bit clear | ARC-AUT-001 / AUTHORIZING | denied/unauthorized_floor | no new activation | access_decision | IDLE | FUN-010 | project mask policy |
| FLT-CTL-001 | request while active | ARC-CTL-001 / OUTPUT_ACTIVE | denied/controller_busy | original output/expiry unchanged | access_decision | remain active | FUN-012, FUN-014 | new request not inspected |
| FLT-CFG-001 | output duration invalid | ARC-CFG-001 / INITIALIZING | error/invalid_configuration | all inactive, non-operational | validation_error if available | correct config; reinitialize | TIM-001 | no default fallback after explicit invalid value |
| FLT-CFG-002 | watchdog config invalid | ARC-CFG-001 / INITIALIZING | error/invalid_configuration | all inactive, non-operational | validation_error if available | correct config; reinitialize | TIM-003 | range beyond default deferred |
| FLT-RST-001 | manual reset while active | ARC-CTL-001 / any | reset/manual_request | immediately all inactive; expiry canceled | manual_reset | preserve config/repo/history; IDLE | RST-001–RST-002 | logical reset only |
| FLT-WDG-001 | watchdog expires while active | ARC-WDG-001 / any | reset/watchdog_timeout | immediately all inactive; expiry canceled | watchdog_reset | preserve config/repo/history; IDLE | RST-004 | simulated watchdog only |
| FLT-LOG-001 | event append fails | ARC-LOG-001 / any | error/logging_error | grant withheld; other required transitions still occur | logging_error only if alternate exposure can record; harness fault always | correct/inject logger; later requests allowed per state | LOG-001–LOG-003 | no redundant/persistent recovery |
| FLT-CRD-005 | repository initialization fails | ARC-CRD-001 / INITIALIZING | error/repository_initialization_failure | all inactive, non-operational | validation_error if available | correct source; reinitialize | DAT-004–DAT-005 | persistence mechanism deferred |

## Architecture-to-requirements summary

`docs/architecture_to_requirements.csv` maps all 60 required requirements with status `designed`; the six optional requirements are `deferred_optional`. Runtime, governance, and conceptual hardware elements all have at least one mapping. No row claims implementation or verification.

## SP-05 implementation handoff

SP-05 should define immutable data types, module contracts, error/result types, configuration/event serialization, precise APIs, test fixtures, and detailed test cases from this architecture. It must preserve ownership, processing precedence, state transitions, enumerations, register semantics, reset order, logging gate, and failure policies. It must not infer physical behavior.

## Limitations

This architecture is not industrial, physical, safety-certified, or product-equivalent. Logical registers and memory are documentation/testing constructs. Conceptual hardware blocks contain no electrical design. Host-software timing cannot establish commercial or elevator performance. Optional persistence, extra profiles, GUI, and physical adapters remain deferred.

## Human-review items

Review the conceptual hardware boundary, seven-state model, busy-before-validation order, reset preservation, explicit-null events, enumerations, logical register map, initialization fail-closed behavior, logging-failure policy, watchdog checkpoints, and full mapping. Owner acceptance supports SP-05 planning; supervisor approval remains pending.
