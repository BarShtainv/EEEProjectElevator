# Methodology

## Project research method

This project uses evidence-gated engineering analysis. It preserves commercial-product evidence, maps external sources to claims, records uncertainty, and develops later reference-model decisions separately. It does not attempt exact reverse engineering.

## Literature-selection method

Sources are first classified by authority and scope. For large manuals, the project records only relevant chapters and pages. Manufacturer manuals and architecture references are used for the systems they document; standards, textbooks, or peer-reviewed work are required where their topics are not locally covered. Topic notes are maintained in `evidence/literature_notes.md`, with unresolved gaps in `evidence/unresolved_sources.md`.

For the SP-02R narrow completion, sufficiency means that one reasonable authoritative source supports each core model area: general RFID, Wiegand input signaling, access authorization, and basic software verification. Exhaustive protocol or standards coverage is deferred unless a later claim requires it. This deadline-oriented threshold permits honest, traceable requirements work without treating incomplete literature as complete.

## Evidence hierarchy and claim classification

| Class | Use in this project |
|---|---|
| verified product evidence | Directly preserved listing material, photographs, markings, or seller statements. |
| external technical evidence | A source-supported statement within the source's own scope. |
| engineering inference | A qualified interpretation based on evidence and accepted practice. |
| proposed reference design | A future project-model choice, not a product fact. |
| unknown or unresolved | A fact or source that cannot currently be established. |

Every planned claim is recorded in `evidence/claim_evidence_matrix.csv`. Confidence labels do not substitute for evidence.

## Product-evidence limitations

Only the owner-supplied AliExpress URLs are preserved. No local product image, listing snapshot, seller statement, component marking, schematic, or manufacturer document is available. Therefore, the commercial processor, protocol support, firmware, electrical outputs, and elevator interface remain unknown.

## Representative architecture sources

RM0008 is used as a representative STM32F10xxx reference for documented memory, GPIO, timing, interrupt, watchdog, reset/clock, and serial-peripheral concepts. It is not evidence that the commercial card uses STM32 or ARM. The ARMv7-A/R manual is restricted to its A/R scope and is not treated as a Cortex-M or STM32 manual. ARMADA material is an example of functional-specification organization, not a design selection.

## Contradictory sources and missing inputs

Conflicting terms or protocol variants are recorded rather than silently reconciled. Current source gaps are documented in `evidence/unresolved_sources.md`. A missing authority prevents the associated technical claim, not its explicit registration as unresolved.

## Citation and paraphrasing discipline

Citations identify a specific source and relevant location. Notes paraphrase rather than reproduce long text. Bibliography metadata is limited to what is visible and verified; incomplete records are omitted and registered as gaps.

## Software-only validation limitation

Later simulation can evaluate only the behavior of a proposed software model under stated assumptions. It cannot demonstrate commercial-card implementation details, physical electrical performance, elevator safety, certification, or field reliability.

## Human-review responsibilities

The project owner or supervisor must provide product captures, confirm report requirements, approve any reference-design choice, and supply or authorize authoritative research for unresolved domains. Human review is also required before any claim expands beyond the recorded scope.

## SP-03 requirements derivation

Requirements are derived from three controlled inputs:

1. product-evidence boundaries and unresolved commercial details;
2. external literature supporting general RFID, Wiegand signaling, authorization, reset/watchdog concepts, and software verification; and
3. explicit project-owner decisions that define the proposed software model.

Source evidence supports general concepts only. Exact field layouts, data models, timing values, event fields, and concurrency rules are classified as proposed reference-design requirements. Each required requirement has an observable acceptance criterion, a planned verification method, and a traceability row. Required behavior is prioritized over every optional extension.

## Conceptual modeling and deterministic simulation

The conceptual model separates logical reader-source metadata, credential-message validation, credential lookup, floor authorization, timed abstract output state, event logging, and fault recovery. It models no RF physics, physical electronics, elevator wiring, motion, or passenger-safety function.

The later Python simulator will use controlled inputs and injectable logical time. Identical inputs, configuration, initial state, time schedule, and reproducibility identifier are expected to produce identical logical decisions and normalized logs. Host execution-time measurements are allowed to vary and are interpreted only in their recorded environment.

## Verification and fault injection

Verification planning combines unit tests for individual validation and data rules with integration tests for complete authorization, timing, logging, reset, and recovery scenarios. Negative tests cover malformed frames, parity errors, unknown or disabled credentials, invalid floors, unauthorized floors, and busy-controller handling.

The test harness will inject logical time, simulated lockup, and missed watchdog service without physical hardware. Expected results and output-state invariants are defined before implementation. Later verification records will retain controlled inputs, expected results, actual results, and evaluation status.

## Scalability experiments and reproducibility

Credential-database experiments will use 10, 100, 1,000, and 10,000 records under one documented workload method. They will preserve counts, timing statistics, throughput, credential count, the Python and host environment, and a seed or configuration identifier. Raw results will be machine-readable and regenerated by documented scripts.

These experiments evaluate the Python data model and test environment only. They do not measure the commercial controller, real RFID readers, physical outputs, elevator response, or safety performance.

## Human review and scope approval

The project owner has authorized SP-03 to proceed with DEC-008's abstract software-only boundary. Supervisor approval remains pending. Before architecture is treated as approved, human reviewers must confirm the working title, `PROJECT_WIEGAND_26` allocation, floor-mask mapping, timing values, watchdog timeout, busy policy, event schema, software-only boundary, and required-versus-optional deliverables. Any physical-integration expansion requires a separate evidence and approval stage.
