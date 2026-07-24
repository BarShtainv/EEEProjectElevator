# Final Engineering Project Plan

## Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller

**Document type:** Durable project operating plan  
**Project phase:** Design and planning  
**Primary environment:** VS Code, Git, Python, pytest, Codex  
**Physical prototype:** Not required in the current scope  
**Project organization:** Eight bounded subprojects; each subproject will later receive its own execution prompt  
**Important:** This file defines the stages and their acceptance criteria. It does **not** contain the eight future prompts.

---

## 1. Project purpose

The project studies a commercial elevator access-control card advertised through an AliExpress listing. The available product evidence is limited to the listing, its photographs, visible labels, seller claims, and any later information that can be preserved from the page. Complete schematics, firmware, component documentation, and a manufacturer technical manual are not currently available.

The final B.Sc. project will therefore not claim to reproduce or reverse-engineer the exact commercial design. Instead, it will develop a scientifically structured **literature review, engineering interpretation, conceptual architecture, and functional software model** for a controller of the advertised class.

The project will answer the following engineering question:

> How can a 16-floor, dual-frequency RFID elevator access-control controller be described, architected, modeled, and evaluated using established embedded-system principles when complete manufacturer documentation is unavailable?

The final work will combine:

1. product evidence collected from the AliExpress listing;
2. a literature review on embedded controllers, ARM/STM32 concepts, RFID, Wiegand communication, access control, reliability, and elevator integration;
3. a proposed reference architecture for a controller with similar advertised functionality;
4. a reproducible Python simulation of credential decoding, authorization, floor-output control, timing, logging, and fault handling;
5. automated verification and quantitative simulation results;
6. a complete engineering project book, presentation, and demonstration package.

---

## 2. Scientific positioning and evidence rules

The project must remain technically plausible without presenting invented details as verified facts. Every important claim about the commercial card will be classified into one of the following evidence classes.

| Evidence class | Meaning | Typical wording |
|---|---|---|
| **Verified product evidence** | Directly visible in the listing, photographs, labels, or a preserved seller statement | “The listing advertises support for 16 floors.” |
| **External technical evidence** | Supported by a manufacturer manual, standard, academic paper, textbook, or reputable technical source | “Memory-mapped GPIO is a common method for controlling digital outputs.” |
| **Engineering inference** | A reasonable interpretation derived from verified evidence and accepted engineering practice | “The output channels are likely intended to interface with floor-selection circuits.” |
| **Proposed reference design** | A design decision made for this project’s conceptual model or simulator | “The reference model uses a 16-bit floor-permission mask.” |
| **Unknown or unresolved** | Information that cannot currently be established | “The exact microcontroller used on the commercial card is unknown.” |

### 2.1 Mandatory wording discipline

The report must not state that the card contains an STM32, an ARM processor, a specific relay type, a specific memory size, or a specific communication interface unless direct evidence is later found.

ARM and STM32 literature will be used as **representative embedded-system references**, not as proof of the commercial card’s exact implementation.

The project may say:

> An STM32F10xxx-class architecture is used as a reference implementation model because its documentation provides a complete and well-structured example of memory organization, GPIO, timers, interrupts, UART, watchdogs, reset, clocks, and memory-mapped peripheral control.

The project must not say:

> The AliExpress card uses an STM32F103.

unless a readable component marking or authoritative document proves it.

### 2.2 Evidence hierarchy

The project will follow this order of authority:

1. official university requirements and supervisor decisions;
2. preserved product-page evidence and readable component markings;
3. official manufacturer manuals and standards;
4. academic papers and reputable technical literature;
5. generated test records and simulation outputs;
6. project design decisions;
7. engineering inference, clearly labeled;
8. unsupported speculation, which must not appear as fact.

---

## 3. Project scope

### 3.1 In scope

- preservation and analysis of the AliExpress listing and product photographs;
- description of the advertised application and likely system role;
- literature review of dual-frequency RFID access control;
- literature review of embedded controller architecture using ARM and STM32 references;
- conceptual study of reader inputs, authorization logic, memory, timing, watchdogs, outputs, and service interfaces;
- proposed 16-floor controller architecture;
- proposed state machine and register model;
- Python implementation of a functional controller simulator;
- automated unit, integration, timing, scalability, and fault-injection tests;
- generation of tables and graphs from reproducible simulation data;
- preparation of the final project book and presentation.

### 3.2 Explicitly out of scope

