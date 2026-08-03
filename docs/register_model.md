# Proposed Logical Memory and Register Model

## Purpose and limitations

This is a proposed simulator-facing documentation and test model. It is not the commercial product's register map, is not tied to ARM, STM32, or any processor, and does not model an instruction set or MCU peripheral. Every address is a project-defined logical offset. No physical memory capacity, bus, electrical interface, or product behavior is implied.

## Access and reset conventions

Registers are 32 bits wide and aligned at four-byte offsets beginning at `0x0000`. `RO`, `WO`, and `RW` mean read-only, write-only, and read/write through the proposed simulator observation/control adapter. Reserved bits read as zero and writes are rejected or ignored according to the later SP-05 API contract; they never change behavior.

The reset value column is the startup-reset value. Manual and watchdog preservation rules are defined separately. Writes are validated atomically; an invalid field value does not partially update a register or controller state.

## Logical memory regions

These are named simulator regions, not Flash/SRAM addresses.

| Region ID | Purpose | Owner | Lifetime | Startup reset | Manual/watchdog reset | Persistence expectation | Primary requirements |
|---|---|---|---|---|---|---|---|
| MEM-CFG-001 | validated profile and timing configuration | ARC-CFG-001 | run/configuration | load defaults then validate | preserve valid configuration | in-memory MVP; file optional | TIM-001, TIM-003, NFR-009 |
| MEM-REQ-001 | source, frame, requested floor | ARC-CTL-001 | one request | clear | clear | transient | FUN-001–FUN-004 |
| MEM-DEC-001 | decoded facility/credential and decision | ARC-CTL-001 | one request | clear | clear | transient | FUN-006–FUN-010 |
| MEM-CRD-001 | validated credential records | ARC-CRD-001 | run | load/initialize and validate | preserve | in-memory MVP; persistence optional | DAT-004–DAT-006 |
| MEM-CTL-001 | controller state and initialization flags | ARC-CTL-001 | run | RESETTING | RESETTING then IDLE if valid | transient state | RST-001, RST-004 |
| MEM-OUT-001 | 16 outputs, active floor, expiry | ARC-OUT-001 | activation | clear | clear/cancel | transient | FUN-011–FUN-015, DAT-007 |
| MEM-WDG-001 | enabled, timeout, last service, deadline, suppression | ARC-WDG-001 | run/fault | initialize | reinitialize | transient except config | TIM-003, RST-004 |
| MEM-LOG-001 | canonical event records and next sequence | ARC-LOG-001 | run | empty; next sequence 1 | preserve records and progression | in-memory MVP | LOG-001–LOG-003 |
| MEM-DIA-001 | case counters, timing samples, seed/config ID | ARC-TST-001 | scenario/experiment | clear or initialize from harness | harness policy; not controller state | machine-readable results later | VER-005–VER-008 |

## Register map

