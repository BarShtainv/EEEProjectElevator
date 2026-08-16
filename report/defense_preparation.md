# Defense Preparation — Final Project Controlled Floor Elevator

This file is a private study aid. Answers should be delivered in the student's own words and adjusted to the examiner's question.

## Ten likely examiner questions and model answers

### 1. What is the actual engineering contribution?

I specified, architected, implemented, verified, and quantitatively evaluated a deterministic software reference model for a 16-floor credential-based elevator access-authorization layer. The contribution integrates strict credential-frame validation and decoding, composite-key credential lookup, a 16-bit floor-permission model, authorization decisions, single timed logical output activation, busy handling, structured logging, deterministic simulated time, reset, watchdog recovery, automated tests, and reproducible experiments. It is a software authorization model, not a physical elevator controller.

### 2. Why was a Python simulation acceptable for this project?

The engineering question was whether a precisely defined authorization design behaves correctly under controlled inputs and faults. Python allowed deterministic modeling, rapid execution of boundary cases, injected time without real waiting, and traceability from requirements to automated tests. This is adequate evidence for the software contracts that were defined. It is not adequate evidence for RF reception, electrical outputs, real-time timing, elevator integration, or passenger safety; those would require hardware and separate validation.

### 3. Why were 16 floors selected, and how are permissions represented?

Sixteen floors were the frozen project size. A 16-bit unsigned mask represents permission compactly: floor 1 maps to bit 0 and floor 16 maps to bit 15. The authorization function validates a floor in the range 1–16, shifts by `floor - 1`, and checks whether that bit is set. All 16 mappings and the mask limits were tested. The mapping is a project design choice, not an inferred property of the commercial product.

### 4. Explain the 26-bit credential profile.

`PROJECT_WIEGAND_26` is a project-defined profile. Bit 1 is leading parity; bits 2–9 contain an 8-bit facility code; bits 10–25 contain a 16-bit credential number; and bit 26 is trailing parity. The `LF` or `HF` source label is separate metadata and is not encoded in these bits. The profile uses familiar Wiegand-style framing concepts, but it is not claimed to match the motivating controller.

### 5. How is parity checked, and what does it detect?

Leading parity is selected so bits 1–13 contain an even number of ones. Trailing parity is selected so bits 14–26 contain an odd number of ones. The decoder checks exact frame length, binary membership, and both parity equations before extracting the fields. The tests independently corrupt the covered regions and verify rejection. Parity detects many frame errors, especially any single-bit error in the covered bits, but it is not cryptographic authentication and cannot detect every possible multi-bit corruption.

### 6. Why does busy handling take precedence over input inspection?

The model permits at most one active output. When an output is active, a new request is denied immediately as `controller_busy`, before source, frame, or floor inspection. This preserves the original output and expiry and prevents a second request—valid, invalid, or even hostile—from replacing or extending the active authorization. The precedence also makes the concurrency policy deterministic and easy to verify.

### 7. What does the watchdog simulate?

It simulates a controller-supervision contract using monotonic logical time. With normal heartbeat service, the watchdog deadline moves forward. Fault injection can suppress service; at the deadline, one reset request clears outputs and transient state, records the recovery event, reinitializes the watchdog, and returns the model to idle while preserving valid configuration, credentials, and earlier events. This demonstrates the project-defined software recovery behavior only. It does not prove MCU watchdog behavior, physical fail-safe operation, or reliability.

### 8. What do the correctness results demonstrate?

They demonstrate exact agreement with the defined deterministic workloads. The mixed experiment accounted for all 39,000 requests: 15,600 grants, 19,500 denials, 3,900 invalid frames, and no other outcomes. The isolated lookup matrix processed 12,000 calls with 6,000 correct hits, 6,000 correct misses, and zero mismatches. The isolated authorization matrix processed 12,000 calls with 4,800 correct grants, 6,000 correct denials, 1,200 correct invalid-floor errors, and zero incorrect authorization outcomes. Together with 976 passing implementation-milestone tests and full required-requirement traceability, this supports conformance for the tested model and cases.

### 9. What do the timing results prove—and what do they not prove?

They provide reproducible observations for three defined Python operation boundaries on one recorded host. Each size has exactly three measured repetition-level averages, using `time.perf_counter_ns`. The results show modest, non-monotonic variation across the four repository sizes. They do not establish statistical significance, constant-time or asymptotic complexity, a deadline, real-time performance, physical-controller performance, or commercial-product performance. The three operation families must not be ranked directly because they measure different work.

### 10. Why are ARM, STM32, and ARMADA manuals cited if the commercial MCU is unknown, and what would be needed for hardware?

Those manuals are representative technical literature for concepts such as memory maps, initialization, GPIO, timers, interrupts, reset, and watchdogs, and for how an embedded architecture is documented. They are not evidence that the commercial controller contains an ARM or STM32 device; ARMv7-A/R material is also not Cortex-M documentation. A hardware stage would need selected components, electrical requirements, reader-interface characterization, output-driver and isolation design, schematics, PCB or prototype implementation, instrumentation, hardware-in-the-loop tests, and an appropriately supervised elevator-interface and safety scope.

## Five project strengths

