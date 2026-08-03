# SP-01 File Change Ledger

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baseline.md` | new | Created baseline record. | Preserve initial repository and evidence state. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/file_change_ledger.md` | new | Created this ledger. | Audit all allowed changes. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/stage_reports/subproject_01.md` | new | Created stage report. | Durable SP-01 completion record. | No pre-existing file overwritten. | UTF-8/readability check. |
| `audit/validation/subproject_01_validation.md` | new | Created validation record. | Record required checks and results. | No pre-existing file overwritten. | Required-file, CSV, Git, and content checks. |
| `evidence/product_evidence.md` | new | Preserved URLs and documented absence of local listing/product evidence. | Establish verified-evidence boundary. | No product files copied, altered, or replaced. | UTF-8/readability and assertion review. |
| `evidence/assumptions_and_unknowns.md` | new | Created inference, future-design, unknown, and missing-input register. | Prevent unsupported assumptions. | No pre-existing file overwritten. | UTF-8/readability and assertion review. |
| `evidence/claim_evidence_matrix.csv` | new | Created initial claim-evidence matrix. | Make claim status auditable. | No pre-existing file overwritten. | Parsed with Python `csv`; header and row widths checked. |
| `evidence/source_index.md` | new | Inventoried supplied URLs and available source documents. | Preserve source provenance without literature synthesis. | Existing sources only referenced, not modified. | UTF-8/readability check. |

No product image or listing snapshot was copied because none was available in the baseline workspace. No path outside the allowed SP-01 paths was modified.

## SP-02 additions

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_02_baseline.md` | new | Recorded current, task, and reference baselines. | Preserve SP-02 starting-state comparison. | No prior file overwritten. | Git history/status and SP-01 prerequisite review. |
| `audit/file_change_ledger.md` | pre-existing | Added SP-02 ledger section. | Maintain canonical change audit. | Prior SP-01 content retained. | UTF-8/readability check. |
| `audit/stage_reports/subproject_02.md` | new | Created SP-02 report. | Record bounded-stage outcome and source gaps. | No prior file overwritten. | Required-file and scope checks. |
| `audit/validation/subproject_02_validation.md` | new | Created SP-02 validation record. | Preserve validation results. | No prior file overwritten. | CSV, source-ID, BibTeX, Git, and wording checks. |
| `evidence/source_index.md` | pre-existing | Expanded source metadata, scope, inspected locations, limitations, and availability. | Make source use auditable. | Existing IDs retained; original sources not changed. | Source-ID/path and UTF-8 checks. |
| `evidence/claim_evidence_matrix.csv` | pre-existing | Added traceable external, proposed, and unresolved claims. | Expand claim-evidence architecture. | Existing header and claims retained. | CSV/schema/ID/source checks. |
| `evidence/literature_notes.md` | new | Created topic-organized literature notes. | Preserve concise scoped paraphrases and source gaps. | No source text copied or source file changed. | Source-ID and manual scope review. |
| `evidence/unresolved_sources.md` | new | Created missing-source register. | Prevent unsupported technical claims. | No product unknown reclassified. | Coverage and blocking-effect review. |
| `evidence/assumptions_and_unknowns.md` | pre-existing | Added PRD-002 and PRD-003. | Label future simulator/reference choices. | Existing SP-01 entries retained. | Cross-reference and scope review. |
| `docs/methodology.md` | new | Created evidence-led research methodology. | Document citation, source, and limitation discipline. | No requirements or architecture design added. | Manual scope review. |
| `docs/literature_review_outline.md` | new | Created controlled literature outline. | Map sections, sources, and gaps. | No final prose or product claims added. | Source-ID review. |
| `docs/decision_log.md` | new | Created decision log. | Preserve evidence-scope decisions. | Product evidence remains intact. | Decision/cross-reference review. |
| `report/references.bib` | new | Created preliminary verified-metadata bibliography. | Support citation traceability. | No original source changed; uncertain metadata omitted. | Structural and unique-key checks. |

## SP-02R narrow completion

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `.gitignore` | new | Added `prompt*.txt`. | Keep local task prompts out of permanent engineering deliverables. | No prior ignore rules existed. | Prompt tracking/local-file checks. |
| `prompt.txt`, `prompt2.txt` | tracked local inputs | Removed from Git index with `git rm --cached`; local files retained. | Implement SP-02R prompt hygiene. | Contents retained locally and ignored. | `git ls-files` and `test -f`. |
| `audit/baselines/subproject_02_repair_baseline.md` | new | Recorded clean `fdad611` baseline, readiness, prompts, and defects. | Audit the narrow repair starting state. | No prior baseline overwritten. | Git and instruction-file inspection. |
| `audit/stage_reports/subproject_01.md` | pre-existing | Replaced custom readiness sentence with `READY FOR HUMAN REVIEW`. | Clarify that missing product captures limit claims but do not block literature/model planning. | Existing missing-evidence explanation retained. | Manual wording review. |
| `evidence/product_evidence.md` | pre-existing | Corrected the malformed original AliExpress URL. | Preserve the exact owner-supplied URL. | Canonical URL and all product limitations retained. | Exact/malformed URL searches. |
| `evidence/source_index.md` | pre-existing | Corrected URL; added four core sources and updated gap coverage. | Establish minimum credible literature coverage. | Existing IDs and source-scope qualifications retained. | Source metadata, IDs, paths, URLs, and hashes checked. |
| `literature/nist_sp_800_98_rfid.pdf` | new | Downloaded official NIST SP 800-98 PDF. | Preserve authoritative RFID source locally. | No existing PDF replaced. | PDF type, metadata, SHA-256, and path checks. |
| `literature/nist_sp_800_53_rev5_1.pdf` | new | Downloaded official NIST SP 800-53 Rev. 5 Release 5.1 derivative PDF. | Preserve authoritative access-authorization source locally. | No existing PDF replaced. | PDF type, metadata, SHA-256, and path checks. |
| `evidence/literature_notes.md` | pre-existing | Replaced core source gaps with concise RFID, Wiegand, authorization, and testing notes; scoped elevator integration. | Meet minimum note coverage without broad rewriting. | Product claims remain prohibited and unknowns retained. | Note/source-ID and manual qualification review. |
| `evidence/unresolved_sources.md` | pre-existing | Marked minimum core gaps resolved and remaining gaps non-blocking where authorized. | Permit SP-03 while retaining limitations. | No gap deleted. | Coverage/readiness review. |
| `evidence/assumptions_and_unknowns.md` | pre-existing | Aligned proposed Wiegand-26 status with the newly available general source while retaining the exact-field-allocation gate. | Remove a stale open-source statement without implying commercial support. | Existing product unknowns retained. | Cross-reference and scope review. |
| `evidence/claim_evidence_matrix.csv` | pre-existing | Updated claims, superseded duplicate CLM-014, and added CLM-021–CLM-026. | Trace future input, authorization, mask, test, and scope decisions. | Existing IDs retained; no wholesale renumbering. | Python CSV and reference validation. |
| `docs/literature_review_outline.md` | pre-existing | Mapped newly covered topics and controlled remaining gates. | Align outline with narrow completion. | Remains an outline, not final prose. | Source-ID review. |
| `docs/decision_log.md` | pre-existing | Added abstract elevator-output boundary and minimum-source-set decisions. | Make physical integration non-blocking for software work. | Safety boundary strengthened. | Decision/scope review. |
| `docs/methodology.md` | pre-existing | Added deadline-oriented literature sufficiency standard. | Explain why minimum authoritative coverage permits progress. | Evidence hierarchy unchanged. | Manual wording review. |
| `report/references.bib` | pre-existing | Added four verified core-source entries. | Support traceable citations. | Uncertain metadata omitted. | Unique-key and brace checks. |
| `audit/stage_reports/subproject_02_repair.md` | new | Recorded repair outcome and non-blocking gates. | Durable SP-02R report. | Historical SP-02 report retained. | Required-content review. |
| `audit/validation/subproject_02_repair_validation.md` | new | Recorded narrow validation. | Preserve audit evidence for readiness. | No earlier validation overwritten. | Required SP-02R checks. |

