# Final Engineering Report Content Architecture

This is a template-neutral content architecture, not final report prose. Numbering and formatting may change only after authoritative university requirements are supplied. The evidence, claim, asset, and limitation mappings below are authoritative inputs for later drafting; they are not approved submission paragraphs.

## 1. Abstract

- **Purpose:** Plan a bounded summary of problem, software-only method, principal verified outcomes, and limitations.
- **Questions:** What was modeled, how was it verified, what evidence was produced, and what cannot be concluded?
- **Canonical sources:** `README.md`; `docs/methodology.md`; `data/results/sp07_independent_review_summary.json`.
- **Evidence classes:** project governance; supported quantitative claim with explicit limitations.
- **Claim IDs:** RPT-013–RPT-025; SP-07 CLM-001–CLM-039 as applicable.
- **Proposed tables and figures:** None unless the approved template permits a graphical abstract.
- **Mandatory limitations:** Software-only abstract access layer; one-host aggregate timings; no product, hardware, real-time, safety, or commercial equivalence.
- **Prohibited claims:** Final approval, product implementation attribution, physical validation, statistical significance, constant-time behavior.
- **Unresolved inputs:** Official title, report/abstract language, word limit, template, student and supervisor identities.
- **Drafting status:** `blocked_by_human_input`.

## 2. Introduction

- **Purpose:** Plan motivation, engineering problem, evidence-led approach, objectives, and chapter map.
- **Questions:** Why is access authorization studied, why is evidence classification necessary, and what is the project boundary?
- **Canonical sources:** `final_engineering_project_plan.md`; `README.md`; `docs/methodology.md`.
- **Evidence classes:** project governance; engineering inference.
- **Claim IDs:** RPT-001; RPT-025; evidence CLM-005 and CLM-016.
- **Proposed tables and figures:** `docs/figures/system_context.mmd` as a planned diagram source, subject to later approved rendering.
- **Mandatory limitations:** Motivation does not establish technical properties of the commercial card.
- **Prohibited claims:** Product reverse engineering, production readiness, physical elevator control, university approval.
- **Unresolved inputs:** Approved title, institutional framing, language, expected introduction length.
- **Drafting status:** `ready_with_limits`.

## 3. Product Under Study and Available Evidence

- **Purpose:** Inventory the preserved product identifier and state precisely what evidence is unavailable.
- **Questions:** What was supplied, what was preserved, and which commercial details remain unknown?
- **Canonical sources:** `evidence/product_evidence.md`; `evidence/assumptions_and_unknowns.md`; `evidence/source_index.md`; `evidence/unresolved_sources.md`.
- **Evidence classes:** verified product evidence; unknown or unresolved.
- **Claim IDs:** RPT-001; RPT-002; RPT-026; evidence CLM-001–CLM-003, CLM-015, CLM-026.
- **Proposed tables and figures:** Product-evidence inventory table; product image only if a preserved file and permission later exist.
- **Mandatory limitations:** Only URLs and limited owner-supplied evidence are preserved; the original capture, listing content, images, markings, and technical documentation are unavailable.
- **Prohibited claims:** Commercial ARM/STM32/MCU, RFID frequency, MIFARE/NFC, Wiegand, relay/driver, voltage, wiring, firmware, or certification attribution.
- **Unresolved inputs:** Original product capture, seller/manufacturer documentation, reproduction permission.
- **Drafting status:** `ready_with_limits`.

## 4. Research Methodology and Limitations

- **Purpose:** Map the evidence hierarchy, literature selection, claim classification, simulation method, and human-review boundary.
- **Questions:** How were sources selected, uncertainties controlled, decisions separated, and results independently reviewed?
- **Canonical sources:** `docs/methodology.md`; `evidence/claim_evidence_matrix.csv`; `evidence/source_index.md`; `audit/validation/subproject_07_04_repair.md`.
- **Evidence classes:** project governance; external technical evidence; engineering inference; unknown or unresolved.
- **Claim IDs:** RPT-027; evidence CLM-020; SP-07 CLM-036–CLM-039.
- **Proposed tables and figures:** Evidence-class definition table; no new figure in SP-08.1.
- **Mandatory limitations:** Lower-authority evidence is never promoted; simulation validates the proposed model only.
- **Prohibited claims:** Complete product characterization, exhaustive literature coverage, supervisor approval, formal statistical inference.
- **Unresolved inputs:** University methodology expectations and citation style.
- **Drafting status:** `ready_for_draft`.

