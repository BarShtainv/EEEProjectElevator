# SP-08.1 Validation — Submission Gate and Report Evidence Architecture

## Gate and source inspection

- Repository/root/remote/branch/history/status: clean `BarShtainv/EEEProjectElevator` `main` at accepted commit `6ec20c1be8c0cbf64f4c04b695c343e59f75704e`; no repository instructions conflicted.
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from the accepted external environment; no install or network access.
- Accepted SP-07.4R hashes: repair `4d75d41c...d4d72`, summary `52a2f9ca...ae1a`, anomalies `cafaddae...5d88`, ledger `c0db9e21...7745`, notes `6fbfdb19...81e6`.
- Baseline after cache cleanup: 1137/1137 passed in 26.78s; zero failures/skips/xfails.
- Inspected the project plan, README, package/dependency metadata, all evidence registers and literature/methodology material, requirements/design/architecture/register/test/reproducibility/decision/traceability documents, production package tree, SP-07 tables/figures/manifest/review outputs, and SP-07.4/R records. Twenty-eight principal hashes are frozen in the SP-08.1 baseline.

## Register validation

- Submission requirements: 37 unique rows, exact nine-column schema, allowed statuses, explicit current values/owners/stages, distinct working/official titles, pending supervisor approval, and 25 SP-08.2-blocking human/unavailable inputs.
- Report outline: exact 15-section order; ten required planning fields per section; controlled status vocabulary; product, literature, architecture, verification, results, discussion, conclusion, reference, and appendix boundaries present.
- Claim matrix: 27 unique ordered rows, exact 11-column schema, valid chapters/classes/statuses, resolvable repository-relative paths and source IDs, and no usable unresolved commercial claim.
- Quantitative mapping: every supported quantitative row maps to one or more of the 39 final-ledger IDs; mixed, lookup, and authorization timing rows include one-host, three-repetition, operation-boundary, no-pooled-statistic, and no-ranking qualifications.
- Asset register: 16 unique rows and exact ten-column schema; all six SP-07 assets present and byte hashes match `SP07_REPORT_ARTIFACTS_V1`; timing titles/semantics retained; missing product image is not report-ready.
- Bibliography readiness: 25 unique rows exactly cover source-index IDs; complete/partial/insufficient/internal classes remain distinct; incomplete sources are not citation-ready; SRC-MISSING-009 and SRC-MISSING-010 remain explicit.
- UTF-8, relative paths, absence of identifying paths, prohibited commercial/safety/performance/completion claims, forbidden report/release formats, unchanged dependency metadata, and 28 protected hashes passed.

The initial focused run collected 16: 14 passed and two failed in 0.47s. One regex did not admit the numeric portion of `SRC-STM32-001`; one claim used unknown-register IDs not represented in the permitted resolver sets. The regex was corrected and the claim was mapped to registered `UNK-004`, `UNK-006`, `UNK-007`, and `SRC-MISSING-010` authorities. No accepted source changed. The corrected focused run passed 16/16 in 0.37s. The first full suite passed 1153/1153 in 28.40s, with zero failures/skips/xfails.

The independent standard-library validator imported no test module and printed `INDEPENDENT_REPORT_GATE=PASS submissions=37 sections=15 claims=27 assets=16 bibliography=25 blocking_human=25`. It independently checked UTF-8, headings/schemas, uniqueness/statuses, source-path/ID/ledger resolution, section order, six asset hashes, bibliography readiness, unsupported claims, and the complete human gate. A final scope-aware rerun initially self-matched the literal `/mnt/` rejection sentinel inside the inspection source; restricting the identifying-path scan to report artifacts corrected that validator defect without changing an artifact, after which it printed `FINAL_INDEPENDENT_REPORT_GATE=PASS submissions=37 sections=15 claims=27 assets=16 bibliography=25 blocking_human=25 paths=10`.

## Commands and final results

```text
/home/bar/.venvs/eeeproject-elevator/bin/python --version
/home/bar/.venvs/eeeproject-elevator/bin/python -m pip --version
/home/bar/.venvs/eeeproject-elevator/bin/python -m pytest --version
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -m pytest tests/inspection/test_report_preparation.py -v
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -m pytest
/home/bar/.venvs/eeeproject-elevator/bin/python -m compileall -q src tests scripts analysis
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -c "import elevator_access_sim"
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -c "from elevator_access_sim import Controller"
git diff --check
git diff --name-only
git status --short --untracked-files=all
```

- Final focused: 16/16 passed in 0.43s; zero failures/skips/xfails.
- Final full suite: 1153/1153 passed in 33.55s; zero failures/skips/xfails.
- Compilation/imports: `compileall` and both prescribed package/controller imports exited 0.
- Git/protected scope/cleanup: exactly ten authorized paths; all principal and accepted SP-07 hashes retained; generated caches, bytecode, test fixtures, comparison files, and orphaned temporaries absent.

No report prose or template, PDF, presentation, demonstration package, benchmark, accepted evidence/result, release, archive, tag, dependency, commit, or push was created or changed. SP-08.2 and later work did not begin.

`READY FOR HUMAN REVIEW`