## SP-03 requirements and scope freeze

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_03_baseline.md` | new | Recorded clean accepted commit, repository inventory, prerequisites, protected hashes, and carried gates. | Preserve the SP-03 starting state. | No prior baseline changed. | Git state/history and prerequisite inspection. |
| `docs/requirements.md` | new | Defined the frozen MVP, system boundary, project input profile, conventions, 60 required requirements, six optional requirements, deliverables, and human-review items. | Give SP-04 a testable bounded specification. | Requirements describe the proposed model and preserve commercial/physical limitations. | ID, field, priority, wording, scope, and traceability checks. |
| `docs/requirements_to_test_traceability.csv` | new | Added one planned-verification row for every required and optional requirement. | Establish requirements-to-test traceability before design and coding. | No verification result was fabricated. | Python `csv`, ID-set, priority, status, and reference checks. |
| `docs/figures/system_context.mmd` | new | Added a Mermaid software-system context diagram with physical/commercial systems outside the boundary. | Make the scope boundary visually reviewable. | No wiring, circuit, or physical-control design added. | Syntax-token, actor, boundary, and outside-scope checks. |
| `docs/methodology.md` | pre-existing | Added requirements derivation, conceptual modeling, deterministic simulation, verification, fault injection, scalability, reproducibility, and human-review sections. | Complete the SP-03 research method. | Existing evidence classes and product limitations retained. | Manual content and terminology review. |
| `docs/decision_log.md` | pre-existing | Updated DEC-008 authorization status and added DEC-010–DEC-025 for title, scope, format, data, timing, logging, experiments, deliverables, MVP, and superseded blockers. | Freeze proposed design choices while retaining history. | DEC-004 and DEC-007 remain visible; only obsolete blocking language is superseded. | Decision-ID, cross-reference, and scope review. |
| `evidence/assumptions_and_unknowns.md` | pre-existing | Updated PRD-001/PRD-002 and added PRD-004–PRD-007 plus MIS-004. | Record proposed values and pending supervisor decisions without changing product unknowns. | UNK-004, UNK-006, UNK-007, and UNK-008 remain unresolved. | ID, qualification, and blocking-effect review. |
| `evidence/claim_evidence_matrix.csv` | pre-existing | Updated frozen proposed claims and added CLM-027–CLM-035. | Trace scope, data, timing, recovery, logging, experiment, title, and deliverable decisions. | No commercial unknown was converted into fact; CLM-014 remains superseded. | Python `csv`, row width, active-ID, source-ID, and path checks. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-03 section. | Maintain the canonical change audit. | Prior stage ledger content retained. | UTF-8 and changed-path review. |
| `audit/stage_reports/subproject_03.md` | new | Recorded the requirements and scope-freeze outcome. | Provide durable stage handoff and review items. | Prior reports retained. | Required-content and exact-readiness review. |
| `audit/validation/subproject_03_validation.md` | new | Recorded narrow SP-03 validation commands and results. | Make validation reproducible. | Prior validations retained. | Required-file, requirements, CSV, diagram, terminology, protected-file, and Git checks. |

## SP-04 conceptual architecture

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_04_baseline.md` | new | Recorded accepted commit, clean status, protected hashes, frozen decisions, outputs, and pending reviews. | Preserve the SP-04 starting state. | No prior baseline changed. | Git history/status and prerequisite inspection. |
| `docs/architecture.md` | new | Defined conceptual hardware blocks, runtime responsibilities, request order, state machine, interfaces, data flow, configuration, timing, reset, watchdog, events, failures, and handoff. | Give SP-05 a complete conceptual design. | Product/electrical details remain unknown or excluded. | Element, state, interface, failure, terminology, and coverage checks. |
| `docs/register_model.md` | new | Defined nine logical memory regions, 19 logical registers, enumerations, floor/output mapping, event format, reset rules, and invariants. | Provide stable documentation/test semantics. | Prominently labeled processor-neutral and non-product. | Offset, alignment, width, access, reset, field, enumeration, and invariant checks. |
| `docs/architecture_to_requirements.csv` | new | Added 84 mappings covering every required requirement, optional deferrals, runtime/governance elements, and conceptual blocks. | Demonstrate complete architecture coverage. | No row claims implementation or verification. | Python `csv`, requirement-set, element, status, and artifact-path checks. |
| `docs/figures/top_level_architecture.mmd` | new | Added focused conceptual/implemented boundary diagram. | Show hardware context without electrical design. | Physical blocks explicitly conceptual/outside. | Mermaid declaration, block, label, and scope checks. |
| `docs/figures/firmware_architecture.mmd` | new | Added responsibility and dependency diagram. | Show ownership and data/control relationships. | No final API or class design. | Mermaid and element checks. |
| `docs/figures/controller_state_machine.mmd` | new | Added seven-state transition diagram. | Make normal, busy, timeout, and reset transitions explicit. | Logical state model only. | State and transition checks. |
| `docs/figures/data_flow.mmd` | new | Added request, failure, logging-gate, reset, and observation flow. | Clarify invalid exits and no physical command. | Ends at abstract permission state. | Mermaid and flow-content checks. |
| `docs/figures/reset_sequence.mmd` | new | Added startup and runtime reset flow. | Show clearing and preservation order. | No physical reset circuit. | Mermaid and reset-policy checks. |
| `docs/figures/watchdog_sequence.mmd` | new | Added simulated service, fault, expiry, and reset flow. | Make deterministic watchdog behavior reviewable. | No MCU equivalence. | Mermaid and watchdog-policy checks. |
| `docs/decision_log.md` | pre-existing | Added DEC-026–DEC-040 covering architecture authorization, boundaries, ownership, states, order, reset, watchdog, events, memory/registers, and failure/readiness policies. | Preserve proposed architecture decisions and review gates. | Earlier decisions retained; supervisor approval remains pending. | Decision-ID and content review. |
| `docs/methodology.md` | pre-existing | Added a short architecture-derivation method. | Explain mapping and consistency discipline. | Evidence classifications and product limits retained. | Manual terminology and scope review. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-04 section. | Maintain canonical change audit. | Prior ledger retained. | UTF-8 and changed-path review. |
| `audit/stage_reports/subproject_04.md` | new | Recorded architecture outcome, coverage, approvals, validation, and readiness. | Durable SP-04 handoff. | Prior reports retained. | Required-content and readiness review. |
| `audit/validation/subproject_04_validation.md` | new | Recorded narrow architecture validation. | Make checks reproducible. | Prior validations retained. | Required-file, mapping, register, state, interface, failure, Mermaid, terminology, hash, and Git checks. |

