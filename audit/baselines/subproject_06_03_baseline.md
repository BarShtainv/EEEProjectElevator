# SP-06.3 Baseline

## Repository and environment

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Accepted starting commit: `4dfd4b2ae0d369c0d45755e9595ac197b1276d67` (`Step_6.2`)
- Initial Git status: clean (`git status --short --untracked-files=all` produced no output before validation)
- External environment: `/home/bar/.venvs/eeeproject-elevator`
- Python: `3.13.13`
- pip: `26.2`
- pytest: `9.1.1`
- Repository instructions: no `AGENTS.md` exists in the repository

The branch, commit, remote, and clean worktree exactly matched the accepted baseline. The committed SP-06.1, SP-06.1R, and SP-06.2 stage and validation records were present. No conflicting user change or repository-local virtual environment existed.

## Existing package and regression

Existing source paths were package `__init__.py`, `models.py`, `config.py`, `clock.py`, and `wiegand.py`. Existing unit tests were `test_models.py`, `test_config.py`, `test_clock.py`, and `test_wiegand.py`. No credentials, authorization, event-log, output, watchdog, controller, CLI, experiment, persistence, database, network, or hardware module existed.

The mandatory pre-edit regression produced:

```text
$ PYTHONPATH=src python -m pytest
collected 218 items
============================= 218 passed in 0.59s ==============================
```

Passed: 218. Failed: 0. Skipped: 0. Xfailed: 0. Validation generated only cache files scheduled for final removal.

## Frozen credential schema

Credential input is a Python string containing one JSON object with exactly required fields `schema_version` and `credentials`. Version is exact integer 1; `credentials` is an array and may be empty. Duplicate JSON members at any object level are invalid credential data.

Each credential entry is exactly an object with required `facility_code`, `credential_number`, `enabled`, and `floor_mask`, plus optional `label`. Facility is exact integer 0–255, credential exact integer 0–65535, enabled an actual Boolean, and mask exact integer 0–65535. Boolean never satisfies an integer field. An omitted label becomes `None`; a present label is a nonempty, non-whitespace, UTF-8-encodable string preserved without normalization. JSON null and lone surrogates are invalid.

Input-array order is preserved in an immutable result tuple. All records validate before publication. The identity is the ordered `CredentialKey(facility_code, credential_number)`; duplicate keys raise `DuplicateCredentialError`, while duplicate JSON member names and all other schema defects raise `CredentialDataError`.

## Frozen repository and authorization order

`CredentialRepository` owns an immutable ordered record tuple and a private key index, exposes lookup/records/length only, treats a valid unknown key as a normal `RepositoryLookup(None)`, validates construction atomically, and raises `StateInvariantError` for malformed trusted lookup keys.

Pure authorization applies this order:

1. validate the trusted decoded credential;
2. return unknown when no record exists;
3. validate the supplied record and matching key;
4. return disabled before inspecting the floor;
5. validate an exact-integer floor 1–16;
6. inspect `1 << (floor - 1)`;
7. return unauthorized when clear or authorized when set.

Thus unknown and disabled reasons take precedence over malformed floors. Floor 1 maps to mask bit 0 and floor 16 to bit 15.

## Authorized and protected scope

Authorized paths are:

- create `src/elevator_access_sim/credentials.py` and `authorization.py`;
- extend `src/elevator_access_sim/config.py` and package `__init__.py`;
- create `tests/unit/test_credential_config.py`, `test_credentials.py`, and `test_authorization.py`;
- create this baseline, `audit/stage_reports/subproject_06_03.md`, and `audit/validation/subproject_06_03_validation.md`;
- append one SP-06.3 section to `audit/file_change_ledger.md`.

Requirements, register model, architecture and mappings/diagrams, software design, test plan/inventory, implementation sequence, traceability, evidence, literature/source PDFs, bibliography, product material, prior audit records, project plan, workflow handbook, and Git history are protected. Event logging and failure injection remain deferred to SP-06.4; outputs, watchdog, controller, resets, CLI, experiments, persistence/database/network, administrator/role/time policy, and hardware remain later or excluded.

## Protected hashes

```text
9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d  docs/requirements.md
f2b836e963de52ccce035277b326601815b2928c1343ac80d3afe547c9106466  docs/register_model.md
89ac9f0925fa0a29d2d690dc86e10ebec3223b20208158dfb6a1c95a19d2a4d5  docs/architecture.md
82401d922484036bd1e011a6068dbef02f3b07bdbe355e9d1fc868e74fdf9476  docs/software_design.md
786e91d8072f053472288e2179291b677f21e8f2277016fdee0221528b371690  docs/test_plan.md
ba6fac0b967fb85bd0b3e2e1a36ddb4d0ac0a37de832a955479eec6becdefd17  docs/test_case_inventory.csv
8106d1a6b4cdc4d12c8c3fa571d1176e50095e2b2bb1a815ec82d7e826ef4129  docs/implementation_sequence.md
9f41034d1ceefb914f106b49e891937a14fdc903d08cd19d65fbda42a597d3ee  docs/decision_log.md
9f6a98889db0ec455d1af99c651eeb1f4f7c347829f051128d32d68261b86f69  audit/stage_reports/subproject_06_01.md
6d95b16f4bd3c5102d0a3c2aca20715f46f03a6d98b2da0e41ccae5b1f8006e3  audit/validation/subproject_06_01_validation.md
d3b4221b280d01cc4f1aabe159c7101a5ab284cf02352eba22cd3405b1aa8e96  audit/stage_reports/subproject_06_01_repair.md
5bb39709f76790eff972f77659718a7b79025127b2bc0c7563dfb4a06e323687  audit/validation/subproject_06_01_repair_validation.md
235a1c0eee4bda27087e7638c94edca4aa1c8e2241df8a5dadf1552509a0f1e0  audit/stage_reports/subproject_06_02.md
de034cac478c5e57f4ff3a4e7c87551a0d1e4f587dccd06469a3d0df7cddcfc4  audit/validation/subproject_06_02_validation.md
```