## 5. Literature Review

- **Purpose:** Plan source-scoped discussion of RFID, Wiegand, authorization, representative embedded concepts, and verification guidance.
- **Questions:** Which general concepts are supported, how do technology layers differ, and where do source gaps remain?
- **Canonical sources:** `evidence/literature_notes.md`; `docs/literature_review_outline.md`; `evidence/source_index.md`; `evidence/unresolved_sources.md`; `report/references.bib`.
- **Evidence classes:** external technical evidence; proposed reference design; unknown or unresolved.
- **Claim IDs:** RPT-003–RPT-005; evidence CLM-006–CLM-012, CLM-017–CLM-022.
- **Proposed tables and figures:** Literature authority/scope table; no copied source figure.
- **Mandatory limitations:** ARM/STM32 sources are representative, not product evidence; ARMv7-A/R is not Cortex-M documentation; RFID frequency, credential technology, and Wiegand framing remain separate layers; incomplete educational-PDF metadata remains explicit.
- **Prohibited claims:** Commercial-card technology attribution, universal Wiegand electrical specification, unverified author/date/title metadata.
- **Unresolved inputs:** SRC-MISSING-006, SRC-MISSING-007, citation style, metadata for SRC-ARM-003/004 and SRC-ACADEMIC-001.
- **Drafting status:** `ready_with_limits`.

## 6. Requirements and System Boundary

- **Purpose:** Plan required/optional behavior, traceability, logical interfaces, and the access-layer safety boundary.
- **Questions:** What must the project model do, what is deferred, and how is every required item verified?
- **Canonical sources:** `docs/requirements.md`; `docs/requirements_to_test_traceability.csv`; `docs/test_case_inventory.csv`; `docs/decision_log.md`.
- **Evidence classes:** proposed reference design; accepted simulator evidence; engineering inference.
- **Claim IDs:** RPT-006–RPT-011; RPT-013; RPT-025; SP-07 CLM-003–CLM-006.
- **Proposed tables and figures:** Requirements summary; `docs/figures/system_context.mmd`; traceability table reference.
- **Mandatory limitations:** Requirements describe the project-specific software model, not commercial behavior; physical elevator motion and passenger safety remain outside scope.
- **Prohibited claims:** Industrial/electrical requirements, product protocol compatibility, safety-system authority.
- **Unresolved inputs:** Supervisor confirmation of scope and physical-component expectation.
- **Drafting status:** `ready_for_draft`.

## 7. Proposed Reference Architecture

- **Purpose:** Plan conceptual blocks, ownership, states, data flow, register model, reset, and watchdog architecture.
- **Questions:** How are responsibilities separated, how does data move, and which elements are conceptual-only?
- **Canonical sources:** `docs/architecture.md`; `docs/register_model.md`; `docs/architecture_to_requirements.csv`; `docs/decision_log.md`; `docs/figures/top_level_architecture.mmd`; `docs/figures/controller_state_machine.mmd`.
- **Evidence classes:** proposed reference design; engineering inference; external technical evidence.
- **Claim IDs:** RPT-006–RPT-011; evidence CLM-004, CLM-011, CLM-013, CLM-025, CLM-027–CLM-031.
- **Proposed tables and figures:** Top-level architecture, firmware architecture, data flow, state machine, watchdog/reset sequences, logical register map.
- **Mandatory limitations:** Every design element is project-specific or representative; logical registers have no physical address/MCU implication; access outputs are abstract permission channels.
- **Prohibited claims:** Exact commercial architecture, electrical interface, MCU selection, elevator motion/safety design.
- **Unresolved inputs:** Supervisor architecture confirmation and any future physical-integration authority.
- **Drafting status:** `ready_with_limits`.

## 8. Software-Model Design and Implementation

- **Purpose:** Plan module responsibilities, immutable models, validation, orchestration, simulated timing, logging, CLI, and implementation evidence.
- **Questions:** How do modules implement the frozen contracts and preserve deterministic state ownership?
- **Canonical sources:** `docs/software_design.md`; `src/elevator_access_sim/`; `docs/register_model.md`; `docs/reproducibility.md`.
- **Evidence classes:** accepted simulator evidence; proposed reference design.
- **Claim IDs:** RPT-006–RPT-012; evidence CLM-013, CLM-023, CLM-027–CLM-031.
- **Proposed tables and figures:** Module-responsibility table; selected architecture/state diagrams; no pasted source code.
- **Mandatory limitations:** Discuss module names and public contracts through canonical paths; implementation is Python software, not firmware for a commercial controller.
- **Prohibited claims:** Hardware execution, MCU register implementation, persistent-database performance, code excerpts as substitute for explanation.
- **Unresolved inputs:** Approved report depth and appendix code-selection policy.
- **Drafting status:** `ready_for_draft`.