## SP-05 software and verification design

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_05_baseline.md` | new | Recorded the exact accepted commit, clean state, prerequisites, frozen behavior, watchdog clarification, allowed scope, and protected hashes. | Preserve the SP-05 starting point before edits. | No prior audit file changed. | Git identity/status, inventory, prerequisite, and SHA-256 checks. |
| `docs/software_design.md` | new | Defined the package, dependency direction, enums, immutable records, exceptions, strict schemas, module/public APIs, orchestration, scheduler, heartbeat, atomicity, reset, fault, CLI, and experiment contracts. | Remove implementation ambiguity before SP-06. | Frozen requirements/register semantics and physical boundary retained. | Module, signature, enum, schema, timing, terminology, and scope checks. |
| `docs/test_plan.md` | new | Defined pytest levels, isolated fixtures, six verified Wiegand vectors, detailed behavioral/fault/replay/scalability cases, result recording, and coverage gates. | Freeze expected verification before code. | No test execution/pass claim or production test file created. | Section, category, vector, parity, timing, and coverage checks. |
| `docs/test_case_inventory.csv` | new | Added 100 uniquely identified designed cases with explicit requirements, inputs, steps, result/state/event expectations, fixtures, and notes. | Resolve existing trace IDs and make every denial/fault/state/mask/reset path implementable. | Existing IDs retained; traceability status remains planned. | Standard-library CSV header/width/ID/status/reference/reason/state/floor checks. |
| `docs/implementation_sequence.md` | new | Divided SP-06 into 11 bounded tasks with scope, files, prerequisites, tests, requirements, commands, gates, and prohibitions. | Keep implementation incremental and independently verifiable. | No production path was created in SP-05. | Task-count and required-field review. |
| `docs/architecture.md` | pre-existing | Narrowly clarified heartbeat formula, chronological priority, collision/reset outcome, transient suppression clearing, and linked SP-05 artifacts. | Resolve the default timing conflict and hand off precise software design. | Conceptual blocks, state model, requirements, register semantics, and other architecture content unchanged. | Focused diff and watchdog consistency review. |
| `docs/figures/watchdog_sequence.mmd` | pre-existing | Replaced the ambiguous checkpoint loop with explicit heartbeat, suppression, expiry, output collision priority, and reset-reinitialization flow. | Make the SP-05 timing clarification reviewable. | Still a simulated logical watchdog with no MCU/physical claim. | Mermaid declaration/flow/token and manual priority checks. |
| `docs/decision_log.md` | pre-existing | Added DEC-041–DEC-058 for package/types/outcomes/formats/heartbeat/scheduler/constraints/atomic startup/repository/API/tests/coverage/scale/preservation/sequence/readiness. | Preserve every consequential SP-05 choice and explicitly clarify DEC-033. | DEC-001–DEC-040 retained without history rewrite. | Decision-ID uniqueness, coverage, and terminology checks. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-05 section. | Maintain the canonical change audit. | All earlier ledger sections retained. | Changed-path and UTF-8 review. |
| `audit/stage_reports/subproject_05.md` | new | Recorded the full SP-05 outcome, human-review items, validation, scope, and readiness. | Provide durable stage handoff. | Earlier reports retained. | Required-content and exact-readiness review. |
| `audit/validation/subproject_05_validation.md` | new | Recorded module/API/schema/watchdog/vector/CSV/coverage/protected-path/Git validation. | Make the design checks reproducible. | Earlier validation records retained. | Final narrow validation suite and Git review. |

`docs/requirements_to_test_traceability.csv` required no update: all 69 existing planned test IDs resolve directly to the inventory and all 66 statuses remain `planned`. No source, test, package, runtime configuration, script, data, result, plot, or report-chapter path was created.

## SP-06.1 package foundation

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_06_01_baseline.md` | new | Recorded accepted commit, clean state, Python/pytest availability, absent package/test paths, corrections, scope, and protected hashes. | Preserve the implementation starting point. | No prior audit record changed. | Git, toolchain, path, prerequisite, and hash inspection. |
| `pyproject.toml` | new | Added minimal setuptools metadata for Python >=3.11, src discovery, zero runtime dependencies, optional pytest, and test discovery. | Establish the package foundation. | No lockfile, environment, build, or publication added. | `tomllib`, compile/import, dependency, and scope checks. |
| `src/elevator_access_sim/__init__.py` | new | Added an explicit stable foundation API and `__all__`. | Give later tasks one curated import boundary. | No later simulator behavior exported or implemented. | Package import and export inspection. |
| `src/elevator_access_sim/models.py` | new | Implemented fixed enums/serialization, exception hierarchy, 15 frozen slotted records, and snapshot invariants. | Implement reviewed shared foundations. | Register numbers/names preserved; source correction uses frozen uppercase labels. | Independent enum, immutability, key, raw-boundary, and snapshot checks; pytest pending. |
| `src/elevator_access_sim/config.py` | new | Implemented documented defaults and strict atomic five-field JSON configuration parsing. | Implement Task 1 configuration only. | Credential-file/startup loading remains deferred. | Independent valid/error/endpoint/duplicate/Boolean/nonfinite checks; pytest pending. |
| `src/elevator_access_sim/clock.py` | new | Implemented the clock protocol and deterministic nonnegative monotonic simulated clock. | Provide time injection without real waits. | No scheduler, callback, wall-clock, thread, or async behavior. | Independent monotonicity/failure-atomicity and import/source checks; pytest pending. |
| `tests/unit/test_models.py` | new | Added focused enum, serialization, immutable record, key, raw request, and snapshot tests. | Cover the shared-model Task 1 contract. | No later module imported or tested. | Syntax compiled; execution blocked by unavailable pytest. |
| `tests/unit/test_config.py` | new | Added strict/default/boundary/type/duplicate/malformed/nonfinite/atomic configuration tests. | Cover the Task 1 configuration contract. | Credential-file loading tests remain deferred. | Syntax compiled; execution blocked by unavailable pytest. |
| `tests/unit/test_clock.py` | new | Added start/advance/error/atomicity and prohibited-dependency clock tests. | Cover deterministic simulated time. | Uses no real wait or mock. | Syntax compiled; execution blocked by unavailable pytest. |
| `docs/software_design.md` | pre-existing | Corrected source serialization to uppercase LF/HF and clarified test-only white-box state construction. | Conform to frozen source labels and remove the undefined observer API. | Other enum text/numbers and design remain unchanged. | Targeted text/JSON/API checks. |
| `docs/test_plan.md` | pre-existing | Corrected source expectations and replaced transition-observer language with public observation plus a test-only valid-state fixture. | Make later state tests implementable without production hooks. | No behavioral redesign or pass claim. | Targeted text and scope checks. |
| `docs/test_case_inventory.csv` | pre-existing | Corrected serialized LF/HF expectations and updated TST-RST-005/TST-STA-001 fixture/steps. | Align inventory with the mandatory corrections. | All 100 IDs/rows/statuses retained. | Standard-library CSV width/ID/status and targeted-row checks. |
| `docs/decision_log.md` | pre-existing | Clarified DEC-042/DEC-046 and added DEC-059 for uppercase source serialization with unchanged values. | Preserve the canonical-name correction and history. | DEC-001–DEC-058 retained; no numeric semantics changed. | Decision ID and wording checks. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-06.1 section. | Maintain the canonical change record. | All prior sections retained. | UTF-8 and changed-path review. |
| `audit/stage_reports/subproject_06_01.md` | new | Recorded implementation, corrections, test/tool status, deferred work, validation, and blocker. | Provide the bounded task handoff. | Prior reports retained. | Required-content and readiness-line review. |
| `audit/validation/subproject_06_01_validation.md` | new | Recorded commands, successful non-pytest checks, failed pytest availability, hashes, scope, and Git state. | Preserve accurate execution evidence. | Prior validations retained. | Final compilation/import/custom/Git checks. |

No Wiegand, credential loading/repository, authorization, event logger, output, watchdog, controller, CLI, experiment, physical, database, network, async, or thread implementation was added. Pytest was not installed or otherwise modified; its absence remains the stage blocker.

