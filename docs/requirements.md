# Requirements and Scope Baseline

## Document status

- Stage: SP-03
- Working title: **Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller**
- Title authority: approved as the current working title by the project owner; supervisor approval is pending.
- System type: deterministic Python software simulator and conceptual access-authorization controller.
- Evidence boundary: every behavior below is a proposed project-model requirement unless its basis is explicitly external evidence. It does not describe verified commercial-product behavior.

## Frozen system boundary

The simulator models credential-message validation, credential lookup, floor authorization, abstract timed permission outputs, event logging, reset, watchdog recovery, and reproducible software-only verification.

“Dual-frequency” means two logical reader-source categories, `LF` and `HF`. The labels do not model RF propagation, modulation, antennas, reader electronics, or a frequency detectable from a Wiegand message. No RFID frequency, credential technology, protocol, or Wiegand support is attributed to the commercial controller.

The project boundary excludes motors, brakes, doors, elevator movement, passenger-safety logic, mains wiring, real reader electronics, physical relay design, physical elevator wiring, certification, and real-world installation. The simulator is an access-authorization layer only.

### Failure-state policy

A denied or invalid request shall not create or change an output activation. When the controller is idle, every failure path therefore leaves all outputs inactive. When an output is already active because of an earlier authorized request, a later denied, invalid, or busy request leaves that one existing activation unchanged until its approved timeout or a reset. This is the only permitted exception to the all-inactive failure-state wording.

## Minimum viable behavior

The required MVP shall:

1. receive one complete simulated credential frame and an `LF` or `HF` source label;
2. validate the `PROJECT_WIEGAND_26` length, binary values, and parity;
3. extract an 8-bit facility code and 16-bit credential number;
4. look up the composite credential key;
5. deny unknown and disabled credentials;
6. accept one requested floor from 1 through 16;
7. check the corresponding bit in an enabled credential's 16-bit floor mask;
8. activate only the granted floor output for a configurable logical duration;
9. reject new requests as `controller_busy` while an output is active;
10. log grants, denials, validation errors, timeouts, resets, and watchdog recovery;
11. return to an all-inactive idle state after reset or watchdog expiration; and
12. support deterministic software-only unit, integration, timing, scalability, and fault tests.

## Frozen logical conventions

### `PROJECT_WIEGAND_26`

This proposed controller-side message profile is sufficient for the simulator and is not claimed to be universal or compatible with the commercial product:

| Bits | Field | Rule |
|---|---|---|
| 1 | leading parity | selected so bits 1–13 contain an even number of one bits |
| 2–9 | facility code | unsigned 8-bit value, 0–255 |
| 10–25 | credential number | unsigned 16-bit value, 0–65535 |
| 26 | trailing parity | selected so bits 14–26 contain an odd number of one bits |

The leading parity bit covers data bits 2–13; the trailing parity bit covers data bits 14–25. External literature supports D0/D1 pulse signaling, framing variation, and parity concepts. The field allocation above is a proposed reference-design decision. Both logical source categories may deliver this same message profile, and the source category cannot be inferred from the 26 bits.

### Floors, credentials, outputs, and time

- Valid floors are 1–16; floor 1 maps to mask bit 0 and floor 16 to mask bit 15.
- A credential record contains `facility_code`, `credential_number`, `enabled`, `floor_mask`, and an optional label.
- The credential key is the ordered composite `(facility_code, credential_number)`, not arithmetic addition.
- Duplicate composite keys are rejected; silent replacement is prohibited in the MVP.
- The controller exposes exactly 16 logical outputs and allows at most one active output.
- A new request while an output is active is denied with reason `controller_busy`; it does not replace or extend the active output.
- Default logical output duration is 3000 ms; the configurable valid range is 100–30000 ms inclusive.
- Default simulated watchdog timeout is 2000 ms.
- Time is injectable or simulated so automated tests never require real waiting.

## Requirement catalog

Every row contains the requirement statement, rationale, basis, acceptance criteria, planned verification, priority, implementation stage, and limitations.

