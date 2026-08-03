# SP-07.3 Stage Report — Integrated Quantitative Artifacts

## Outcome

SP-07.3 integrated the accepted mixed `Controller.submit` evidence and corrected direct-call isolated-operation evidence into a new versioned catalog, integrated summary, three report-ready tables, three deterministic accessible SVG figures, and a hash manifest. The accepted starting point was clean `main` at `7bd1a9b08bc2b4ebe99563821f128e7bfa64f29f`; the external environment was Python 3.13.13, pip 26.2, and pytest 9.1.1. The prescribed baseline passed 1077/1077 in 22.83s with zero failures, skips, and xfails.

## Source identity

The nine canonical source hashes are catalog `c9a8568d...f1cb`, historical summary `dc168fec...9cc0`, mixed config `93ec6808...1921`, mixed results `009381bf...c4f`, mixed environment `ed910911...e4ba`, isolated config `6668ba4...9838`, corrected isolated results `9d8edd07...0bdf`, isolated environment `106eba0f...7ec`, and timing-repair validation `1524a88d...ef90`. The generator requires canonical resolved paths and exact bytes, including when used from a copied repository; substituted or copied individual inputs fail.

The historical catalog and summary remain unchanged. Their EXP-05 remains a historical `gap_identified` record. The new integrated catalog updates only EXP-05 to `complete_existing_with_limit`, preserving its mapped IDs and mixed evidence while adding the corrected isolated config/result/environment and repair record. Its scope distinguishes mixed `Controller.submit`, direct repository lookup, and direct authorization; retains host/raw-sample/database/hardware/real-time/constant-time/asymptotic limitations; and assigns independent claim review to SP-07.4.

## Reconciliation and statistics

- Accepted SP-06 verification snapshot: 976 collected/passed, pass rate 1.0; explicitly not the current repository analysis-test count.
- Requirements/inventory: 60 required verified and six optional deferred; 94 implemented and six optional designed.
- Mixed controller: 12 repetition rows, 39000 processed, 15600 grants, 19500 denials (7800 unauthorized-floor, 5850 disabled, 5850 unknown), 3900 invalid-frame failures, zero other outcomes.
- Direct lookup: 12000 processed, 6000 correct hits, 6000 correct misses, zero mismatches.
- Direct authorization: 12000 processed, 4800 correct grants, 6000 correct denials, 1200 correct invalid-floor errors, zero incorrect grants, zero incorrect denials, zero other mismatches.

The timing table has exactly 12 rows: four separate rows each for mixed controller submit, credential repository lookup, and authorization decision, ordered by 10/100/1000/10000 credentials. Each row summarizes exactly three repetition aggregates using min/ordinary median/max for repetition average, repetition median, repetition nearest-rank p95, and throughput. No pooled request statistic, confidence interval, significance result, constant-time claim, asymptotic claim, or unlike-operation ranking is present.

## Figures and deterministic generation

The three separate 960x600 SVGs use categorical credential sizes and zero-based linear axes with deterministic nice ticks. Each plots 12 individual repetition-average square points, four median-of-repetition-average circular points connected by a dashed line, and four min/max whiskers. Accessible title/description linkage, units, sample semantics, operation boundary, and host-software limits are embedded. The files have no scripts, external resources, timestamp, host identity, raster content, or cross-family overlay.

The standard-library generator validates and builds all nine artifacts in memory, stages sibling temporary files, publishes with rollback, reparses published bytes, and emits one stable line. Two official generations exited 0 and produced byte-identical outputs. The manifest hashes the nine sources and eight other outputs, deliberately excluding its own recursively impossible hash.

Generated hashes:

| Artifact | SHA-256 |
|---|---|
| integrated catalog | `b86c084193ecf38cc70eb35bbac32a063266843bae724b3f4a58817d4a81db9a` |
| integrated summary | `95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c` |
| coverage table | `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f` |
| correctness table | `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224` |
| timing table | `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811` |
| mixed-controller SVG | `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930` |
| lookup SVG | `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096` |
| authorization SVG | `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9` |
| manifest | `f4fe7d5181310d731919dea350abefe13d2c753948d1d40aa90d9f00e14816b1` |

Independent standard-library validation passed all source/output hashes, schemas, ordering, aggregates, descriptive statistics, XML/accessibility fields, plotted values, axes, units, scope notes, and prohibited-content checks. Focused validation passed 26/26 in 0.72s, and the first full suite passed 1103/1103 in 23.28s, both with zero failures, skips, and xfails.

## Limits, deferrals, and readiness

These artifacts are bounded quantitative source material, not final report or discussion prose. Values are accepted host-software observations with different operation boundaries; raw per-call samples are unavailable. No database server, physical reader, electrical output, elevator movement, reliability, safety, certification, commercial controller, real-time, constant-time, or asymptotic result is established.

No benchmark was executed and no accepted measurement was changed. Production, runners, configs, accepted results/environments, historical SP-07.1 artifacts, prior audits, existing tests, plans, documentation, report, and presentation remain protected. SP-07.4 claim review and all Subproject-8 work remain deferred. There were no substantive deviations; cache removal used the environment-safe `find -delete` equivalent. No commit or push occurred.

READY FOR HUMAN REVIEW