- claiming exact reverse engineering of the commercial PCB;
- controlling an actual elevator;
- designing elevator motion, braking, door, or safety logic;
- bypassing or defeating a real access-control system;
- physical experiments involving elevator wiring;
- certification for safety-critical use;
- destructive PCB analysis;
- extraction of firmware from the commercial product;
- fabrication of a replacement commercial board;
- claims of compliance with elevator safety standards without an appropriate expert review.

### 3.3 Safety boundary

The studied card will be treated as an **access-authorization layer**, not as an elevator safety or motion controller. The conceptual outputs may represent permission signals or floor-enable channels, but the project will not model direct control of motors, brakes, doors, or passenger-safety functions.

---

## 4. Expected final deliverables

The complete project package should contain the following durable artifacts.

### 4.1 Engineering report

A structured B.Sc. project book containing:

- abstract;
- introduction and motivation;
- product under study;
- methodology and evidence limitations;
- literature review;
- requirements;
- conceptual architecture;
- software model;
- verification methodology;
- simulation experiments;
- results and discussion;
- conclusions, limitations, and future work;
- references;
- appendices.

### 4.2 Engineering design package

- product evidence inventory;
- claim-evidence matrix;
- assumptions and unresolved-input register;
- system context diagram;
- conceptual hardware block diagram;
- software architecture diagram;
- state-machine diagram;
- data-flow diagram;
- proposed register map;
- interface table;
- failure-mode table;
- requirements-to-test traceability matrix.

### 4.3 Software package

- Wiegand message decoder, beginning with Wiegand-26;
- credential database;
- floor-permission representation;
- authorization engine;
- 16-channel output model;
- timeout and timer model;
- event logger;
- watchdog and safe-reset model;
- command-line simulation interface;
- test-data generator;
- result-analysis scripts.

### 4.4 Verification package

- automated tests;
- test plan;
- test results in machine-readable form;
- performance measurements;
- scalability measurements;
- fault-injection results;
- plots and summary tables;
- validation report.

### 4.5 Submission package

- final PDF;
- presentation;
- source archive or repository tag;
- reproducibility instructions;
- demonstration script;
- final checksum record;
- release handoff note.

---

## 5. Planned repository structure

The repository should use a small number of canonical files and avoid duplicate documentation.

```text
elevator-rfid-final-project/
├── README.md
├── PROJECT_PLAN.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── evidence/
│   ├── product_evidence.md
│   ├── assumptions_and_unknowns.md
│   ├── claim_evidence_matrix.csv
│   ├── source_index.md
│   ├── images/
│   └── snapshots/
│
├── docs/
│   ├── requirements.md
│   ├── methodology.md
│   ├── architecture.md
│   ├── register_model.md
│   ├── test_plan.md
│   ├── decision_log.md
│   └── figures/
│
├── src/
│   └── elevator_access/
│       ├── __init__.py
│       ├── wiegand.py
│       ├── credentials.py
│       ├── authorization.py
│       ├── outputs.py
│       ├── controller.py
│       ├── watchdog.py
│       ├── event_log.py
│       └── cli.py
│
├── tests/
│   ├── test_wiegand.py
│   ├── test_credentials.py
│   ├── test_authorization.py
│   ├── test_outputs.py
│   ├── test_watchdog.py
│   └── test_end_to_end.py
│
├── data/
│   ├── example_users.json
│   ├── generated_cases/
│   └── results/
│
├── analysis/
│   ├── run_experiments.py
│   ├── analyze_results.py
│   └── generate_figures.py
│
├── report/
│   ├── main.tex
│   ├── chapters/
│   ├── figures/
│   ├── tables/
│   └── references.bib
│
└── audit/
    ├── baseline.md
    ├── stage_reports/
    ├── validation/
    ├── file_change_ledger.md
    └── release_handoff.md
```

The exact structure may be adjusted after the project directory is inspected. Existing canonical files must be updated rather than duplicated.

---

## 6. Roles and responsibilities

### 6.1 Human project owners

The students are responsible for:

- confirming the academic topic and scope;
- obtaining supervisor approval;
- preserving authoritative university requirements;
- deciding final engineering assumptions;
- reviewing every major claim;
- understanding and defending the software and analysis;
- approving the final report and presentation;
- making the final submission.

### 6.2 Coordinator or reviewing assistant

The coordinator is responsible for:

- maintaining continuity between stages;
- checking whether each stage stayed within scope;
- reviewing evidence classification;
- verifying high-impact claims independently where possible;
- deciding whether a stage is ready, needs narrow repair, or is blocked;
- preparing the next bounded execution prompt after the previous stage is accepted.

### 6.3 Codex execution agent

Codex will be used for bounded tasks such as:

- repository inspection;
- file creation and controlled editing;
- implementation of isolated software modules;
- test creation;
- static checks;
- report scaffolding;
- figure and table generation;
- evidence-ledger maintenance.

Codex must not invent missing facts, expand scope without approval, or approve its own high-impact assumptions.

---

## 7. Rules that apply to all eight subprojects

Each subproject will later receive a separate prompt. Every prompt will specify:

- task identity;
- current repository version;
- task baseline;
- objective;
- required inspection;
- authoritative sources;
- allowed files;
- forbidden files;
- protected content;
- required changes;
- validation commands;
- required records;
- readiness wording;
- whether a commit is authorized.

### 7.1 Stage lifecycle

Every subproject follows the same lifecycle:

1. inspect the current repository state;
2. record the baseline;
3. identify protected material;
4. inspect only the sources relevant to the stage;
5. make the smallest sufficient change;
6. run validation;
7. write a stage report;
8. perform independent review;
9. declare a readiness state;
10. continue, repair narrowly, or block.

### 7.2 Allowed readiness states

Each stage must end with one of the following exact states:

```text
READY FOR NEXT STAGE
READY FOR NEXT STAGE WITH NON-BLOCKING GATES
BLOCKED BEFORE NEXT STAGE — REASON
READY FOR HUMAN REVIEW
READY FOR RELEASE PREPARATION
```

### 7.3 Stage records

Each stage should produce or update:

- a stage report;
- file-change ledger;
- decision log;
- unresolved-input list;
- validation results;
- commit or version identifier when authorized.

### 7.4 Narrow repairs

A failed detail should trigger a narrow repair stage, not a complete rewrite. Examples include:

- correcting one unsupported claim;
- replacing one low-quality source;
- fixing one failing test group;
- correcting one diagram;
- repairing one report section;
- restoring one omitted limitation.

---

# 8. Eight-subproject plan

---

## Subproject 1 — Repository baseline and product-evidence preservation

### Objective

Establish the project root, protect the initial state, preserve the available AliExpress evidence, and create a clear boundary between known product facts, engineering inference, proposed design decisions, and unknown information.

### Starting state

- VS Code and Codex are available.
- The AliExpress link is known.
- Three product images are available in the current working context.
- ARM, STM32, ARMADA, workflow, and example Ariel project sources are available.
- The actual project repository may not yet be initialized or may not yet contain a canonical structure.

### Required work

1. Inspect the target project directory before creating files.
2. Record the repository root, branch, status, and existing documentation.
3. Preserve the product URL and access date.
4. Copy or reference the available product images in the project evidence area.
5. Record all readable labels, connectors, visible components, and seller claims without interpretation.
6. Create a table of verified facts, inferred functions, proposed-model elements, and unresolved questions.
7. Record the absence of an authoritative schematic, datasheet, processor identification, and firmware description.
8. Create the initial source inventory.
9. Establish naming conventions and the project’s canonical files.

### Expected outputs

- `audit/baseline.md`
- `evidence/product_evidence.md`
- `evidence/assumptions_and_unknowns.md`
- initial `evidence/claim_evidence_matrix.csv`
- initial `evidence/source_index.md`
- preserved product images or references
- initialized `audit/file_change_ledger.md`

### Protected material

- original uploaded source files;
- original product images;
- original AliExpress URL;
- any pre-existing repository content not explicitly authorized for editing.

### Validation

- every product claim is traceable to a screenshot, visible marking, or preserved listing text;
- no processor family is asserted without evidence;
- no exact electrical rating is invented;
- all unknowns are explicit;
- repository status is recorded before and after the stage;
- evidence files open correctly in VS Code.

### Readiness gate

The stage is ready only when another reviewer can determine exactly what is known about the card and what remains unknown without relying on chat history.

### Explicit exclusions

- no broad literature review;
- no simulator implementation;
- no detailed hardware architecture;
- no attempt to infer exact PCB traces from low-resolution images.

---

## Subproject 2 — Literature review and claim-evidence architecture

### Objective

Build a structured, defensible literature base that supports the final report’s explanations of the card’s function and the project’s reference architecture.

