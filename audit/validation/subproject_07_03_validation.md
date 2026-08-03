# SP-07.3 Validation — Integrated Quantitative Artifacts

## Gate and baseline

| Command/gate | Exact result |
|---|---|
| repository identity/history/status | Correct root and `BarShtainv/EEEProjectElevator`; clean `main`; exact `7bd1a9b08bc2b4ebe99563821f128e7bfa64f29f`; accepted history |
| instructions and mandated inspection | No `AGENTS.md`; project plan, analyzers, both configurations/results/environments, historical catalog/summary, SP-07.1/R and SP-07.2/R validations, and analysis/inspection tests inspected |
| versions | Python 3.13.13; pip 26.2; pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator` |
| bounded cleanup | Removed only Python/pytest caches and bytecode using the command runner's narrow `find -delete` equivalent |
| baseline | `PYTHONPATH=src python -m pytest`: 1077 collected/passed in 22.83s; zero failed/skipped/xfailed |

The nine exact canonical source hashes are recorded in `audit/baselines/subproject_07_03_baseline.md`. Strict validation confirmed the historical 7-row/9-column catalog and EXP-05 gap, historical schema-1 summary and 976/60/6/94/6 snapshot, mixed schema/identity/12 rows/39000 requests/checksums/host limits, isolated identity/direct timer/24 rows/diagonal matrices/24000 calls/checksums/environment, and repair record's corrected hash plus superseded timing identity.

## Implementation and focused validation

`analysis/generate_figures.py` imports only the standard library and has no benchmark-runner, production-simulator, network, database, plotting, subprocess, thread, async, multiprocessing, or sleep execution path. It provides strict UTF-8/JSON/CSV/path/hash/source validation, source reconciliation, repetition statistics, integrated object/table/SVG/manifest construction, deterministic serialization, nine-file staging/rollback, post-write parsing, required argparse CLI, and stable handled errors.

An in-memory smoke build after compilation produced nine artifacts with expected structures; it wrote no official output and executed no benchmark. The focused command `PYTHONPATH=src python -m pytest tests/analysis/test_generate_figures.py -v` collected and passed 26/26 in 0.72s with zero failures/skips/xfails. Cases cover all requested input corruptions and substitutions, integrated catalog/summary/tables, exact source-derived statistics, three SVG contracts and plotted values, two-build/two-directory determinism, manifest hashes, successful and injected-failure publication, stable CLI behavior, all-required argparse options, and AST boundaries.

## Official double generation

The exact prescribed 18-option command was run twice after focused tests. Each exited 0 and printed:

`completed: experiments=7 timing_groups=3 timing_rows=12 svg_figures=3 manifest_artifacts=8`

Both runs produced byte-identical outputs:

| Output | SHA-256 |
|---|---|
| `data/results/sp07_experiment_catalog_integrated.csv` | `b86c084193ecf38cc70eb35bbac32a063266843bae724b3f4a58817d4a81db9a` |
| `data/results/sp07_quantitative_summary_integrated.json` | `95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c` |
| `data/results/sp07_table_experiment_coverage.csv` | `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f` |
| `data/results/sp07_table_correctness.csv` | `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224` |
| `data/results/sp07_table_timing_summary.csv` | `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811` |
| `docs/figures/sp07_mixed_controller_average_ns.svg` | `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930` |
| `docs/figures/sp07_lookup_average_ns.svg` | `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096` |
| `docs/figures/sp07_authorization_average_ns.svg` | `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9` |
| `data/results/sp07_report_artifact_manifest.json` | `f4fe7d5181310d731919dea350abefe13d2c753948d1d40aa90d9f00e14816b1` |

The manifest uses `SP07_REPORT_ARTIFACTS_V1`, records all nine source hashes and hashes all eight other generated artifacts, and states the deterministic/no-benchmark/no-edit/three-repetition/no-pooled-percentile contract. It omits its own hash to avoid recursion.

## Content and independent validation

- Integrated catalog: exact historical schema/order, six rows semantically identical, EXP-05 `complete_existing_with_limit`, mixed and isolated evidence, bounded next action.
- Integrated summary: exact 14-field order and `SP07_ANALYSIS_INTEGRATED_V1`; exact accepted verification/requirements/inventory/mixed/isolated/correctness identities and availability/null semantics.
- Coverage table: seven exact rows and repository-relative references.
- Correctness table: 22 ordered calculated rows, including exact 976 snapshot, mixed 39000/15600/19500/7800/5850/5850/3900/0, lookup 12000/6000/6000/0, and authorization 12000/4800/6000/1200/0/0/0.
- Timing table: 12 ordered source-derived rows; exactly three repetition aggregates per row; mixed calls 1000/1000/1000/10000 and isolated calls 1000; min/median/max repetition average, median, nearest-rank p95, and throughput.
- SVGs: strict UTF-8 valid XML/SVG namespace, 960x600, title/description/ARIA, white background, axes/units/four sizes, zero-based linear nice ticks, 12 repetition points, four median points, four whiskers, correct source values, explicit operation/sample/host scope, no script/external/identifying content.

The independent command did not import the generator and printed `INDEPENDENT_VALIDATION=PASS sources=9 catalog=7 correctness=22 timing=12 svg=3 manifest=8 mixed=39000 isolated=24000`. It independently recalculated hashes, counts, every timing statistic, and plotted source values.

First post-implementation full suite: 1103/1103 passed in 23.28s; zero failures/skips/xfails.

## Final commands and scope

| Check | Exact result |
|---|---|
| final focused suite | 26/26 passed in 0.70s; zero failures/skips/xfails |
| final full suite | 1103 collected/passed in 22.89s; zero failures/skips/xfails |
| compilation/imports | `python -m compileall -q src tests scripts analysis`, `import elevator_access_sim`, and `from elevator_access_sim import Controller` all exited 0 |
| independent/hash rerun | Passed 9 sources, 7 catalog rows, 22 correctness rows, 12 timing rows, 3 SVGs, 8 manifest entries, statistics, and deterministic hashes; all nine output hashes unchanged |
| Git/cleanup/protected paths | `git diff --check` passed; exact `main` and accepted HEAD; exactly 15 authorized paths; all nine canonical hashes unchanged; caches, bytecode, `.tmp` files, local environments, raw collections, raster/report/release additions absent |

Neither benchmark runner was executed. No accepted source measurement, matrix, checksum, environment, simulator, runner, config, historical SP-07.1 output, existing test, report, presentation, SP-07.4, Subproject-8, or release artifact changed. No repository-local environment, raw sample/request/credential collection, raster artifact, commit, or push was created.

READY FOR HUMAN REVIEW
