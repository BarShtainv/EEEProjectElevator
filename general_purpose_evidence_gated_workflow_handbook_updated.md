# General-Purpose Evidence-Gated Project Workflow Handbook

## 1. Purpose

This handbook is a reusable baseline for complex projects in research, engineering, policy, analysis, design, operations, and other fields where an AI agent edits files, produces deliverables, or coordinates multi-stage work.

It is not limited to machine learning, software, or thesis writing.

The workflow is designed for projects that have some combination of:

- an existing folder or repository;
- source materials;
- generated artifacts;
- external requirements;
- multiple contributors;
- human approval gates;
- high cost of silent mistakes;
- a need to resume work across conversations or agents.

The central pattern is:

> Inspect first, establish evidence and scope, make one bounded change, validate it independently, commit or version it, and only then move forward.

---

## 2. Roles

### 2.1 Human owner

The human owner is responsible for:

- goals and priorities;
- authoritative facts not present in the project;
- value judgments;
- domain decisions;
- acceptance of risk;
- final approval;
- external communication or submission.

The human should not be expected to perform mechanical checks that an agent can reliably automate, but the agent must not replace human judgment where evidence is incomplete or authority is required.

### 2.2 Coordinator or reviewing assistant

The coordinator:

- understands the overall workflow;
- inspects completed work;
- compares intended and actual scope;
- verifies high-impact claims;
- decides readiness;
- prepares the next bounded task;
- separates human responsibilities from agent responsibilities;
- preserves continuity across stages.

### 2.3 Execution agent

The execution agent:

- inspects files and folders;
- edits only allowed paths;
- runs authorized validation;
- creates durable records;
- reports uncertainty;
- preserves protected material;
- does not invent missing facts;
- does not broaden scope without approval.

---

## 3. Start by inspecting the project

Before changing anything, inspect the workspace.

### 3.1 Determine the root

Identify:

- the project root;
- nested projects or repositories;
- active branch or version;
- current working state;
- local instruction files;
- primary deliverables;
- external source files.

### 3.2 Inspect the folder hierarchy

Use a shallow-to-deep approach:

1. list the root;
2. identify major functional folders;
3. read local indexes and instructions;
4. inspect one level deeper only where relevant;
5. avoid recursively reading large binary, generated, cache, dependency, or data folders without need.

For each important folder, determine:

- purpose;
- authoritative files;
- generated files;
- active versus legacy content;
- ownership;
- whether edits are allowed;
- whether the folder has its own instructions.

### 3.3 Read local instructions before acting

Look for:

```text
AGENTS.md
README.md
CONTRIBUTING.md
WORKFLOW.md
PLAN.md
SCRIPTS.md
STYLE_GUIDE.md
```

Instructions closer to a file normally take precedence over broad project guidance.

### 3.4 Record the baseline

Record enough information to distinguish pre-existing state from agent changes.

Typical checks include:

- file status;
- branch or version;
- recent history;
- nested project state;
- existing generated outputs;
- known dirty files;
- hashes for protected material.

Never silently clean, reset, normalize, or overwrite a pre-existing workspace.

### 3.5 Distinguish current version, task baseline, and reference baseline

The newest version is not always the version that defines the task. A project may advance because of unrelated work while an earlier deliverable is being reviewed or repaired.

Record:

- **current version** — the state from which the execution agent must work;
- **task baseline** — the version containing the deliverable under review;
- **reference baseline** — an earlier version useful for comparison or selective restoration;
- **intervening changes** — later changes classified as relevant, unrelated, or conflicting.

When intervening changes are unrelated:

1. inspect and classify them;
2. continue from the current version;
3. protect the unrelated files or subtree;
4. compare the target deliverable with the correct task baseline;
5. do not reset or rewrite unrelated history simply to recreate an older workspace.

Only a material conflict should block the stage. Repository or folder advancement alone is not a defect.

---

## 4. Decide whether a Markdown file is needed

Markdown files are useful coordination artifacts, but unnecessary documentation creates confusion.

### 4.1 Create or update a Markdown file when it has a durable role

Examples:

- project overview;
- folder map;
- workflow handbook;
- operating plan;
- runnable-command index;
- decision log;
- evidence map;
- unresolved-question register;
- validation report;
- release handoff;
- reusable agent context.

### 4.2 Do not create a Markdown file for transient narration

Avoid new files that merely contain:

- a temporary thought process;
- information already present elsewhere;
- a one-time command transcript with no future value;
- generic advice unrelated to the project;
- duplicated status summaries.

### 4.3 Before creating a new file

1. inspect the target folder;
2. search for an existing file with the same purpose;
3. identify the canonical documentation location;
4. update the existing file when appropriate;
5. create a new file only when the audience, lifecycle, or authority differs.

