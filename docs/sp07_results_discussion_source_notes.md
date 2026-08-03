# SP-07 Results and Discussion Source Notes

This is evidence-led source material, not final report prose. It must not be copied without human technical review. All timing values are host-software observations.

## 1. Evidence and artifact status

Observation: all accepted manifest hashes, tables, and figures reconcile. Interpretation must follow `audit/validation/subproject_07_final_validation_ledger.csv` and `data/results/sp07_anomaly_register.csv`.

## 2. Accepted verification snapshot

Observation: the accepted SP-06 snapshot is 976 collected and 976 passed with pass rate 1.0; it is historical and not the current repository-wide count (`data/results/sp07_quantitative_summary_integrated.json`).

## 3. Correctness observations

Observation: the mixed workload processed 39000 requests with 15600 grants, 19500 denials, 3900 invalid-frame failures, and 0 other outcomes (`results/scalability_results.json`).
Observation: isolated lookup processed 12000 calls with 6000 correct hits, 6000 correct misses, and 0 mismatches; authorization processed 12000 calls with 4800 correct grants, 6000 correct denials, 1200 correct errors, and zero incorrect grants/denials/other mismatches (`data/results/sp07_isolated_operation_results.json`). Interpretation: these are deterministic constructed workloads, not a zero field error rate.

## 4. Mixed-controller timing observations

Observation: median repetition-level averages for 10/100/1000/10000 credentials are 7820.085, 7032.656, 7882.918, and 8189.5002 ns/request (`data/results/sp07_table_timing_summary.csv`). The 10000 group uses 10000 requests per repetition while smaller groups use 1000 (`results/scalability_results.json`). Interpretation: do not claim monotonic scaling or statistical significance.

## 5. Isolated lookup timing observations

Observation: median repetition-level lookup averages are 297.496, 278.224, 292.728, and 351.938 ns/lookup (`data/results/sp07_table_timing_summary.csv`). The 10000 group has greater observed spread; this requires cautious wording and is not proof of degradation. The public in-memory repository lookup is not a persistent-database query.

## 6. Isolated authorization timing observations

Observation: median repetition-level authorization averages are 590.139, 565.264, 616.682, and 614.437 ns/decision (`data/results/sp07_table_timing_summary.csv`). Interpretation: no monotonic or statistically significant trend is established.

## 7. Figure and table interpretation

Each timing median is a median of three repetition-level averages; whiskers are repetition-average minima/maxima, not pooled request percentiles (`data/results/sp07_table_timing_summary.csv`). Unlike operation families must not be ranked directly.

## 8. Anomalies and variability

Non-monotonicity and the larger 10000-credential lookup spread are observations, not diagnosed software defects (`data/results/sp07_anomaly_register.csv`).

## 9. Threats to validity

One host, three repetitions, absent raw samples, unequal mixed request counts, constructed workloads, and distinct operation boundaries limit inference (`data/results/sp07_anomaly_register.csv`).

## 10. Conclusions supported by evidence

Required software behavior was verified in the accepted snapshot; deterministic workloads reconcile; bounded host timings exist; tables and figures reproduce sources; no incorrect grant or denial occurred in the isolated workload (`audit/validation/subproject_07_final_validation_ledger.csv`).

## 11. Conclusions not supported

Constant-time, asymptotic complexity, persistent-database performance, population error rate, hardware, real-time, production readiness, reliability, safety, certification, and commercial equivalence are not supported (`audit/validation/subproject_07_final_validation_ledger.csv`).

## 12. Suggested report-safe wording

Suggested wording: “On the recorded host, three repetition-level aggregate observations were available for each size; these bounded software measurements show variability and do not establish a monotonic trend or hardware performance” (`data/results/sp07_table_timing_summary.csv`).

## 13. Table and figure insertion map

- `data/results/sp07_table_experiment_coverage.csv` — bounded evidence-coverage table.
- `data/results/sp07_table_correctness.csv` — deterministic correctness reconciliation.
- `data/results/sp07_table_timing_summary.csv` — repetition-level timing summary.
- `docs/figures/sp07_mixed_controller_average_ns.svg` — suggested caption: mixed Controller.submit host timing.
- `docs/figures/sp07_lookup_average_ns.svg` — suggested caption: direct repository lookup host timing.
- `docs/figures/sp07_authorization_average_ns.svg` — suggested caption: direct authorization host timing.

## 14. Subproject-8 handoff

Subproject 8 must preserve the final ledger and anomaly limitations, conduct human technical review, and treat these notes as source material rather than final prose.