### Scope and boundary requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| SCP-001 | The project shall use the exact working title stated in this document until a human-approved replacement is recorded. | Stabilizes academic and technical terminology. | Project-owner SP-03 instruction; DEC-010. | The exact title appears in the requirements, decision log, and context diagram; supervisor-pending status is visible. | Document inspection. | required | SP-03 and all later stages | Working-title approval is not supervisor approval. |
| SCP-002 | The simulator shall model only an access-authorization layer with abstract floor-permission outputs. | Preserves the safety boundary. | SRC-PLAN-001; DEC-008; DEC-011. | Inputs, decisions, outputs, and logs are modeled without elevator motion or safety control. | Requirements and architecture review. | required | SP-03–SP-07 | Proposed software model only. |
| SCP-003 | The simulator shall represent two logical reader-source categories named `LF` and `HF`. | Supports the working dual-frequency study without RF modeling. | Project-owner SP-03 instruction; DEC-012; CLM-021. | Both labels are accepted and retained as metadata; no physical-frequency behavior is modeled. | Unit and integration tests. | required | SP-05–SP-06 | Labels do not assert commercial frequency support. |
| SCP-004 | The simulator shall represent floors 1–16 with exactly 16 abstract permission-output channels. | Freezes the project size. | SRC-PLAN-001; DEC-008; DEC-014; DEC-015. | State inspection shows 16 channels and rejects all other floor identifiers. | Unit and boundary tests. | required | SP-04–SP-06 | No physical output or relay is implied. |
| SCP-005 | Normal simulation and automated verification shall require no RFID reader, controller board, elevator hardware, GPIO, serial interface, or network service. | Keeps the project reproducible and safe. | SRC-PLAN-001; DEC-011. | A clean software environment can execute the planned tests using generated inputs only. | Environment and test review. | required | SP-05–SP-07 | Physical adapters are outside the MVP. |
| SCP-006 | Required MVP work shall be completed before any optional feature is implemented. | Protects the deadline-driven scope. | DEC-023; DEC-024. | Required deliverables are separately listed and optional work cannot be a prerequisite for required tests. | Traceability and milestone review. | required | SP-03–SP-08 | Optional features require later approval. |
| SCP-007 | Expansion toward physical integration or a commercial-equivalence claim shall require a recorded scope change and supervisor approval. | Prevents unauthorized physical or product claims. | DEC-002; DEC-008; project-owner SP-03 instruction. | No current requirement depends on such an expansion; any future proposal is gated in the decision log. | Document and change-control review. | required | All stages | Current owner authorization covers the abstract model only. |

