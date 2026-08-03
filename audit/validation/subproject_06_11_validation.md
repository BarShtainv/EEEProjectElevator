# SP-06.11 Validation

## Starting state and baseline

- Root/repository: recorded baseline root in `audit/baselines/subproject_06_11_baseline.md`; `BarShtainv/EEEProjectElevator`.
- Branch/HEAD: `main`; `28a9dbebf23b0220ca87afdae143b7432ab0d8dc`.
- Initial status: clean, with no conflicting user change.
- Environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from the accepted external environment; no install or network access.
- Cache cleanup before baseline: exit 0; Python/pytest caches removed; no local virtual environment.
- Exact baseline `PYTHONPATH=src python -m pytest`: 965 collected/passed in 3.58s; 0 failed/skipped/xfailed.
- Accepted repair: `audit/validation/subproject_06_11_baseline_flake_repair.md` present at SHA-256 `aafcd53bd960a5ada73860625dfa8f4a3040f55e08ee634b868303388f43c318`; hardened node remained collected and passing.

## Documentation and reconciliation execution

| Command or gate | Exact result |
|---|---|
| verification-record node before inventory promotion | 1 collected/passed in 0.63s; exact 13-column/100-row/order/expected-actual/evidence reconciliation passed. |
| first complete documentation module | 11 collected; 10 passed and one failed in 1.10s because the inspection required one exact limitation phrase despite equivalent README wording. |
| corrected README node | 1 collected/passed in 0.12s. |
| corrected documentation module | 11 collected/passed in 1.14s; 0 failed/skipped/xfailed. |
| historical resolver module | 2 collected/passed in 0.41s; historical CSV counts/order/classes/evidence and optional boundaries retained. |
| standalone CSV/JSON reconciliation | Exit 0; `inventory=94/6 traceability=60/6 verification=100`; all seven required artifacts passed. |

The documentation-test correction changed only the overly literal assertion to require negative modeling context and the physical-reader subject independently. It did not weaken the required absence claim.

Inventory comparison to HEAD shows exactly one changed cell: `TST-TRC-005.status`, `designed` to `implemented`. Traceability comparison shows exactly 66 changed cells, all in `status`: 60 `planned` to `verified` and six `planned` to `optional_deferred`. The historical SP-06.9 resolution CSV has no diff.

The final verification CSV has 100 unique, inventory-ordered rows and the exact 13 columns. Evaluation counts are 94 `passed` and six `optional_deferred`; expected and actual fields differ; every evidence/environment reference is nonempty and repository-relative; test nodes resolve; all five experiment records reference tests/results/environment; `TST-TRC-005` records complete verification-schema reconciliation.

## Published test commands

| Command | Exact result |
|---|---|
| `PYTHONPATH=src python -m pytest tests/unit` | 667 collected/passed in 1.32s. |
| `PYTHONPATH=src python -m pytest tests/integration` | 192 collected/passed in 0.50s. |
| `PYTHONPATH=src python -m pytest tests/end_to_end` | 4 collected/passed in 0.13s. |
| `PYTHONPATH=src python -m pytest tests/inspection` | 19 collected/passed in 1.92s. |
| `PYTHONPATH=src python -m pytest tests/experiment/test_run_experiments.py` | 94 collected/passed in 0.62s. |
| first reconciled `PYTHONPATH=src python -m pytest` | 976 collected/passed in 4.24s; 0 failed/skipped/xfailed. |

The optional editable-install shape was inspected against unchanged package metadata but not executed because this stage explicitly prohibits installing packages. The canonical no-install path and every published pytest command were executed.

## CLI, experiment, and copied-tree reproduction

The CLI used strict temporary UTF-8 schema-1 configuration and one enabled facility-1/credential-100/all-floor/`demo-user` credential, then executed the documented module command with LF, frame `10000000100000000011001000`, floor 1, and advance-to 3000. It exited 0. Initialization succeeded; submission was `granted/authorized`; timeout was `completed/output_expired` at simulated 3000; final state was idle with 16 false outputs; events were one access decision at 0 and one output timeout at 3000; no watchdog reset appeared. A second run was byte-identical. Temporary files were removed.

The first shell containing reviewer cleanup `rm -rf "$temporary_directory"` was rejected by the execution safety layer before process creation, so it produced no result or artifact. The same procedure was executed with bounded `find -delete`/empty-directory cleanup and passed. This is a tool-execution deviation, not a simulator or documentation failure.