## 9. Verification and Experimental Method

- **Purpose:** Plan traceable tests, deterministic workloads, timing boundaries, environment capture, and independent review.
- **Questions:** What was tested, which snapshot is historical, how were workloads generated, and what exactly was timed?
- **Canonical sources:** `docs/test_plan.md`; `audit/validation/subproject_06_11_verification_records.csv`; `docs/reproducibility.md`; `experiments/scalability_config.json`; `experiments/isolated_operations_config.json`; `data/results/sp07_quantitative_summary_integrated.json`.
- **Evidence classes:** accepted simulator evidence; supported quantitative claim with explicit limitations; external technical evidence.
- **Claim IDs:** RPT-013–RPT-014; RPT-016; RPT-018; RPT-020; SP-07 CLM-001–CLM-006, CLM-026–CLM-031, CLM-036–CLM-038.
- **Proposed tables and figures:** Experiment-coverage table; workload/boundary table; verification traceability appendix reference.
- **Mandatory limitations:** The accepted 976-test SP-06 verification snapshot is historical and distinct from later repository-wide totals; workloads are deterministic; mixed `Controller.submit`, direct lookup, and direct authorization boundaries differ; timings are one-host, three-repetition aggregates with no raw pooled samples.
- **Prohibited claims:** Pooled percentiles, significance, monotonic scaling, constant-time/asymptotic proof, hardware timing.
- **Unresolved inputs:** None for method planning; citation/format decisions remain human inputs.
- **Drafting status:** `ready_with_limits`.

## 10. Results

- **Purpose:** Plan source-faithful presentation of accepted verification, correctness, timing tables, and figures.
- **Questions:** Which outcomes were observed, which aggregates are report-usable, and which qualifiers accompany them?
- **Canonical sources:** `data/results/sp07_table_experiment_coverage.csv`; `data/results/sp07_table_correctness.csv`; `data/results/sp07_table_timing_summary.csv`; `docs/figures/sp07_mixed_controller_average_ns.svg`; `docs/figures/sp07_lookup_average_ns.svg`; `docs/figures/sp07_authorization_average_ns.svg`; `audit/validation/subproject_07_final_validation_ledger.csv`.
- **Evidence classes:** supported quantitative claim with explicit limitations.
- **Claim IDs:** RPT-013–RPT-021; SP-07 CLM-001–CLM-038.
- **Proposed tables and figures:** All three SP-07 tables and three SP-07 SVGs registered in `report/report_asset_register.csv`.
- **Mandatory limitations:** Use final-ledger wording; points are repetition averages, line is their three-value median, whiskers are repetition-average minima/maxima; operation families are not ranked.
- **Prohibited claims:** Pooled statistics, significance, monotonic scaling, constant-time, hardware/field/commercial performance.
- **Unresolved inputs:** Template placement, caption style, numbering, and language.
- **Drafting status:** `ready_with_limits`.

## 11. Discussion

- **Purpose:** Plan bounded interpretation of correctness, variability, anomalies, evidence strength, and implications.
- **Questions:** What do accepted observations support, what variation is visible, and which conclusions remain unavailable?
- **Canonical sources:** `data/results/sp07_anomaly_register.csv`; `data/results/sp07_independent_review_summary.json`; `audit/validation/subproject_07_final_validation_ledger.csv`; `docs/sp07_results_discussion_source_notes.md`.
- **Evidence classes:** supported quantitative claim with explicit limitations; engineering inference.
- **Claim IDs:** RPT-022–RPT-024; SP-07 CLM-001–CLM-039.
- **Proposed tables and figures:** Anomaly/validity-threat summary; references to registered results assets, not new plots.
- **Mandatory limitations:** Source notes are non-final material; observation and interpretation stay distinct; one host, three repetitions, no raw pooling, unequal mixed counts, distinct boundaries, and constructed workloads remain visible.
- **Prohibited claims:** Diagnosed defect from ordinary variation, causal scaling, significance, population error rates, product performance.
- **Unresolved inputs:** Human technical interpretation review and approved report voice/language.
- **Drafting status:** `ready_with_limits`.

## 12. Limitations and Validity Threats