### Functional requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| FUN-001 | The simulator shall receive one complete credential frame per processing request. | Defines an atomic input boundary. | DEC-024; proposed reference design. | One frame produces one validation outcome; partial or multiple concatenated frames are rejected. | Unit tests with complete, partial, and concatenated inputs. | required | SP-05–SP-06 | Pulse timing acquisition is not modeled. |
| FUN-002 | The simulator shall receive and record exactly one reader-source label, `LF` or `HF`, with each credential request. | Retains logical source provenance. | DEC-012. | Valid labels appear in the resulting event; other labels are rejected without activation. | Parameterized unit and integration tests. | required | SP-05–SP-06 | Frequency cannot be derived from frame bits. |
| FUN-003 | The MVP shall accept only frames containing exactly 26 ordered bit values. | Freezes the initial parser scope. | PRD-002; DEC-013. | Length 26 proceeds to bit/parity checks; every other length yields `invalid_frame` and no new activation. | Boundary tests for 0, 25, 26, and 27 bits. | required | SP-05–SP-06 | Other Wiegand lengths are optional. |
| FUN-004 | The simulator shall reject a frame containing any value other than binary 0 or 1. | Makes malformed-input handling explicit. | DEC-013; SRC-TEST-001. | Each representative non-binary value yields `invalid_frame`, is logged, and creates no activation. | Parameterized malformed-value unit tests. | required | SP-05–SP-06 | Input container representation is deferred. |
| FUN-005 | The simulator shall validate both `PROJECT_WIEGAND_26` parity regions before extracting a credential. | Detects defined frame corruption. | SRC-WIEGAND-001; DEC-013. | Correct parity passes; independent corruption of either parity region yields `parity_failure` and no new activation. | Leading- and trailing-parity unit tests. | required | SP-05–SP-06 | This is project-profile validation, not universal compatibility. |
| FUN-006 | For a valid frame, the simulator shall extract the facility code and credential number using the frozen field allocation. | Produces the lookup key deterministically. | DEC-013; DAT-001. | Reference vectors decode to the expected 0–255 facility code and 0–65535 credential number, including boundary values. | Table-driven decoder tests. | required | SP-05–SP-06 | No commercial credential semantics are inferred. |
| FUN-007 | The simulator shall look up the ordered composite credential key in the configured credential database. | Separates decoding from authorization. | SRC-AUTH-001; DEC-016. | A stored composite key returns exactly its record; a missing key returns an unknown result. | Unit tests with colliding arithmetic sums and distinct tuples. | required | SP-05–SP-06 | Storage implementation is deferred. |
| FUN-008 | The simulator shall deny unknown credentials with reason `unknown_credential` and disabled credentials with reason `disabled_credential`. | Defines deterministic credential failure behavior. | SRC-AUTH-001; DEC-024. | Each condition returns the specified reason, logs one denial, and creates no new output activation. | Credential and end-to-end tests. | required | SP-05–SP-06 | Does not describe commercial behavior. |
| FUN-009 | After a valid enabled credential is identified, the simulator shall receive exactly one requested floor and validate it as an integer from 1 through 16. | Defines the authorization target. | DEC-014. | Floors 1 and 16 are accepted; non-integers and values outside the range yield `invalid_floor`. | Boundary and type-validation tests. | required | SP-05–SP-06 | Interface representation is deferred. |
| FUN-010 | The simulator shall grant a request only when the requested floor's mapped permission bit is set in the credential's floor mask. | Implements the proposed authorization rule. | SRC-AUTH-001; DEC-015. | Test vectors for set and clear bits return `grant` and `unauthorized_floor` respectively. | Table-driven authorization tests for all 16 bits. | required | SP-05–SP-06 | Mask use is a project choice. |
| FUN-011 | A granted request shall activate only the logical output corresponding to the requested floor. | Prevents unintended permission outputs. | DEC-017. | Immediately after grant exactly one channel is active and its index matches the floor. | Output-state unit and integration tests. | required | SP-05–SP-06 | Abstract output only. |
| FUN-012 | While any output is active, the simulator shall reject every new request with result `denied` and reason `controller_busy`. | Provides a small deterministic concurrency policy. | DEC-018. | A second request neither replaces, extends, nor adds an activation; the original activation retains its scheduled expiry. | Simulated-time busy-controller integration test. | required | SP-05–SP-06 | Applies to otherwise valid or invalid new requests after busy state is detected. |
| FUN-013 | The simulator shall deactivate the active output when its configured logical duration expires. | Completes timed permission behavior. | DEC-019. | At time just before expiry one output is active; at expiry all 16 are inactive and one timeout event is logged. | Boundary tests using injected time. | required | SP-05–SP-06 | No physical timing claim. |
| FUN-014 | A denied or invalid request shall create no new activation and shall not alter an already authorized activation except through timeout or reset. | Makes all failure paths safe and testable. | Frozen failure-state policy; DEC-018. | Idle failures leave all outputs inactive; failures during an active interval leave only the original channel active with unchanged expiry. | Failure-path state-invariant tests. | required | SP-05–SP-06 | Explicit exception is an existing authorized timed output. |
| FUN-015 | The controller shall return to an idle state after output timeout, manual reset, or watchdog reset and shall then accept a new valid request. | Ensures continued deterministic processing. | DEC-019; DEC-020. | A valid post-recovery request can be granted and timed normally. | End-to-end recovery tests. | required | SP-05–SP-06 | No hardware recovery claim. |
| FUN-016 | The simulator may support additional Wiegand frame lengths through separately named profiles. | Provides a bounded extension path. | DEC-023. | If implemented, each profile has documented fields and independent tests without changing `PROJECT_WIEGAND_26`. | Optional profile tests and review. | optional | Post-MVP only | Must not delay required work or imply product support. |
| FUN-017 | The simulator may add administrator roles, multiple facilities, or time-based permissions. | Records possible study extensions. | DEC-023. | Any implemented extension is disabled by default, documented, and tested separately. | Optional feature tests. | optional | Post-MVP only | Not part of SP-03 readiness. |