| Register ID | Offset | Width | Access | Startup reset | Field definition | Owner | Update rule | Related requirements | Limitation |
|---|---:|---:|---|---:|---|---|---|---|---|
| REG-CAPABILITY | `0x0000` | 32 | RO | `0x0001101A` | 31:16 architecture version=1; 15:8 outputs=16; 7:0 frame bits=26 | ARC-REG-001 | constant for this architecture revision | SCP-004, DAT-001 | logical capability only |
| REG-CONTROL | `0x0004` | 32 | WO | `0x00000000` | bit0 submit request; bit1 manual reset; bit2 watchdog-service suppression; 31:3 reserved | ARC-CTL-001 | commands are edge-triggered; bits do not latch except suppression state owned by watchdog | FUN-001, RST-002, RST-004 | not a hardware control register |
| REG-STATUS | `0x0008` | 32 | RO | `0x00000000` | 2:0 state; bit3 output active; bit4 initialized; bit5 config valid; bit6 repository ready; bit7 logging fault; 31:8 reserved | ARC-CTL-001 | recomputed on committed transition | RST-001, NFR-009 | logical observation |
| REG-OUTPUT-DURATION-MS | `0x000C` | 32 | RW | `0x00000BB8` | 31:0 duration; valid 100–30000 | ARC-CFG-001 | writable only through validated configuration while non-active | TIM-001 | milliseconds are simulated |
| REG-WATCHDOG-TIMEOUT-MS | `0x0010` | 32 | RW | `0x000007D0` | 31:0 timeout; valid 1–4294967295; default 2000 | ARC-CFG-001 | validated before initialization | TIM-003 | logical milliseconds; no MCU timing claim |
| REG-INPUT-SOURCE | `0x0014` | 32 | RW | `0x00000000` | 1:0 source encoding; 31:2 reserved | ARC-INP-001 | staged with atomic request; invalid encoding rejected | FUN-002, DAT-003 | source is metadata |
| REG-INPUT-FRAME | `0x0018` | 32 | RW | `0x00000000` | 25:0 PROJECT_WIEGAND_26; 31:26 must be zero | ARC-INP-001 | staged with request; validated before decode | FUN-003–FUN-006, DAT-001 | complete frame, not D0/D1 timing |
| REG-REQUESTED-FLOOR | `0x001C` | 32 | RW | `0x00000000` | 4:0 floor 1–16; 31:5 reserved | ARC-AUT-001 | staged with request; zero means none outside request | FUN-009 | invalid values rejected |
| REG-DECODED-FACILITY | `0x0020` | 32 | RO | `0x00000000` | 7:0 facility code; 31:8 zero | ARC-INP-001 | updated after successful decode; cleared with transient state | FUN-006, DAT-004 | project profile field |
| REG-DECODED-CREDENTIAL | `0x0024` | 32 | RO | `0x00000000` | 15:0 credential number; 31:16 zero | ARC-INP-001 | updated after successful decode; cleared with transient state | FUN-006, DAT-004 | project profile field |
| REG-SELECTED-FLOOR-MASK | `0x0028` | 32 | RO | `0x00000000` | 15:0 floor mask; 31:16 zero | ARC-CRD-001 | copied from selected validated record; cleared with transient state | DAT-006 | product storage unknown |
| REG-OUTPUT-STATE | `0x002C` | 32 | RO | `0x00000000` | 15:0 outputs for floors 1–16; 31:16 always zero | ARC-OUT-001 | atomic grant sets one bit; timeout/reset clears all | FUN-011–FUN-014, DAT-007 | abstract outputs only |
| REG-ACTIVE-FLOOR | `0x0030` | 32 | RO | `0x00000000` | 4:0 floor 1–16; zero means no active output; 31:5 zero | ARC-OUT-001 | changes atomically with output state | FUN-011–FUN-013 | at most one floor |
| REG-OUTPUT-EXPIRY-MS | `0x0034` | 32 | RO | `0x00000000` | 31:0 low-order logical expiry milliseconds; zero means none | ARC-OUT-001 | set with grant; cleared at timeout/reset | FUN-013, TIM-002 | full internal time type deferred |
| REG-WATCHDOG-LAST-SERVICE-MS | `0x0038` | 32 | RO | `0x00000000` | 31:0 low-order logical service timestamp | ARC-WDG-001 | updated only at defined service checkpoints unless suppressed | TIM-003, RST-004 | logical view only |
| REG-EVENT-SEQUENCE | `0x003C` | 32 | RO | `0x00000000` | 31:0 latest successful event sequence; zero means none | ARC-LOG-001 | increments once after successful append | LOG-003 | wrap policy deferred; internal value may be wider |
| REG-LAST-EVENT-TYPE | `0x0040` | 32 | RO | `0x00000000` | 3:0 event encoding; 31:4 zero | ARC-LOG-001 | updated on successful append | LOG-001–LOG-002 | textual name canonical |
| REG-LAST-RESULT | `0x0044` | 32 | RO | `0x00000000` | 2:0 result encoding; 31:3 zero | ARC-LOG-001 | updated on successful append | LOG-002 | textual name canonical |
| REG-LAST-REASON | `0x0048` | 32 | RO | `0x00000000` | 4:0 reason encoding; 31:5 zero | ARC-LOG-001 | updated on successful append | LOG-002 | textual name canonical |

## Register field definitions

`REG-CONTROL` request submission snapshots source, frame, and floor as one request only while `IDLE`. While `OUTPUT_ACTIVE`, submission triggers busy handling and the staged values are not validated. Manual reset has priority over submission. Watchdog reset has priority over all normal processing.

`REG-STATUS` state encoding is the only state field. Output-active bit mirrors `REG-OUTPUT-STATE != 0`. Initialized is true only in `IDLE`, request-processing states, or `OUTPUT_ACTIVE` after successful configuration/repository initialization. Configuration and repository flags remain false during a blocked initialization.

## Controller-state encoding

| Value | Canonical state |
|---:|---|
| 0 | `RESETTING` |
| 1 | `INITIALIZING` |
| 2 | `IDLE` |
| 3 | `VALIDATING` |
| 4 | `LOOKUP` |
| 5 | `AUTHORIZING` |
| 6 | `OUTPUT_ACTIVE` |