### 4.4 Place documentation near its subject

- Project-wide rules belong near the root.
- Folder-specific guidance belongs in the folder.
- Stage logs belong in a logs or audit folder.
- Durable plans belong in planning or project sources.
- Release records belong with release artifacts.
- Agent context should summarize, not replace, canonical files.

### 4.5 Keep documentation auditable

A useful Markdown artifact should state:

- scope;
- sources inspected;
- current status;
- unresolved items;
- ownership;
- next action;
- date or version when staleness matters.

---

## 5. Build an evidence hierarchy

Not all information has the same authority.

A general evidence hierarchy is:

1. **Authoritative external source** — law, policy, official form, signed decision, approved specification.
2. **Versioned primary source** — code, design file, source dataset, contract, approved manuscript.
3. **Execution record** — logs, run summaries, build reports, test output.
4. **Generated artifact** — PDF, chart, export, report, binary.
5. **Derived validation record** — checked table, checksum, reconstruction, audit ledger.
6. **Secondary source** — literature, documentation, commentary.
7. **Human decision** — approved interpretation, prioritization, acceptance.
8. **Inference** — reasoned conclusion that must be labeled as such.

Do not allow a lower-level source to silently replace a higher-level one.

Examples:

- A requirements file describes an intended environment; it does not prove the environment used historically.
- A generated report does not prove the source values were correct.
- A filename does not prove a process completed.
- An official public rule does not prove a specific project received approval.

A primary deliverable should remain self-contained for its central concepts, decisions, methods, and conclusions. A supporting evidence package may contain exhaustive source mappings, hashes, logs, or operational details, but it must not become the only place where a reader can understand a core construct.

---

## 6. Use bounded stages

Break work into stages that can be independently verified.

Each stage should define:

- objective;
- expected starting state;
- authoritative sources;
- allowed edits;
- forbidden edits;
- protected material;
- validation;
- required outputs;
- readiness decision.

Avoid prompts such as “finish the project” or “improve everything.”

### 6.1 Stage lifecycle

1. Verify baseline.
2. Protect critical material.
3. Inspect relevant sources.
4. Make the smallest sufficient change.
5. Validate.
6. Produce an evidence report.
7. Version or commit.
8. Independently review.
9. Continue, repair narrowly, or block.

### 6.2 Readiness states

Use explicit states:

```text
READY FOR NEXT STAGE
READY FOR NEXT STAGE WITH NON-BLOCKING GATES
BLOCKED BEFORE NEXT STAGE — REASON
READY FOR HUMAN REVIEW
READY FOR RELEASE PREPARATION
```

This prevents uncertainty from being hidden inside prose.

---

## 7. Protect critical material

Before editing, identify files that must not change.

Protected material may include:

- approved data;
- verified numbers;
- legal text;
- signed documents;
- accepted design assets;
- published content;
- baseline code;
- previous audit reports;
- external source packages;
- prior-stage deliverables.

Use hashes or exact snapshots when byte-level preservation matters.

For text-heavy deliverables, snapshot important tokens or structures, such as:

- numbers;
- dates;
- names;
- citations;
- identifiers;
- headings;
- labels;
- links;
- table values;
- captions.

After editing, compare the protected baseline with the final state.

---

## 8. Validate the actual artifact, not only the source

Different artifact types require different validation.

### 8.1 Documents and PDFs

Check:

- successful build or export;
- page count;
- unresolved references;
- missing fonts or glyphs;
- structural integrity;
- clipping and overlap;
- margins;
- tables and figures;
- headers and footers;
- blank pages;
- multilingual text;
- page-level readability;
- effective line and paragraph spacing;
- environment-specific spacing in tables, captions, contents, bibliography, equations, and title material.

Do not validate formatting only by checking that a global command exists. Inspect the existing template and the rendered result. Preserve an already compliant implementation, avoid duplicate formatting mechanisms, and apply requirements contextually rather than multiplying every vertical dimension. A contact sheet is useful for navigation but is not a substitute for page-level review.

### 8.2 Spreadsheets

Check:

- formulas;
- references;
- units;
- totals;
- filters;
- hidden rows or sheets;
- data types;
- input/output separation;
- chart source ranges;
- scenario assumptions.

### 8.3 Presentations

Check:

- narrative sequence;
- slide density;
- readability at presentation scale;
- image quality;
- source attribution;
- consistent terminology;
- presenter notes;
- no clipped objects.

### 8.4 Code and systems

Check:

- tests;
- static analysis;
- runtime behavior;
- configuration;
- environment assumptions;
- side effects;
- generated outputs;
- rollback or recovery path.

### 8.5 Visuals and figures