### Data and format requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| DAT-001 | `PROJECT_WIEGAND_26` shall contain bit 1 leading parity, bits 2–9 facility code, bits 10–25 credential number, and bit 26 trailing parity. | Freezes the project parser contract. | DEC-013; PRD-002; SRC-WIEGAND-001 for general concepts. | Reference encodings preserve all field widths and decode to their source values. | Encoder/decoder reference-vector tests. | required | SP-04–SP-06 | Exact allocation is a project decision. |
| DAT-002 | Leading parity shall make bits 1–13 even, and trailing parity shall make bits 14–26 odd. | Removes parity ambiguity. | DEC-013. | Exhaustive or representative vectors verify both parity equations and independent failure detection. | Unit tests over boundary and generated vectors. | required | SP-05–SP-06 | General parity concepts are externally supported; coverage is proposed. |
| DAT-003 | The reader-source label shall be stored separately from frame bits and shall not be inferred from facility or credential fields. | Separates RF category from controller message format. | CLM-021; DEC-012. | Identical frames tagged LF and HF decode identically while retaining distinct source metadata. | Paired-source deterministic tests. | required | SP-05–SP-06 | No RF physics is modeled. |
| DAT-004 | A credential record shall contain facility code 0–255, credential number 0–65535, Boolean `enabled`, unsigned 16-bit `floor_mask`, and an optional text label. | Defines the minimum authorization data. | DEC-016; DEC-015. | Boundary-valid records are accepted; out-of-range, wrong-type, or missing required fields are rejected. | Data-model unit tests. | required | SP-04–SP-06 | Persistence format is deferred. |
| DAT-005 | The logical credential key shall be the ordered composite `(facility_code, credential_number)`, and duplicate keys shall be rejected deterministically. | Prevents key ambiguity and silent replacement. | DEC-016. | Distinct tuples with equal arithmetic sums coexist; inserting an existing tuple yields a defined duplicate-key error with no database change. | Credential-database unit tests. | required | SP-05–SP-06 | Database data structure is deferred. |
| DAT-006 | Floor mask bit 0 shall authorize floor 1, bit 15 shall authorize floor 16, and values outside unsigned 16-bit range shall be rejected. | Freezes floor-permission mapping. | DEC-015. | Single-bit masks authorize only their mapped floors; negative and greater-than-65535 masks fail validation. | Exhaustive 16-floor mapping and range tests. | required | SP-04–SP-06 | Proposed data model, not product fact. |
| DAT-007 | Output state shall be represented as exactly 16 Boolean logical channels indexed consistently with floors 1–16. | Enables invariant checking. | DEC-014; DEC-017. | State serialization always contains 16 channels and never exposes an invalid channel index. | State-shape and boundary tests. | required | SP-04–SP-06 | Representation type is deferred. |

### Timing requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| TIM-001 | Logical output duration shall default to 3000 ms and accept configured integer values from 100 through 30000 ms inclusive. | Freezes a usable bounded timing parameter. | DEC-019; PRD-005. | Defaults and endpoints are accepted; non-integers and values outside the range are rejected before activation. | Configuration boundary tests. | required | SP-05–SP-06 | Proposed software value only. |
| TIM-002 | Output expiration, event timestamps, and watchdog expiration shall use an injectable or simulated monotonic time source. | Makes timing tests deterministic and fast. | SRC-TEST-001; DEC-019; DEC-020. | Tests advance logical time without wall-clock waiting and reproduce identical transitions. | Simulated-clock unit and integration tests. | required | SP-05–SP-06 | Calendar time is optional. |
| TIM-003 | The simulated watchdog timeout shall default to 2000 ms and expire when service is missed for that logical interval. | Freezes fault-recovery timing. | DEC-020; PRD-006. | At less than 2000 ms no watchdog reset occurs; at the deadline a single watchdog reset occurs. | Injected-time watchdog boundary test. | required | SP-05–SP-06 | Proposed model, not commercial timing. |

### Logging requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| LOG-001 | The simulator shall log valid grant, unauthorized-floor denial, unknown-credential denial, disabled-credential denial, invalid frame, parity failure, invalid floor, busy-controller denial, output timeout, manual reset, and watchdog reset events. | Makes every required decision and recovery observable. | SRC-AUTH-001; DEC-021. | Each listed scenario produces exactly one corresponding primary event with the expected result and reason. | Parameterized event-type tests. | required | SP-05–SP-06 | Product logging behavior remains unknown. |
| LOG-002 | Every event shall contain sequence number, simulated timestamp, event type, result, reason, and reader source, facility code, credential number, and requested floor when applicable or available. | Provides reproducible decision context. | DEC-021. | Schema validation succeeds for all events; unavailable conditional fields are explicitly null or omitted according to one later documented serialization rule. | Schema and end-to-end log tests. | required | SP-05–SP-06 | Final serialization choice is deferred. |
| LOG-003 | Event sequence numbers shall increase monotonically within a run, and event timestamps shall come from the simulated time source. | Supports ordering and deterministic replay. | DEC-021; TIM-002. | A multi-event scenario has strictly increasing sequence numbers and nondecreasing deterministic timestamps. | Integration and replay tests. | required | SP-05–SP-06 | Cross-run persistence is optional. |

