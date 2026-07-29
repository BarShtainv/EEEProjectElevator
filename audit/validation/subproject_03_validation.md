# SP-03 Validation

## Scope

Validation covers only SP-03 deliverables and authorized updates: required-file readability, requirements completeness, traceability, CSV integrity, source/decision references, context-diagram content, terminology qualifications, protected files, forbidden paths, and Git scope.

## Required files and encoding

Checked for existence and UTF-8 readability:

```text
audit/baselines/subproject_03_baseline.md
audit/stage_reports/subproject_03.md
audit/validation/subproject_03_validation.md
docs/requirements.md
docs/requirements_to_test_traceability.csv
docs/figures/system_context.mmd
```

Result: passed.

## Requirements and traceability

A Python standard-library script parsed requirement-table rows from `docs/requirements.md`, checked the nine required fields, enforced unique IDs and required “shall” wording, and compared the exact ID set with the traceability CSV.

```text
REQUIREMENTS_TOTAL=66
REQUIRED=60 OPTIONAL=6
REQUIREMENT_IDS_UNIQUE=yes
REQUIRED_FIELDS_COMPLETE=yes
REQUIRED_SHALL_STATEMENTS=yes
TRACEABILITY_HEADER_VALID=yes
TRACEABILITY_ROWS_MATCH_REQUIREMENTS=yes
TRACEABILITY_PLANNED_TESTS_COMPLETE=yes
```

Every required requirement has acceptance criteria, planned verification, and at least one planned test ID. Optional rows are explicitly marked `optional`. Manual review confirmed that no required behavior depends on physical hardware and no requirement asserts commercial-product behavior.

The failure-state review confirmed that a failure creates no new activation. An already authorized timed activation may continue unchanged until timeout or reset under the explicitly frozen policy in FUN-014 and DEC-018.

## CSV and reference validation

Both CSV files were parsed with Python's standard `csv` module.

```text
docs/requirements_to_test_traceability.csv: header=yes rows=66 widths=yes active_ids_unique=yes
evidence/claim_evidence_matrix.csv: header=yes rows=35 widths=yes active_ids_unique=yes
TRACE_REFERENCE_IDS_VALID=yes count=32
CLAIM_SOURCE_IDS_AND_PATHS_VALID=yes rows=35
```

The traceability header exactly matches the SP-03 instruction. Every traceability requirement ID exists in the requirements document. Referenced source, decision, assumption, unknown, claim, and requirement IDs resolve in the canonical records where practical.

## Context diagram

A focused Python token/structure check and manual review produced:

```text
MERMAID_BASIC_SYNTAX=yes
MERMAID_REQUIRED_ACTORS=yes
MERMAID_PROJECT_BOUNDARY=yes
MERMAID_PHYSICAL_SYSTEMS_OUTSIDE=yes
```

The Mermaid source uses `flowchart LR`, balanced `subgraph`/`end` blocks, and the required nodes. It contains no circuit or electrical wiring diagram. Rendering was not required and no rendering dependency was added.

## Terminology review

Command:

```text
rg -n -i 'commercial card|commercial controller|ARM|STM32|Wiegand|Wiegand-26|125 kHz|13.56 MHz|MIFARE|ISO 14443|NFC|relay|voltage|elevator|motor|brake|door|safety|certified|compliant' <SP-03 edited files>
```

Manual context review confirmed:

- `PROJECT_WIEGAND_26`, LF/HF labels, mask, timing, watchdog, logging, and busy behavior are qualified as proposed project decisions.
- ARM/STM32 occurrences remain representative-source statements or prohibited commercial claims.
- Commercial processor, RFID frequency, protocol, Wiegand support, electrical behavior, and elevator interface remain unknown.
- Physical elevator, relay, wiring, motion, safety, certification, and installation terms occur only in exclusions, limitations, or outside-boundary labels.

## Protected files

Final SHA-256 checks match the SP-03 baseline:

```text
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
```

Git status contains no modified source PDF, product image, product evidence, source index, literature note, unresolved-source register, report source, bibliography, project plan, or workflow handbook.

## Forbidden-path and implementation check

No `src/`, `tests/`, or `analysis/` directory exists. No simulator code, automated test, experiment script, detailed architecture, register map, state-machine implementation, electrical design, or report chapter was created.

The allowed-path check found only the six created SP-03 deliverables and the five authorized updates listed in the stage instruction.

## Git checks

Commands:

```text
git diff --check
git diff --name-only
git status --short
git rev-parse HEAD
```

Results:

- `git diff --check`: passed with no output.
- `HEAD`: `88a646026c0bf468e28102bf80c00ef4cb3ea57f`.
- The working tree contains only authorized SP-03 changes.
- No commit or push was performed.

Final `git status --short --untracked-files=all`:

```text
 M audit/file_change_ledger.md
 M docs/decision_log.md
 M docs/methodology.md
 M evidence/assumptions_and_unknowns.md
 M evidence/claim_evidence_matrix.csv
?? audit/baselines/subproject_03_baseline.md
?? audit/stage_reports/subproject_03.md
?? audit/validation/subproject_03_validation.md
?? docs/figures/system_context.mmd
?? docs/requirements.md
?? docs/requirements_to_test_traceability.csv
```

## Unresolved validation concerns

None blocking. Mermaid rendering is optional and was not performed. Requirements and decisions remain planned/proposed until human review; supervisor confirmation remains pending.

## Result

All narrow SP-03 validation checks passed.

READY FOR HUMAN REVIEW