- **Purpose:** Plan explicit treatment of product evidence gaps, construct/internal/external validity, timing scope, and deployment exclusions.
- **Questions:** Which missing evidence or method boundary constrains each conclusion?
- **Canonical sources:** `evidence/assumptions_and_unknowns.md`; `evidence/unresolved_sources.md`; `data/results/sp07_anomaly_register.csv`; `data/results/sp07_independent_review_summary.json`.
- **Evidence classes:** unknown or unresolved; engineering inference; supported quantitative claim with explicit limitations.
- **Claim IDs:** RPT-002; RPT-022; RPT-024–RPT-027; SP-07 CLM-030–CLM-031, CLM-036–CLM-039.
- **Proposed tables and figures:** Validity-threat table derived from the accepted anomaly register.
- **Mandatory limitations:** Preserve every accepted anomaly and product/deployment boundary; absence of evidence is not a negative product finding.
- **Prohibited claims:** Zero field error rate, reliability, certification, safety, real-time behavior, commercial equivalence.
- **Unresolved inputs:** Product capture, university requirements, physical-integration and fail-safe/fail-secure authorities.
- **Drafting status:** `ready_for_draft`.

## 13. Conclusions and Future Work

- **Purpose:** Plan only conclusions authorized by the final independent review and clearly separated future work.
- **Questions:** What was verified, what artifacts are reusable, and what remains optional, unresolved, or human-controlled?
- **Canonical sources:** `data/results/sp07_independent_review_summary.json`; `audit/validation/subproject_07_final_validation_ledger.csv`; `README.md`; `evidence/unresolved_sources.md`.
- **Evidence classes:** supported quantitative claim with explicit limitations; unknown or unresolved; proposed reference design.
- **Claim IDs:** RPT-023–RPT-027; SP-07 CLM-001–CLM-039.
- **Proposed tables and figures:** Optional future-work/status table; no new performance figure.
- **Mandatory limitations:** Conclusions are limited to accepted simulator verification, deterministic outcome reconciliation, bounded host-software observations, and source-faithful assets.
- **Prohibited claims:** Constant-time/asymptotic behavior, persistent-database performance, physical RFID/electrical/elevator results, field reliability, production readiness, safety/certification, commercial equivalence, population error rate, statistical significance.
- **Unresolved inputs:** Human approval of final conclusions and prioritization of optional work.
- **Drafting status:** `ready_with_limits`.

## 14. References

- **Purpose:** Plan a verified bibliography whose metadata and authority remain source-scoped.
- **Questions:** Which sources are citation-ready, conditional, incomplete, internal-only, or missing?
- **Canonical sources:** `report/bibliography_readiness.csv`; `evidence/source_index.md`; `evidence/literature_notes.md`; `report/references.bib`.
- **Evidence classes:** external technical evidence; project governance; unknown or unresolved.
- **Claim IDs:** RPT-003–RPT-005; RPT-027.
- **Proposed tables and figures:** None; bibliography entries follow the future approved citation style.
- **Mandatory limitations:** Incomplete educational-PDF and example-project metadata is not invented; internal files are not automatically external bibliography entries.
- **Prohibited claims:** Citation readiness for missing sources or fabricated author/year/title/publisher/standard data.
- **Unresolved inputs:** Citation style, reference-count requirement, incomplete source metadata, university requirements source.
- **Drafting status:** `blocked_by_human_input`.

## 15. Appendices

- **Purpose:** Plan supporting reproducibility, traceability, verification, configurations, CLI demonstration, and selected code references.
- **Questions:** Which durable artifacts aid audit and reproduction without displacing essential main-text explanation?
- **Canonical sources:** `docs/reproducibility.md`; `docs/requirements_to_test_traceability.csv`; `audit/validation/subproject_06_11_verification_records.csv`; `experiments/scalability_config.json`; `experiments/isolated_operations_config.json`; `src/elevator_access_sim/`.
- **Evidence classes:** accepted simulator evidence; project governance; proposed reference design.
- **Claim IDs:** RPT-006–RPT-014; RPT-022.
- **Proposed tables and figures:** Traceability and final-ledger excerpts or references; experiment configurations; CLI procedure; selected module references.
- **Mandatory limitations:** Appendices support but never replace system, method, result, or limitation explanations in the main report.
- **Prohibited claims:** Entire source dumps as analysis, unapproved archive/release content, credentials or generated raw workloads.
- **Unresolved inputs:** Template appendix rules, length limits, and code-listing policy.
- **Drafting status:** `appendix_only`.
