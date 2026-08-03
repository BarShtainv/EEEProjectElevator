# SP-07.2 Validation — Isolated Credential Lookup and Authorization

## Starting gate and baseline

| Command or gate | Exact result |
|---|---|
| root/name/remote/branch/HEAD/history/status | Correct `EEEProjectElevator` / `BarShtainv/EEEProjectElevator`; `main`; exact `415fc24cfbc64d224f95474bc9fc9017a2e9fb01`; accepted history; clean status. |
| instructions and required-artifact inspection | No repository instruction file; all prescribed SP-07.1/R, mixed benchmark, production interface, plan, result, and test artifacts present. |
| EXP-05 inspection | `gap_identified` for isolated lookup/authorization and explicit expected-versus-actual matrix. |
| Python/pip/pytest | Python 3.13.13; pip 26.2; pytest 9.1.1 from the accepted external environment. |
| bounded cache cleanup | Removed only generated pytest/Python caches and bytecode. |
| baseline `PYTHONPATH=src python -m pytest` | 1012/1012 passed in 22.14s; zero failures/skips/xfails. |

Accepted hashes at the gate were catalog `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb`, summary `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0`, mixed config `93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921`, mixed results `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f`, and mixed environment `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba`.

## Focused validation matrix

The first and post-output focused commands collected 64 cases. They validate:

- exact official parsing plus malformed UTF-8/JSON, duplicate members, wrong root, missing/unknown fields, Boolean integers, schema/ID/workload/seed/size/count/repetition substitutions, reordered/duplicate sizes, category defects, integer/positive/total/exact-percentage defects, and no defaults;
- four exact unique ascending record sets and 60/20/20 pools, repository validation, deterministic regeneration/checksums, seed sensitivity, local random-state isolation, and facility-255 miss separation;
- four exact 500/500 immutable deterministic lookup schedules whose hits resolve and misses do not;
- four exact 400/200/150/150/100 immutable authorization schedules producing the required public result/reason, valid/invalid floors, and `record=None` unknown cases;
- exact diagonal matrices, correct grant/denial/error counts, and injected incorrect-grant, incorrect-denial, and other-mismatch classification with no discarded mismatch;
- nearest-rank p95 for 1/2/20/100/duplicate/unsorted samples and rejection of empty/Boolean/negative/noninteger values;
- exact fake-timer elapsed values, mean, median, p95, throughput, processed and outcome counts;
- repository construction/classification outside lookup timing and classification outside authorization timing; one public target operation between timer reads; 24 measured rows and no warm-up row;
- exact result/environment schemas, order, matrices, finite metrics, checksum/environment consistency, no raw/identifying data;
- successful two-file publication, injected second-replacement rollback, temporary cleanup, handled CLI error/output preservation, argparse exit 2/all arguments required;
- AST-only standard-library/accepted-simulator imports and no controller, Wiegand, mixed-runner, network, database server, plotting, thread, async, multiprocessing, subprocess, sleep, or external package.

Results:

| Focused command | Exact result |
|---|---|
| before official output | 64/64 passed in 0.86s; zero failures/skips/xfails. |
| after official output | 64/64 passed in 0.79s; zero failures/skips/xfails. |

## Official command and reproduction

The official command was executed once:

`PYTHONPATH=src python analysis/run_experiments.py --config experiments/isolated_operations_config.json --results data/results/sp07_isolated_operation_results.json --environment data/results/sp07_isolated_operation_environment.json`

It exited 0 in 0.186s operational context and printed `completed: sizes=4 operations=2 measured_rows=24 timer=time.perf_counter_ns`. No selective rerun or metric edit occurred.

The temporary reproduction used the same config and temporary destinations. It exited 0; all 24 deterministic row fields/checksums/matrices/counts and the environment `env-5b6705a77f411683` matched. Both runs had finite positive timing metrics; timing equality was not required. The temporary directory was removed without overwriting accepted output.

## Row and aggregate reconciliation

All 24 rows are ordered as 12 lookup rows then 12 authorization rows, each by 10/100/1000/10000 and repetitions 1/2/3. Each processed exactly 1000 operations with finite positive average/median/throughput and observed integer nearest-rank p95.

- Lookup: 12000 processed, 6000 hits, 6000 misses, 12000 correct, zero mismatches. Every 2x2 matrix is complete and diagonal; authorization fields are null.
- Authorization: 12000 processed, 4800 correct grants, 6000 correct denials (2400 unauthorized floor, 1800 disabled, 1800 unknown), 1200 correct errors, zero incorrect grants, zero incorrect denials, zero other mismatches, and zero actual `other`.
- Combined: 24000 measured operations and zero mismatch rows.

Same-size credential checksums are identical across both operations and repetitions. Same-size per-operation case checksums are identical across repetitions. Credential and case checksums differ across sizes.

## Independent, structural, and final validation

The separate standard-library validator printed `INDEPENDENT_VALIDATION=PASS rows=24 lookup=12000 authorization=12000 mismatches=0` and confirmed strict UTF-8, exact configuration/schemas/order, diagonal matrices, aggregates, finite metrics, integer p95, checksums, environment consistency/limits, and absence of raw or identifying content.

Tracked hashes:

- config `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838`;
- results `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1`;
- environment `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec`.

The first complete post-implementation suite passed 1076/1076 in 22.06s with zero failures, skips, or xfails. `python -m compileall -q src tests scripts analysis` and imports of `elevator_access_sim`, `CredentialRepository`, and `authorize` exited 0.

## Final scope and readiness

- Final post-audit `PYTHONPATH=src python -m pytest`: 1076 collected/passed in 22.26s; zero failures, skips, and xfails.
- Git/cleanup/protected result: exact `main`/accepted HEAD and nine authorized paths; `git diff --check` passed; production, accepted mixed artifacts, SP-07.1 artifacts/audits, existing tests, documentation, and all protected hashes remained unchanged; caches, bytecode, temporaries, repository-local environments, raw generated collections/cases/timing files, unexpected result files, plots, and release artifacts were absent.
- Accepted production, mixed benchmark, SP-07.1 catalog/summary/analyzer/audits, existing tests, requirements/traceability/verification/documentation, and dependencies did not change.
- No raw credentials/cases/timing arrays, figure, plot, report, release, SP-07.3, or SP-07.4 artifact exists.
- No commit or push occurred.

READY FOR HUMAN REVIEW
