# SP-07.2 Stage Report — Isolated Credential-Lookup and Authorization Experiment

## Starting point and objective

SP-07.2 began from clean `main` commit `415fc24cfbc64d224f95474bc9fc9017a2e9fb01` with Python 3.13.13, pip 26.2, and pytest 9.1.1 from the accepted external environment. The untouched baseline passed 1012/1012 in 22.14s with zero failures, skips, and xfails.

EXP-05 identified that the accepted mixed `Controller.submit` observations did not independently measure `CredentialRepository.lookup`, `authorize`, or expected-versus-actual correctness. This stage closes only that gap. The simulator and accepted mixed benchmark remain unchanged.

## Exact configuration and deterministic generation

- Configuration/workload/seed: `SP07_ISOLATED_OPERATIONS_V1`, `LOOKUP_AUTHORIZATION_MATRIX_V1`, 270516.
- Credential sizes: 10, 100, 1000, and 10000.
- Cases: 1000 per operation per repetition; one complete unmeasured warm-up and three measured repetitions.
- Record pools: exactly 60% enabled/all floors, 20% enabled/no floors, 20% disabled/all-floor mask. Thus the four sizes contain 6/2/2, 60/20/20, 600/200/200, and 6000/2000/2000 records.
- Lookup cases: exactly 500 hits and 500 facility-255 misses.
- Authorization cases: exactly 400 authorized, 200 unauthorized-floor, 150 disabled, 150 unknown, and 100 invalid-floor cases.

Three SHA-256-derived domain seeds isolate credential-category assignment, lookup ordering, and authorization ordering. Only local `random.Random` instances are used. Credentials are unique facility-1 records numbered 0 through size-minus-one, validated by `CredentialRepository.from_records`, and returned in ascending order. Cases and records are immutable and canonically checksummed without timing or host data. Same-size repetitions reuse identical sequences and checksums; all sizes have distinct credential and per-operation case checksums.

## Operation and timing boundaries

`credential_repository_lookup` times exactly `repository.lookup(key)`: method overhead, trusted-key validation, Python dictionary lookup, and `RepositoryLookup` construction. Repository construction, generation, checksums, classification, authorization, Wiegand, controller, and export are outside the interval.

`authorization_decision` times exactly `authorize(decoded, record, requested_floor)`: method overhead, trusted decoded/record validation, precedence/floor-mask logic, and `AuthorizationDecision` construction. Repository lookup, decoding, controller coordination, logging, output behavior, and export are outside the interval.

Each case uses `time.perf_counter_ns` immediately before and after exactly one operation. Classification/counting occur afterward. Elapsed samples must be nonnegative integers and total repetition duration positive. Timer overhead is retained; no sample is clamped, discarded, fabricated, or adjusted.

Metrics are arithmetic mean, standard median, nearest-rank p95 at `sorted_samples[ceil(0.95*n)-1]`, and `processed * 1_000_000_000 / sum(sample_ns)`. There is no performance threshold, constant-time claim, or asymptotic inference.

## Matrices and official results

The official command exited 0 in 0.186s operational context with four sizes, two operations, and 24 measured rows. Each row contains 1000 calls and a complete expected-versus-actual matrix.

- Lookup aggregate: 12000 processed; 6000 hits and 6000 misses; 12000 correct; zero mismatches.
- Authorization aggregate: 12000 processed; 4800 correct grants; 6000 correct denials (2400 unauthorized-floor, 1800 disabled, 1800 unknown); 1200 correct invalid-floor errors; zero incorrect grants, incorrect denials, other mismatches, or `other` outcomes.
- Combined: 24000 measured calls and zero mismatch rows.

All matrices are diagonal. Lookup authorization-specific count fields are null. Authorization rows explicitly distinguish correct grants/denials/errors from incorrect grants, incorrect denials, and other mismatches.

Tracked output hashes are:

- configuration: `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838`;
- results: `5739eaf829fabce8aa83f9c7905d23093f9853753afb8e15c411541c2b2c64a1`;
- environment: `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec`.

The environment ID is `env-5b6705a77f411683`. The result schema has seven ordered top-level fields and 24 rows with the exact 23 ordered fields. The environment has the exact 19 ordered fields, distinct operation definitions, and explicit software/host/timer/exclusion/variability/no-threshold/no-physical-claim limits. Neither artifact contains raw credentials, cases, decoded inputs, selected records, timing arrays, controller/event state, paths, username, or hostname.

## Reproduction and validation

The required temporary reproduction exited 0. Every deterministic result field, checksum, matrix/count, row order, and the environment ID matched the official artifacts; timing values were only required to be finite and positive. The temporary directory was removed.

An independent standard-library validator passed strict UTF-8, exact config/result/environment schemas, row order, matrices, aggregate totals, zero incorrect outcomes, finite metrics, integer p95, checksums, environment consistency/limits, and raw/identifying-data exclusions.

Focused tests passed 64/64 before output generation in 0.86s and 64/64 after tracked outputs existed in 0.79s. The first full post-implementation suite passed 1076/1076 in 22.06s. Compilation and package/repository/authorization imports passed. No implementation or validation deviation occurred.

## Limits, protection, and handoff

The results are observational Python-operation host timings on one recorded environment. They are not raw dictionary/database-server timings, persistent-database or commercial-controller results, real-time guarantees, or physical RFID/electrical/elevator/reliability/safety/certification evidence.

Only the nine authorized SP-07.2 paths changed. Production, the accepted mixed runner/config/results/environment, SP-07.1 analyzer/catalog/summary and audits, existing tests, requirements/design/traceability/verification, documentation, report/presentation, and dependencies remain protected.

SP-07.3 remains responsible for ingesting these artifacts into a new analysis and producing bounded tables/figures. SP-07.4 remains responsible for independent quantitative review and results/discussion source notes. Neither stage was started. No commit or push occurred.

The final post-audit full suite passed 1076/1076 in 22.26s with zero failures, skips, and xfails. Exact nine-path Git scope, accepted hashes, protected content, cleanup, and artifact-boundary checks passed.

READY FOR HUMAN REVIEW
