# SP-07.4 Stage Report — Independent Quantitative Claim Review

SP-07.4 began from clean `main` at `7b6ad373014e047ac454d11578f18a017d462057`, using Python 3.13.13, pip 26.2, and pytest 9.1.1. The prescribed baseline passed 1106/1106 in 24.13s with zero failures, skips, and xfails.

The independent reviewer uses only the standard library and does not import or execute an analysis generator, benchmark runner, or simulator. It validates 29 canonical source hashes, strict schemas/UTF-8/XML, the `SP07_REPORT_ARTIFACTS_V1` manifest's nine sources/eight generated entries, and relative/non-identifying paths.

Independent reconciliation confirmed the accepted historical 976/976 snapshot (pass rate 1.0), 60 required verified/six optional deferred, 94 implemented/six optional designed, and 94 passed/six deferred verification records. Mixed results reconcile to 12 rows, 39000 processed, 15600 grants, 19500 denials (7800/5850/5850), 3900 invalid frames, and zero other outcomes. Isolated results reconcile to 24000 calls: lookup 12000/6000 hits/6000 misses/zero mismatch and authorization 12000/4800 grants/6000 denials/1200 errors/zero incorrect grants, denials, or other mismatches.

All 12 timing rows independently match min/median/max across exactly three repetition aggregates. All three SVGs match every source point, median, and whisker and retain axes, units, accessibility, separate operation boundaries, and host limits. The manifest and all accepted artifacts remain unchanged.

The final ledger contains 39 unique claims: 39 `supported_with_limit`, zero unresolved, zero not supported, and zero blocking. The anomaly register contains 14 nonblocking entries: one information, two low, nine medium, and two high. They preserve non-monotonic variation, larger 10000-lookup spread, three repetitions, one host, absent raw/pooled/statistical evidence, unequal mixed request counts, distinct operation boundaries, constructed workloads, absent branch coverage, historical/current test-count distinction, and absent physical/real-time/safety/commercial evidence without labeling variation a defect.

Authorized conclusions are limited to accepted simulator verification, deterministic outcome reconciliation, bounded host-software timing availability, source-faithful tables/figures, and zero incorrect grants/denials within the isolated constructed workload. Constant-time/asymptotic, persistent database, physical/electrical/elevator, field reliability, production readiness, real-time, safety/certification, commercial equivalence, population error-rate, and statistical-significance conclusions are prohibited.

The source notes are evidence-led, non-final material with observation/interpretation separation, repository-relative citations, safe wording, six-artifact insertion map, and final-ledger/anomaly authorities. Subproject 8 must preserve limitations and obtain human technical review.

Two official generations were byte-identical. Output hashes are summary `7d48384b258c1cd033efe84aa6aba1fa65cd1f23621ed382fd1df4f0c38c9b92`, anomalies `0f997c8e10f53fa104718acb2823b25e134309f0dd7ad201bc87be447392f7c9`, ledger `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745`, and notes `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6`. Separate validation passed with 29 sources, 39 claims, 14 anomalies, 12 timing rows, three figures, and zero blockers.

Focused validation passed 26/26 in 1.88s after one recorded initial 22/23 run exposed and corrected raw missing-file propagation; the final expansion explicitly covers repair identity, handled CLI failure, and incomplete rollback recovery. The first full suite passed 1129/1129 in 24.18s; final validation passed 1132/1132 in 28.24s with zero failures, skips, and xfails. Compilation and imports passed. No benchmark, accepted artifact mutation, report/presentation, release, or Subproject-8 work occurred. No substantive deviation occurred beyond the narrow handled-error correction and correction of an independent-validator SVG class-name expectation before its passing rerun. No commit or push occurred.

`READY FOR HUMAN REVIEW`
