# SP-05 Validation

## Scope and method

Validation is limited to SP-05 design artifacts and the authorized narrow architecture/decision/ledger updates. Standard-library inline Python scripts, `sha256sum`, targeted `rg`, and Git read-only checks were used. No executable validation file remains in the repository.

An initial inline scheduler harness needed one correction to handle an empty due-event set after reset; the corrected independent harness passed. This was an audit-script issue only, not production code or a design-artifact failure.

## Required files and UTF-8

The following files exist and decode strictly as UTF-8:

```text
audit/baselines/subproject_05_baseline.md
audit/stage_reports/subproject_05.md
audit/validation/subproject_05_validation.md
docs/software_design.md
docs/test_plan.md
docs/test_case_inventory.csv
docs/implementation_sequence.md
```

Result: passed.

## Module, ownership, dependency, and API checks

An inline parser/token check and manual contract review produced:

```text
PLANNED_DOMAIN_MODULES=11 all documented=yes
TYPED_FUNCTION_OR_METHOD_SIGNATURES=53
REQUIRED_SHARED_TYPES=16 complete=yes
PRIMARY_RESPONSIBILITY_PER_MODULE=yes
OWNED_MUTABLE_STATE_EXPLICIT=yes
DEPENDENCY_DIRECTION_ACYCLIC=yes
PHYSICAL_OR_NETWORK_API_DEPENDENCY=no
```

The package direction is models → stateless/owned managers → controller → CLI. No manager imports the controller/CLI in the design. Each module table row identifies responsibility, state, dependencies, requirements/elements, reset behavior, and tests. Public inputs/outputs are typed. The raw request's `object` fields deliberately retain normal invalid-input coverage.

Domain denials/failures use `Result`/`Reason`, not exceptions. The seven-class exception hierarchy is limited to configuration/credential startup data, clock misuse, logger infrastructure, and state invariants. Atomic candidate construction and controller conversion/propagation rules are documented.

## Type, enum, and schema checks

The enum tables were compared with `docs/register_model.md`:

```text
ReaderSource=2 values 1..2
ControllerState=7 values 0..6
EventType=6 values 1..6
Result=5 values 1..5
Reason=17 values 1..17
CANONICAL_TEXT_LOWERCASE=yes
NUMERICAL_ENCODINGS_MATCH=yes
```

All minimum immutable record names and exact fields are present, including both event values, configuration, response, controller snapshot, and 16-channel output snapshot. Events retain all nine fields and conditional values are typed `None`/JSON `null`.

Python `json.loads` parsed all three JSON code blocks in `docs/software_design.md`:

```text
JSON_EXAMPLES=3 parse=yes
CONFIG_EXAMPLE_EXACT=yes
CREDENTIAL_EXAMPLE_EXACT=yes
EVENT_EXAMPLE_NINE_FIELDS=yes
```

Manual/schema-token review confirmed strict required/unknown/missing/version/type/range rules; 3000 and 100–30000 ms output rules; 2000 default and 1–4294967295 watchdog rules; facility 0–255; credential/mask 0–65535; actual Boolean validation; optional non-empty label; empty repository; duplicate rejection; input-order preservation; and all-or-nothing publication. No invalid explicit field silently defaults.

## Watchdog and scheduler validation

A separate inline event-scheduler calculation implemented only the documented due-time and priority rules. It did not import or create project implementation code. Results:

```text
NORMAL_3000=(output_timeout, 3000); watchdog_reset=0
SUPPRESSED_DEFAULT=(watchdog_reset, 2000); output_timeout=0
NORMAL_30000=(output_timeout, 30000); watchdog_reset=0
LARGE_SMALL_EQUIVALENT=yes
COLLISION_AT_2000=watchdog_reset only
REPEATED_POLL_DUPLICATES=0
RESET_CLEARS_SUPPRESSION=yes
WATCHDOG_VALIDATION=passed
```

The design jumps between due timestamps and requires no wall-clock wait, per-millisecond loop, thread, async task, or physical watchdog. Same-time priority is heartbeat service, watchdog expiry, output expiry. A suppressed heartbeat is consumed without service; watchdog reset cancels a coincident output timeout. One armed deadline emits once.

## Wiegand vector validation

An independent inline encoder rebuilt each table value from an 8-bit facility field and 16-bit credential field, then recalculated parity and decoded slices. It imported no production code.

```text
VECTORS=6
LENGTH_26=6/6
BINARY_ONLY=6/6
LEADING_EVEN=6/6
TRAILING_ODD=6/6
FIELDS_DECODE=6/6
DOCUMENTED_BITS_MATCH_RECALCULATION=6/6
NEGATIVE_VARIANTS=24/24 rejected
```

The four negative variants per vector flip bit 1, 26, 2, or 14. Each invalidates the appropriate leading or trailing parity region. No script was retained.

## Test inventory and traceability

Both CSVs were parsed with `csv.reader`/`csv.DictReader`:

```text
INVENTORY_HEADER_EXACT=yes
INVENTORY_ROWS=100
ROW_WIDTHS=13/13
TEST_IDS_UNIQUE=yes
INVENTORY_STATUSES=designed
TRACEABILITY_ROWS=66
REQUIRED_TRACE_ROWS=60
OPTIONAL_TRACE_ROWS=6
REFERENCED_TEST_IDS=69
UNRESOLVED_REFERENCED_TEST_IDS=0
TRACEABILITY_STATUSES=planned
REQUIRED_ROWS_WITH_PLANNED_TEST=60/60
```

No traceability edit was necessary. Automated token/category checks plus manual review produced:

```text
CANONICAL_REASONS=17/17 covered
CONTROLLER_STATES=7/7 covered
FLOOR_MASK_BITS=16/16 covered
MANUAL_RESET_FROM_STATES=7/7 designed
EVENT_TYPES=6/6 covered
RESULT_VALUES=5/5 covered
WATCHDOG_NORMAL_SUPPRESSED_COLLISION_RECOVERY=yes
LOG_FAILURE_GRANT_DENIAL_BUSY_TIMEOUT_MANUAL_WATCHDOG=yes
LF_HF_AND_REPLAY=yes
REQUIRED_END_TO_END_CATEGORIES=yes
```

Parameterized inventory entries explicitly cover the required state transitions and floor ranges. All expected runtime outcomes use canonical result/reason names. Inspection-only/optional entries state that a domain result is not applicable and do not claim execution. No test status is passed.

## Scalability and implementation-plan checks

The test plan freezes all four credential counts, at least `max(1000, count)` mixed cases, one warm-up, three measured repetitions, `perf_counter_ns`, average/median/nearest-rank p95/throughput, all frozen counts, seed/config/Python/host metadata, and software-model limitations. It retains small fixtures/config/seed/aggregates/environment and regenerates large inputs.

`docs/implementation_sequence.md` contains exactly 11 numbered bounded tasks. Each task states objective, expected files, prerequisites, tests, requirements, validation command, completion gate, and prohibited unrelated work.

## Protected material and scope

Final SHA-256 values match the SP-05 baseline:

```text
9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d  docs/requirements.md
059388cae0320965a3ee38ac7d6ac488e968d51aceba1eb3c694802490e8b294  docs/requirements_to_test_traceability.csv
f2b836e963de52ccce035277b326601815b2928c1343ac80d3afe547c9106466  docs/register_model.md
629c4e986e38aff724dc5cdbe8241232ede81c03c8c216fba60993102660f4b9  docs/architecture_to_requirements.csv
2f15218127660b422c578c6da1e5ca0c6cb72d336edb0f613fad49f6fe7a47e0  docs/figures/system_context.mmd
d4a47d131b93fae53e3725260a86312f747b7e06f931d172fabf019f88e2fc64  docs/figures/controller_state_machine.mmd
c797ce5d0456593bace5796bfdb1f2b39adf155471552e0ca4094c6f666f36bc  docs/figures/data_flow.mmd
8b116413c1173700d0fe19017cecdacffba124fd9ceac19e3d54b0fc7605a475  docs/figures/firmware_architecture.mmd
1fbb0c45d57a1d55ffbe741a7d534f4c3cc7af6208726f35c91f9f18933058bb  docs/figures/reset_sequence.mmd
660c47967333b86e6a600821a2607375cdc24abd24de0609515a154f0981e605  docs/figures/top_level_architecture.mmd
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
f8a4031d92a47e816f132456e1e68e145f8104689f83ec765e96e82730ab1d66  evidence/claim_evidence_matrix.csv
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
```

All protected source PDFs and evidence paths are absent from Git status.

Targeted terminology review confirmed every ARM/STM32/Wiegand/LF/HF/elevator/watchdog/electrical occurrence is a representative reference, proposed logical design, unknown, or explicit exclusion. No commercial compatibility, physical output, motion/safety, electrical rating, or certification claim was introduced.

No `src/`, `tests/`, package metadata, sample runtime configuration, script, data/result/plot, or report-chapter path exists. Only `docs/figures/watchdog_sequence.mmd` changed among protected diagrams. Requirements, register model, mapping, context and other SP-04 diagrams, evidence, sources, bibliography, plan/workflow, and prior audits are unchanged.

## Git validation

Commands:

```text
git diff --check
git diff --name-only
git status --short --untracked-files=all
git rev-parse HEAD
```

Results:

- `git diff --check`: passed with no output.
- `HEAD`: `08e7985f3d01303b9c28066d3693833fa3aa614e`.
- Changed paths are exactly the 11 authorized paths listed below.
- No commit or push was performed.

```text
 M audit/file_change_ledger.md
 M docs/architecture.md
 M docs/decision_log.md
 M docs/figures/watchdog_sequence.mmd
?? audit/baselines/subproject_05_baseline.md
?? audit/stage_reports/subproject_05.md
?? audit/validation/subproject_05_validation.md
?? docs/implementation_sequence.md
?? docs/software_design.md
?? docs/test_case_inventory.csv
?? docs/test_plan.md
```

## Unresolved validation concerns

None blocking. Mermaid rendering is optional and was not performed. The package/API/schema/heartbeat/priority/fault/vector/workload/sequence choices remain proposed pending human review; supervisor approval remains pending.

## Result

All narrow SP-05 design validation checks passed.

READY FOR HUMAN REVIEW
