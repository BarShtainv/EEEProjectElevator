# Methodology

## Project research method

This project uses evidence-gated engineering analysis. It preserves commercial-product evidence, maps external sources to claims, records uncertainty, and develops later reference-model decisions separately. It does not attempt exact reverse engineering.

## Literature-selection method

Sources are first classified by authority and scope. For large manuals, the project records only relevant chapters and pages. Manufacturer manuals and architecture references are used for the systems they document; standards, textbooks, or peer-reviewed work are required where their topics are not locally covered. Topic notes are maintained in `evidence/literature_notes.md`, with unresolved gaps in `evidence/unresolved_sources.md`.

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