Validate both data and appearance:

1. reconstruct or inspect source values;
2. verify labels and ordering;
3. verify exclusions;
4. inspect the rendered image;
5. record what the approval does and does not imply.

Visual approval does not automatically validate the underlying analysis.

---

## 9. Treat warnings as evidence to investigate

Do not chase warning counts blindly.

Classify warnings as:

- material defect;
- minor readability defect;
- benign diagnostic;
- tool artifact;
- unresolved.

For a layout warning, connect:

- source location;
- warning magnitude;
- rendered page;
- visible effect;
- repair decision.

A large warning with no visible defect may be benign, but it needs explicit explanation. A small warning that clips important content may be blocking.

---

## 10. Compress and restructure without weakening the deliverable

Compression is sometimes necessary for documents, presentations, plans, reports, and other large artifacts. The objective is not to hit a number mechanically; it is to improve focus while preserving the information required for correct use and evaluation.

Distinguish:

- **substantive scope** — the claims, decisions, methods, requirements, evidence, and conclusions that define the work;
- **documentary scope** — repeated explanation, audit detail, path inventories, status matrices, version history, and operational evidence that can be summarized or relocated.

A good compression pass may:

- merge overlapping sections;
- remove repeated explanations;
- consolidate tables;
- replace path-heavy narration with a precise reference to a technical package;
- shorten transitions;
- centralize qualifications;
- move exhaustive traceability records outside the main artifact.

It must not:

- remove the information needed to understand a central construct;
- hide important assumptions;
- make the reader inspect implementation files to understand the method;
- alter verified values or decisions;
- manipulate typography merely to reduce page or slide count;
- treat an arbitrary length target as the definition of success.

After compression, perform an independent completeness review. Ask not only “Is it shorter?” but also:

- Can the artifact still stand on its own?
- Are operational definitions still understandable?
- Are essential settings and assumptions still present?
- Did relocation preserve a clear and durable reference?
- Were any necessary local qualifications removed?

If the compression is broadly successful but one essential area became too thin, use a narrow restoration stage.

---

## 11. Use narrow repair stages

When a completed stage is mostly correct but one problem remains, create a repair stage.

A repair stage should:

- name the specific defect;
- preserve all unrelated work;
- limit allowed edits;
- define success precisely;
- rerun only necessary validation;
- produce its own report.

Examples:

- high-resolution visual verification after a low-resolution review;
- one table overflow repair;
- one citation-key correction;
- one missing metadata field;
- one deployment configuration defect.

Do not reopen an entire project for a localized issue.

---

## 12. Separate machine work from human work

### 12.1 Machine responsibilities

Agents are well suited for:

- inventory;
- comparison;
- consistency checks;
- static validation;
- controlled transformation;
- formatting;
- build and export;
- evidence ledgers;
- checksum generation;
- locating unresolved fields.

### 12.2 Human responsibilities

Humans must provide:

- authoritative identity and organizational facts;
- approval and authorization;
- scientific or professional judgment;
- ethical and legal determinations;
- strategic priorities;
- acceptance of ambiguity or risk;
- final content ownership;
- final release or submission.

### 12.3 Two-level human review

For major deliverables, use two human-review levels.

#### Level 1 — Owner first-draft review

The owner checks:

- factual accuracy;
- structure;
- names and terminology;
- tone and authorship;
- missing context;
- whether every statement can be defended;
- whether the output matches the actual work.

#### Level 2 — Deep expert or supervisor review

The owner and expert check:

- correctness;
- methodology;
- interpretation;
- risk;
- compliance;
- contribution;
- final positioning;
- release readiness.

Consolidate comments into one controlled change list before returning to the execution agent.

---

## 13. Manage missing authoritative inputs explicitly

Create a register for missing inputs with fields such as:

```text
item
why required
where used
responsible provider
acceptable evidence
current status
blocking effect
```

Examples include:

- official names;
- approval wording;
- form versions;
- dates;
- legal determinations;
- data-use terms;
- budget assumptions;
- security requirements;
- customer sign-off;
- clinical or domain review.

Do not infer these from usernames, file paths, company names, commit authors, or contextual hints.

---

## 14. Independent review procedure

When someone says “move to the next part,” the coordinator should:

1. identify the current version or commit;
2. identify the task baseline and any useful reference baseline;
3. classify intervening changes as relevant, unrelated, or conflicting;
4. verify the sequence without resetting unrelated work;
5. inspect changed files;
6. read the execution agent’s report;
7. independently verify high-impact claims;
8. inspect the main artifact;
9. choose:
   - ready;
   - ready with non-blocking gates;
   - narrow repair;
   - blocked;
10. issue the next bounded task.