### Reset and watchdog requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| RST-001 | Startup and manual reset shall set all 16 outputs inactive and place the controller in its initial idle state. | Defines the safe logical baseline. | DEC-011; DEC-020. | Startup inspection and reset from every modeled state show all outputs false and idle state active. | State-transition unit tests. | required | SP-04–SP-06 | “Safe” refers only to abstract output state. |
| RST-002 | Manual reset shall cancel any pending output timeout and log one `manual_reset` event. | Prevents stale activation after reset. | DEC-020; DEC-021. | Advancing time after reset cannot reassert or re-time-out the canceled output. | Simulated-time reset test. | required | SP-05–SP-06 | No physical reset circuit is modeled. |
| RST-003 | Invalid input shall not corrupt credentials, configuration, event ordering, time state, or the controller's ability to process the next valid request. | Ensures fault containment. | SRC-TEST-001; DEC-024. | After each invalid-input class, a known valid scenario produces its reference result without state repair. | Fault-injection sequence tests. | required | SP-05–SP-06 | Existing authorized activation follows FUN-014. |
| RST-004 | The test harness shall be able to trigger a simulated lockup or missed watchdog service, after which watchdog expiration shall deactivate all outputs, log one `watchdog_reset`, clear transient state, return to idle, and permit a later valid request. | Defines observable watchdog recovery. | SRC-STM32-001 and SRC-ARMADA-001 as representative concepts; DEC-020. | A fault scenario demonstrates the full reset sequence and successful post-reset request. | Watchdog fault-injection integration test. | required | SP-05–SP-06 | Does not claim a commercial watchdog implementation. |

