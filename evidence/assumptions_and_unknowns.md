# Assumptions and Unknowns

This register separates inference and potential future choices from product facts. No item below establishes a property of the commercial card.

## Engineering inferences

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| INF-001 | engineering inference | The card is being studied as an access-authorization layer, not as elevator motion or passenger-safety control. | Project scope in `final_engineering_project_plan.md`. | Preserves the project safety boundary. | Supervisor-approved scope change or authoritative product documentation for a broader claim. | scope interpretation only | Non-blocking for baseline; applies to future work. |

## Possible future reference-design elements

| ID | category | statement | basis | why it matters | acceptable evidence needed | current status | blocking effect |
|---|---|---|---|---|---|---|---|
| PRD-001 | possible proposed-design element | A later reference design may model 16 floor-permission channels if independently justified by future requirements and evidence. | Project title and plan describe a 16-floor study; this is not verified product evidence. | Bounds possible simulator scope. | Approved requirements and cited external technical evidence. | deferred; not designed in this stage | Non-blocking for baseline. |
| PRD-002 | possible proposed-design element | A later simulator may use Wiegand-26 as an initial reference input format if approved. | Project plan names Wiegand-26 for a future software package; SRC-WIEGAND-001 supports the general signaling and frame concepts, but no product evidence establishes support. | Separates future simulation scope from product claims. | Approved requirements and a documented project-specific Wiegand-26 field allocation. | minimum general source available; exact field allocation deferred | Non-blocking for requirements and software-model planning; the exact field allocation must be documented before parser implementation. |
| PRD-003 | possible proposed-design element | STM32F10xxx may be used later as a representative reference architecture for explaining embedded-controller concepts. | The local RM0008 manual has suitable documented scope; no product evidence identifies an STM32. | Makes source scope explicit. | Approved requirements and continued citation discipline. | reference-only; not a hardware selection | Non-blocking for literature architecture. |

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
