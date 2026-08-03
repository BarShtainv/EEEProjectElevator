# SP-06.1 Baseline

## Stage identity

- Stage: `SP-06.1 — Package foundation, shared models, configuration, and simulated clock`
- Recorded: `2026-08-03T12:19:03+03:00`
- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Current and accepted starting commit: `7a0b173724038aeac9f25f783a52a586a83619bf`
- Commit subject: `Step_5`
- Initial `git status --short --untracked-files=all`: clean; no output

## Recent history

```text
7a0b173 (HEAD -> main, origin/main, origin/HEAD) Step_5
08e7985 Step_4
94b051c step3
88a6460 step2Repair
4cba9bb step2Repair
fdad611 Step 2
```

The current commit exactly matches the project-owner-specified SP-06.1 baseline. No intervening or conflicting work is present.

## Instructions and inspected prerequisites

No repository-local `AGENTS.md`, `CONTRIBUTING.md`, or separate package instruction exists. Applicable instructions are the SP-06.1 task, `final_engineering_project_plan.md`, and `general_purpose_evidence_gated_workflow_handbook_updated.md`.

Inspected prerequisites include the SP-05 stage and validation records, frozen requirements/register model, architecture, software design, test plan/inventory, implementation sequence, decision log, existing metadata, and existing production/test paths. No `src/`, `tests/`, Python source, `pyproject.toml`, setup file, requirements file, or package/test artifact existed at baseline.

## Toolchain

```text
python --version: Python 3.13.13
python -m pytest --version: /home/bar/miniforge3/bin/python: No module named pytest
python3 --version: Python 3.13.13
/usr/bin/python3 --version: Python 3.14.4
pytest availability: unavailable for every inspected interpreter; no pytest executable on PATH
```

Python satisfies the 3.11+ constraint. Pytest is unavailable. The task prohibits installing packages or accessing the network, so scoped implementation and non-pytest validation may proceed, but SP-06.1 cannot claim its required test execution gate and must end with the specific pytest blocker unless the local tool state changes independently.

## Mandatory specification corrections

Before production files, SP-06.1 must narrowly correct:

1. `ReaderSource` canonical serialization from lowercase `lf`/`hf` to frozen uppercase `LF`/`HF`, without changing values 1/2 or lowercasing rules for other enums.
2. Intermediate-state reset testing from an undefined transition observer/pause mechanism to public snapshot/event observation plus a focused white-box test-only fixture that constructs internally valid states. No production state-forcing/observer API, thread, async task, pause, or reentrant callback is permitted.

Only `docs/software_design.md`, `docs/test_plan.md`, `docs/test_case_inventory.csv`, and `docs/decision_log.md` may receive these corrections.

## Authorized implementation scope

SP-06.1 may create minimal setuptools metadata, the `elevator_access_sim` package foundation (`models.py`, `config.py`, `clock.py`, explicit `__init__.py`), three focused unit-test files, and its baseline/report/validation records. It may update the four correction documents and canonical ledger only.

Wiegand, credential-file loading, repository, authorization, logger, output, watchdog, controller, CLI, experiment, hardware, database, network, thread, and async behavior remain deferred or prohibited.

## Protected paths and hashes

The requirements, register model, architecture/mapping/diagrams, evidence, literature/source PDFs, bibliography, product material, plan, workflow handbook, implementation sequence, and prior audit records are protected.

```text
9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d  docs/requirements.md
f2b836e963de52ccce035277b326601815b2928c1343ac80d3afe547c9106466  docs/register_model.md
89ac9f0925fa0a29d2d690dc86e10ebec3223b20208158dfb6a1c95a19d2a4d5  docs/architecture.md
629c4e986e38aff724dc5cdbe8241232ede81c03c8c216fba60993102660f4b9  docs/architecture_to_requirements.csv
8106d1a6b4cdc4d12c8c3fa571d1176e50095e2b2bb1a815ec82d7e826ef4129  docs/implementation_sequence.md
d4a47d131b93fae53e3725260a86312f747b7e06f931d172fabf019f88e2fc64  docs/figures/controller_state_machine.mmd
c797ce5d0456593bace5796bfdb1f2b39adf155471552e0ca4094c6f666f36bc  docs/figures/data_flow.mmd
8b116413c1173700d0fe19017cecdacffba124fd9ceac19e3d54b0fc7605a475  docs/figures/firmware_architecture.mmd
1fbb0c45d57a1d55ffbe741a7d534f4c3cc7af6208726f35c91f9f18933058bb  docs/figures/reset_sequence.mmd
2f15218127660b422c578c6da1e5ca0c6cb72d336edb0f613fad49f6fe7a47e0  docs/figures/system_context.mmd
660c47967333b86e6a600821a2607375cdc24abd24de0609515a154f0981e605  docs/figures/top_level_architecture.mmd
bd1f9b85700d82723fc226403a0e2ba320c1534937206161a10c1cf9826e1be6  docs/figures/watchdog_sequence.mmd
d7b54357cb414f8df32f4d99684ac0e02146d6993341652cc3f15fe5ab578911  evidence/assumptions_and_unknowns.md
f8a4031d92a47e816f132456e1e68e145f8104689f83ec765e96e82730ab1d66  evidence/claim_evidence_matrix.csv
a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52  evidence/literature_notes.md
750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361  evidence/product_evidence.md
639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868  evidence/source_index.md
9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102  evidence/unresolved_sources.md
65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307  report/references.bib
fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33  final_engineering_project_plan.md
1091f402282c31c0958db3fffe7df06d1d965a2235a9a58d52e2945db58b128c  general_purpose_evidence_gated_workflow_handbook_updated.md
f802687366ca935c32b19bbac60daab2d212115cd01b0852911c2abd8fdc2739  audit/stage_reports/subproject_05.md
259129d27af4d2bc4f128925cf04fdf45fad6cbe5e5c14124418f9eb16e220b3  audit/validation/subproject_05_validation.md
```

Source PDF and other prior-audit preservation will also be confirmed through final Git path checks.