### Nonfunctional requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | Identical input sequence, configuration, initial state, simulated-time schedule, and seed shall produce identical logical results and event content. | Enables reproducibility. | SRC-TEST-001; DEC-024. | Replaying a recorded scenario twice yields equal decisions, states, and normalized logs. | Deterministic replay test. | required | SP-05–SP-07 | Host timing metrics may vary. |
| NFR-002 | Software shall be divided into modules with separately testable responsibilities for frame handling, credentials, authorization, outputs, controller coordination, watchdog, logging, and interfaces. | Limits complexity and supports unit testing. | SRC-PLAN-001; conceptual modeling method. | Design review maps each responsibility to one module contract without cyclic behavior dependencies. | SP-05 design review and unit-test inventory. | required | SP-04–SP-06 | Detailed APIs are not defined in SP-03. |
| NFR-003 | The simulator and normal tests shall perform no network access and require no physical hardware. | Supports offline reproducibility. | DEC-011; SCP-005. | Tests pass with network unavailable and no device interfaces configured. | Environment-isolation test and dependency review. | required | SP-05–SP-07 | Download/install actions are setup, not normal execution. |
| NFR-004 | The implementation shall support Python 3.11 or later and shall prefer the Python standard library plus `pytest`. | Freezes a modest dependency policy. | Project-owner SP-03 instruction; DEC-024. | Project metadata declares Python >=3.11; runtime imports and test dependencies match the approved list. | Metadata and import/dependency inspection. | required | SP-05–SP-06 | No dependency is added during SP-03. |
| NFR-005 | All required unit and integration tests shall run through one documented `pytest` command with deterministic defaults. | Simplifies verification. | SRC-TEST-001. | The documented command collects and executes all required automated tests without manual interaction. | Clean-environment test execution. | required | SP-05–SP-07 | Coverage threshold is deferred. |
| NFR-006 | Generated test data shall be reproducible from a recorded seed or configuration identifier. | Makes experiments repeatable. | SRC-TEST-001; DEC-022. | Regeneration from the same identifier yields the same credential and request cases. | Data-generation checksum comparison. | required | SP-05–SP-07 | Cryptographic randomness is outside scope. |
| NFR-007 | Test and experiment results shall be exportable in a documented machine-readable CSV or JSON form. | Supports independent analysis. | DEC-021; DEC-022. | A schema-valid result file contains cases, outcomes, reasons, configuration identifier, and metric fields. | Schema validation and round-trip parsing. | required | SP-05–SP-07 | Final schema is detailed later. |
| NFR-008 | Project-authored text and data files shall use UTF-8 and repository-relative internal paths. | Supports portability and auditability. | SRC-WORKFLOW-001. | UTF-8 decoding succeeds and no generated project record requires an absolute local path. | Encoding and path scan. | required | SP-03–SP-08 | Baseline audit may record the repository root. |
| NFR-009 | Invalid input and configuration shall produce explicit deterministic errors or denial reasons without unhandled termination of a normal scenario. | Makes failure behavior observable. | SRC-TEST-001; DEC-024. | Required invalid cases return documented results, preserve invariants, and allow later processing. | Negative and recovery tests. | required | SP-05–SP-06 | Programmer defects are not required to be masked. |
| NFR-010 | A persistent local credential file may be added after the in-memory MVP is verified. | Allows a bounded usability extension. | DEC-023. | If implemented, its schema, error handling, and deterministic loading are tested independently. | Optional persistence tests. | optional | Post-MVP only | A database server is not required. |
| NFR-011 | A graphical or enhanced command-line interface may be added after required deliverables pass. | Records presentation options without expanding the core. | DEC-023. | If implemented, it calls the same tested controller interfaces and adds no authorization behavior. | Optional interface integration tests. | optional | Post-MVP only | A simple CLI demonstration remains required. |
| NFR-012 | Physical serial, GPIO, reader, or elevator adapters may be considered only after a separately approved scope change. | Prevents optional hardware from entering the MVP implicitly. | SCP-007; DEC-011. | No adapter is present in the MVP; any future adapter has new evidence, safety review, and requirements. | Scope and repository review. | optional | Outside current plan | Not authorized by SP-03. |

### Verification and experiment requirements

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| VER-001 | Every required requirement shall trace to at least one planned test, inspection, analysis, or review record. | Provides requirements-to-verification coverage. | SRC-TEST-001; DEC-024. | The traceability CSV contains one valid `planned` row per required ID and no unknown requirement ID. | Automated cross-file traceability check. | required | SP-03 and maintained through SP-07 | Passing tests are not claimed in SP-03. |
| VER-002 | Planned automated tests shall cover valid frame, invalid length, invalid bit value, leading parity error, trailing parity error, enabled credential, disabled credential, unknown credential, authorized floor, unauthorized floor, invalid floor, and busy controller. | Covers input and authorization behavior. | SRC-TEST-001; MVP freeze. | The later test inventory contains at least one case for every named category with expected result and output invariant. | Test-inventory review and pytest execution. | required | SP-05–SP-07 | Software-only cases. |
| VER-003 | Planned tests shall cover output activation, output timeout, manual reset, simulated watchdog reset, recovery, and event-log completeness. | Covers time and fault behavior. | SRC-TEST-001; DEC-019–DEC-021. | Each named category has controlled inputs, expected state transitions, and expected log records. | Simulated-time integration and fault tests. | required | SP-05–SP-07 | No wall-clock wait required. |
| VER-004 | Planned tests shall exercise both LF and HF source labels and deterministic replay. | Verifies dual-source metadata and reproducibility. | DEC-012; NFR-001. | Equivalent LF/HF cases retain their labels and repeated runs yield identical normalized logical outputs. | Parameterized source and replay tests. | required | SP-05–SP-07 | Does not compare RF technology performance. |
| VER-005 | Scalability experiments shall execute with credential counts of 10, 100, 1,000, and 10,000. | Provides a bounded database-size study. | DEC-022. | Each size produces a complete machine-readable result record under the same documented workload method. | Reproducible experiment script and result-schema validation. | required | SP-07 | No strict real-time target is imposed. |
| VER-006 | Experiments shall collect total processed cases, granted cases, denied cases by reason, validation failures, average processing time, median processing time, 95th-percentile processing time, throughput, credential count, and seed or configuration identifier. | Defines comparable quantitative outputs. | DEC-022. | Every required metric is present and internally reconciles with case totals; percentile method is documented later. | Automated result validation and analysis review. | required | SP-07 | Host timing is observational. |
| VER-007 | Unit, integration, timing, scalability, and fault verification shall run without physical hardware and shall preserve controlled inputs, expected results, actual results, and evaluation status. | Implements the literature-supported verification method. | SRC-TEST-001. | Each verification record identifies category, input/configuration, expected result, actual result, and pass/fail evaluation. | Test-report schema review. | required | SP-05–SP-07 | Formal verification is optional. |
| VER-008 | Reports shall state the Python version, host/test environment, configuration identifier, workload, and interpretation limits for every timing or throughput result. | Prevents software measurements from becoming product claims. | SRC-TEST-001; LIM-004. | Each published performance table or plot has the required environment and limitation metadata. | Result and report inspection. | required | SP-07–SP-08 | No commercial or physical performance inference. |
| VER-009 | Additional experiment sizes or protocol profiles may be evaluated after all required experiment records are complete. | Permits bounded extension. | DEC-023. | Optional results are labeled separately and do not replace the required four sizes. | Optional result review. | optional | Post-MVP only | Must not delay required analysis. |

