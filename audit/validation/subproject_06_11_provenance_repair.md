# SP-06.11R Verification-Record Provenance Repair

## Starting state and baseline

- Accepted branch/commit: `main` at `7b47e51a907dde6c20b89e2536022d886ebff6d3` (`Step_6.11.2`).
- Initial status: clean; no conflicting user change was present.
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from the accepted external environment. No install or network access occurred.
- Cache cleanup preceded the baseline. Exact `PYTHONPATH=src python -m pytest`: 976 collected/passed in 4.76s; 0 failed/skipped/xfailed.
- Accepted SP-06.11 README, reproducibility, inventory 94/6, traceability 60/6, experiment evidence, baseline, stage/validation records, and hardened PathLike repair were present.

## Defect and authoritative analysis

The accepted final verification CSV had valid paths and nodes but assigned some rows to a validation stage based on inventory-category ownership rather than the creation and execution history of the cited executable evidence. This produced historically impossible early references and several unnecessarily late references.

Every executable evidence path in all 100 rows was audited with `git log --diff-filter=A` and `git log --follow`. The creation commit for each cited test file was compared with the creation commit and execution content of the proposed validation record. The SP-06.1 repair through SP-06.11 validations were inspected for direct scoped or full-suite execution. Git ancestry validation confirmed each final validation record was created with or after its cited test and actually records direct or full-suite execution containing that evidence.

No evidence node or artifact reference was wrong, so the `evidence` column required no correction. Exactly 15 `environment_reference` cells changed; all other CSV fields remained byte-for-byte at their row values.

## Corrected provenance

| Test ID | Previous environment reference | Corrected environment reference | Evidence establishing stage |
|---|---|---|---|
| `TST-DAT-003` | `audit/validation/subproject_06_02_validation.md` | `audit/validation/subproject_06_07_validation.md` | `tests/integration/test_controller_requests.py` was added at `6ad5614` and executed directly plus in the SP-06.7 full suite. |
| `TST-CRD-006` | `audit/validation/subproject_06_03_validation.md` | `audit/validation/subproject_06_07_validation.md` | `tests/unit/test_controller_initialization.py` was added at `6ad5614` and executed directly plus in the SP-06.7 full suite. |
| `TST-DAT-004` | `audit/validation/subproject_06_02_validation.md` | `audit/validation/subproject_06_03_validation.md` | Both `tests/unit/test_authorization.py` and `tests/unit/test_credential_config.py` were added at `2677b8d` and included in SP-06.3 scoped/full validation. |
| `TST-OUT-001` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_05_validation.md` | `tests/unit/test_outputs.py` was added at `c75475e` and executed directly plus in the SP-06.5 full suite. |
| `TST-OUT-004` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_01_repair_validation.md` | `tests/unit/test_models.py` was added at the SP-06.1 implementation and passed the accepted SP-06.1 repair suite. |
| `TST-TIM-002` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_01_repair_validation.md` | `tests/unit/test_config.py` was added at the SP-06.1 implementation and passed the accepted SP-06.1 repair suite. |
| `TST-TIM-003` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_01_repair_validation.md` | `tests/unit/test_clock.py` was added at the SP-06.1 implementation and passed the accepted SP-06.1 repair suite. |
| `TST-WDG-006` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_06_validation.md` | `tests/unit/test_watchdog.py` was added at `42f3bf4` and executed in SP-06.6 watchdog/full validation. |
| `TST-LOG-001` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_04_validation.md;audit/validation/subproject_06_07_validation.md` | The row cites `tests/unit/test_event_log.py` added/executed at `510250c`/SP-06.4 and `tests/integration/test_controller_logging_faults.py` added/executed at `6ad5614`/SP-06.7. |
| `TST-LOG-002` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_04_validation.md` | Its event-log node was added and directly executed at SP-06.4. |
| `TST-LOG-003` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_04_validation.md;audit/validation/subproject_06_07_validation.md` | The row cites both the SP-06.4 event-log test and SP-06.7 logging-fault integration test, so both originating validations are retained. |
| `TST-LOG-004` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_04_validation.md` | Its JSON Lines event-log node was added and directly executed at SP-06.4. |
| `TST-CFG-004` | `audit/validation/subproject_06_01_repair_validation.md` | `audit/validation/subproject_06_03_validation.md` | `tests/unit/test_credential_config.py` was added and executed at SP-06.3. |
| `TST-CFG-005` | `audit/validation/subproject_06_01_repair_validation.md` | `audit/validation/subproject_06_07_validation.md` | `tests/unit/test_controller_initialization.py` was added and executed at SP-06.7. |
| `TST-E2E-001` | `audit/validation/subproject_06_07_validation.md` | `audit/validation/subproject_06_08_validation.md` | `tests/integration/test_cli.py` was added at `9a6c448` and executed directly plus in the SP-06.8 full suite. |

All other 85 rows already had appropriate provenance. The five experiment rows retain `results/scalability_environment.json` and `audit/validation/subproject_06_10_validation.md`; `TST-TRC-005` retains SP-06.11 documentation/CSV evidence and `audit/validation/subproject_06_11_validation.md`; six optional rows retain the SP-06.11 deferral environment.

## Automated and independent validation

The semantic regression extension uses an explicit immutable mapping from all 21 executable test paths to their originating validation records. It parses every semicolon-separated evidence reference, resolves test nodes, supports multi-stage rows, requires exact appropriate environments, and separately enforces experiment, final-documentation, and optional provenance.

Before the CSV repair, the focused node failed as designed at `TST-DAT-003`, showing actual SP-06.2 versus required SP-06.7 provenance. After correction:

- focused verification-record node: 1/1 passed in 0.62s;
- complete documentation inspection module: 11/11 passed in 1.05s;
- historical inventory/resolver module: 2/2 passed in 0.47s;
- independent standard-library validator: exit 0; exact schema, 100 ordered unique rows, 94 passed/6 optional-deferred, all paths/nodes/environments, Git ancestry, special provenance, and identifying-path exclusions passed; it printed all 15 changes above;
- full suite: 976/976 passed in 4.10s with zero failures/skips/xfails;
- copied working-tree suite: 976/976 passed in 1.17s with zero failures/skips/xfails; copy removed;
- `python -m compileall -q src tests scripts`: exit 0;
- package, `Controller`/`load_startup_files`, and CLI `run` imports: exit 0.

## Scope, cleanup, and readiness

Final Git/cleanup validation confirmed only the verification CSV, documentation inspection, this repair record, and ledger changed. Production source, runner/configuration/results, README/reproducibility/test plan, inventory 94/6, traceability 60/6, historical SP-06.9 resolution, SP-06.11 baseline/stage/validation, baseline-flake repair, requirements/design/architecture/evidence, dependencies, and prior tests remained unchanged. No optional or Subproject-7 work was created.

Generated pytest/Python caches, copied trees, temporary validator output, orphan `.tmp`, and bytecode were removed. No repository-local environment or release artifact exists. No commit or push occurred.

READY FOR HUMAN REVIEW
