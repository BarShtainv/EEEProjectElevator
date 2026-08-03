# SP-05 Baseline

## Stage identity

- Stage: `SP-05 — Software Model Design and Verification Design`
- Recorded: `2026-08-03T11:45:31+03:00`
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Current and accepted starting commit: `08e7985f3d01303b9c28066d3693833fa3aa614e`
- Commit subject: `Step_4`
- Initial `git status --short --untracked-files=all`: clean; no output

## Recent history and prerequisites

```text
08e7985 (HEAD -> main, origin/main, origin/HEAD) Step_4
94b051c step3
88a6460 step2Repair
4cba9bb step2Repair
fdad611 Step 2
```

The current commit is exactly the project-owner-specified SP-05 baseline. The SP-03 requirements and traceability artifacts and the SP-04 architecture, register model, requirement mapping, six focused architecture diagrams, stage reports, and validation records are present. SP-03 contains 60 required and six optional requirements. The requirements traceability file contains 69 unique planned test IDs, all of which must resolve in the SP-05 inventory.

No repository-local `AGENTS.md`, `CONTRIBUTING.md`, or separate workflow instruction was found. Applicable instructions are the SP-05 project-owner instruction, `final_engineering_project_plan.md`, and `general_purpose_evidence_gated_workflow_handbook_updated.md`.

The project owner authorizes the SP-03 requirements and SP-04 architecture as the design basis. This is not supervisor approval; supervisor confirmation remains pending.

## Frozen design basis

- Proposed input profile: `PROJECT_WIEGAND_26`, with its existing field and parity definitions.
- Logical reader-source labels: `LF` and `HF` only.
- Floors 1–16 map to mask/output bits 0–15.
- Credential keys are ordered `(facility_code, credential_number)` pairs; duplicates are rejected.
- Exactly 16 Boolean outputs exist, with no more than one active.
- Busy detection precedes request inspection and preserves the active output and expiry.
- Output duration defaults to 3000 ms and accepts 100–30000 ms inclusive.
- Watchdog timeout defaults to 2000 ms.
- Manual/watchdog reset clears outputs, expiry, and transients while preserving validated configuration, credentials, event history, and sequence progression.
- Event records contain all nine canonical fields and explicit nulls.
- The seven controller states and all source/event/result/reason enumerations remain unchanged.
- The system remains a deterministic Python software model of an abstract access-authorization layer.

## Mandated watchdog clarification

SP-05 must clarify, without redesigning SP-04, that the logical heartbeat interval is `max(1, watchdog_timeout_ms // 2)`. Simulated time advances chronologically without millisecond loops. At one timestamp, priority is normal unsuppressed heartbeat service, then watchdog expiry evaluation, then output expiry. Suppression skips service but not time. If watchdog and output expiry coincide under suppression, watchdog reset wins, cancels the output timeout, and produces exactly one watchdog outcome. No thread, asynchronous framework, wall-clock sleep, or physical watchdog is permitted.

## Authorized outputs and changes

SP-05 may create its baseline, stage report, validation record, software-design document, test plan, test inventory, and implementation sequence. It may narrowly update `docs/architecture.md`, `docs/figures/watchdog_sequence.mmd`, `docs/decision_log.md`, `docs/requirements_to_test_traceability.csv` only if necessary, and `audit/file_change_ledger.md`.

It must not create production code, pytest files, package metadata, runtime configuration files, experiment scripts, generated data, results, plots, or report chapters. It must not commit or push.

## Protected material

The frozen requirements, register model, architecture-to-requirements mapping, context/state/data/firmware/reset/top-level diagrams, evidence and literature records, bibliography, project plan, workflow handbook, and prior audit records are protected. The watchdog diagram is the only diagram authorized for a narrow clarification.

Baseline SHA-256 values:

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

Source PDF hashes remain protected through Git path checks and the prior validation records.

## Entry assessment

No baseline conflict exists. SP-05 may proceed as documentation and verification design only. Human review must cover the package/API/type choices, schemas, scheduler priority, heartbeat formula, error policy, event-log failure behavior, fixtures/vectors, behavioral coverage, scalability workload, generated-data policy, and bounded implementation sequence.
