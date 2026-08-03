# SP-07.4 Validation — Final Subproject-7 Review

## Executed gates

- Repository/remote/branch/history/status: exact clean `main` at `7b6ad373014e047ac454d11578f18a017d462057`; no `AGENTS.md`.
- Versions: Python 3.13.13, pip 26.2, pytest 9.1.1 in the accepted external environment.
- Canonical inspection/hash capture: 29 prescribed governance, historical, mixed, isolated, integrated, manifest, figure, and execution-evidence inputs; hashes recorded in the SP-07.4 baseline.
- Baseline after generated-cache removal: 1106/1106 passed in 24.13s; zero failures/skips/xfails.

## Independent implementation and reconciliation

The standard-library reviewer independently parses strict UTF-8 CSV/JSON/Markdown/XML; rejects duplicate JSON; verifies canonical hashes and manifest 9/8 structure; reconciles the 976/976 historical snapshot, 66 requirements (60/6), 100 inventory rows (94/6), and 100 verification records (94/6). It independently derives mixed 12/39000/15600/19500/7800/5850/5850/3900/0 and isolated 24/24000, lookup 12000/6000/6000/0, authorization 12000/4800/6000/1200/0/0/0.

Every timing table row matches all 12 independently recalculated min/median/max statistics from three repetitions. Every SVG's 12 points, four medians, four whiskers, axes, units, scope, accessibility, and resource boundary match accepted sources. No pooled statistic, cross-family ranking, complexity, significance, or hardware inference was made.

The first focused run collected 23: 22 passed and one failed in 1.62s because missing canonical files propagated raw `FileNotFoundError`. `digest()` was narrowly corrected to emit stable `ReviewError`; no review arithmetic/output changed. Final pre-generation focused: 23/23 in 1.64s, zero failures/skips/xfails. First full suite: 1129/1129 in 24.18s, zero failures/skips/xfails.

## Official outputs and independent validation

The exact four-option official command ran twice. Both exited 0 and printed `completed: ledger_rows=39 anomalies=14 blocking=0 figures=3 timing_rows=12`; bytes were identical.

| Output | SHA-256 |
|---|---|
| `data/results/sp07_independent_review_summary.json` | `7d48384b258c1cd033efe84aa6aba1fa65cd1f23621ed382fd1df4f0c38c9b92` |
| `data/results/sp07_anomaly_register.csv` | `0f997c8e10f53fa104718acb2823b25e134309f0dd7ad201bc87be447392f7c9` |
| `audit/validation/subproject_07_final_validation_ledger.csv` | `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745` |
| `docs/sp07_results_discussion_source_notes.md` | `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6` |

The ledger has 39 supported-with-limit claims, zero unresolved/not-supported/blocking. The anomaly register has 14 nonblocking rows and explicit implications. The summary has the exact 16-field schema/readiness and zero blockers. Notes have all 14 required sections, cited numeric observations, six-artifact map, bounded conclusions, and non-final status.

The separate standard-library command did not import review or analysis scripts and printed `INDEPENDENT_VALIDATION=PASS sources=29 ledger=39 anomalies=14 timing_rows=12 figures=3 blocking=0`. It verified output hashes/schemas, important totals, ledger status, anomaly implications, note values/sections, and every accepted source hash. Its first post-expansion invocation failed only because that validator expected nonexistent generic SVG class names; inspection established the accepted names (`repetition-point`, `median-point`, and `whisker`), and the corrected independent invocation passed without changing any reviewed artifact.

## Final commands

The required commands were executed with the accepted external interpreter (shown explicitly below); the official generation command was executed twice, followed by hash comparison and the separate inline standard-library validator.

```text
/home/bar/.venvs/eeeproject-elevator/bin/python --version
/home/bar/.venvs/eeeproject-elevator/bin/python -m pip --version
/home/bar/.venvs/eeeproject-elevator/bin/python -m pytest --version
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -m pytest tests/analysis/test_review_results.py -v
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -m pytest
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -m pytest -q
/home/bar/.venvs/eeeproject-elevator/bin/python -m compileall -q src tests scripts analysis
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -c "import elevator_access_sim"
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python -c "from elevator_access_sim import Controller"
PYTHONPATH=src /home/bar/.venvs/eeeproject-elevator/bin/python analysis/review_results.py --review-summary-output data/results/sp07_independent_review_summary.json --anomaly-register-output data/results/sp07_anomaly_register.csv --validation-ledger-output audit/validation/subproject_07_final_validation_ledger.csv --source-notes-output docs/sp07_results_discussion_source_notes.md
git diff --check
git diff --name-only
git status --short --untracked-files=all
```

Cleanup used bounded `find` deletion for generated bytecode/cache files and inspected `*.tmp`, `*.backup.*`, `.pytest_cache`, `__pycache__`, and repository-local environment names. SHA-256 comparison covered all four outputs and all 29 sources; protected tracked content was compared with `HEAD`.

| Check | Exact result |
|---|---|
| final focused | `26 passed in 1.88s`; zero failures/skips/xfails |
| final full suite | `1132 passed in 28.24s`; zero failures/skips/xfails |
| compilation/imports | `compileall` and both prescribed imports exited 0 |
| protected hashes and independent rerun | 29 canonical hashes and four output hashes matched; independent validator passed with 39/14/12/3/0 |
| Git/cleanup | ten authorized paths only; protected tracked content unchanged except the authorized ledger append; caches, bytecode, temporary outputs, and recovery backups absent |

Neither benchmark was executed. No accepted measurement, table, figure, manifest, catalog, summary, simulator, existing test, governance artifact, prior audit, report, presentation, release, or Subproject-8 artifact changed. No commit or push occurred.

`READY FOR HUMAN REVIEW`
