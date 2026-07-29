# Literature-Review Outline

This controlled outline maps later report sections to evidence; it is not final report prose.

| Planned section | Purpose and claims to support | Source IDs | Unresolved needs / product limitation | Relationship to later work |
|---|---|---|---|---|
| 1. Evidence-led study framing | Explain why the project separates product evidence from reference design. | SRC-PLAN-001, SRC-WORKFLOW-001, SRC-PRODUCT-001, SRC-PRODUCT-002 | No listing content supports technical product claims. | Constrains requirements and architecture. |
| 2. RFID foundations | Define tag, reader, controller, passive identification, and identifier-security limits. | none locally adequate | SRC-MISSING-001. No RFID technology is assigned to the product. | Needed before protocol-related requirements. |
| 3. LF and HF RFID technology classes | Contrast 125 kHz and 13.56 MHz technologies without conflating frequency and protocol. | none locally adequate | SRC-MISSING-002, SRC-MISSING-003. No tag standard or card capability is verified. | Needed before reader/credential assumptions. |
| 4. Reader-to-controller signaling | Explain Wiegand concepts and variants if an authoritative source is obtained. | none locally adequate; PRD-002 only as project boundary | SRC-MISSING-004. Wiegand-26 is not product evidence. | Needed before selecting a simulator input format. |
| 5. Representative embedded-controller concepts | Explain memory mapping, initialization, GPIO, interrupts, timers, serial interfaces, reset, and watchdogs. | SRC-STM32-001, SRC-ARM-001 | STM32/ARM are reference sources only. | Provides rationale for a later reference architecture. |
| 6. ARM terminology and scope | Clarify registers, load/store, branches, exceptions, and A/R versus M-profile scope. | SRC-ARM-002, SRC-ARM-003, SRC-ARM-004 | ARMv7-A/R is not STM32 Cortex-M documentation and proves nothing about the product. | Prevents scope errors in architecture rationale. |
| 7. Credential storage and authorization | Support credential records, decisions, permissions, logging, and integrity. | PRD-001 is a future choice only | SRC-MISSING-005; product behavior unknown. | Needed before authorization requirements. |
| 8. Conceptual elevator access integration | Describe access authorization boundary and inactive/denial model without safety or motion control. | SRC-PLAN-001 | SRC-MISSING-006; no direct motor, brake, door, or safety claim. | Bounds later context/architecture work. |
| 9. Reliability and verification | Support reset, watchdog, deterministic timing, fault records, and simulation evaluation boundaries. | SRC-STM32-001, SRC-ARMADA-001, SRC-WORKFLOW-001 | SRC-MISSING-007 and SRC-MISSING-008. No certification or physical-performance claim. | Needed before test methodology and simulator verification. |
| 10. Report method and structure | Explain evidence classification and plan a traceable academic report. | SRC-WORKFLOW-001, SRC-ACADEMIC-001 | SRC-MISSING-009 for formal university rules. | Guides later report organization only. |
