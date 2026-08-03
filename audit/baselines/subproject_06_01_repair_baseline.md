# SP-06.1R Repair Baseline

## Repository state

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `b155165f279f88699517998e877248bfa62e4a70` (`Step_6`)
- Starting Git status: clean (`git status --short --untracked-files=all` produced no output)
- Base Python before environment activation: `Python 3.13.13`
- Base pytest availability: unavailable (`/home/bar/miniforge3/bin/python: No module named pytest`)
- Intended isolated environment: `/home/bar/.venvs/eeeproject-elevator`
- Initial isolated-environment state: absent

The branch and commit exactly match the accepted repair baseline. Recent history places `Step_6` immediately after `Step_5`. No conflicting user changes were present.

## Original blocked result

The committed SP-06.1 stage report and validation remain historical records. Their exact readiness line is:

```text
BLOCKED BEFORE NEXT STAGE — pytest is unavailable in the active Python environment
```

## Inspected SP-06.1 paths

The package metadata, four foundation source files, three unit-test files, original stage report, and original validation record were inspected before environment creation. Their SHA-256 hashes were:

```text
fbade5bbcb8950427a3a626a184f2af1959a59e6c030578b4e98e749cdc664cc  pyproject.toml
957a072c986e46d98c5bbbc25329eb830da3c6ca3b6ae795b5744fc582278ffd  src/elevator_access_sim/__init__.py
62302429842152aa1cc3f22bed60e6102eb5ccecc17d82d95cb6c815f578cc86  src/elevator_access_sim/clock.py
b74cba3fb05785401e355f80eb309bdb9e89b8b82c2f055614f1709f86c3e4e2  src/elevator_access_sim/config.py
646b703fd7096f39c05394b693ae05e5b95390f671b794089e0213be830292d1  src/elevator_access_sim/models.py
a563eb080128164cf708cb4606ff342d46f4eb7176932a88972de021fce52f50  tests/unit/test_clock.py
770f837cbeddfa4b47ebf87ec9316f1261d0dc1b94983c1b8702f77b376e079b  tests/unit/test_config.py
f4a0ae97eefe418761fe92a7ff3dc6d23885e8d001b2e8b90781bd95a017724f  tests/unit/test_models.py
9f6a98889db0ec455d1af99c651eeb1f4f7c347829f051128d32d68261b86f69  audit/stage_reports/subproject_06_01.md
6d95b16f4bd3c5102d0a3c2aca20715f46f03a6d98b2da0e41ccae5b1f8006e3  audit/validation/subproject_06_01_validation.md
```

## Authorized and protected scope

Authorized unconditional repository changes are this baseline, `audit/stage_reports/subproject_06_01_repair.md`, `audit/validation/subproject_06_01_repair_validation.md`, and an appended SP-06.1R section in `audit/file_change_ledger.md`. The four existing production files and three existing test files may change only if real pytest execution exposes a genuine defect.

Requirements, register model, architecture and mappings/diagrams, evidence, literature and source PDFs, bibliography, product material, prior audit reports and validations, project plan, workflow handbook, implementation sequence, Git history, and all later-stage implementation paths are protected. No protected path was initially changed.

SP-06.2 has not begun: no Wiegand validation, Wiegand encoding, or other later-stage production or test module exists.
