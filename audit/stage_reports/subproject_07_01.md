# SP-07.1 Stage Report — Experiment Evidence Consolidation and Quantitative-Analysis Baseline

## Handoff and environment

SP-07.1 began from the accepted clean `main` commit `a07ec409e01606913d3f20eef99a8d884263a658`. Python 3.13.13, pip 26.2, and pytest 9.1.1 came from the accepted repository-external environment. The untouched baseline passed 976/976 in 4.60s with zero failures, skips, and xfails.

The seven canonical sources and their hashes are recorded in `audit/baselines/subproject_07_01_baseline.md` and embedded in `data/results/sp07_quantitative_summary.json`. The analyzer uses no third-party library, network, database, simulator import, benchmark subprocess, plotting, concurrency, sleep, or new dependency.

## Evidence consolidation

| Experiment | Classification | Existing evidence and bounded conclusion | Remaining limit or action |
|---|---|---|---|
| `EXP-01` Protocol validation | `complete_existing` | 13 mapped records cover logical source metadata, proposed 26-bit structure, parity, vectors, allocation, and corruptions. | Software profile only; no physical-reader or commercial-card claim. |
| `EXP-02` Authorization correctness | `complete_existing` | 11 mapped records cover repository identity, enabled/disabled/unknown precedence, floors 1-16, and mask authorization. | In-memory deterministic model only; timing isolation belongs to SP-07.2. |
| `EXP-03` Output timing | `complete_existing_with_limit` | 11 mapped records cover the one-output invariant, timeout boundaries, long output, and partition equivalence. | Values are simulated milliseconds, not electrical, host, or elevator timing. |
| `EXP-04` Watchdog and fault recovery | `complete_existing_with_limit` | 15 mapped records cover scheduling, suppression, collision, reset, data preservation, and injected logging-fault recovery. | Scenario verification is not a field failure rate, reliability result, or safety evidence. |
| `EXP-05` Database scalability | `gap_identified` | Five mapped experiment records and 12 accepted aggregates cover mixed `Controller.submit` host timing, outcomes, and throughput at four sizes. | Isolated credential lookup, isolated authorization, and an explicit expected-versus-actual matrix are assigned to SP-07.2. |
| `EXP-06` End-to-end scenarios | `complete_existing` | Eight mapped records cover LF/HF, denial, busy, invalid recovery, timeout, watchdog recovery, and state transitions. | Logical software flows only; no physical elevator journey. |
| `EXP-07` Robustness and malformed configuration | `complete_existing` | 16 mapped records cover malformed frames/configuration, strict UTF-8, invalid records, duplicates, and corrected-startup recovery. | Specified input boundary only; no broader field reliability or adversarial-security claim. |

Four experiments are complete from existing evidence, two are complete with explicit limits, and one has a bounded measurement gap.

## Quantitative baseline

The accepted source reconciles to 976/976 and pass rate 1.0; 60 required requirements verified and six optional deferred; 94 inventory entries implemented and six optional designed; 94 verification records passed and six optional deferred.

The 12 aggregate timing rows contain three repetitions at each of 10, 100, 1000, and 10000 credentials. Derived totals are 39000 processed, 15600 granted, 19500 denied, 7800 unauthorized-floor denials, 5850 disabled-credential denials, 5850 unknown-credential denials, 3900 invalid frames, and zero other outcomes.

For each size the summary calculates only minimum/median/maximum across the three repetition-level averages, repetition-level medians, repetition-level nearest-rank p95 values, and throughputs. It does not reconstruct raw samples or pooled percentiles. Host timing remains observational and variable.

Unavailable numeric metrics are JSON null: isolated lookup, isolated authorization, raw request samples, pooled request median/p95, independently measured incorrect grants/denials, branch coverage, physical-reader/electrical/elevator timing, field reliability, and safety/certification evidence.

## Deterministic generation and validation

The official command ran twice with identical completion lines and byte-identical outputs:

- catalog: seven rows, SHA-256 `511d0955fae5d501c0a4cb1caffaf64a8535a32cda366f0eea74b99da8916808`;
- summary: ordered schema-1 object, SHA-256 `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0`.

An independent standard-library command validated UTF-8, schemas/order, mapped IDs/references, source hashes, counts, totals, finite statistics, null unavailable values, bounded wording, relative paths, and the same hashes. Focused analysis validation passed 31/31. The first post-implementation full suite passed 1007/1007 in 18.09s; the final post-audit suite passed 1007/1007 in 17.91s, both with zero failures, skips, and xfails.

Two focused structural-test attempts each passed 30/31 before a test-only wording correction: substring checks falsely treated legitimate `total_processed_requests` and the accepted evidence filename `test_run_experiments.py` as execution dependencies. The final AST-based import boundary passed. An initial independent-validator wording check similarly treated a required negative real-time limitation as an affirmative claim; its negation-aware correction passed. None of these validation-test deviations changed the analyzer, outputs, simulator, or accepted evidence.

## Scope and next stages

Only the eight authorized SP-07.1 paths changed. Production behavior, accepted measurements, runner/configuration/results/environment, Subproject-6 tests and records, README/reproducibility, requirements/design/test plan, inventory, traceability, and final verification/provenance evidence remain protected. No benchmark, figure, report prose, raw timing dataset, optional feature, release, commit, or push occurred.

SP-07.2 remains responsible for the smallest missing isolated lookup/authorization experiment and explicit outcome classification. SP-07.3 and SP-07.4 remain responsible for figures/tables and independent results review/source notes. Subproject 8 was not started.

READY FOR HUMAN REVIEW