## SP-06.1R pytest validation unblock

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_06_01_repair_baseline.md` | new | Recorded the accepted commit, clean state, base pytest blocker, external-environment path, authorized scope, protected paths, and pre-repair hashes. | Preserve the narrow repair starting point. | Original blocked records and all protected engineering content retained. | Git, Python/pytest availability, path, history, later-module, and SHA-256 checks. |
| `audit/stage_reports/subproject_06_01_repair.md` | new | Recorded isolated-tool versions, no-defect/no-code-change decision, pytest results, compile/import results, protected scope, deferred work, and readiness. | Provide the SP-06.1R handoff without overwriting historical blocked evidence. | No prior stage report changed. | Scoped/full pytest, compile/import, metadata/API, path, hash, cache, and Git checks. |
| `audit/validation/subproject_06_01_repair_validation.md` | new | Preserved exact environment, installation, version, pytest, compile/import, inspection, cleanup, and Git evidence. | Replace the environmental blocker with reproducible real-pytest evidence. | No source, test, frozen engineering document, or later-stage path changed. | 114/114 scoped and 114/114 full tests passed; final whitespace/status/scope checks passed. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-06.1R section. | Maintain the canonical change audit. | Every prior ledger section retained. | Final diff, UTF-8, whitespace, changed-path, and status review. |

No production or test file changed because real pytest exposed no defect. No Wiegand or later-stage implementation was added. The isolated environment exists only at `/home/bar/.venvs/eeeproject-elevator`, outside the repository.

## SP-06.2 PROJECT_WIEGAND_26 codec

| Path | Pre-existing or new | Change made | Reason | Protected-content check | Validation performed |
|---|---|---|---|---|---|
| `audit/baselines/subproject_06_02_baseline.md` | new | Recorded accepted commit, clean status, external tool versions, 114-test pre-edit result, frozen profile/vectors, authorized/deferred scope, and protected hashes. | Preserve the Task 2 starting point before implementation. | Prior audit and frozen engineering records retained. | Git/history/path/environment, baseline pytest, design consistency, and SHA-256 checks. |
| `src/elevator_access_sim/wiegand.py` | new | Added stateless exact-frame validation, two-region parity, trusted MSB-first encoding/decoding, and structural helper behavior for the single proposed profile. | Implement only SP-06 Task 2. | Imports only reviewed models; no source inference, alternate profile, timing, credential, controller, or physical behavior. | 104 scoped tests, 218 full tests, compile/import, AST/signature, independent vectors, corruptions, malformed inputs, and boundaries. |
| `tests/unit/test_wiegand.py` | new | Added six immutable canonical vectors, independent calculation, 24 corruptions, malformed/trusted-misuse/boundary/round-trip/source-independence/API tests. | Verify FUN-001–FUN-006, DAT-001–DAT-003, VER-002, and VER-004 within Wiegand scope. | Inventory statuses and all protected test-design records unchanged. | 104/104 focused cases passed; no skips or xfails. |
| `src/elevator_access_sim/__init__.py` | pre-existing | Exported `validate_frame`, `decode_frame`, `encode_frame`, and `has_valid_parity` while retaining the complete existing API. | Expose the reviewed Task 2 public contracts. | No private helper or later-stage API exported. | Package and four-symbol imports, `__all__`, signature, cycle, and full-regression checks. |
| `audit/stage_reports/subproject_06_02.md` | new | Recorded implementation, representation/parity/error behavior, vectors/corruptions, exact test results, protected scope, deferred work, and readiness. | Provide the bounded stage handoff. | Prior reports retained. | Required-content, exact-result, scope, and readiness review. |
| `audit/validation/subproject_06_02_validation.md` | new | Recorded commands and evidence for baseline/scoped/full pytest, compile/import, independent validation, cleanup, protected hashes, and Git state. | Preserve reproducible execution evidence. | No protected file changed. | Final pytest, compile/import, programmatic, whitespace, path, cache, and Git checks. |
| `audit/file_change_ledger.md` | pre-existing | Added this SP-06.2 section. | Maintain the canonical change audit. | Every prior ledger section retained. | Final diff, UTF-8, whitespace, authorized-path, and status review. |

No SP-06.3 or later behavior was implemented. The existing external pytest environment was reused without package installation or network access.

## SP-06.3 credential repository and authorization

| Path | Change | Purpose and validation | Protected result |
|---|---|---|---|
| `audit/baselines/subproject_06_03_baseline.md` | new | Captured accepted commit, 218/218 baseline, frozen schema/precedence, scope, and hashes. | Prior records retained. |
| `src/elevator_access_sim/config.py` | modified | Added strict atomic credential/startup JSON loading; schema, duplicate, label, endpoint, atomicity, and error-identity tests passed. | Existing configuration behavior retained. |
| `src/elevator_access_sim/credentials.py` | new | Added validated ordered in-memory repository and composite-key lookup; repository tests passed. | No persistence/database/network. |
| `src/elevator_access_sim/authorization.py` | new | Added pure frozen-precedence floor authorization; 16 grant and 16 denial mappings passed. | No output/log/controller dependency. |
| `src/elevator_access_sim/__init__.py` | modified | Exported repository, authorization, and two loaders while retaining prior API. | No private/later API exported. |
| `tests/unit/test_credential_config.py` | new | Added strict JSON/startup tests. | Inventory unchanged. |
| `tests/unit/test_credentials.py` | new | Added construction/lookup/immutability tests. | No internal index exposed. |
| `tests/unit/test_authorization.py` | new | Added precedence/floor/mask/invariant/purity tests. | No later effects tested or implemented. |
| `audit/stage_reports/subproject_06_03.md` | new | Recorded implementation, exact results, scope, and readiness. | Prior reports retained. |
| `audit/validation/subproject_06_03_validation.md` | new | Recorded pytest, compile/import, programmatic, cleanup, and Git evidence. | Protected hashes retained. |
| `audit/file_change_ledger.md` | modified | Added this section. | Earlier ledger retained. |

Scoped 149/149 and full 367/367 pytest cases passed. SP-06.4 and later behavior remains deferred.

## SP-06.4 event log

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_04_baseline.md` | New baseline with accepted commit, 367/367 gate, frozen schema/API, and scope. | Prior records retained. |
| `src/elevator_access_sim/event_log.py` | New atomic in-memory log, sequence/timestamp ownership, failure injection, startup clear, and JSONL; 58 scoped/425 full tests passed. | Models-only dependency; no persistence/later behavior. |
| `tests/unit/test_event_log.py` | New sequence, timestamp, failure, enum, null/order/export, clear, invariant, and inspection tests. | Inventory unchanged. |
| `src/elevator_access_sim/__init__.py` | Exported `EventLog`, retaining prior API. | No private/later export. |
| `audit/stage_reports/subproject_06_04.md` | New bounded handoff. | Prior reports retained. |
| `audit/validation/subproject_06_04_validation.md` | New execution and scope evidence. | Protected paths unchanged. |
| `audit/file_change_ledger.md` | Added this section. | Earlier ledger retained. |

SP-06.5 and later behavior remains deferred; no commit or push occurred.

## SP-06.5 output manager

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_05_baseline.md` | New accepted baseline and 425/425 gate. | Prior records retained. |
| `src/elevator_access_sim/outputs.py` | New atomic 16-channel activation, expiry, reset, and snapshot manager; 63 scoped/488 full passed. | Models-only; no event/watchdog/controller/physical behavior. |
| `tests/unit/test_outputs.py` | New all-floor, duration, invalid/concurrent, expiry, reset, immutability, and clock-caller tests. | Inventory unchanged. |
| `src/elevator_access_sim/__init__.py` | Exported `OutputManager`. | Prior API retained. |
| `audit/stage_reports/subproject_06_05.md` | New handoff. | Prior reports retained. |
| `audit/validation/subproject_06_05_validation.md` | New execution/scope evidence. | Protected paths unchanged. |
| `audit/file_change_ledger.md` | Added this section. | Earlier ledger retained. |

SP-06.6 watchdog and later behavior remain deferred; no commit or push occurred.

## SP-06.6 watchdog

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_06_baseline.md` | New accepted baseline, 488/488 gate, frozen schedule/API/scope. | Prior records retained. |
| `tests/unit/test_outputs.py` | Added inactive invalid-expiry and startup-reset closure tests; 71/71 passed. | `outputs.py` unchanged. |
| `src/elevator_access_sim/watchdog.py` | New deterministic heartbeat/service/suppression/one-shot-expiry/reinitialize manager. | Models-only; no clock/output/event/controller behavior. |
| `tests/unit/test_watchdog.py` | Added 66 formula, boundary, service, suppression, heartbeat, expiry, epoch, schedule, invalid, and inspection cases. | Inventory unchanged. |
| `src/elevator_access_sim/__init__.py` | Exported `Watchdog`, retaining prior API. | No private/later export. |
| `audit/stage_reports/subproject_06_06.md` | New bounded handoff. | Prior reports retained. |
| `audit/validation/subproject_06_06_validation.md` | New execution, correction, and scope evidence. | Protected paths unchanged. |
| `audit/file_change_ledger.md` | Added this section. | Earlier ledger retained. |

