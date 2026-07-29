# Literature Notes

## Purpose and scope

These notes are a topic-organized evidence map for later stages, not final report prose. `external_technical_evidence` explains a source's stated scope only. It never establishes a property of the commercial card.

## Evidence-use rules

- Preserve the source's scope and identify its exact chapter, section, or page.
- Use product facts only from `evidence/product_evidence.md`.
- Label a later simulator choice as `proposed_reference_design`; label a product gap as `unknown_or_unresolved`.
- No local source is used to infer a particular reader protocol, processor, electrical output, or elevator interface for the commercial card.

## LIT-01 RFID fundamentals

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-001 | An RFID system includes an RF subsystem with tags and readers and commonly an enterprise subsystem that stores, processes, or analyzes reader-acquired data. Passive tags use energy received from a reader transmission to reply. | `SRC-RFID-001`, §§2.2–2.3.1, pp.2-2–2-5. | NIST government technical guidance for general RFID systems. | Define credential/tag, reader, and backend-processing roles and passive operation. | The source describes general RFID systems; it does not identify the commercial card's frequency, tag type, reader interface, or backend. | external_technical_evidence |

## LIT-02 125 kHz systems

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-002 | NIST treats operating frequency and identifier format as distinct tag characteristics and lists 125/134 kHz as common US LF RFID frequencies. | `SRC-RFID-001`, §2.3.1.1 pp.2-3–2-4; §2.3.1.3 and Table 2-1, pp.2-5–2-7. | NIST government technical guidance for general RFID systems. | Explain LF as a technology class and separate RF frequency from encoded identifiers or controller messages. | No 125 kHz capability or tag standard is attributed to the commercial product. | external_technical_evidence |

## LIT-03 13.56 MHz systems

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-003 | NIST lists 13.56 MHz within the HF technology class and discusses operating frequency separately from identifier formats, functionality, and security mechanisms. | `SRC-RFID-001`, §2.3.1 and Table 2-1, pp.2-3–2-7. | NIST government technical guidance for general RFID systems. | Provide minimum HF background without an exhaustive smart-card protocol comparison. | No 13.56 MHz, MIFARE, ISO/IEC 14443, NFC, or cryptographic capability is attributed to the commercial product. | external_technical_evidence |

## LIT-04 Wiegand signaling

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-004 | BALTECH documents Wiegand as a read-only connection from a card reader to an access-control system; card data is transmitted as asynchronous low pulses on D0 for zero bits and D1 for one bits. | `SRC-WIEGAND-001`, “Wiegand specification” and “Data wires.” | Official manufacturer documentation for BALTECH reader firmware. | Support the initial reader-input pulse model. | Implementation-specific timing or electrical values are not generalized, and commercial-product Wiegand support remains unknown. | external_technical_evidence |
| LN-005 | BALTECH documents configurable message length, standard frames with leading even and trailing odd parity, and raw frames without parity, demonstrating that Wiegand framing can vary. Wiegand-26 remains the project's proposed initial format. | `SRC-WIEGAND-001`, “Message size” and “Frame format”; `PRD-002`. | Manufacturer implementation evidence plus a proposed project choice. | Support length/parity validation and record the Wiegand-26 selection boundary. | The BALTECH page does not define the project's exact 26-bit field allocation; Wiegand-26 is not verified product behavior. | proposed_reference_design |

## LIT-05 Embedded-controller architecture

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-006 | RM0008 organizes the documented STM32F10xxx family around memory/bus architecture, memory organization, memory mapping, and boot configuration. | `SRC-STM32-001`, ch.3, pp.48–61. | Manufacturer manual for STM32F10xxx. | Representative controller-architecture explanation. | Not evidence of commercial-card hardware. | external_technical_evidence |
| LN-007 | The ADS guide treats system initialization, ROM memory-map considerations, and memory-mapped I/O as embedded-development topics. | `SRC-ARM-001`, ch.6 §§6.1–6.9. | ARM ADS developer guide. | Representative startup and memory-map rationale. | Historical tool-suite context; not STM32 or product proof. | external_technical_evidence |

## LIT-06 ARM concepts

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-008 | The ARMv7-A/R manual distinguishes application-level, system-level, and debug views, and describes instruction sets, exceptions, and memory-model concepts for A/R profiles. | `SRC-ARM-002`, Preface “About this manual,” pp.xiv–xv. | ARMv7-A/R architecture manual. | Terminology and scope discipline. | It explicitly points to a separate ARMv7-M manual; it is not a Cortex-M or STM32 manual. | external_technical_evidence |
| LN-009 | The ARM University material presents registers, status flags, processor modes, and exception-vector concepts as ARM instruction-set background. | `SRC-ARM-003`, pp.2–10. | Educational ARM material; metadata incomplete. | Accessible supporting explanation, if cross-checked. | Do not use alone for high-stakes technical claims or for the commercial product. | external_technical_evidence |
| LN-010 | The supplementary instruction-set PDF organizes branch, condition-field, status-register, and load/store material in chapter 4. | `SRC-ARM-004`, §§4.1–4.11. | Supplementary technical material; metadata incomplete. | Narrow terminology support. | Not a product source; bibliography metadata requires verification. | external_technical_evidence |

## LIT-07 STM32 reference architecture

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-011 | RM0008 documents reset/clock control, GPIO/alternate functions, and an NVIC for its STM32F10xxx family. | `SRC-STM32-001`, ch.7 pp.90–121; ch.9 pp.159–175; ch.10.1 p.196. | Manufacturer manual for STM32F10xxx. | Representative peripheral and initialization concepts. | STM32 is a reference architecture only; the commercial processor is unknown. | external_technical_evidence |
| LN-012 | RM0008 documents timers, independent and window watchdog chapters, and USART chapters for the STM32F10xxx family. | `SRC-STM32-001`, chs.14–15 pp.292–405; ch.19 p.485; ch.20 p.491; ch.27 p.770 onward. | Manufacturer manual for STM32F10xxx. | Representative timing, recovery, and serial-peripheral concepts. | Does not establish commercial-card timers, watchdog, or serial interfaces. | external_technical_evidence |