The temporary experiment command exited 0 with `completed: sizes=4 measured_rows=12 timer=time.perf_counter_ns` in 0.729s operational wall context. All four sizes, 12 rows, request counts, exact 40/20/15/15/10 outcomes, zero other outcomes, equations, finite positive metrics, integer p95, committed same-size generated-input checksums, one environment ID, seven interpretation limits, and raw-data exclusions passed. Timing equality was not required. Temporary outputs were removed; tracked result/environment hashes remained unchanged.

The first copy command omitted `cd` and therefore ran 976/976 in 4.28s from the original root; it was explicitly rejected as copied-tree evidence and its copy was removed. The corrected excluded copy ran from a system temporary repository root and passed 976/976 in 1.16s with zero failures/skips/xfails. It required no original absolute path, Git metadata, cache, local environment, network, database, device, GUI, or interaction. The copied tree was removed.

## Artifact, claim, and package results

- UTF-8: relevant Markdown, CSV, TOML, Python, and JSON decoded strictly.
- Paths/links: README/reproducibility Markdown links resolved; new/live references were repository-relative and contained no developer path, username, hostname, home, executable, or virtual-environment detail.
- Test plan: prospective SP-05 design remained intact; separated SP-06 actual-evidence section and six canonical paths resolved.
- Package: Python requirement `>=3.11`, empty runtime dependencies, pytest test extra, console entry, and test discovery remained exact.
- Claims: deterministic software-only/proposed/logical/simulated/observational wording passed; physical, electrical, elevator-control, safety, certification, reliability, production-readiness, real-time, and commercial-equivalence boundaries remained explicit.
- Scalability: schema, configuration/workload/seed, 12 rows, counts, metrics, checksums, environment link/limits, and raw-data exclusion passed with no threshold.
- Baseline repair: accepted record hash and hardened absolute bytes path/open guard/exact identity/message/no-I/O assertions passed.

## Final command gate

| Final command or gate | Exact result |
|---|---|
| `PYTHONPATH=src python -m pytest tests/inspection/test_documentation_reproducibility.py -v` | 11 collected/passed in 1.04s; 0 failed/skipped/xfailed. |
| `PYTHONPATH=src python -m pytest tests/inspection/test_inventory_traceability.py -v` | 2 collected/passed in 0.46s; 0 failed/skipped/xfailed. |
| `PYTHONPATH=src python -m pytest` | 976 collected/passed in 4.10s; 0 failed/skipped/xfailed. |
| `python -m compileall -q src tests scripts` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "import elevator_access_sim"` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "from elevator_access_sim import Controller, load_startup_files"` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "from elevator_access_sim.cli import run"` | Exit 0 with no diagnostics. |
| final standalone CSV/JSON reconciliation | Exit 0; inventory 94/6, traceability 60/6, verification 100, experiment rows 12. |
| final clean copied-tree full suite | 976 collected/passed in 1.19s; 0 failed/skipped/xfailed; copy removed. |
| final temporary CLI reproduction | Exit 0; exact initialize/grant/timeout/idle/two-event/no-watchdog outcome; files removed. |
| final temporary experiment reproduction | Exit 0; four sizes and 12 rows; exact counts/checksums/metrics/environment/raw-data checks; outputs removed; operational wall 0.758s. |
| `git diff --check` | Exit 0 with no diagnostics. |
| `git diff --name-only` and `git status --short --untracked-files=all` | Reviewed exactly six authorized modified and six authorized created paths. |
| protected-path/hash checks | No production, runner/config/result, package, earlier-test, historical-resolution, or repair-record diff. Repair/result/environment SHA-256 values remained `aafcd53b…`, `009381bf…`, and `ed910911…`. |
| cleanup | No `.pytest_cache`, `__pycache__`, bytecode, orphan `.tmp`, copied repository, CLI/experiment temporary output, local environment, raw generated data, timing-sample file, archive, or release artifact remained. |

The final changed paths are `README.md`, `docs/reproducibility.md`, `docs/test_plan.md`, `docs/test_case_inventory.csv`, `docs/requirements_to_test_traceability.csv`, `tests/inspection/test_inventory_traceability.py`, `tests/inspection/test_documentation_reproducibility.py`, `audit/baselines/subproject_06_11_baseline.md`, `audit/stage_reports/subproject_06_11.md`, `audit/validation/subproject_06_11_validation.md`, `audit/validation/subproject_06_11_verification_records.csv`, and `audit/file_change_ledger.md`.

Supervisor approval and other human approvals remain pending. Optional features, engineering report, presentation, release preparation, submission, and physical/commercial work remain deferred. No behavior, optional feature, report, presentation, release, tag, archive, submission package, commit, or push occurred.

READY FOR HUMAN REVIEW
