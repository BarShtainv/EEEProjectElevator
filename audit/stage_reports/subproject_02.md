# Subproject 02 Report

## Objective

Build a topic-organized literature and claim-evidence architecture without making product-specific implementation claims or beginning requirements, architecture, implementation, experiments, or final report drafting.

## Starting version and SP-01 baseline

SP-02 started on `main` at `326346649ea40755b6af287324b1bfef034f7163` (`3263466 Step1`). The SP-01 task baseline is that commit; reference baseline `9e46275` is comparison-only. `prompt2.txt` was the sole untracked working-tree file and is unrelated but non-conflicting.

## SP-01 prerequisite result

Passed. Product URLs, classifications, unknowns, source inventory, matrix schema, and readiness records are present. Missing product captures remain an explicit product-evidence limitation.

## Sources and sections inspected

- Project plan, workflow handbook, and all SP-01 audit/evidence records.
- RM0008 introduction; ch.3; ch.7; ch.9; ch.10.1; chs.14–15; chs.19–20; ch.27.
- ARM Developer Suite contents, ch.5, and ch.6.
- ARMv7-A/R preface/“About this manual.”
- ARM instruction-set educational material on modes, registers, flags, exceptions, branches, and load/store.
- ARMADA 38x preface, address-map, boot-flow, and timers/watchdog sections.
- Example academic project table of contents only.

## Literature domains covered

All LIT-01 through LIT-11 domains are represented in `evidence/literature_notes.md`. Local embedded, ARM, STM32, workflow, and report-organization coverage is recorded as external evidence. RFID, LF/HF, Wiegand, authorization, elevator integration, formal fail-safe terminology, and software-verification authorities are explicitly unresolved.

## Files created and modified

Created: SP-02 baseline, stage report, validation record, literature notes, unresolved-source register, methodology, outline, decision log, and bibliography.

Modified: source index, claim-evidence matrix, assumptions/unknowns register, and canonical file-change ledger.

## Claims and scope qualifications

Claims CLM-006 through CLM-020 were added. STM32 is a representative reference architecture only; ARMv7-A/R is not a Cortex-M manual; Wiegand-26 is a possible future simulator choice only; commercial processor and output characteristics remain unknown; and elevator safety/motion control remains outside scope.

## Missing sources and human-review items

`evidence/unresolved_sources.md` records ten gaps. Priority blockers for technical requirements are authoritative RFID, LF/HF, Wiegand, authorization, and elevator-integration sources. Human review must provide/authorize those sources, product captures, and university report requirements.

## Validation, deviations, and result

Validation covers file existence/readability, CSV schema and IDs, source references, BibTeX structure, forbidden-path review, Git state, and manual scope review. No web research was performed because it was not authorized. No original source or product evidence was modified.

## Exact readiness state

**BLOCKED BEFORE NEXT STAGE — authoritative RFID, Wiegand, authorization, and conceptual elevator-access-integration sources are absent, so defensible technical requirements cannot yet be defined.**