1. The engineering boundary is precise: authorization is separated from elevator motion and passenger-safety functions.
2. The design is deterministic and modular, with explicit ownership of credential, output, event, clock, watchdog, and controller state.
3. Every required requirement is traceable to executed verification, including boundary, failure, integration, and recovery cases.
4. Correctness totals reconcile exactly across mixed and isolated experiments, with preserved configurations and result artifacts.
5. Claims are disciplined: commercial-product unknowns, representative literature, host timing, and software-only evidence are not overstated.

## Five limitations to acknowledge confidently

1. The implementation is host software; no physical RFID reader, card, controller board, output circuit, or elevator interface was tested.
2. The `LF` and `HF` labels, 26-bit frame, floor mask, watchdog, and logical outputs are project-defined abstractions, not recovered commercial behavior.
3. Timing data come from one host and only three measured repetitions per size; raw per-call samples were not retained.
4. The workloads are deterministic constructed cases, so zero mismatches are not a field error rate or reliability estimate.
5. No real-time, electrical, security-hardening, safety, certification, production-readiness, or commercial-equivalence conclusion is supported.

## Two-minute project explanation

The project addresses floor-selective elevator access as an authorization problem. A credential must be validated and decoded, its record located, the requested floor checked against that record's permissions, and one permission output activated for a limited time. I deliberately separated that function from elevator motion, doors, brakes, and passenger-safety control.

I designed and implemented a deterministic Python reference model for 16 floors. It supports a project-defined 26-bit credential frame with parity, separate logical LF and HF source labels, composite facility-code and credential-number lookup, a 16-bit floor mask, explicit grant and denial reasons, one active logical output, busy-request precedence, structured events, simulated time, reset, and watchdog recovery.

Verification was requirement-driven. All 60 required requirements are mapped to tests, and the implementation milestone collected and passed 976 tests. The quantitative evaluation then reconciled 39,000 mixed controller requests plus 24,000 isolated lookup and authorization operations. The isolated experiments produced zero mismatches against their constructed expected outcomes. Timing was measured at four repository sizes on one host with three repetitions per size.

The result is a reproducible and testable authorization reference design. Its boundary matters: it is not a physical RFID system, does not operate an elevator, does not prove real-time or safety behavior, and is not claimed to reproduce the commercial controller.

## Five-minute technical explanation

The model begins after physical signal acquisition. Each request contains one complete 26-bit frame, a logical source label, and a requested floor. The frame profile allocates one leading parity bit, eight facility-code bits, sixteen credential-number bits, and one trailing parity bit. Leading parity makes bits 1–13 even; trailing parity makes bits 14–26 odd. Validation rejects the wrong length, nonbinary values, or parity failures before decoding. The reader-source label remains separate because RF frequency cannot be inferred from the credential bits.

Decoded identity is the ordered pair `(facility_code, credential_number)`. The in-memory repository validates all records before publication and rejects duplicate keys. Each record contains an enabled flag and an unsigned 16-bit floor mask. Authorization validates the floor and checks bit `floor - 1`. Unknown, disabled, invalid-floor, unauthorized-floor, busy, validation-error, and grant outcomes are distinct and observable.

The controller is an orchestrator rather than a single stateful monolith. The repository owns credentials, the output manager owns the 16-channel state and expiry, the event log owns immutable records and sequence allocation, and the watchdog owns its service deadline. A grant event must be appended successfully before activation, so a logging fault cannot create an unrecorded grant. At most one output can be active. A request received during activation is rejected as busy without inspecting its fields and without changing the original expiry.

Time is an injected monotonic integer clock. The scheduler jumps between the next heartbeat, watchdog deadline, and output expiry rather than waiting in real time. At a shared timestamp, heartbeat service is handled first, watchdog expiry second, and output expiry third. Suppressing heartbeat service causes the watchdog to request one reset at its deadline. Runtime reset clears outputs, expiry, request transients, and fault suppression while preserving validated configuration, credentials, prior events, and event-sequence progression.

Verification combines unit, integration, end-to-end, fault-injection, experiment, and inspection tests. The frozen implementation milestone passed all 976 collected tests, and all 60 required requirements are verified. The mixed quantitative workload processed 39,000 requests and reconciled every grant, denial, and invalid frame. Isolated lookup and authorization each processed 12,000 calls, with zero mismatches against the constructed cases.

For performance, `time.perf_counter_ns` measured three distinct public software boundaries at repository sizes 10, 100, 1,000, and 10,000. There was one warm-up and three measured repetitions. Mixed controller processing includes more work than direct lookup or authorization, so the operation families cannot be ranked as equivalent benchmarks. The observed values are non-monotonic, which is plausible in a host interpreter affected by scheduling, caching, and runtime state, but the data do not identify a cause. With one host, three repetition aggregates, and no raw per-call samples, the correct conclusion is a bounded observation—not statistical significance, complexity proof, real-time performance, or hardware timing.

The next engineering stage would be a separately scoped hardware prototype: characterize or select a reader interface, define electrical requirements, design protected input and isolated output stages, choose a controller, implement persistent storage as needed, and conduct hardware-in-the-loop verification. Any connection to an elevator or passenger-safety system would require specialist supervision, new safety requirements, and independent validation.
