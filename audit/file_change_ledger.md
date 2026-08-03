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