Final watchdog 66/66 and full 562/562 passed. SP-06.7 controller remains deferred; no commit or push occurred.

## SP-06.7 controller coordination

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_07_baseline.md` | New accepted-commit, clean-tree, environment, 562/562 baseline, reviewed contracts, scope, and deferred-work record. | Prior records retained. |
| `tests/unit/test_watchdog.py` | Added direct two-epoch suppression reinjection and disabled-reinitialization coverage; final 68/68 passed. | `watchdog.py` and SP-06.6 records unchanged. |
| `src/elevator_access_sim/controller.py` | New deterministic controller implementing atomic startup, seven states, busy-first processing, validation/lookup/authorization coordination, grant logging gate, due-time scheduler, timeout, resets, immutable observations, and narrow log-fault conversion. | Uses only reviewed managers/models; no CLI, files, experiment, persistence, network, hardware, thread, or async behavior. |
| `src/elevator_access_sim/__init__.py` | Exported `Controller` while retaining every prior public export and explicit `__all__`. | No private helper or later-stage API exported. |
| `tests/unit/test_controller_initialization.py` | New constructor, exact API, startup validation/mapping, atomic publication, correction, guard, and import-scope tests; 45/45 passed. | No JSON/file adapter used. |
| `tests/integration/test_controller_requests.py` | New LF/HF, all-floor, validation/denial/grant/busy, context, order, atomicity, recovery, and invalid-collaborator tests; 94/94 passed. | No production observer or state-forcing API. |
| `tests/integration/test_controller_timing.py` | New clock-boundary, heartbeat, exact timeout, 3000/2000, 30000/2000, suppression, collision, reinjection, partition, replay, and stale-marker tests; 29/29 passed. | Simulated due-time jumps only; no real wait. |
| `tests/integration/test_controller_resets.py` | New manual/watchdog preservation, canceled-timeout, recovery, null-context, and all-seven-state white-box reset tests; 12/12 passed. | State construction remains test-only. |
| `tests/integration/test_controller_logging_faults.py` | New 11-path append-failure matrix, sequence recovery, ordering, and no-op fault persistence tests; 15/15 passed. | No synthetic logging-error event. |
| `audit/stage_reports/subproject_06_07.md` | New bounded implementation handoff with exact results and readiness. | Prior reports retained. |
| `audit/validation/subproject_06_07_validation.md` | New command, outcome, timing, transition, fault, replay, API, scope, cleanup, and Git evidence. | Protected paths unchanged. |
| `audit/file_change_ledger.md` | Added this SP-06.7 section. | Every earlier ledger section retained. |

Final output 71/71, watchdog 68/68, controller 195/195, and full 759/759 suites passed. All named frozen documents, protected source collaborators, prior tests, prior audits, dependency metadata, and Git history remained unchanged. SP-06.8 CLI/file adapters and all later work remain deferred; no commit or push occurred.

## SP-06.8 strict startup files and offline CLI

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_08_baseline.md` | New accepted-commit, clean-tree, environment, 759/759 baseline, reviewed contracts, and scope record. | Prior records retained. |
| `src/elevator_access_sim/config.py` | Added `load_startup_files` with string/PathLike validation, explicit strict UTF-8 reads, atomic text-loader delegation, and configuration/credential error identity. | Existing JSON text loaders and validation rules unchanged; no defaults or cache. |
| `src/elevator_access_sim/cli.py` | Added the four reviewed CLI APIs, all-or-none request parser, exclusive time options, raw source/frame adaptation, ordered controller delegation, deterministic response/snapshot/event JSON, exit policy, and module guard. | No domain-rule duplication, persistent write, service, device, thread, async, or later behavior. |
| `src/elevator_access_sim/__init__.py` | Exported `load_startup_files` while retaining all prior exports. | CLI helpers remain available only from `elevator_access_sim.cli`. |
| `pyproject.toml` | Added the single `elevator-access-sim = "elevator_access_sim.cli:run"` console entry. | Package name/version/Python requirement/dependencies/build/test policy unchanged. |
| `tests/unit/test_config_files.py` | Added 58 temporary-file tests for valid paths/data/order/Unicode/endpoints, strict UTF-8, schemas, duplicates, path/read failures, atomicity, and text-loader preservation. | All test files are under pytest temporary directories. |
| `tests/integration/test_cli.py` | Added 42 parser, adaptation, delegation, domain, timing/reset/watchdog, formatting, exit, determinism, metadata, and structural tests. | Normal execution remains offline and read-only. |
| `audit/stage_reports/subproject_06_08.md` | New bounded handoff with exact results, smoke evidence, scope, and readiness. | Prior reports retained. |
| `audit/validation/subproject_06_08_validation.md` | New command, file/CLI matrix, smoke, compile/import, cleanup, Git, and scope evidence. | Protected paths unchanged. |
| `audit/file_change_ledger.md` | Added this SP-06.8 section. | Every earlier ledger section retained. |

File adapter 58/58, CLI 42/42, and full 859/859 suites passed. The real temporary-file module smoke exited 0 with LF grant and output timeout at 3000, then its temporary directory was removed. SP-06.9 inventory consolidation, experiments/scalability, persistence, networking, databases, GUI, hardware, physical behavior, additional profiles, and optional policies remain deferred; no commit or push occurred.