### Literature domains

1. RFID fundamentals;
2. 125 kHz identification systems;
3. 13.56 MHz RFID and smart-card systems;
4. Wiegand signaling and frame formats;
5. embedded controller architecture;
6. ARM RISC and programmer’s-model concepts;
7. STM32 memory, GPIO, timers, interrupts, UART, watchdog, reset, and clocks;
8. nonvolatile credential storage;
9. access-control authorization models;
10. elevator floor-access integration at a conceptual level;
11. reliability, fail-safe startup, and watchdog recovery;
12. software testing and simulation methodology.

### Use of uploaded literature

- **General-Purpose Evidence-Gated Project Workflow Handbook:** project governance, evidence hierarchy, stage gates, validation, and release discipline.
- **STM32F10xxx Reference Manual:** representative microcontroller organization and peripheral concepts.
- **ARM Developer Suite Developer Guide:** initialization, ROM-based firmware, memory maps, exception handling, memory-mapped I/O, and debugging concepts.
- **ARM instruction-set materials:** accessible explanation of registers, flags, branches, load/store behavior, and processor modes.
- **ARMv7-A/R Architecture Reference Manual:** formal architectural terminology and distinction between application-level, system-level, and debug behavior. It must not be used to imply that the commercial card implements ARMv7-A/R.
- **ARMADA 38x Functional Specification:** example of professional functional-specification organization, address maps, boot flow, interfaces, and register documentation.
- **Uploaded Ariel B.Sc. project book:** example report structure, requirements, implementation chapters, experiments, result presentation, conclusions, and appendices.

### Required work

1. Build a source index containing source type, authority, scope, relevance, and planned report use.
2. Expand the claim-evidence matrix.
3. Extract only relevant sections from large manuals rather than summarizing them completely.
4. Identify missing literature requiring later web or library research.
5. Draft literature notes organized by topic, not by source filename.
6. Record contradictory definitions or protocol variants.
7. Define citation and bibliography conventions.
8. Create a preliminary literature-review outline.

### Expected outputs

- expanded `evidence/source_index.md`
- expanded `evidence/claim_evidence_matrix.csv`
- literature notes in a canonical location
- preliminary `report/references.bib`
- `docs/methodology.md` section describing evidence classification
- literature-review chapter outline
- unresolved-source register

### Protected material

- product evidence classification from Subproject 1;
- original source documents;
- any supervisor-approved project title or scope statement.

### Validation

- each planned technical claim has at least one appropriate source or is marked as inference/proposed design;
- official manuals are not misrepresented as product-specific evidence;
- the ARMv7-A/R manual is not treated as an STM32 Cortex-M manual;
- source notes preserve the source’s terminology and scope;
- bibliography entries are complete enough to identify each source;
- no copied text exceeds reasonable quotation needs.

### Readiness gate

The stage is ready when the project has enough literature to support the background, methodology, architecture rationale, and verification approach without padding the report with irrelevant ARM material.

### Explicit exclusions

- no final report prose beyond a controlled outline and source notes;
- no implementation claims about the commercial card;
- no software coding other than small source-management utilities if required.

---

## Subproject 3 — Requirements, scope freeze, and research methodology

### Objective

Convert the product evidence and literature base into a bounded engineering specification for the conceptual controller and its simulator.

### Required decisions

- exact project title;
- target use case;
- supported floor count;
- supported credential-message formats;
- authorization data model;
- output activation behavior;
- event logging behavior;
- timeout behavior;
- reset and watchdog behavior;
- failure responses;
- simulation metrics;
- report limitations;
- minimum acceptable deliverables.

### Functional requirements

At minimum, the reference system should:

1. accept a simulated RFID-reader credential message;
2. validate the message format;
3. extract a credential identifier;
4. look up the credential in a database;
5. determine the permitted floors;
6. represent up to 16 floor permissions;
7. accept a simulated floor request;
8. grant only authorized requests;
9. activate the corresponding output for a configured duration;
10. keep all outputs inactive after denial, reset, or unrecoverable error;
11. log access and error events;
12. recover from a simulated software lock through a watchdog model.

### Nonfunctional requirements

- deterministic results for identical inputs;
- modular implementation;
- complete automated tests for defined behavior;
- reproducible experiments;
- safe inactive startup state;
- explicit input validation;
- no dependency on physical hardware;
- clear separation between product facts and reference-design choices;
- response-time and scalability measurements labeled as software-model results.