## LIT-08 Credential storage and authorization

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-013 | NIST PE-2 calls for authorization credentials and an approved access list; PE-3 calls for verifying individual authorization before granting access and maintaining physical-access audit logs. | `SRC-AUTH-001`, PE-2 pp.167–168 and PE-3 pp.168–172. | NIST government control guidance for organizational physical access. | Support a credential lookup, grant/deny decision boundary, and event logging in the proposed model. | A local lookup table, denial rule, and log schema are project design choices; none is attributed to the commercial product. | external_technical_evidence |
| LN-014 | A 16-bit floor-permission mask is a potential later project model, not a verified product feature. | `PRD-001`; `evidence/assumptions_and_unknowns.md`. | Proposed reference-design boundary. | Future simulator data-model choice. | Requires requirements approval and suitable external evidence. | proposed_reference_design |

## LIT-09 Elevator access-control integration

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-015 | The project scope treats the studied card as an access-authorization layer and excludes elevator motion, braking, door, and passenger-safety control. | `SRC-PLAN-001`, §§3.2–3.3. | Project-authoritative safety boundary. | Scope and model limitations. | This is not a statement about the commercial card's actual interface. | engineering_inference |
| LN-016 | Physical elevator integration remains outside the software-project scope. The simulator will expose only an abstract 16-floor permission output and will not specify wiring or control motors, brakes, doors, or passenger-safety functions. | `DEC-008`; `docs/decision_log.md`. | Controlled project scope decision requiring owner/supervisor approval. | Bound the later requirements and software model. | An authoritative elevator-integration source remains desirable for final-report context and mandatory for any physical integration claim. | proposed_reference_design |

## LIT-10 Reliability and fault handling

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-017 | RM0008 provides a representative family-specific basis for reset/clock, timer, and watchdog concepts. | `SRC-STM32-001`, ch.7; chs.14–15; chs.19–20. | Manufacturer manual for STM32F10xxx. | Reference-model reliability rationale. | It does not define project fail-safe behavior or certify any product. | external_technical_evidence |
| LN-018 | The ARMADA functional specification illustrates counters, reload behavior, interrupts, and watchdog-trigger effects in a documented SoC. | `SRC-ARMADA-001`, ch.8, pp.95–97. | Marvell ARMADA 38x functional specification. | Example of functional-specification documentation. | Unrelated SoC; not proposed project hardware. | external_technical_evidence |
| LN-019 | Authoritative terminology for fail-safe and fail-secure remains missing locally. | `SRC-MISSING-007`; `evidence/unresolved_sources.md`. | Unresolved source gap. | Future reliability terminology. | Do not use these terms as if their application-specific meaning has been established. | unknown_or_unresolved |

## LIT-11 Software simulation and verification

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-020 | The workflow handbook requires evidence hierarchy, bounded work, missing-input records, validation, and readiness decisions. | `SRC-WORKFLOW-001`, §§3, 5, 6, 11. | Project governance handbook. | Project process and validation discipline. | It is not an authoritative software-testing methodology. | external_technical_evidence |
| LN-021 | The example academic project’s table of contents illustrates separating requirements, theory, planning, implementation, tests, results, conclusions, appendices, and references. | `SRC-ACADEMIC-001`, table of contents pp.4–6. | Illustrative academic example. | Report organization only. | Unrelated project; do not copy technical claims or prose. | external_technical_evidence |
| LN-022 | NASA guidance links software requirements to verification, identifies unit and integration test levels, and expects controlled inputs, expected outputs, repeatable procedures, recorded results, and evaluation against criteria. | `SRC-TEST-001`, SWE-052 §§1–2; SWE-062; SWE-065 §§1–3; SWE-068 §§1–3. | Official NASA software-engineering guidance. | Support traceable, repeatable unit and integration testing of the simulator. | Project-specific acceptance criteria must still be defined; software results do not establish physical-hardware performance. | external_technical_evidence |

## Cross-source terminology

- *Product evidence* identifies what is directly preserved about the item; *external technical evidence* explains an external source; *engineering inference* interprets within project scope; and *proposed reference design* is a future project decision.
- “ARMv7-A/R” and “ARMv7-M/Cortex-M” must remain distinct. `SRC-ARM-002` is not an STM32 Cortex-M source.
- Carrier frequency, credential technology, reader-to-controller signaling, and simulator message format are separate concepts. No local source links any of them to the commercial card.

## Source conflicts and variants

- The ARMv7-A/R manual explicitly has A/R scope, while RM0008 references a separate Cortex-M3 programming manual. They are complementary only at a high conceptual level, not interchangeable architecture references.
- RFID frequency, identifier format, and reader-to-controller Wiegand framing are separate layers. Detailed RFID and Wiegand variants remain deferred, while Wiegand-26 is selected only as the proposed first simulator format.

## Missing literature

See `evidence/unresolved_sources.md` for every missing domain and recommended source type.

## Prohibited product-specific conclusions

Do not conclude that the commercial card uses ARM, STM32, STM32F103, Wiegand, Wiegand-26, 125 kHz, 13.56 MHz, MIFARE, ISO/IEC 14443, NFC, a relay, a particular output rating, a particular storage method, or a particular elevator interface. Its processor, protocol support, electrical characteristics, and firmware remain unknown.