### Limitations and prohibited interpretations

| ID | Requirement statement | Rationale | Evidence or decision basis | Acceptance criteria | Planned verification method | Priority | Implementation stage | Notes or limitation |
|---|---|---|---|---|---|---|---|---|
| LIM-001 | Project artifacts shall identify `PROJECT_WIEGAND_26`, the floor mask, timing values, watchdog behavior, event schema, and busy policy as proposed project decisions rather than commercial-product facts. | Preserves evidence classification. | DEC-006; DEC-013–DEC-021. | Terminology review finds a project-choice qualification at each substantive use. | Targeted text search and manual review. | required | All stages | Product implementation remains unknown. |
| LIM-002 | No project requirement or result shall claim that the commercial controller uses ARM, STM32, Wiegand, Wiegand-26, LF, HF, 125 kHz, 13.56 MHz, MIFARE, ISO 14443, NFC, a relay, or any voltage or output rating. | Prevents unsupported product attribution. | DEC-002; UNK-004; UNK-006; UNK-007. | Targeted terminology review finds only qualified unknown, external-source, or proposed-model statements. | Automated search plus manual context review. | required | All stages | Direct future evidence would require controlled revision. |
| LIM-003 | The simulator shall not model or claim control of physical elevator wiring, movement, motors, brakes, doors, passenger-safety systems, mains power, certification, compliance, or installation. | Maintains the physical safety boundary. | DEC-008; DEC-011. | Requirements, diagrams, code, tests, and results contain no physical-control interface or claim. | Scope and terminology review. | required | All stages | Physical integration remains a blocking gap for such claims. |
| LIM-004 | Timing, throughput, scalability, reset, and watchdog results shall be described only as behavior of the Python software model in its recorded test environment. | Prevents invalid generalization. | SRC-TEST-001; software-only limitation. | Result captions and conclusions contain the model/environment qualification and no hardware equivalence language. | Report and result review. | required | SP-07–SP-08 | No safety, certification, or field-reliability claim. |

## Deliverable scope freeze

Required final-project deliverables:

- existing evidence and literature records;
- this requirements document and traceability matrix;
- system context diagram;
- conceptual architecture;
- proposed register and state model;
- Python simulator;
- simple command-line demonstration;
- automated unit and integration tests;
- watchdog and fault-injection tests;
- reproducible experiment script;
- machine-readable result data;
- summary plots and tables;
- final engineering report;
- presentation; and
- reproducibility instructions.

Optional unless later approved:

- GUI;
- physical prototype or real RFID reader;
- database server;
- network or cloud service;
- mobile application;
- cryptographic card emulation;
- physical elevator interface;
- safety certification; and
- exact commercial-board reproduction.

## Human-review decisions

Human review must confirm:

- working title;
- `PROJECT_WIEGAND_26` field and parity layout;
- floor numbering and mask convention;
- 3000 ms default output duration and 100–30000 ms range;
- 2000 ms watchdog timeout;
- one-output-at-a-time and `controller_busy` policy;
- abstract software-only elevator boundary;
- required and optional deliverables; and
- whether any optional feature is later authorized.
