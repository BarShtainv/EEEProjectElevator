# SP-04 Validation

## Scope

Validation is limited to SP-04 architecture files and authorized log/method updates: required files, requirement/element mapping, registers, state machine, interfaces, failure policies, Mermaid sources, terminology, protected files, forbidden paths, and Git state.

## Required-file and UTF-8 checks

The baseline, architecture, register model, mapping, six diagrams, stage report, and this record exist and decode as UTF-8.

## Architecture coverage

Python standard-library `csv` and Markdown-ID checks produced:

```text
REQUIRED_REQUIREMENTS=60 OPTIONAL=6
MAPPING_ROWS=84 REQUIRED_COVERAGE=100%
MAPPED_ELEMENTS=33 ALL_CATALOG_ELEMENTS_MAPPED=yes
DESIGN_STATUS_VALUES_VALID=yes
ARTIFACT_PATHS_EXIST=yes
```

All required requirements have at least one `designed` row. Optional requirements use `deferred_optional`. No row uses `implemented` or `verified`. Every runtime, governance, and conceptual hardware element has a mapping.

## Register and memory checks

The register-table parser and targeted field/enumeration checks produced:

```text
LOGICAL_MEMORY_REGIONS=9
REGISTERS=19 OFFSETS_UNIQUE=yes ALIGNED_32=yes
WIDTHS_AND_ACCESS_VALID=yes
RESET_VALUES_FIT_32_BITS=yes
REGISTER_FIELDS_NON_OVERLAPPING=yes
STATE_SOURCE_EVENT_RESULT_REASON_ENCODINGS_UNIQUE=yes
FLOOR_AND_OUTPUT_MAPPING_VALID=yes
```

All registers are 32-bit logical simulator constructs. Offsets range from `0x0000` to `0x0048`. Output state uses only bits 15:0; the remaining bits are zero. Floor-mask/output mapping is floor 1→bit 0 and floor 16→bit 15.

## State-machine, interface, and failure checks

```text
STATES=7 complete=yes
TRANSITION_AND_RESET_POLICIES_PRESENT=yes
INTERFACES=14 unique_complete=yes
FAILURE_CATEGORIES=19 complete=yes
INITIALIZATION_FAIL_CLOSED=yes
EVENT_LOG_FAILURE_POLICY=yes
```

Manual and watchdog reset apply from every state. Invalid/denied paths return idle, busy stays OUTPUT_ACTIVE without changing expiry, timeout returns idle, and reset/initialization keep outputs inactive. Every failure has output effect and recovery; no failure creates a new activation.

## Mermaid checks

Six files have `flowchart` or `stateDiagram-v2` declarations and proposed-project labels. Flowchart subgraphs are balanced. Required nodes and boundaries are present. No diagram defines electrical wiring; physical reader/elevator systems remain outside the implemented boundary.

Rendering is optional and was not performed. No rendering dependency was added.

## Terminology review

Targeted `rg` searches covered commercial controller/card, ARM, STM32, Wiegand, LF/HF, named RFID technologies, relay, voltage/current, elevator, motion/safety terms, certification, and compliance. Manual context review confirmed each occurrence is an external/reference statement, proposed logical/conceptual architecture, unknown commercial behavior, or explicit exclusion. No physical rating, MCU, product compatibility, or elevator-control claim was introduced.

## Protected paths

Final SHA-256 values match the SP-04 baseline:

```text
9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d  docs/requirements.md
059388cae0320965a3ee38ac7d6ac488e968d51aceba1eb3c694802490e8b294  docs/requirements_to_test_traceability.csv
2f15218127660b422c578c6da1e5ca0c6cb72d336edb0f613fad49f6fe7a47e0  docs/figures/system_context.mmd
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
```

Source PDF paths are unchanged in Git status. No protected path changed.

## Forbidden-path and implementation checks

No `src/`, `tests/`, `analysis/`, or `docs/test_plan.md` exists. No code, test, experiment data, implementation configuration, Python package, final API, electrical design, or report chapter was created.

## Git checks

Commands:

```text
git diff --check
git diff --name-only
git status --short --untracked-files=all
git rev-parse HEAD
```

Results:

- `git diff --check`: passed with no output.
- `HEAD`: `94b051cfeebed08db8aec9b590fb99d60c87aee3`.
- Only authorized SP-04 paths changed.
- No commit or push occurred.

Final `git status --short --untracked-files=all`:

```text
 M audit/file_change_ledger.md
 M docs/decision_log.md
 M docs/methodology.md
?? audit/baselines/subproject_04_baseline.md
?? audit/stage_reports/subproject_04.md
?? audit/validation/subproject_04_validation.md
?? docs/architecture.md
?? docs/architecture_to_requirements.csv
?? docs/figures/controller_state_machine.mmd
?? docs/figures/data_flow.mmd
?? docs/figures/firmware_architecture.mmd
?? docs/figures/reset_sequence.mmd
?? docs/figures/top_level_architecture.mmd
?? docs/figures/watchdog_sequence.mmd
?? docs/register_model.md
```

## Unresolved validation concerns

None blocking. Diagram rendering is optional and remains unperformed. All architecture choices remain proposed pending human review; supervisor confirmation remains pending.

## Result

All narrow SP-04 validation checks passed.

READY FOR HUMAN REVIEW
