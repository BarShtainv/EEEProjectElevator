# SP-03 Stage Report

## Objective and baseline

SP-03 converted the accepted product-evidence boundary and SP-02R literature foundation into a bounded, testable requirements baseline for a deterministic software-only controller simulator.

- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `88a646026c0bf468e28102bf80c00ef4cb3ea57f` (`step2Repair`)
- Starting status: clean
- Baseline record: `audit/baselines/subproject_03_baseline.md`

The accepted SP-02R work was present. The project owner authorized proceeding with DEC-008's abstract scope; this is not supervisor approval.

## Requirements baseline

`docs/requirements.md` contains 66 uniquely identified requirements:

- 60 required;
- six optional;
- nine groups: `SCP`, `FUN`, `DAT`, `TIM`, `LOG`, `RST`, `NFR`, `VER`, and `LIM`.

Every required requirement uses a testable “shall” statement and includes rationale, evidence or decision basis, acceptance criteria, planned verification, priority, implementation stage, and limitation notes.

## Frozen MVP

The model receives one complete frame with an LF/HF logical source, validates `PROJECT_WIEGAND_26`, extracts the composite credential key, performs credential and floor authorization, controls at most one of 16 abstract outputs for a configured logical duration, logs decisions and recovery, and supports deterministic reset/watchdog behavior.

Frozen choices include:

- exact working title, project-owner approved with supervisor approval pending;
- software-only access-authorization boundary;
- LF/HF as metadata rather than inferred frequency;
- project-specific Wiegand-26 field and parity layout;
- floors 1–16 and bit 0–15 mask mapping;
- composite credential key with duplicate rejection;
- one active output maximum;
- `controller_busy` rejection while active;
- default 3000 ms output duration with 100–30000 ms range;
- default 2000 ms simulated watchdog;
- minimum event schema;
- experiment sizes 10, 100, 1,000, and 10,000;
- required-versus-optional deliverables.

DEC-025 supersedes only the obsolete source-blocking language in DEC-004 and DEC-007. Their history remains visible. Commercial behavior and physical integration remain unresolved.

## Required and optional scope

Required final deliverables include the evidence/literature package, requirements, context diagram, conceptual architecture and state/register model, Python simulator, simple CLI, automated unit/integration/fault tests, reproducible experiments and machine-readable results, plots/tables, report, presentation, and reproducibility instructions.

GUI, physical prototype, real reader, database server, network/cloud/mobile integration, cryptographic emulation, physical elevator interface, certification, and exact commercial-board reproduction are optional or outside current authorization. They may not delay the MVP.

## Traceability and context diagram

`docs/requirements_to_test_traceability.csv` contains one `planned` row for all 66 requirement IDs. Each row has a verification method, planned test ID, and evidence or decision basis. Passing tests are not claimed at this stage.

`docs/figures/system_context.mmd` shows both simulated reader sources, credential and floor inputs, controller, credential database, abstract outputs, log, and test harness inside the project boundary. Commercial hardware, physical RFID, the physical elevator controller, and motion/safety systems are outside the boundary with explicit non-equivalence and no-control labels.

## Methodology

The methodology now covers evidence/decision-based requirement derivation, proposed design classification, prioritization, conceptual modeling, deterministic simulated time, unit/integration verification, fault injection, scalability experiments, reproducibility, interpretation limits, and human review.

## Remaining human approvals

Human review must confirm:

- working title;
- `PROJECT_WIEGAND_26` layout;
- floor and mask mapping;
- output-duration default and range;
- watchdog timeout and recovery;
- one-output and busy-controller policy;
- event schema;
- abstract software-only elevator boundary; and
- required and optional deliverables.

Supervisor confirmation remains non-blocking for SP-04 conceptual design but is required before final academic submission or any physical-scope expansion.

## Validation and deviations

Narrow validation passed for required files, UTF-8, requirement structure, unique IDs, traceability, both CSV files, reference IDs and paths, Mermaid content, terminology qualifications, protected hashes, forbidden paths, and Git scope. Details are in `audit/validation/subproject_03_validation.md`.

No new literature was added. No product evidence, source index, literature note, unresolved-source register, bibliography, source PDF, project plan, or workflow handbook changed. No simulator, test, experiment, architecture, register-map, or state-machine implementation was created. No deviation from the authorized SP-03 scope occurred.

## Exact readiness state

READY FOR HUMAN REVIEW