## SP-06.9 required integration completion and inventory resolution

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_09_baseline.md` | Recorded accepted commit, clean tree, external environment, exact 859/859 baseline, module/document counts, and authorized/protected ownership. | No implementation edit preceded the prescribed baseline. |
| `tests/end_to_end/test_required_flows.py` | Added one four-case public-flow test for invalid source/frame/parity/floor followed by valid grant; 4/4 passed. | No production behavior or CLI command changed. |
| `tests/inspection/test_inventory_traceability.py` | Added parsed requirement/trace/inventory resolution plus concrete-node and status/ownership checks; 2/2 passed. | Frozen traceability contained no broken ID and remained unchanged. |
| `tests/inspection/test_scope_environment.py` | Added six deterministic AST/file inspections for title, scope, optional gates, ownership, environment, UTF-8/paths, and claim boundaries; 6/6 passed. | No network, device, fragile limitation-term rejection, or production mutation. |
| `docs/test_case_inventory.csv` | Promoted 88 evidence-backed Task-9 rows from `designed` to `implemented`; retained 12 later/optional rows as `designed`. | Columns, IDs, requirements, expectations, fixtures, and notes unchanged. |
| `audit/validation/subproject_06_09_inventory_resolution.csv` | Added 100 ordered mappings: 67 existing, 3 SP-06.9 executable, 18 SP-06.9 inspection, 5 SP-06.10, 1 SP-06.11, 6 optional, 0 unresolved. | No experiment or final-documentation row is falsely passed. |
| `audit/stage_reports/subproject_06_09.md` | Added bounded gap analysis, evidence matrices, ownership, exact validation, deviations, and readiness. | Later stages and optional work remain distinct. |
| `audit/validation/subproject_06_09_validation.md` | Added command outcomes, CSV/resolver results, behavior/fault/value matrices, scope checks, cleanup, and Git evidence. | No skipped/xfail result or unsupported claim. |
| `audit/file_change_ledger.md` | Added this SP-06.9 section. | Every earlier ledger section retained. |

Final end-to-end 4/4, integration 192/192, inspection 8/8, focused canonical matrix 97/97, and full 871/871 suites passed with no failures, skips, or xfails. Compilation, imports, and three-file standard-library CSV validation passed. No production source, requirement, traceability, architecture, register, design, sequence, decision, dependency, prior test/audit, evidence, literature, or Git-history change occurred. SP-06.10 experiments and SP-06.11 final documentation remain scheduled; optional work remains deferred; no commit or push occurred.

## SP-06.10 deterministic scalability experiments and evidence repair

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/baselines/subproject_06_10_baseline.md` | Recorded accepted SP-06.9 commit, clean 871/871 baseline, 88/12 inventory handoff, authorized paths, and interpretation boundary. | Preserved unchanged through repair. |
| `audit/baselines/subproject_06_10_repair_baseline.md` | Recorded incomplete commit, clean 962/962 repair baseline, six existing artifacts, missing evidence, strict-mix defect, and repair boundary. | Original baseline/prior audits retained. |
| `experiments/scalability_config.json` | Added strict schema-1 `SP06_SCALABILITY_V1` configuration with seed 260516, four sizes, 1/3 repetitions, 100/2000 timing configuration, disabled watchdog, and 40/20/15/15/10 mix. | Program defaults and requirements unchanged. |
| `scripts/run_experiments.py` | Added strict parser, domain-seeded immutable generation, canonical checksums, public-controller repetitions, `Controller.submit` timing, fmean/median/nearest-rank-p95/throughput aggregation, reconciliation, environment/results validation, CLI, and atomic sibling output. Repair made the official mix an exact immutable comparison. | No production optimization, new dependency, concurrency, device/service, or threshold. |
| `tests/experiment/test_run_experiments.py` | Added 94 configuration/generation/size/mix/outcome/p95/fake-timer/schema/environment/export/CLI/structure cases, including two positive total-100 official substitution regressions and non-official support. | No skip, xfail, external dependency, raw fixture, or production mutation. |
| `results/scalability_results.json` | Runner-generated 12 aggregate rows for four sizes and three measured repetitions; all counts, metrics, checksums, and environment references validate. | Contains no generated inputs, event records, sample arrays, identifiers, paths, or threshold claim. |
| `results/scalability_environment.json` | Runner-generated bounded non-secret environment/configuration/limitation record with stable ID. | Explicitly observational software-model evidence only. |
| `docs/test_case_inventory.csv` | Promoted only `TST-REP-001`, `TST-REP-002`, and `TST-SCL-001`–`003`; final status 93 implemented/7 designed. | `TST-TRC-005`, six optional rows, every other cell, order, and IDs retained. |
| `tests/inspection/test_inventory_traceability.py` | After a reproduced 964/1 regression, narrowly allowed historically scheduled SP-06.10 rows to reflect later implementation while still requiring SP-06.11 to remain designed. | SP-06.9 resolution CSV, class/status history, ID links, optional deferrals, and SP-06.11 gate retained. |
| `audit/stage_reports/subproject_06_10.md` | Added complete handoff, generation/checksum, execution/metric, result, inventory, repair, scope, and readiness record. | SP-06.11 remains deferred. |
| `audit/validation/subproject_06_10_validation.md` | Added exact commands/results, smoke/full outcomes, 12-row reconciliation, checksums, defect evidence/correction, final gates, cleanup, and scope record. | No unexecuted result claimed. |
| `audit/file_change_ledger.md` | Added this complete SP-06.10/R/R2 section. | Every earlier ledger section retained. |

R2 baseline 965/965, experiment 94/94, bounded smoke, official 12-row run, standalone schema/count/metric/checksum/environment checks, targeted resolver 2/2, corrected regression 965/965, compilation, imports, and final Git/scope/cleanup checks passed. The first promoted-inventory regression intentionally recorded the stale-test defect at 964/965 before its narrow correction. No SP-06.11 work, optional behavior, production source change, commit, or push occurred.

## Pre-SP-06.11 nondeterministic baseline investigation and PathLike test hardening

| Path | Change and validation | Protected result |
|---|---|---|
| `tests/unit/test_config_files.py` | Hardened only the bytes-resolving configuration `PathLike` test with an absolute `tmp_path`-derived bytes path, a guarded `builtins.open`, exact exception identity/message assertions, and zero-open verification. The original failure did not reproduce after cache removal; pre- and post-repair 100-node, 30-file, and five-full-suite matrices passed. | Production startup-file behavior, the other 57 module tests, dependencies, and unrelated tests remained unchanged. |
| `audit/validation/subproject_06_11_baseline_flake_repair.md` | Recorded the reported failure, local module origin, mutation/cache inspection, evidence-versus-inference boundary, reproduction matrices, narrow hardening, canonical 965/965 baseline, structural validation, cleanup, and scope. | Does not claim an unproved stale-bytecode or pollution cause and does not begin SP-06.11 documentation. |
| `audit/file_change_ledger.md` | Added only this narrow repair section. | Every earlier ledger section retained. |

Final repaired-node 100/100, configuration-file 30/30 at 58 tests per run, varied-seed full-suite 5/5 at 965 tests per run, and canonical baseline 965/965 validation passed with zero failures, skips, or xfails. Compilation and imports passed. No production source, SP-06.11 documentation, inventory, traceability, scalability artifact, dependency, optional feature, commit, or push occurred.

## SP-06.11 final documentation, reproducibility, verification, and reconciliation

| Path | Change and validation | Protected result |
|---|---|---|
| `README.md` | Replaced the one-line placeholder with the exact title, status, capabilities, repository map, setup/test/CLI/experiment entry points, final verification state, and limitations/later work. | No unsupported commercial, physical, safety, real-time, production-readiness, CI, or approval claim. |
| `docs/reproducibility.md` | Added the single detailed no-install/editable/focused-test/temporary-CLI/temporary-experiment/result-validation/cleanup/troubleshooting authority. | Uses repository-relative paths; no developer identity/path; no duplicate manual or timing threshold. |
| `docs/test_plan.md` | Appended only `SP-06 execution outcome and canonical evidence`, distinguishing prospective SP-05 design from actual records and linking six canonical artifacts. | Every earlier designed expectation and non-pass disclaimer retained. |
| `audit/validation/subproject_06_11_verification_records.csv` | Added 100 inventory-ordered expected-versus-actual rows with the exact 13 columns, 94 passed and six optional-deferred evaluations, concrete evidence, and environment references. | Optional work is not falsely passed; no fabricated timing or absolute path. |
| `docs/test_case_inventory.csv` | Promoted only `TST-TRC-005.status` from designed to implemented after its verification-record test passed. | Final 94 implemented/6 optional designed; every other cell/order/ID retained. |
| `docs/requirements_to_test_traceability.csv` | Changed only status cells: 60 required planned rows to verified and six optional planned rows to optional_deferred. | All other columns/order/IDs preserved; no optional requirement claimed verified. |
| `tests/inspection/test_inventory_traceability.py` | Narrowly allowed the one historically scheduled SP-06.11 row, like SP-06.10 rows, to reflect later live implementation. | Historical SP-06.9 CSV/classes/counts/order/evidence/reference checks and optional-designed rule retained. |
| `tests/inspection/test_documentation_reproducibility.py` | Added 11 README/reproducibility/verification/inventory/traceability/test-plan/UTF-8/link/claim/metadata/repair/scalability inspections. | Context-aware limitations; no order dependence, production import, network, or optional execution. |
| `audit/baselines/subproject_06_11_baseline.md` | Recorded accepted clean commit/environment, 965/965 baseline, repair hash, 93/7 and 66-planned handoff, experiment artifacts, scope, approvals, and deferrals. | No edit preceded the prescribed baseline. |
| `audit/stage_reports/subproject_06_11.md` | Added final documentation/reconciliation and reproduction handoff, including deviations and boundaries. | Human/later-project work remains explicit. |
| `audit/validation/subproject_06_11_validation.md` | Added exact baseline, test, smoke, copy, artifact, failure/correction, final-command, cleanup, scope, and readiness evidence. | No unexecuted success or behavioral claim. |
| `audit/file_change_ledger.md` | Added only this SP-06.11 section. | Every earlier ledger section retained. |

SP-06.11 final validation passed the documentation and historical resolver modules, every published pytest command, 976-test repository and copied-tree suites, CLI grant/timeout reproduction, temporary 12-row experiment, standalone reconciliation, compilation/import, UTF-8/path/link/schema/claim/metadata/repair preservation, Git scope, and cleanup gates. No protected behavior, optional feature, prior evidence, release, commit, or push occurred.

## SP-06.11R final verification-record provenance repair

