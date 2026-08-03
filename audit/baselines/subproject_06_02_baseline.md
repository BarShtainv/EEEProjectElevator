# SP-06.2 Baseline

## Repository and environment

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Accepted starting commit: `b449bed3300b341360964128b951df9b80b4fcf3` (`Step_6.1`)
- Initial Git status: clean (`git status --short --untracked-files=all` produced no output before validation)
- External environment: `/home/bar/.venvs/eeeproject-elevator`
- Python: `3.13.13`
- pip: `26.2`
- pytest: `9.1.1`
- Repository instructions: no `AGENTS.md` exists in the repository

The branch, commit, remote repository, and clean status exactly match the accepted task baseline. The accepted SP-06.1 and SP-06.1R stage and validation records are present. No conflicting user change exists, and no repository-local virtual environment exists.

## Existing package and regression

Existing source paths were `src/elevator_access_sim/__init__.py`, `models.py`, `config.py`, and `clock.py`. Existing tests were `tests/unit/test_models.py`, `test_config.py`, and `test_clock.py`. No Wiegand or later-stage module existed.

The required pre-edit regression command produced:

```text
$ PYTHONPATH=src python -m pytest
collected 114 items
============================= 114 passed in 0.37s ==============================
```

Failed: 0. Skipped: 0. Xfailed: 0. The run generated only cache files, which are validation by-products scheduled for final removal.

## Frozen `PROJECT_WIEGAND_26` profile

This proposed simulator profile uses exactly 26 ordered exact-integer bits. Documentation bit 1 is leading parity; bits 2–9 are an unsigned 8-bit facility code; bits 10–25 are an unsigned 16-bit credential number; and bit 26 is trailing parity. Bits 1–13 have even parity, and bits 14–26 have odd parity. Fields are most-significant-bit first. Facility range is 0–255; credential range is 0–65535. LF/HF source metadata is external and cannot be inferred from frame bits.

The reviewed canonical strings are:

```text
WV-001  facility=0    credential=0      00000000000000000000000001
WV-002  facility=255  credential=65535  01111111111111111111111111
WV-003  facility=1    credential=1      10000000100000000000000010
WV-004  facility=85   credential=4660   10101010100010010001101001
WV-005  facility=42   credential=43690  10010101010101010101010101
WV-006  facility=1    credential=100    10000000100000000011001000
```

## Authorized and protected scope

Authorized paths are:

- create `src/elevator_access_sim/wiegand.py` and `tests/unit/test_wiegand.py`;
- update `src/elevator_access_sim/__init__.py`;
- create this baseline, `audit/stage_reports/subproject_06_02.md`, and `audit/validation/subproject_06_02_validation.md`;
- append the SP-06.2 section to `audit/file_change_ledger.md`.

Requirements, register model, architecture and mappings/diagrams, software design, test plan/inventory, implementation sequence, traceability, evidence, literature/source PDFs, bibliography, product material, prior audit records, project plan, workflow handbook, and Git history are protected. Credential loading/repository, authorization, event logging, outputs, watchdog, controller, CLI, experiments, alternate Wiegand profiles/lengths, pulse timing, and physical adapters remain deferred.

## Protected baseline hashes

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
```
