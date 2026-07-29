# Assumptions and Unknowns

This register separates inference and potential future choices from product facts. No item below establishes a property of the commercial card.

## Engineering inferences

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| INF-001 | engineering inference | The card is being studied as an access-authorization layer, not as elevator motion or passenger-safety control. | Project scope in `final_engineering_project_plan.md`; project-owner authorization of DEC-008 for SP-03. | Preserves the project safety boundary. | Supervisor-approved scope change or authoritative product documentation for a broader claim. | owner-authorized study boundary; supervisor confirmation pending | Non-blocking for the software model; blocks every physical motion or safety claim. |

## Possible future reference-design elements

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| PRD-001 | possible proposed-design element | The proposed model uses 16 abstract floor-permission channels and a 16-bit permission mask, with floor 1 at bit 0 and floor 16 at bit 15. | Project title and plan; DEC-008, DEC-014, and DEC-015. | Bounds simulator scope and authorization data. | Human review of `docs/requirements.md`. | frozen proposed design for review | Non-blocking for SP-04; not verified product behavior. |
| PRD-002 | possible proposed-design element | The proposed simulator uses `PROJECT_WIEGAND_26`: leading even parity, 8-bit facility code, 16-bit credential number, and trailing odd parity with the coverage defined in DEC-013. | SRC-WIEGAND-001 supports general signaling/framing/parity; DEC-013 supplies the project field allocation. | Provides a testable initial input profile. | Human approval of DEC-013 and later implementation verification. | frozen proposed design for review | Non-blocking for SP-04; product support and universal compatibility remain unknown. |
| PRD-003 | possible proposed-design element | STM32F10xxx may be used later as a representative reference architecture for explaining embedded-controller concepts. | The local RM0008 manual has suitable documented scope; no product evidence identifies an STM32. | Makes source scope explicit. | Approved requirements and continued citation discipline. | reference-only; not a hardware selection | Non-blocking for literature architecture. |
| PRD-004 | possible proposed-design element | The working title is “Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller.” | SP-03 project-owner instruction and DEC-010. | Stabilizes current project terminology. | Supervisor confirmation or an approved replacement title. | project-owner approved; supervisor approval pending | Non-blocking for technical work; blocks final title approval. |
| PRD-005 | possible proposed-design element | The proposed logical output duration defaults to 3000 ms and accepts configured values from 100 through 30000 ms. | SP-03 project-owner instruction and DEC-019. | Defines deterministic timed-output behavior. | Human review and later simulated-time tests. | frozen proposed design for review | Non-blocking for architecture; not a product timing fact. |
| PRD-006 | possible proposed-design element | The proposed simulated watchdog timeout defaults to 2000 ms and produces an all-inactive reset to idle after missed service. | Representative external watchdog concepts; SP-03 instruction; DEC-020. | Defines software fault-recovery behavior. | Human review and later fault-injection tests. | frozen proposed design for review | Non-blocking for architecture; not a product implementation claim. |
| PRD-007 | possible proposed-design element | The simulator exposes only abstract 16-floor permission outputs and excludes physical elevator wiring, motors, brakes, doors, movement, passenger-safety logic, mains wiring, physical relays, certification, and installation. | DEC-008 and DEC-011; project-owner authorization for SP-03. | Preserves the software-only safety boundary. | Supervisor confirmation before final submission; new approval and evidence for any expansion. | owner-authorized scope freeze; supervisor confirmation pending | Non-blocking for software work; blocking for every physical-integration claim. |

## Unknowns

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| UNK-001 | unknown | Exact manufacturer. | No preserved manufacturer documentation or readable product evidence. | Provenance and support. | Authoritative manufacturer record or preserved seller statement. | unresolved | Blocks manufacturer-specific claims. |
| UNK-002 | unknown | Exact model and revision. | No readable listing content, label, or image. | Configuration and compatibility. | Readable label, authoritative listing, or manufacturer document. | unresolved | Blocks model-specific claims. |
| UNK-003 | unknown | Complete schematic. | No schematic supplied. | Hardware analysis boundary. | Manufacturer schematic or lawful authoritative release. | unresolved | Blocks circuit-level claims. |
| UNK-004 | unknown | Microcontroller identity and processor architecture. | No readable component marking or authoritative documentation. | Prevents processor-family claims. | Readable marking plus authoritative datasheet, or manufacturer document. | unresolved | Blocks ARM, STM32, or specific-processor claims. |
| UNK-005 | unknown | Firmware behavior, memory capacity, and watchdog implementation. | No firmware or technical manual supplied. | Functional and reliability claims. | Authoritative manual, firmware documentation, or validated test record. | unresolved | Blocks implementation claims. |
| UNK-006 | unknown | Supported reader protocols and credential formats. | No preserved listing text or interface documentation. | Input-model validity. | Authoritative manual, readable terminal marking, or seller statement. | unresolved | Blocks protocol claims. |
| UNK-007 | unknown | Output electrical characteristics, relay or driver type, and isolation design. | No image, schematic, or datasheet available. | Safe interface interpretation. | Readable part/terminal markings and authoritative documentation. | unresolved | Blocks electrical claims. |
| UNK-008 | unknown | Elevator-side interface and configuration protocol. | No preserved interface documentation. | Scope and integration boundary. | Authoritative manual or seller statement. | unresolved | Blocks integration claims. |
| UNK-009 | unknown | Event-storage behavior and certification or compliance status. | No authoritative documentation supplied. | Operational and compliance claims. | Authoritative manual, certificate, or issuer record. | unresolved | Blocks compliance and storage claims. |

## Missing authoritative inputs

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| MIS-001 | missing authoritative input | The three product images referenced by the project plan are not in the baseline workspace. | Workspace inventory and `final_engineering_project_plan.md` section 7.1. | Prevents visual evidence preservation and marking inventory. | Original supplied image files with provenance. | missing | Blocks image-based product claims. |
| MIS-002 | missing authoritative input | No locally preserved listing snapshot, exported text, or seller statement is available. | Workspace inventory; canonical URL access attempt failed. | Prevents preservation of advertised features or seller claims. | Owner-provided capture/export or accessible public listing content. | missing | Blocks listing-content claims. |

## Questions requiring human review

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| MIS-003 | missing authoritative input | Provide the original three product images and any listing screenshot or exported text, and confirm that they may be copied into the evidence area. | Required product evidence is absent locally. | Enables byte-identical preservation and auditable product observations. | Original files or owner-approved source location. | human input required | Blocks product-feature evidence collection; does not block this baseline record. |
| MIS-004 | missing authoritative input | Confirm the working title, proposed input profile, floor-mask convention, timing values, watchdog behavior, busy policy, abstract software-only boundary, and required-versus-optional deliverables. | SP-03 freezes these project-owner decisions for review but does not supply supervisor approval. | Required before treating the scope as academically approved or expanding it. | Recorded supervisor decision or approved review notes. | project-owner decisions recorded; supervisor review pending | Non-blocking for SP-04 conceptual design; blocking before final academic submission or physical-scope expansion. |