| Path | Change and validation | Protected result |
|---|---|---|
| `audit/validation/subproject_06_11_verification_records.csv` | Corrected only 15 historically inaccurate `environment_reference` cells after auditing all 100 evidence rows against test-file creation commits and stage execution records. | Exact schema/order/content/evaluation counts retained; evidence nodes unchanged; experiment/SP-06.11/optional special provenance retained. |
| `tests/inspection/test_documentation_reproducibility.py` | Extended the existing verification-record test with an explicit immutable 21-test-path provenance map, multi-stage semantics, exact environment ownership, special-case checks, and five named regressions. | Existing schema/order/expected-actual/node/inventory/traceability/UTF-8/path/claim/metadata/repair checks remain intact; test count stays 976. |
| `audit/validation/subproject_06_11_provenance_repair.md` | Added accepted baseline, complete 15-row before/after evidence, pre-repair failure, semantic/standalone/full/copied/structural validation, scope, cleanup, and readiness. | Does not rewrite accepted SP-06.11 records or infer provenance from inventory category. |
| `audit/file_change_ledger.md` | Added only this narrow provenance-repair section. | Every earlier ledger section retained. |

Final provenance validation passed all 100 rows, documentation 11/11, resolver 2/2, full and copied-tree suites 976/976, compilation/import, Git scope, and cleanup. Inventory remains 94/6 and traceability remains 60/6. No simulator behavior, Subproject-7 work, release, commit, or push occurred.

## SP-07.1 experiment evidence consolidation and quantitative-analysis baseline

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/analyze_results.py` | Added a strict standard-library evidence analyzer with UTF-8/duplicate-JSON/exact-CSV validation, provenance and count reconciliation, frozen-result checks, descriptive summaries, deterministic serialization, CLI contracts, and rollback-safe paired publication. | Does not import or change the simulator, run a benchmark, add a dependency, network, plot, thread, async task, sleep, or threshold. |
| `data/results/sp07_experiment_catalog.csv` | Generated seven ordered experiment rows mapping implemented test IDs, concrete evidence, completeness, quantitative artifacts, limits, and bounded actions. | Optional work is not executed; EXP-05 identifies rather than conceals the isolated-timing gap. |
| `data/results/sp07_quantitative_summary.json` | Generated schema-1 `SP07_ANALYSIS_BASELINE_V1` with seven source hashes, 976/976, 60/6, 94/6, seven-experiment coverage, 12-row/39000-request totals, per-size repetition statistics, null unavailable metrics, limits, and deferred work. | Existing mixed-submit host timing is not labeled lookup/query latency; no pooled percentile, host determinism, hardware, real-time, safety, or commercial inference. |
| `tests/analysis/test_analyze_results.py` | Added 31 focused cases for schemas, corruptions, reconciliations, catalog, totals/statistics, claims, determinism, atomicity, CLI, and structural boundaries. | Uses temporary corruptions/outputs and leaves accepted evidence unchanged. |
| `audit/baselines/subproject_07_01_baseline.md` | Recorded exact clean commit/environment, 976/976 baseline, hashes, counts, identifiers, scope, limitations, and deferrals. | No implementation edit preceded the prescribed baseline. |
| `audit/stage_reports/subproject_07_01.md` | Recorded seven-experiment classification, existing evidence/gaps, quantitative values, statistical rules, hashes, validation, deviations, scope, and handoff. | SP-07.2/3/4 and Subproject 8 remain deferred. |
| `audit/validation/subproject_07_01_validation.md` | Recorded executed commands, failure/correction evidence, source/catalog/summary checks, hashes, totals, determinism, atomicity, tests, compilation/imports, scope, cleanup, and readiness. | No unexecuted success or new measurement claim. |
| `audit/file_change_ledger.md` | Added only this SP-07.1 section. | Every earlier ledger section retained. |

The catalog and summary hashes are `511d0955fae5d501c0a4cb1caffaf64a8535a32cda366f0eea74b99da8916808` and `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0`. The accepted inputs remain byte-identical. SP-07.1 creates no benchmark result, raw timing data, figure, report prose, optional behavior, Subproject-8 work, release, commit, or push.

## SP-07.1R catalog evidence and canonical-source integrity repair

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/analyze_results.py` | Added explicit EXP-07 direct/context evidence, mandatory sufficiency validation, and seven-input CLI canonical resolved-path identity enforcement before parsing/publication. | Lower-level temporary-fixture validation remains available; output paths remain selectable; no benchmark, package, simulator, or dependency change. |
| `tests/analysis/test_analyze_results.py` | Added five focused tests covering complete EXP-07 evidence, resolving-but-incomplete rejection, relative/absolute canonical identity, byte-identical/valid substitute rejection, label/hash identity, stable CLI error, and output preservation. | Generic catalog, optional, EXP-05, corruption, determinism, atomicity, CLI, and structural checks remain intact. |
| `data/results/sp07_experiment_catalog.csv` | Deterministically regenerated EXP-07 with three required executable nodes plus SP-06.8/SP-06.7 validation context; new hash `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb`. | Same nine columns, seven ordered rows, mapped IDs, classifications, quantitative artifacts, limitations, and actions. |
| `audit/validation/subproject_07_01_repair.md` | Added exact baseline, defects, corrections, regressions, regeneration/hashes, independent validation, test/structural results, scope, cleanup, and readiness. | Accepted SP-07.1 baseline, stage, and validation records remain historical and unchanged. |
| `audit/file_change_ledger.md` | Added only this narrow SP-07.1R section. | Every earlier ledger section retained. |

The quantitative summary remains byte-identical at `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0`; all seven accepted source hashes and quantitative totals remain unchanged. No accepted measurement, behavior, traceability, benchmark, figure, SP-07.2 work, commit, or push occurred.

## SP-07.2 isolated credential-lookup and authorization experiment

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/run_experiments.py` | Added the distinct strict standard-library runner with exact config parsing, three-domain deterministic generation, canonical checksums, isolated public-operation timing, complete matrices, nearest-rank metrics, validation, bounded environment collection, CLI, and rollback-safe paired publication. | No `Controller`, Wiegand, old-runner import, simulator mutation, dependency, network/database server, concurrency, sleep, plot, or threshold. |
| `experiments/isolated_operations_config.json` | Added exact schema-1 `SP07_ISOLATED_OPERATIONS_V1` / `LOOKUP_AUTHORIZATION_MATRIX_V1`, seed 270516, four sizes, 1000 cases, 1/3 repetitions, 60/20/20 pools, 50/50 lookup, and 40/20/15/15/10 authorization. | Accepted mixed configuration remains unchanged. |
| `data/results/sp07_isolated_operation_results.json` | Official single-run 24-row aggregate output with 12000 lookup plus 12000 authorization calls, diagonal matrices, explicit correct/incorrect counts, finite metrics, checksums, and one environment ID. | Contains no raw records/cases/samples, controller/event state, path, identity, or threshold claim. |
| `data/results/sp07_isolated_operation_environment.json` | Added deterministic bounded host/config/operation-definition/interpretation record `env-5b6705a77f411683`. | Explicit software/host variability and no physical, real-time, safety, certification, or commercial inference. |
| `tests/analysis/test_run_isolated_experiments.py` | Added 64 strict-config, generation, case, matrix, mismatch, metric, boundary, schema, environment, atomicity, CLI, and structural cases. | Existing tests and production remain unchanged. |
| `audit/baselines/subproject_07_02_baseline.md` | Recorded clean accepted commit/environment, 1012/1012 baseline, accepted hashes, gap, scope, boundaries, and deferrals. | No implementation edit preceded the baseline. |
| `audit/stage_reports/subproject_07_02.md` | Added exact configuration/generation/boundary/matrix/metric/run/reproduction/result/limit/test/protection/handoff record. | SP-07.3 and SP-07.4 remain deferred. |
| `audit/validation/subproject_07_02_validation.md` | Added command, focused matrix, official run, reproduction, 24-row/aggregate/checksum/environment/independent/full/structural/scope/cleanup evidence. | No unexecuted success or unsupported performance claim. |
| `audit/file_change_ledger.md` | Added only this SP-07.2 section. | Every earlier ledger section retained. |

Official hashes are config `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838`, results `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1`, and environment `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec`. No simulator, accepted mixed benchmark, SP-07.1 artifact, figure, report, SP-07.3/SP-07.4 work, commit, or push occurred.

## SP-07.2R direct-call timing-boundary repair

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/run_experiments.py` | Removed the callable-executing timer helper and lambda wrappers; added captured-reading validation and direct lookup/authorization calls between timer reads. | Workload generation, classification, matrices, metrics, schemas, public operations, and production source remain unchanged. |
| `tests/analysis/test_run_isolated_experiments.py` | Added an AST regression proving direct operation placement, no lambda/generic executor, post-timer classification, pre-timer argument binding, and pre-loop repository construction. | Retained behavioral event-order, fake-timer, 24-row, schema, CLI, atomicity, and structural coverage. |
| `data/results/sp07_isolated_operation_results.json` | Replaced the superseded wrapper-inclusive timing values with the single corrected direct-call run. | All non-timing fields are identical; no raw cases, credentials, or timing samples were added. |
| `audit/validation/subproject_07_02_timing_boundary_repair.md` | Added accepted-state, defect, correction, regression, single-run, identity, reproduction, independent, final-validation, scope, and readiness evidence. | Existing SP-07.2 baseline/stage/validation records remain historical and unchanged. |
| `audit/file_change_ledger.md` | Added only this SP-07.2R section. | Every earlier ledger section retained. |