### Required work

1. Write the project requirements in testable language.
2. Assign unique requirement identifiers.
3. Define acceptance criteria for every requirement.
4. Create a system boundary and context diagram.
5. Define the research methodology: literature analysis, conceptual modeling, software simulation, and verification.
6. Freeze the minimum viable project.
7. Identify optional extensions that must not delay completion.
8. Create the initial requirements-to-test traceability matrix.
9. Obtain human approval of scope before architecture or coding expands.

### Expected outputs

- `docs/requirements.md`
- completed methodology section in `docs/methodology.md`
- context diagram
- initial requirements-to-test traceability matrix
- updated `docs/decision_log.md`
- updated unresolved-input register
- approved minimum viable scope

### Protected material

- evidence classifications;
- source records;
- supervisor-approved terminology;
- declared safety boundary.

### Validation

- each requirement is measurable or reviewable;
- no requirement depends on unavailable physical hardware;
- optional features are clearly separated from required features;
- no requirement claims exact behavior of the commercial card;
- the minimum scope can realistically be completed;
- every functional requirement has a planned verification method.

### Readiness gate

The stage is ready when the students and reviewer agree on what will be built, tested, and written—and what will not be attempted.

### Explicit exclusions

- no full simulator implementation;
- no speculative circuit schematic presented as the real board;
- no user interface unless it is required for the final demonstration.

---

## Subproject 4 — Conceptual hardware and firmware architecture

### Objective

Develop a complete reference architecture for a controller of the advertised class, grounded in literature and clearly labeled as a proposed model.

### Architecture elements

- power input, regulation, and protection block at a conceptual level;
- external RFID-reader interface;
- input-conditioning or isolation concept;
- embedded controller block;
- program memory and data memory concept;
- credential database storage;
- timer and watchdog functions;
- event logging;
- service or configuration interface;
- 16 floor-output channels;
- output isolation or driver concept;
- connection boundary to the elevator access interface;
- safe reset and startup behavior.

### Proposed firmware elements

- reset and initialization;
- reader-frame acquisition;
- frame validation;
- credential lookup;
- authorization decision;
- floor-request handling;
- timed output activation;
- event logging;
- watchdog service;
- error handling;
- return to idle state.

### Required engineering artifacts

1. system context diagram;
2. top-level block diagram;
3. input/output interface table;
4. controller state machine;
5. data-flow diagram;
6. proposed memory map;
7. proposed register map;
8. floor-mask bit definition;
9. event format;
10. reset sequence;
11. watchdog sequence;
12. failure-mode and safe-state table;
13. rationale for major design decisions.

### Expected outputs

- `docs/architecture.md`
- `docs/register_model.md`
- figures under `docs/figures/`
- interface and failure-mode tables
- updated decision log
- architecture-to-requirements mapping

### Protected material

- frozen requirements;
- evidence classification;
- safety boundary;
- source citations already approved.

### Validation

- every architecture block maps to at least one requirement;
- every proposed element is labeled as a reference-design choice;
- the architecture does not imply control of elevator safety or motion;
- reset produces inactive outputs;
- denied access cannot activate an output in the model;
- the register and state definitions are internally consistent;
- figures remain readable in the final report format;
- terminology is consistent across diagrams and text.

### Readiness gate

The stage is ready when a developer can implement the simulator from the architecture documents without inventing major behavior.

### Explicit exclusions

- no claim that the proposed register map exists on the commercial card;
- no detailed mains-voltage or elevator wiring design;
- no safety certification calculations;
- no unnecessary processor pipeline or instruction-set implementation.

---

## Subproject 5 — Software model design and verification design

### Objective

Translate the approved architecture into a precise Python software design and a test strategy before implementation begins.

### Planned modules

- `wiegand.py`: frame validation and credential extraction;
- `credentials.py`: user and credential records;
- `authorization.py`: floor-permission decisions;
- `outputs.py`: 16 output states and timeout behavior;
- `controller.py`: state-machine coordination;
- `watchdog.py`: lockup detection and safe reset;
- `event_log.py`: structured event records;
- `cli.py`: controlled demonstration interface.

### Required design decisions

- type definitions;
- exception hierarchy;
- floor numbering convention;
- bit-mask convention;
- time representation;
- configuration-file format;
- credential database schema;
- event-log schema;
- controller-state enumeration;
- invalid-input behavior;
- dependency policy;
- test framework and coverage expectations.

