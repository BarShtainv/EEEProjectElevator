# SP-07.3 Baseline — Integrated Quantitative Artifacts

## Accepted state

- Repository: `BarShtainv/EEEProjectElevator`, branch `main`.
- Starting commit: `7bd1a9b08bc2b4ebe99563821f128e7bfa64f29f` (`Step_7.2R`).
- Initial `git status --short --untracked-files=all`: clean.
- Repository instructions: no `AGENTS.md` found.
- Environment: external `/home/bar/.venvs/eeeproject-elevator`; Python 3.13.13, pip 26.2, pytest 9.1.1.
- Cache cleanup removed only generated Python/pytest caches and bytecode.
- Baseline: `PYTHONPATH=src python -m pytest` collected 1077 and passed 1077 in 22.83s, with zero failures, skips, and xfails.

## Canonical inputs

| Path | SHA-256 |
|---|---|
| `data/results/sp07_experiment_catalog.csv` | `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb` |
| `data/results/sp07_quantitative_summary.json` | `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0` |
| `experiments/scalability_config.json` | `93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921` |
| `results/scalability_results.json` | `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f` |
| `results/scalability_environment.json` | `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba` |
| `experiments/isolated_operations_config.json` | `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838` |
| `data/results/sp07_isolated_operation_results.json` | `9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf` |
| `data/results/sp07_isolated_operation_environment.json` | `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec` |
| `audit/validation/subproject_07_02_timing_boundary_repair.md` | `1524a88db09641bd5f31a0411341d0e0e9b454ff2502ea99948fefc50879ef90` |

The SP-07.1 catalog and summary are historical, immutable inputs: EXP-05 remains `gap_identified` there. The accepted SP-07.2 result is the corrected direct-call artifact; its repair record marks the original wrapper-inclusive timing rows superseded.

## Scope and semantics

Authorized work is limited to the generator, new integrated catalog/summary/tables/manifest, three deterministic SVGs, one new focused test module, this baseline, new SP-07.3 stage/validation records, and an appended ledger section. All simulator source, runners, configurations, accepted results/environments, historical SP-07.1 outputs, existing tests, plans, requirements/design/traceability/verification, report, and presentation paths are protected.

Statistics summarize exactly three repetition-level aggregates per operation and size: minimum, ordinary median, and maximum for repetition average, repetition median, repetition nearest-rank p95, and throughput. They do not reconstruct pooled request statistics, confidence intervals, significance, constant-time behavior, or asymptotic guarantees.

Figures use categorical sizes, a zero-based linear y-axis, three repetition-average points, a median-of-repetition-average line, and min/max whiskers. Mixed `Controller.submit`, direct repository lookup, and direct authorization remain separate host-software figures with explicit boundaries and limitations.

SP-07.4 independent claim review and all Subproject-8 report, presentation, release, defense, rendered-PDF, and approval work remain deferred. No benchmark, commit, or push is authorized.
