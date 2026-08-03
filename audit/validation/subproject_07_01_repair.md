# SP-07.1R Validation — Catalog Evidence and Canonical-Source Integrity Repair

## Accepted start and baseline

- Repository/branch/commit: `BarShtainv/EEEProjectElevator`, `main`, `1bf26f841d5c3fe35656649da835f3b59f9d310e` (`Step_7.1`).
- Initial status: clean; no conflicting user change and no repository instruction file.
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from the accepted repository-external environment. No install or network access occurred.
- Generated caches were removed before the baseline without deleting tracked or user-created files.
- Baseline `PYTHONPATH=src python -m pytest`: 1007 collected/passed in 18.89s; zero failures, skips, and xfails.
- The accepted SP-07.1 baseline, stage report, and validation record remain unchanged as historical evidence.

## Defects and corrections

### EXP-07 evidence sufficiency

The accepted catalog classified EXP-07 `complete_existing` and claimed strict-UTF-8 startup-file rejection and corrected startup recovery, but the row derived evidence only from mapped verification records and lacked the direct executable nodes for those claims.

The internal EXP-07 definition now declares and catalog construction appends, resolves, and first-occurrence de-duplicates these mandatory references in order:

1. `tests/unit/test_config_files.py::test_configuration_file_failures_keep_configuration_identity`;
2. `tests/unit/test_config_files.py::test_credential_file_failures_keep_credential_identity`;
3. `tests/unit/test_controller_initialization.py::test_corrected_initialization_after_failure_clears_error_event`;
4. `audit/validation/subproject_06_08_validation.md`;
5. `audit/validation/subproject_06_07_validation.md`.

The first two nodes contain the direct strict-UTF-8 configuration/credential startup-file rejection cases; the third contains corrected initialization following startup failure. The validation reports remain evidence context, not quantitative measurements. No optional inventory ID or verification record changed.

`validate_experiment_evidence` independently requires the three direct nodes before EXP-07 may remain `complete_existing`. Its negative regression first confirms every remaining reference resolves, removes one required direct node from a constructed row, and then proves semantic sufficiency fails with `EXP-07 mandatory direct evidence is missing`.

### Canonical source identity

The accepted CLI could parse a caller-selected substitute while writing the fixed canonical label into `source_artifacts`. This allowed a label and hashed source identity to diverge even when the substitute was byte-identical or structurally valid.

`validate_canonical_source_paths` now resolves each of the seven CLI input paths and requires equality with `ROOT / CANONICAL_SOURCES[index]` before parsing, analysis construction, or output publication. It uses repository-derived paths only. Relative canonical paths from the repository root and absolute canonical paths pass; output paths remain unrestricted. A byte-identical inventory copy and a semantically valid alternate final-validation file both fail with a stable message containing `canonical source path`. Lower-level parsers and `build_analysis` remain usable with temporary corruption fixtures.

The CLI substitute test returns 1, emits exactly one `error: ` line without traceback, and preserves both pre-existing outputs. The label/hash regression proves every recorded source label resolves to the same canonical file supplied to the CLI and hashes those bytes.

## Tests, regeneration, and independent validation

| Command or gate | Exact result |
|---|---|
| focused `PYTHONPATH=src python -m pytest tests/analysis/test_analyze_results.py -v` | 36/36 passed in 17.86s; zero failures/skips/xfails. |
| official generation, first run | Exit 0; seven experiments, 12 measured rows, 39000 processed; hashes below. |
| official generation, second run | Exit 0 with the identical completion line and hashes. |
| byte comparison | Catalog and summary were byte-identical across both repair runs. |
| accepted-source SHA-256 check | All seven canonical source hashes passed unchanged. |
| accepted scalability Git check | Configuration, results, and environment unchanged. |
| independent standard-library validator | `INDEPENDENT_VALIDATION=PASS catalog_rows=7 exp07_required=3 sources=7 processed=39000`. |
| excluded copied-repository official CLI | Exit 0 from the copied root with the same catalog/summary hashes; the copied analyzer accepted its own canonical sources and the copy was removed. |
| first repaired full suite | 1012/1012 passed in 21.90s; zero failures/skips/xfails. |
| `python -m compileall -q src tests scripts analysis` | Exit 0 with no diagnostics. |
| required package and `Controller` imports | Both exited 0. |

Output hashes before and after repair:

| Output | Before | After |
|---|---|---|
| `data/results/sp07_experiment_catalog.csv` | `511d0955fae5d501c0a4cb1caffaf64a8535a32cda366f0eea74b99da8916808` | `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb` |
| `data/results/sp07_quantitative_summary.json` | `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0` | `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0` |

The catalog changed only because EXP-07 gained direct/context evidence. The quantitative summary legitimately remained byte-identical: mapped IDs, experiment status, source hashes, counts, totals, statistics, limitations, and deferred work did not change.

The independent validator confirmed exact catalog schema/order, all three mandatory nodes, SP-06.7/SP-06.8 records, every path and pytest node, seven canonical labels and hashes, 39000 processed/15600 granted/19500 denied/3900 invalid/zero other, finite per-size aggregates, null unavailable metrics, bounded claims, and deterministic hashes.

## Final scope, cleanup, and readiness

- Final post-audit `PYTHONPATH=src python -m pytest`: 1012 collected/passed in 21.51s; zero failures, skips, and xfails.
- Final Git/scope/cleanup: exact `main`/accepted HEAD; exactly five changed paths; `git diff --check` passed; all protected paths, seven accepted source hashes, accepted scalability artifacts, historical SP-07.1 records, and the quantitative summary remained unchanged; caches, bytecode, temporary files, repository-local environments, unexpected result files, raw datasets, figures, and release artifacts were absent.
- Accepted measurements, simulator behavior, production source, Subproject-6 tests, scalability inputs/results/environment, verification records, inventory, traceability, README/reproducibility/test plan, and prior baseline/stage/validation records remain unchanged.
- No benchmark, raw timing dataset, figure, report, presentation, release, optional behavior, or SP-07.2 work was created.
- No commit or push occurred.

READY FOR HUMAN REVIEW