### Test categories

- valid Wiegand frame tests;
- parity-error tests;
- malformed-frame tests;
- known and unknown credentials;
- enabled and disabled users;
- authorized and unauthorized floor requests;
- administrator or all-floor access if included;
- output timeout tests;
- reset-state tests;
- watchdog-expiry tests;
- duplicate-event tests;
- database-scale tests;
- end-to-end scenario tests;
- fault-injection tests.

### Required work

1. Write module contracts and data structures.
2. Define public APIs.
3. Define test fixtures and reference cases.
4. Define deterministic time control for tests.
5. Create the detailed test plan.
6. Link every test group to requirements.
7. Define performance and scalability experiments.
8. Define what generated data will be stored and what will be recreated.
9. Review design complexity before writing production code.

### Expected outputs

- software-design section in `docs/architecture.md`
- completed `docs/test_plan.md`
- API and data-schema definitions
- test-case inventory
- updated requirements-to-test traceability matrix
- implementation sequence

### Protected material

- frozen requirements;
- conceptual architecture;
- evidence documents;
- report source material unrelated to implementation.

### Validation

- every module has a single clear responsibility;
- all external input is validated;
- time-dependent tests can run without real waiting;
- no test requires physical hardware;
- expected behavior is specified before coding;
- test cases cover denial and fault paths, not only successful access;
- the design remains small enough for timely completion.

### Readiness gate

The stage is ready when the implementation can proceed module by module using bounded Codex tasks and predefined tests.

### Explicit exclusions

- no graphical interface as a required feature;
- no premature optimization;
- no database server unless explicitly approved;
- no undocumented behavior added during coding.

---

## Subproject 6 — Simulator implementation and integration

### Objective

Implement the functional software model in small, testable increments and integrate it into a reproducible command-line demonstration.

### Implementation sequence

1. project packaging and configuration;
2. credential and user data models;
3. Wiegand-26 encoder/decoder test utilities;
4. authorization engine;
5. floor-output model;
6. controller state machine;
7. event logger;
8. watchdog and safe reset;
9. configuration loading;
10. command-line demonstration;
11. integration tests;
12. static and style checks.

### Engineering rules

- one bounded change per Codex task;
- tests written with or before each module;
- typed interfaces where practical;
- explicit exceptions for invalid data;
- no silent failure;
- safe default output state;
- no modification of evidence files by implementation tasks;
- no unapproved dependency expansion;
- no claims that simulator timing equals commercial-card timing.

### Expected outputs

- complete `src/elevator_access/` package
- complete core `tests/` suite
- example configuration and user database
- runnable CLI demonstration
- implementation notes
- stage validation report
- updated file-change ledger

### Validation

At minimum:

- all automated tests pass;
- valid frames decode correctly;
- parity errors are rejected;
- unknown credentials are denied;
- unauthorized floors are denied;
- authorized floors activate exactly one intended output unless multi-output behavior is explicitly designed;
- outputs deactivate after timeout;
- reset and watchdog recovery clear all outputs;
- events are logged with deterministic fields;
- package installation and test commands work from a clean environment;
- static checks report no unresolved critical issue.

### Readiness gate

The stage is ready when the simulator demonstrates all required functional behaviors and the results are reproduced through automated tests.

### Explicit exclusions

- no rewriting of the architecture to match accidental code behavior;
- no broad refactoring after tests pass unless a concrete defect is identified;
- no GUI unless all required deliverables are already secure.

---

## Subproject 7 — Experiments, quantitative analysis, and independent validation

### Objective

Use the completed simulator as an engineering experiment platform and generate reproducible quantitative results for the final report.

### Required experiments

#### Experiment 1 — Protocol validation

Test valid and corrupted Wiegand messages, including parity errors, incorrect lengths, illegal characters, and repeated frames.

#### Experiment 2 — Authorization correctness

Test combinations of known, unknown, active, disabled, authorized, and unauthorized credentials and floors.

#### Experiment 3 — Output timing

Verify activation, configured duration, timeout, reset, and denial behavior for all 16 modeled channels.

#### Experiment 4 — Watchdog and fault recovery

Inject controller lockups or missed watchdog refreshes and verify return to a safe inactive-output state.

#### Experiment 5 — Database scalability

Measure credential-lookup and authorization time for increasing database sizes.

#### Experiment 6 — End-to-end scenarios