The coordinator should be honest about what was not independently inspected. A report generated by the same agent that made the change is evidence, not independent confirmation.

---

## 15. Versioning and commits

Use one version or commit per meaningful stage.

A stage record should make it possible to answer:

- what changed;
- why it changed;
- what was protected;
- what validation ran;
- what remains unresolved;
- what the next authorized action is.

If a commit message does not exactly match the conceptual stage, record the mapping rather than rewriting history unnecessarily.

If unrelated commits are added after a completed stage, keep them. A later repair should begin from the current version, protect the unrelated changes, and use the earlier stage commit as the comparison baseline. Do not reset or revert unrelated work merely because it is outside the current task.

Do not mix unrelated work into one stage commit when the stage is being created. When unrelated work already exists in later commits, classify and protect it rather than rewriting history.

---

## 16. Evidence reports and ledgers

Useful records include:

- baseline report;
- file-change ledger;
- decision register;
- claim-evidence matrix;
- frozen-content snapshot;
- validation results;
- visual-review ledger;
- warning-localization ledger;
- unresolved-input checklist;
- release handoff;
- final checksum record.

A good report should be reproducible enough that another agent can continue without relying on chat memory.

---

## 17. Prompt contract for execution agents

A robust prompt includes:

```text
Task identity
Current version
Task baseline and optional reference baseline
Intervening-change classification
Objective
Context and authority
Allowed tools
Forbidden execution
Baseline verification
Protected paths
Required inspection
Required changes
Allowed files
Forbidden files
Validation
Required records
Readiness wording
No commit or push unless authorized
```

The prompt should state what not to do as clearly as what to do.

---

## 18. Common failure modes

### Starting with creation instead of inspection

The agent duplicates or contradicts existing work.

### Creating excessive Markdown files

Canonical information becomes fragmented and stale.

### Treating generated artifacts as authoritative sources

A polished output can still contain unsupported content.

### Treating a successful build as acceptance

Build success is necessary but not sufficient.

### Trusting self-reported validation without inspection

The report may be incomplete or mechanically generated.

### Using broad rewrites for localized defects

This introduces unnecessary risk.

### Hiding missing human facts behind placeholders

Unresolved inputs should be explicit and owned.

### Confusing review roles

An execution agent should not approve its own high-impact judgment without independent review.

### Promising asynchronous work

Work must be completed in the current interaction or scheduled through an authorized mechanism.

### Assuming the newest version is the task baseline

Unrelated later work can exist. Classify it, protect it, and compare against the correct baseline instead of resetting the project.

### Optimizing an arbitrary length or count

A page, slide, file, or warning target is not a quality definition. Preserve the information needed for correct interpretation and use.

### Moving essential information entirely into supporting files

A technical package may hold exhaustive evidence, but the primary artifact must still explain its central constructs and decisions.

### Applying formatting rules mechanically

Inspect effective formatting and local context. Do not stack global commands or force body-style spacing into tables, captions, references, or other dense environments.

---

## 19. Release workflow

A general release sequence is:

1. complete machine hardening;
2. perform a shallow independent artifact check;
3. supply known missing authoritative inputs;
4. owner first-draft review;
5. controlled revision;
6. deep owner–expert review;
7. approved revision;
8. insert final authoritative metadata and forms;
9. clean build or export;
10. full artifact inspection;
11. protected-hash verification;
12. produce release and archival artifacts;
13. record checksums and version;
14. human sign-off;
15. release or submit.

Do not label a draft “final” while authoritative inputs or approval gates remain unresolved.

---

## 20. Definition of done

A project deliverable is done when:

- the intended scope is complete;
- authoritative inputs are present;
- protected material is intact;
- validation passes;
- unresolved issues are either closed or explicitly accepted;
- the final artifact has been inspected;
- the primary artifact is self-contained for its central concepts, decisions, assumptions, and conclusions, while supporting packages retain exhaustive evidence;
- the correct humans have approved it;
- the released artifact is the same artifact that was approved;
- version and checksums are recorded when appropriate;
- the next maintainer can understand the state from project files alone.

---

## 21. Compact operational checklist

### Before work

- Find the root.
- Read local instructions.
- Inspect folders and existing documentation.
- Record current version, task baseline, reference baseline, and dirty state.
- Classify intervening changes.
- Identify protected files, including unrelated later work.
- Confirm the task and authority.

### During work

- Stay within scope.
- Use primary evidence.
- Record decisions and uncertainty.
- Avoid inventing missing facts.
- Prefer small, reviewable changes.

### After work

- Validate source and artifact.
- Compare protected state.
- Write the evidence report.
- State unresolved gates.
- Version the work.
- Obtain independent review.
- Proceed, repair narrowly, or block.
