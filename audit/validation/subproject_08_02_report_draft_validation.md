# SP-08.2D Report-Draft Validation

## Environment and baseline

- Repository: `BarShtainv/EEEProjectElevator`; branch `main`; starting commit `87004b22f49fd4c0c481f8a3128b663bb8f7fc83`.
- Environment: Python 3.13.13; pip 26.2; pytest 9.1.1.
- Initial tree: clean; tracked Python/pytest cache artifacts: zero.
- Baseline command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -p no:cacheprovider`.
- Baseline result: 1,176 collected and 1,176 passed in 25.61 seconds (25.83 seconds measured wall time); zero failed, skipped, or xfailed.
- Drafting authorization: affirmative; six of six gate groups resolved; exact terminal line present; frozen drafting snapshot SHA-256 `947437b0d8ba64776cf789a03acab1b6d7fe6b4e44b42fb0f157d8e9eaed5863`.

## Protected inputs

The following principal protected hashes were captured before drafting and reconciled after implementation:

| Input | SHA-256 |
|---|---|
| Drafting authorization | `9e068de045547c64cc57c238f44fabd48c67b6d098a7b7459dffa0d9f1f7b1fa` |
| Supervisor authorization | `c88e229ac3c02c28bbc288342cc9409e1be18c79dd1cbc98d9b08325d9f80b53` |
| Report outline | `cece1ff5aed996350c4a2f2ba45dff59b7b2d1020b61dd6c108080476b5e05d0` |
| Claim/source matrix | `ca2cc6a0c0cb9b8158e62cae0dcb45b0dc1c9f8373cc5fac461f01aaeec9b5be` |
| Asset register | `72f8b90a37bc47df3cc235e0807a847e8e3e68f9ec23310fb0c4b29aea4a4285` |
| Bibliography readiness | `53f01e1dd8010c7df713dcc029bc6ba1d6774902c6edaefd524adf87d7eeeffc` |
| `references.bib` | `65ef36178bda47d965a650e1a7d9c37575162c703e935066dafcee555617e307` |

Accepted SP-07 coverage, correctness, timing, anomaly, independent-review, integrated-summary, manifest, and three SVG hashes matched the baseline table in `audit/baselines/subproject_08_02_report_draft_baseline.md`.

## Draft inspections

- Report word count: 6,707 by `wc -w`.
- Main sections: exactly 15 in the required order.
- Citations/references: eight numeric citations and eight matching IEEE-style references; first-use numbering contiguous 1–8; every entry cited.
- Traceability: exact eight-column schema; 15 rows in report order; 40 distinct canonical source paths resolved.
- RPT reconciliation: all 27 accepted RPT IDs mapped; no invented ID; unknown-only and not-for-report material appears only as an unknown or explicit limitation.
- Citation-key reconciliation: every traceability key exists in `report/references.bib`; the internal workflow-handbook record is not promoted into the external reference list.
- Asset reconciliation: all used asset IDs registered; accepted tables and figures byte-identical; seven Mermaid sources deferred; no product image.
- Quantitative cross-check: requirement 66/60/6 totals, 39,000 mixed outcomes, denial reasons, 24,000 isolated outcomes, 12 timing rows, four sizes, exactly three repetitions, one-host scope, and `time.perf_counter_ns` semantics matched accepted artifacts.
- Privacy scan: no identifier-like nine-digit value in the new report, traceability, test, or baseline paths.
- Forbidden-claim scan: passed for unsupported commercial attribution, physical validation, safety certification, statistical significance, constant-time/asymptotic behavior, and hardware-performance conclusions.
- Forbidden outputs: no report DOCX/PDF, presentation, product image, new Mermaid export, archive, or release.

## Executed validation

1. New report inspection: 22 passed in 0.31 seconds after correcting the submission-date label to the exact authorized plain-text marker.
2. Mandated focused suite: 61 passed in 1.26 seconds (1.46 seconds measured wall time); zero failed, skipped, or xfailed.
3. First full suite: 1,198 passed in 27.28 seconds (27.48 seconds measured wall time); zero failed, skipped, or xfailed.
4. Independent validator: passed with the concise result `INDEPENDENT REPORT VALIDATOR PASSED: 15 sections, 15 trace rows, 8 citations/references, 27 RPT claims, protected inputs intact.`
5. Compilation/imports: `compileall` passed using an isolated `/tmp/eeeproject-sp08d-pycache.*` directory; `import elevator_access_sim` and `from elevator_access_sim import Controller` both passed; the temporary directory was removed.
6. Final focused suite: 61 passed in 0.97 seconds (1.26 seconds measured wall time); zero failed, skipped, or xfailed.
7. Final full suite: 1,198 collected and 1,198 passed in 25.90 seconds (26.11 seconds measured wall time); zero failed, skipped, or xfailed.
8. Final independent validator: passed with the same 15-section, 15-row, 8-reference, 27-claim, quantitative, scope, and protected-input result.
9. `git diff --check`: passed with no whitespace error.

The initial rejected combined validator/cleanup command executed no work because the command safety layer disallowed its cleanup form. The validator and compilation checks were then executed separately with an explicitly scoped temporary directory; both passed.

## Cleanup and readiness

Final cleanup removed `.pytest_cache`, generated `__pycache__` directories, `.pyc`/`.pyo` files, and the isolated compile directory. The final scan found zero tracked cache artifacts and zero repository-local generated cache artifacts. It found no DOCX, PDF, PPTX, product image, new Mermaid rendering, archive, release, repository-local virtual environment, or identifier-like student value.

Final Git scope contains exactly the six authorized created paths plus the authorized `audit/file_change_ledger.md` update. Principal protected hashes and all accepted SP-07 table/figure hashes matched. No history rewrite, commit, or push occurred.

READY FOR HUMAN REVIEW