Run realistic sequences of credential presentation, floor request, authorization, output activation, logging, timeout, and return to idle.

#### Experiment 7 — Robustness and malformed configuration

Test invalid floor numbers, duplicate credentials, corrupted configuration data, missing fields, and invalid timeouts.

### Required metrics

- number of test cases;
- test pass rate;
- correct grant count;
- correct denial count;
- incorrect grant count;
- incorrect denial count;
- processing-time statistics;
- database-size versus lookup-time results;
- watchdog recovery result;
- output-state invariant violations;
- code or branch coverage where practical.

### Required work

1. Create reproducible experiment scripts.
2. Fix random seeds where random data is used.
3. Save raw results in CSV or JSON.
4. Generate plots from raw data through scripts.
5. Compare results to frozen requirements.
6. Investigate warnings and anomalies rather than hiding them.
7. Perform an independent review of high-impact results.
8. Record limitations of software timing measurements.
9. Produce a validation ledger.

### Expected outputs

- `analysis/run_experiments.py`
- `analysis/analyze_results.py`
- `analysis/generate_figures.py`
- raw result files under `data/results/`
- generated plots and tables
- validation report under `audit/validation/`
- completed requirements-to-test traceability matrix
- results and discussion draft material

### Protected material

- accepted implementation baseline;
- raw experiment outputs;
- frozen requirements;
- accepted architecture diagrams.

### Validation

- experiments can be rerun from documented commands;
- graphs are generated from preserved raw data;
- axes, units, sample counts, and conditions are stated;
- timing results are described as host-software measurements, not product hardware measurements;
- no result is manually edited to improve appearance;
- discrepancies are explained or marked unresolved;
- all required requirements have evidence of verification.

### Readiness gate

The stage is ready when the project has sufficient reproducible evidence to support its conclusions and when the limitations of those conclusions are explicit.

### Explicit exclusions

- no fabricated measurement data;
- no physical-performance claims;
- no claim of safety certification;
- no selective removal of failing cases without documentation.

---

## Subproject 8 — Final report, presentation, release, and defense preparation

### Objective

Assemble the accepted evidence, literature, architecture, implementation, and experimental results into a self-contained B.Sc. engineering submission package.

### Proposed report structure

1. Abstract
2. Introduction
3. Product under study and available evidence
4. Research methodology and limitations
5. Literature review
6. Requirements and system boundary
7. Proposed reference architecture
8. Software-model design and implementation
9. Verification and experimental method
10. Results
11. Discussion
12. Limitations and validity threats
13. Conclusions and future work
14. References
15. Appendices

### Required work

1. Create or update the report source in the university-approved format.
2. Convert source notes into original, coherent report prose.
3. Insert citations and bibliography entries.
4. Include evidence-status wording where product details are discussed.
5. Integrate readable figures and tables.
6. Include requirement and test traceability.
7. Include implementation and reproduction instructions.
8. Prepare a presentation with a clear engineering narrative.
9. Prepare a short live demonstration.
10. Prepare likely defense questions and evidence-based answers.
11. Perform owner review.
12. Perform supervisor or expert review.
13. Apply one controlled revision list.
14. Build the final PDF.
15. Inspect the actual rendered PDF page by page.
16. Produce release artifacts, version tag, checksums, and handoff notes.

### Expected outputs

- final report source and PDF
- final bibliography
- presentation
- demonstration script
- source-code release archive or repository tag
- reproducibility guide
- final audit report
- final checksum record
- release handoff

### Final artifact validation

- successful clean build;
- no unresolved citations or references;
- no clipped figures or tables;
- readable Hebrew and English text if both are used;
- consistent terminology;
- every commercial-card claim is evidence-labeled;
- figures match the final accepted architecture;
- result tables match preserved raw data;
- appendices include necessary code or links without replacing essential explanations in the main report;
- owner and supervisor comments are resolved or explicitly recorded;
- no draft is labeled final before approval.

### Readiness gate

The project reaches:

```text
READY FOR RELEASE PREPARATION
```

only after technical validation and human review. It becomes ready for submission only after the required university approval and final sign-off.

### Explicit exclusions

- no last-minute broad redesign;
- no unsupported claims added for presentation impact;
- no replacement of results after report approval without reopening the validation record.

---

## 9. Suggested stage-to-commit mapping

Use one commit or version per accepted stage when repository policy permits.

