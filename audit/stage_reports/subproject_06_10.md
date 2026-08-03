# SP-06.10 Stage Report

## Handoff and outcome

SP-06.10 began from accepted SP-06.9 commit `a7ae9f0ec835150fd0b4a37809c93b2502b8d949`. Incomplete implementation commit `d3679748096ed39d8e72996e203d06b0a9e3590f` supplied the runner, official configuration, tests, aggregate outputs, environment output, and original baseline. Correction commit `1c746552f192302209fa7eb2e9bee34adbb30463` supplied the exact official-mix enforcement, direct regressions, and repair baseline. SP-06.10R2 completed execution evidence, inventory promotion, and audit records.

The R2 starting tree was clean. Python 3.13.13, pip 26.2, and pytest 9.1.1 came from `/home/bar/.venvs/eeeproject-elevator`. Its prescribed baseline passed 965/965 with no failures, skips, or xfails in 3.63 seconds. Final post-audit regression validation passed 965/965 with no failures, skips, or xfails in 3.16 seconds.

## Configuration and deterministic generation

The strict UTF-8 configuration uses schema 1, configuration `SP06_SCALABILITY_V1`, workload `MIXED_REQUESTS_V1`, seed 260516, credential sizes 10/100/1,000/10,000, minimum 1,000 requests, one warm-up, three measured repetitions, `PROJECT_WIEGAND_26`, 100 ms logical output duration, 2,000 ms watchdog timeout, and a disabled simulated watchdog. The exact official mix is 40% granted, 20% unauthorized floor, 15% disabled credential, 15% unknown credential, and 10% invalid frame.

The repair replaced the insufficient “all percentages positive” official check with an immutable exact 40/20/15/15/10 comparison. Direct tests reject positive total-100 substitutions 39/21/15/15/10 and 20/20/20/20/20 with the stable official-substitution error while preserving bounded non-official configuration support.

Each size uses domain-separated SHA-256-derived seeds for local `random.Random` instances. Credential keys are unique and ordered; enabled all-floor, enabled zero-mask, and disabled pools are nonempty. Requests are generated once per size as immutable values, deterministically shuffled, include LF and HF, use a collision-free unknown namespace, contain no busy category, and are regenerated rather than committed.

Canonical SHA-256 checksums are stable across all warm-up/measured repetitions of a size:

| Credentials | Credential checksum | Request checksum |
|---:|---|---|
| 10 | `e6b71173d03d5aa5a6529afb86f62a0db1c39057a8cfc208bc90ff06330beaee` | `93dbc8c1f8fe624fad47c9e8a13d02f814bd6a0166777923719fb35456ab30b8` |
| 100 | `2dbe74a204c5968756397ce3531a835f8f1a122e542048eb4ac8a1aba0077e3f` | `c08bf3b836778aede71c75ace428bc7de76fab0f31828cda40e8ff208313a0da` |
| 1,000 | `decf95c5b5002df2d80219c5b5a0adcad49c4956f9476ac7ad5c363649e1f87d` | `625b9c80bdf6c2fd1ce0a2b45d8692ca347dc2e4377070cf7c7b7ba6be740d76` |
| 10,000 | `2c859c5b59825058c02ac7d6ae98e05632d35318f08e1937317aa9ac85fb2b1d` | `c1ff8a6c7e6d63bfb50b323ee2d217ceddc7a2943927c88022464244f06eb55b` |

## Execution and metrics

Every size generates once, runs one complete unmeasured warm-up in a fresh graph, then runs measured repetitions 1, 2, and 3 in separate fresh graphs. Initialization precedes timing. Each sample brackets only `Controller.submit(request)` with `time.perf_counter_ns`. Grant output expiry advances simulated time outside the timed region; generation, checksums, controller construction, initialization, classification, cleanup, validation, environment capture, and export are excluded.

Per repetition, processed is the timed submission count; average is `statistics.fmean(samples)`; median uses standard median semantics; p95 is the observed sample at one-based `ceil(0.95*n)` without interpolation; throughput is `processed * 1_000_000_000 / sum(samples)`. There is no latency target or performance pass threshold.

The final fixed-path bounded temporary smoke ran 10 credentials, 100 requests, one warm-up, and one measured repetition. It exited 0 in 0.123 seconds operational wall context with 40 grants, 20 unauthorized, 15 disabled, 15 unknown, 10 invalid frames, and zero other outcomes. Metrics were finite/positive, p95 was an integer, environment output parsed, raw data was absent, and the temporary directory was removed.

The official command exited 0 in 0.691 seconds operational wall context and wrote 12 measured rows plus one environment record. For each repetition of sizes 10, 100, and 1,000, 1,000 processed requests reconcile to 400 grants, 200 unauthorized, 150 disabled, 150 unknown, 100 invalid frames, and zero other. For each 10,000-size repetition, 10,000 processed requests reconcile to 4,000 grants, 2,000 unauthorized, 1,500 disabled, 1,500 unknown, 1,000 invalid frames, and zero other. All metrics are finite/positive and all same-size checksums agree.

## Schemas, inventory, and boundaries

`results/scalability_results.json` contains only schema/configuration/workload/seed/timer metadata and the 12 documented aggregate rows. `results/scalability_environment.json` uses environment ID `env-ffbfdbefc2f5ed62` and bounded non-secret Python/platform/configuration metadata plus explicit limitations. Strict UTF-8, JSON schemas, IDs, row counts, repetitions, outcomes, equations, metrics, checksums, environment references, and raw-data exclusions passed standalone validation.

After all execution gates, only the status cells for `TST-REP-001`, `TST-REP-002`, and `TST-SCL-001` through `TST-SCL-003` changed from `designed` to `implemented`. The inventory is 93 implemented and seven designed; `TST-TRC-005` plus six optional rows remain designed. All 100 IDs remain unique, and historical SP-06.9 resolution evidence is unchanged.

## Deviation and correction

The first promoted-inventory regression produced 964 passes and one failure because the SP-06.9 inspection permanently required historically scheduled SP-06.10 rows to remain live-status `designed`. R2 allowed correction after executed evidence exposed a genuine test defect. The smallest change permits SP-06.10-owned historical scheduled rows to be designed or implemented while still requiring the SP-06.11 row to remain designed. Targeted inspection then passed 2/2 and complete regression passed 965/965. This narrow stale-assertion correction was the only R2 deviation from the evidence/inventory/audit-only path set.

Measurements describe one Python software model on the recorded host. They are observational, may vary by host/run, are not real-time guarantees, do not measure RFID hardware, electrical outputs, elevator motion or safety, and establish no reliability or commercial-controller equivalence. No production source, runner behavior during R2, official configuration, requirements/design/traceability, prior audit, dependency, optional feature, or SP-06.11 documentation was changed. No optimization, caching, concurrency, database, network, GUI, or hardware behavior was added. No commit or push occurred.

READY FOR HUMAN REVIEW