## Reader-source encoding

| Value | Canonical source |
|---:|---|
| 0 | `null` / not supplied |
| 1 | `LF` |
| 2 | `HF` |

## Event-type encoding

| Value | Canonical event type |
|---:|---|
| 0 | `null` |
| 1 | `access_decision` |
| 2 | `validation_error` |
| 3 | `output_timeout` |
| 4 | `manual_reset` |
| 5 | `watchdog_reset` |
| 6 | `logging_error` |

## Result and reason encoding

Results:

| Value | Canonical result |
|---:|---|
| 0 | `null` |
| 1 | `granted` |
| 2 | `denied` |
| 3 | `error` |
| 4 | `completed` |
| 5 | `reset` |

Reasons:

| Value | Canonical reason |
|---:|---|
| 0 | `null` |
| 1 | `authorized` |
| 2 | `unknown_credential` |
| 3 | `disabled_credential` |
| 4 | `unauthorized_floor` |
| 5 | `invalid_source` |
| 6 | `invalid_frame` |
| 7 | `parity_failure` |
| 8 | `invalid_floor` |
| 9 | `controller_busy` |
| 10 | `output_expired` |
| 11 | `manual_request` |
| 12 | `watchdog_timeout` |
| 13 | `invalid_configuration` |
| 14 | `invalid_credential_record` |
| 15 | `duplicate_credential` |
| 16 | `repository_initialization_failure` |
| 17 | `logging_error` |

All encoding values are unique within their enumeration. Text names remain canonical; numbers exist only for the proposed logical register view.

## Floor-mask definition

Only bits 15:0 are valid. For floor `f` in 1–16, the permission bit is `f - 1`. Thus floor 1 is bit 0 and floor 16 is bit 15. Bits 31:16 are zero and a mask outside `0x0000`–`0xFFFF` is invalid.

## Output-state definition

`REG-OUTPUT-STATE` uses the same mapping. Valid states are zero or exactly one set bit. `REG-ACTIVE-FLOOR` is zero exactly when output state is zero; otherwise it equals the one-based floor of the set bit. One nonzero expiry exists exactly when an output is active.

## Event-record format

The canonical record contains all fields in this order: `sequence_number`, `timestamp_ms`, `event_type`, `reader_source`, `facility_code`, `credential_number`, `requested_floor`, `result`, `reason`. Conditional unavailability is explicit `null`. The register view exposes only the latest sequence/type/result/reason; full records remain in MEM-LOG-001.

## Reset values and preservation rules

Startup clears transient, output, watchdog, event, and diagnostic state; sequence begins with the first successful append at 1. Defaults are loaded then validated. Invalid configuration/repository leaves `INITIALIZING` and all outputs inactive.

Manual/watchdog reset clears request, decode, decision, outputs, active floor, expiry, and watchdog timestamps; it preserves valid configuration values, credential records, prior events, and sequence progression. The corresponding reset event is appended after outputs clear. If append fails, reset still completes and the harness receives a logging fault.

## Register invariants

- Every offset is unique, 32-bit aligned, and logical.
- Reserved bits are zero and fields within a register do not overlap.
- `REG-OUTPUT-STATE & 0xFFFF0000 == 0`.
- Output state has population count 0 or 1.
- Active floor and expiry are both zero iff no output is active.
- Busy handling does not alter output state or expiry.
- Decoded fields are meaningful only after validation and are cleared on transient reset.
- Grant activation cannot occur unless the grant event append succeeds.
- Initialization failure never sets initialized/status-ready flags.

## Example logical transaction

1. While `IDLE`, stage source, 26-bit frame, and floor in the input registers.
2. Submit through `REG-CONTROL.bit0`; the coordinator snapshots all three values.
3. Observe state progression through validation, lookup, and authorization.
4. For a grant, the logger first appends `access_decision/granted/authorized`; output state then atomically gains the selected bit and expiry.
5. Advance simulated time; at expiry output state, active floor, and expiry clear, and an `output_timeout/completed/output_expired` event is attempted.
6. A request submitted while active produces busy handling without interpreting staged input.

## Implementation handoff

SP-05 must choose Python types and APIs that preserve these fields, validations, state ownership, atomic update rules, encodings, null handling, and reset preservation. It may use wider internal counters/timestamps while exposing the documented 32-bit logical view. It must not treat this map as hardware or commercial-product evidence.