| Stage | Suggested commit label |
|---|---|
| 1 | `stage-01-product-evidence-baseline` |
| 2 | `stage-02-literature-and-evidence-map` |
| 3 | `stage-03-requirements-scope-freeze` |
| 4 | `stage-04-reference-architecture` |
| 5 | `stage-05-software-and-test-design` |
| 6 | `stage-06-simulator-implementation` |
| 7 | `stage-07-experiments-and-validation` |
| 8 | `stage-08-final-report-and-release` |

Commits should not be created or pushed unless the corresponding execution prompt authorizes them.

---

## 10. Minimum viable project and optional extensions

### 10.1 Minimum viable project

The project is technically sufficient only when it includes:

- preserved product evidence;
- an evidence-labeled literature review;
- a proposed reference architecture;
- a functioning Wiegand-26 decoder;
- a credential database;
- 16-floor permission handling;
- grant and denial behavior;
- timed output activation;
- event logging;
- watchdog-safe reset behavior;
- automated verification;
- at least five reproducible experiment groups;
- final report and presentation.

### 10.2 Optional extensions

Optional work may begin only after the minimum project is secure:

- Wiegand-34 support;
- graphical user interface;
- administrator configuration workflow;
- multiple reader simulation;
- anti-passback logic;
- time-of-day permissions;
- encrypted credential database;
- serial-service-port model;
- comparison of data structures for credential lookup;
- formal state-machine checking;
- containerized reproduction environment.

Optional work must not delay final report completion.

---

## 11. Major risks and controls

| Risk | Control |
|---|---|
| Treating seller claims as a technical datasheet | Preserve claims separately and label their authority |
| Claiming a specific MCU without evidence | Use “representative reference architecture” wording |
| Writing an ARM textbook unrelated to the card | Extract only concepts that support the controller model |
| Project appears to be only a product summary | Include architecture, simulator, tests, and experiments |
| Project becomes too large | Freeze minimum requirements in Subproject 3 |
| No physical experiments | Use reproducible simulation experiments and state their validity limits |
| Unsafe elevator-control implications | Maintain a strict access-layer boundary |
| Codex modifies unrelated files | Every task prompt defines allowed and forbidden paths |
| AI-generated code is trusted without review | Require tests, inspection, and student understanding |
| Results cannot be reproduced | Preserve raw data, scripts, versions, and commands |
| Report contains unsupported certainty | Maintain the claim-evidence matrix through release |
| Last-minute changes break accepted work | Use narrow repair stages and protected baselines |

---

## 12. Unresolved authoritative inputs

The following items require human or supervisor confirmation and must not be silently invented:

| Item | Why needed | Responsible party | Blocking effect |
|---|---|---|---|
| Official project title | Cover page and registration | Students/supervisor | Blocks formal submission documents |
| University report template | Final formatting | Students/department | Blocks final report layout |
| Required language | Hebrew, English, or mixed | Supervisor/department | Affects writing plan |
| Required page range | Scope and compression | Supervisor/department | Non-blocking during early design |
| Required number of references | Literature target | Supervisor/department | Non-blocking initially |
| Permission to use AliExpress images | Report reproduction practice | Students/supervisor | May affect final figures |
| Expected physical component | Determines whether simulation-only is acceptable | Supervisor | Potentially blocking |
| Required presentation duration | Defense preparation | Department | Non-blocking until Stage 8 |
| Team-member ownership split | Project management | Students | Needed before implementation |
| Exact submission deadline | Stage schedule | Students | Needed for calendar planning |

---

## 13. Definition of done

The final project is done only when:

- the product evidence is preserved and auditable;
- verified facts, inferences, and proposed design decisions remain distinct;
- the literature review supports the report’s central concepts;
- the report is self-contained and does not require the reader to inspect code to understand the system;
- the simulator implements the frozen requirements;
- automated tests pass;
- experimental results can be reproduced from documented commands;
- conclusions match the evidence and do not exceed it;
- limitations are explicit;
- the final PDF and presentation have been visually inspected;
- unresolved authoritative inputs are closed or formally accepted as non-blocking;
- the students and supervisor approve the release package.

---

## 14. Next action

Place this file in the project directory as the canonical project plan, preferably:

```text
PROJECT_PLAN.md
```

After the repository is inspected and this plan is accepted, construct the execution prompt for **Subproject 1 only**. The later prompts must be created sequentially after the previous subproject has been reviewed and assigned a readiness state.