The result hash changed from `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1` to `9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf`; environment bytes remain unchanged. The original timing rows are superseded, and no cross-boundary performance comparison was made. No simulator, mixed benchmark, SP-07.1 artifact, SP-07.3/SP-07.4 work, commit, or push occurred.

## SP-07.3 integrated quantitative analysis, tables, and SVG figures

Canonical inputs were the immutable historical catalog/summary, accepted mixed config/results/environment, accepted isolated config/corrected results/environment, and SP-07.2R repair validation. Their exact hashes are recorded in the SP-07.3 baseline, stage report, validation record, and generated manifest.

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/generate_figures.py` | Added strict standard-library source validation, integration, statistics, CSV/JSON/SVG/manifest serialization, canonical CLI, deterministic staging, rollback, and post-write validation. | Imports/calls no runner, simulator, plotting package, network, database, subprocess, thread, async, multiprocessing, or sleep. |
| `data/results/sp07_experiment_catalog_integrated.csv` | Added seven ordered historical-schema rows; only integrated EXP-05 meaning changes to `complete_existing_with_limit`. | Historical catalog remains byte-identical; mapped IDs and six other row meanings retained. |
| `data/results/sp07_quantitative_summary_integrated.json` | Added versioned 14-field integration of accepted verification, requirements, inventory, mixed, isolated, correctness, timing, availability, limitations, and deferrals. | No timestamp, identifying path, pooled statistic, threshold, or unsupported guarantee. |
| `data/results/sp07_table_experiment_coverage.csv` | Added seven report-ready coverage rows with repository-relative evidence and bounded scope. | No final report conclusion or optional execution claim. |
| `data/results/sp07_table_correctness.csv` | Added 22 calculated rows for the accepted 976 snapshot, mixed outcomes, lookup matrix, and authorization classifications. | `other_outcomes` remains reconciliation, not a false-positive/false-negative measure. |
| `data/results/sp07_table_timing_summary.csv` | Added 12 ordered rows with min/median/max across exactly three repetition aggregates for four separate sizes in three operation groups. | No pooling, cross-family ranking, significance, constant-time, or asymptotic claim. |
| `docs/figures/sp07_mixed_controller_average_ns.svg` | Added accessible deterministic mixed `Controller.submit` SVG with source-derived repetition points, median line, min/max whiskers, axes, and limits. | Explicitly not isolated lookup timing or hardware/real-time evidence. |
| `docs/figures/sp07_lookup_average_ns.svg` | Added accessible deterministic direct lookup SVG with source-derived values and boundary note. | Repository construction excluded; no comparison ranking. |
| `docs/figures/sp07_authorization_average_ns.svg` | Added accessible deterministic direct authorization SVG with source-derived values and boundary note. | Credential lookup excluded; no comparison ranking. |
| `data/results/sp07_report_artifact_manifest.json` | Added nine source hashes, eight nonrecursive generated hashes, media/count metadata, generation contract, and limits. | Excludes its own recursive hash; no host/timestamp identity. |
| `tests/analysis/test_generate_figures.py` | Added 26 focused parser, corruption, identity, reconciliation, table, SVG, determinism, rollback, CLI, and AST cases. | Uses temporary fixtures/outputs only and executes no benchmark or simulator operation. |
| `audit/baselines/subproject_07_03_baseline.md` | Recorded exact accepted commit, environment, 1077 baseline, source hashes, scope, statistical/figure semantics, and deferrals. | No implementation preceded the baseline. |
| `audit/stage_reports/subproject_07_03.md` | Added bounded outcome, source, reconciliation, statistics, SVG, deterministic generation, hash, validation, limitation, and handoff record. | Not final report or discussion prose; later stages deferred. |
| `audit/validation/subproject_07_03_validation.md` | Added exact gates, commands, schemas, hashes, double generation, independent checks, tests, scope, cleanup, and readiness evidence. | Claims only executed validation results. |
| `audit/file_change_ledger.md` | Added only this SP-07.3 section. | Every earlier ledger section retained. |

Generated hashes are integrated catalog `b86c0841...db9a`, integrated summary `95f532d8...670c`, coverage `f7aef893...c78f`, correctness `2ee80a42...224`, timing `5c777e8f...0811`, mixed SVG `7ad5f265...6930`, lookup SVG `26269c62...a096`, authorization SVG `43394313...2f9`, and manifest `f4fe7d51...16b1`. Two official generations were byte-identical. No benchmark, accepted-source mutation, report, presentation, SP-07.4, Subproject-8, release, commit, or push occurred.

## SP-07.3R integrated-catalog semantics and publication-rollback repair

| Path | Change and validation | Protected result |
|---|---|---|
| `analysis/generate_figures.py` | Added the exact repaired EXP-05 question and semantic validator; pre-backs up all destinations; attempts all restorations; retains failed-recovery backups; distinguishes complete/incomplete rollback without catching programming defects. | Calculations, sources, tables, figures, manifest schema, dependencies, and no-benchmark boundary retained. |
| `tests/analysis/test_generate_figures.py` | Added exact historical/repaired question checks, stale-question rejection, incomplete-rollback restoration/backup/recovery coverage, and honest CLI failure coverage. | All existing success, identity, determinism, table, SVG, manifest, normal rollback, CLI, and AST tests retained. |
| `data/results/sp07_experiment_catalog_integrated.csv` | Deterministically regenerated only the EXP-05 planned question; hash `b86c0841...db9a` → `9270a15c...6ff8`. | Six rows and all other EXP-05 fields remain identical; historical catalog unchanged. |
| `data/results/sp07_report_artifact_manifest.json` | Deterministically refreshed only the integrated-catalog generated-artifact hash; manifest hash `f4fe7d51...16b1` → `69235fab...4851`. | Manifest schema, sources, seven other generated hashes, contract, and limitations retained. |
| `audit/validation/subproject_07_03_repair.md` | Added baseline, defects, exact question delta, rollback algorithm, recovery, tests, regeneration, hashes, independent/final validation, scope, cleanup, and readiness evidence. | Prior SP-07.3 audit records remain unchanged historical evidence. |
| `audit/file_change_ledger.md` | Added only this narrow SP-07.3R section. | Every prior ledger section retained. |

The integrated summary, three tables, and three SVGs remain byte-identical. No benchmark, accepted measurement/configuration, simulator, historical analysis, report, presentation, SP-07.4, Subproject-8, release, commit, or push occurred.
