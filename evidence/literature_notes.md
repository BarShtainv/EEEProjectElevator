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
| LN-001 | No local authoritative source presently supports a technical explanation of RFID system components, passive identification, credential identifiers, or identifier-only security limits. | `SRC-MISSING-001`; `evidence/unresolved_sources.md` | Unresolved source gap. | Background literature. | Do not substitute product URL or a general embedded manual. | unknown_or_unresolved |

## LIT-02 125 kHz systems

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-002 | Local material does not establish low-frequency RFID read range, data rate, tag standard, credential behavior, or security properties. | `SRC-MISSING-002`; `evidence/unresolved_sources.md` | Unresolved source gap. | Technology-class background. | No 125 kHz capability is attributed to the commercial card. | unknown_or_unresolved |

## LIT-03 13.56 MHz systems

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-003 | Local material does not support a technical comparison of HF RFID, smart-card protocols, cryptographic capabilities, or interoperability. | `SRC-MISSING-003`; `evidence/unresolved_sources.md` | Unresolved source gap. | Technology-class background. | No MIFARE, ISO/IEC 14443, NFC, or other standard is attributed to the commercial card. | unknown_or_unresolved |

## LIT-04 Wiegand signaling

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-004 | No local authoritative source is available for D0/D1 pulse conventions, framing, parity, variants, or error handling. | `SRC-MISSING-004`; `evidence/unresolved_sources.md` | Unresolved source gap. | Reader-to-controller background and later simulator rationale. | Wiegand support and Wiegand-26 support remain unknown for the commercial card. | unknown_or_unresolved |
| LN-005 | Wiegand-26 may be selected later as an initial simulator input format, but it is a project choice requiring authoritative protocol literature before implementation. | `PRD-002`; `evidence/assumptions_and_unknowns.md` | Proposed reference-design boundary. | Future simulator scope only. | Not verified product evidence. | proposed_reference_design |

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
| LN-013 | A credential record, enable/disable state, permission mask, denial path, audit record, and integrity mechanism are not yet supported by a local access-control authority. | `SRC-MISSING-005`; `evidence/unresolved_sources.md`. | Unresolved source gap. | Future authorization and storage rationale. | No such behavior is attributed to the commercial product. | unknown_or_unresolved |
| LN-014 | A 16-bit floor-permission mask is a potential later project model, not a verified product feature. | `PRD-001`; `evidence/assumptions_and_unknowns.md`. | Proposed reference-design boundary. | Future simulator data-model choice. | Requires requirements approval and suitable external evidence. | proposed_reference_design |

## LIT-09 Elevator access-control integration

| Note ID | Paraphrased statement | Source / location | Authority and scope | Planned report use | Limitation | Evidence class |
|---|---|---|---|---|---|---|
| LN-015 | The project scope treats the studied card as an access-authorization layer and excludes elevator motion, braking, door, and passenger-safety control. | `SRC-PLAN-001`, §§3.2–3.3. | Project-authoritative safety boundary. | Scope and model limitations. | This is not a statement about the commercial card's actual interface. | engineering_inference |
| LN-016 | No local authoritative elevator-integration or safety source is available to support interface, isolation, fail-safe, or floor-enable practice. | `SRC-MISSING-006`; `evidence/unresolved_sources.md`. | Unresolved source gap. | Future integration literature. | No direct motor, brake, door, or safety-control design may be proposed here. | unknown_or_unresolved |

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
| LN-022 | No local authoritative software-verification source supports a later detailed testing methodology. | `SRC-MISSING-008`; `evidence/unresolved_sources.md`. | Unresolved source gap. | Future verification-method section. | Simulation results must not be presented as physical-hardware performance. | unknown_or_unresolved |

## Cross-source terminology

- *Product evidence* identifies what is directly preserved about the item; *external technical evidence* explains an external source; *engineering inference* interprets within project scope; and *proposed reference design* is a future project decision.
- “ARMv7-A/R” and “ARMv7-M/Cortex-M” must remain distinct. `SRC-ARM-002` is not an STM32 Cortex-M source.
- Carrier frequency, credential technology, reader-to-controller signaling, and simulator message format are separate concepts. No local source links any of them to the commercial card.

## Source conflicts and variants

- The ARMv7-A/R manual explicitly has A/R scope, while RM0008 references a separate Cortex-M3 programming manual. They are complementary only at a high conceptual level, not interchangeable architecture references.
- Wiegand framing, RFID frequency, and credential-protocol variants cannot be resolved from local sources; no preferred variant is selected.

## Missing literature

See `evidence/unresolved_sources.md` for every missing domain and recommended source type.

## Prohibited product-specific conclusions

Do not conclude that the commercial card uses ARM, STM32, STM32F103, Wiegand, Wiegand-26, 125 kHz, 13.56 MHz, MIFARE, ISO/IEC 14443, NFC, a relay, a particular output rating, a particular storage method, or a particular elevator interface. Its processor, protocol support, electrical characteristics, and firmware remain unknown.
