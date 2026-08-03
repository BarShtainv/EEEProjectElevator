# SP-07.2R Validation — Direct-Call Timing-Boundary Repair

## Accepted state and baseline

| Gate | Exact result |
|---|---|
| Repository | `BarShtainv/EEEProjectElevator`, root `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`, branch `main` |
| Starting commit | Exact accepted `6caffb8b2fcd55a89d5421409e147ade2aa14afe`; recent history inspected; initial status clean |
| Instructions and environment | No repository `AGENTS.md`; external `/home/bar/.venvs/eeeproject-elevator` available; no install or network access |
| Versions | Python 3.13.13; pip 26.2; pytest 9.1.1 |
| Cache cleanup | Removed only generated Python/pytest caches and bytecode before the baseline |
| Baseline | `PYTHONPATH=src python -m pytest`: 1076 collected, 1076 passed in 22.78s; zero failures, skips, and xfails |

Accepted hashes were runner `5acf3d2ef163a44b1157866108eb475f5c93029f36357c566474a049907631ee`, focused tests `8df4cedd773c0b1e1c682c1391fc881bf3817e3d5323fb26d26c82812ce0c5e1`, configuration `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838`, result `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1`, and environment `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec`. The existing SP-07.2 baseline, stage report, and validation report remain unchanged historical records of the superseded timing run.

## Defect and correction

The former measured region called `_timer_sample(timer, lambda: target(...))`. `_timer_sample` read the timer, invoked the lambda, and read the timer again, so the published interval included an extra Python callable-wrapper invocation even though the environment document described only `CredentialRepository.lookup` or `authorize` as timed.

`_timer_sample` was deleted and replaced by `elapsed_nanoseconds(start, end)`, which only validates already-captured nondecreasing integer timer values. The repaired loops now use these direct boundaries:

- lookup: bind `key`; timer; direct `repository.lookup(key)`; timer; elapsed validation; lookup classification;
- authorization: bind `decoded`, `record`, and `requested_floor`; timer; direct `authorize(decoded, record, requested_floor)`; timer; elapsed validation; authorization classification.

Repository construction, tuple conversion, case validation and field extraction, classification, count updates, checksum work, metric calculation, and output construction remain outside the intervals. No timer-overhead subtraction, operation optimization, metric/schema change, or production-source change was made.

## Regression and pre-publication validation

The new AST regression proves both repetition functions contain no lambda or `_timer_sample` executor; finds the direct public operation assignment between consecutive `timer()` assignments; verifies classification follows the second timer read; verifies lookup repository construction precedes its case loop; and verifies all authorization arguments are bound before timing. The retained behavioral test observed exactly `repository construction, timer, lookup, timer, classify` and `timer, authorize, timer, classify`. Existing fake-timer tests retained exact elapsed, average, median, nearest-rank p95, throughput, count, and 24-row checks.

| Command | Exact result |
|---|---|
| Focused suite before publication | 65/65 passed in 0.89s; zero failures/skips/xfails |
| First full suite before publication | 1077/1077 passed in 22.35s; zero failures/skips/xfails |

Before replacement, the tracked result, all credential and case checksums, operation/size/repetition order, expected and actual outcomes, complete matrices, correctness/mismatch counts, and environment ID were captured. Its non-timing projection SHA-256 was `b9c782213e331cc5de0062af8276f22a91cddc6e0dd61acd79f5eac0f006d633`, and its environment ID was `env-5b6705a77f411683`.

## Corrected official run and deterministic identity

The corrected tracked command was executed exactly once:

`PYTHONPATH=src python analysis/run_experiments.py --config experiments/isolated_operations_config.json --results data/results/sp07_isolated_operation_results.json --environment data/results/sp07_isolated_operation_environment.json`

It exited 0 in 0.20s operational context and printed `completed: sizes=4 operations=2 measured_rows=24 timer=time.perf_counter_ns`. It was not rerun to seek preferred timing and measurements were not manually edited.

- old result SHA-256: `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1`;
- corrected result SHA-256: `9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf`;
- environment SHA-256: unchanged at `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec`;
- configuration SHA-256: unchanged at `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838`;
- before/after non-timing projection SHA-256: identical at `b9c782213e331cc5de0062af8276f22a91cddc6e0dd61acd79f5eac0f006d633`.

The comparison found changes only in `average_ns`, `median_ns`, `p95_ns`, and `throughput_cases_per_second`; 95 timing values differed. Every configuration/workload identifier, row/order field, checksum, outcome, matrix, correctness count, and environment ID remained identical. The unchanged environment bytes continue to state the correct direct-operation boundaries.

The original timing rows are superseded by the corrected run. No old/new performance comparison or improvement inference is valid because the measurement boundaries differ.

## Reproduction and independent validation

One temporary repaired run exited 0 with 24 rows. Its schema, order, operations, sizes, repetitions, checksums, outcomes, matrices, correctness counts, and environment were identical to the corrected tracked documents; all timing metrics were finite and positive. Timing equality was not required. The temporary directory was removed.

A separate standard-library validator passed strict UTF-8, exact 24-row schema/order, pre-repair non-timing equality, configuration and environment identity, finite positive metrics, integer p95, absent raw inputs/samples, direct-operation environment definitions, and protected SP-06/SP-07.1 scope. Aggregate reconciliation was:

- lookup: 12000 processed, 6000 hits, 6000 misses, zero mismatches;
- authorization: 12000 processed, 4800 correct grants, 6000 correct denials, 1200 correct errors, zero incorrect grants, zero incorrect denials, zero other mismatches, and zero total mismatches;
- combined: 24000 measured direct target calls in 24 rows of 1000 calls.

## Final validation and scope

| Check | Exact result |
|---|---|
| Final focused suite | 65/65 passed in 0.81s; zero failures/skips/xfails |
| Final full suite | 1077 collected, 1077 passed in 22.56s; zero failures/skips/xfails |
| Compilation and imports | `python -m compileall -q src tests scripts analysis` and imports of `elevator_access_sim`, `CredentialRepository`, and `authorize` all exited 0 |
| Independent and non-timing reruns | Both passed; 24 rows, 24000 aggregate operations, zero mismatches, direct-boundary environment, protected scope, and identical `b9c782...` non-timing projection reconfirmed |
| Git, protected scope, and cleanup | `git diff --check` passed; exact `main` and accepted HEAD retained; exactly five authorized paths changed/created; caches, bytecode, orphan `.tmp` files, temporary reproduction/comparison files, and repository-local environments absent |

No simulator source, accepted mixed-controller result, SP-07.1 artifact, configuration, dependency, figure, report, release artifact, or prior audit record was changed. SP-07.3 and SP-07.4 were not started. No commit or push occurred.

READY FOR HUMAN REVIEW
