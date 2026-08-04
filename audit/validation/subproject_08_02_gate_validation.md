# SP-08.2G Validation — Human Drafting-Input Resolution Gate

## Handoff, environment, and baseline

- Repository `BarShtainv/EEEProjectElevator`, branch `main`, accepted starting commit and unchanged HEAD `2c0b631cbc42bc59e713c5e8e67c3e89474432bd`.
- Initial status was clean; recent history ended at `2c0b631 Step_8.1R`; no repository `AGENTS.md` or conflicting user change was present.
- External environment: Python 3.13.13, pip 26.2, pytest 9.1.1; no installation, network, document converter, office tool, or repository-local environment.
- Cache-clean baseline: 1157 collected and 1157 passed in 32.22s; zero failures, skips, and xfails.
- The five SP-08.1 report-register hashes recorded in `audit/baselines/subproject_08_02_gate_baseline.md` matched. Six SP-07 table/figure hashes matched `SP07_REPORT_ARTIFACTS_V1`.

## Commands executed

```text
pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git log -5 --oneline --decorate
git status --short --untracked-files=all
find .. -name AGENTS.md -print
source "$HOME/.venvs/eeeproject-elevator/bin/activate"
python --version
python -m pip --version
python -m pytest --version
git ls-tree -r --name-only HEAD report audit/baselines audit/stage_reports audit/validation
sed -n ... report/submission_requirements.md report/report_outline.md report/report_claim_source_matrix.csv report/report_asset_register.csv report/bibliography_readiness.csv audit/validation/subproject_08_01_validation.md audit/validation/subproject_08_01_asset_repair.md final_engineering_project_plan.md README.md
find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
find . -depth -type d -name '__pycache__' -delete
find .pytest_cache -depth -delete
PYTHONPATH=src python -m pytest
sha256sum report/submission_requirements.md report/report_outline.md report/report_claim_source_matrix.csv report/report_asset_register.csv report/bibliography_readiness.csv
python - <<'PY'  # independent canonical-row and blocker counts
PYTHONPATH=src python -m pytest tests/inspection/test_drafting_gate_packet.py -v
python - <<'PY'  # independent standard-library packet validator; no test-module import
PYTHONPATH=src python -m pytest
python -m compileall -q src tests scripts analysis
PYTHONPATH=src python -c "import elevator_access_sim"
PYTHONPATH=src python -c "from elevator_access_sim import Controller"
git diff --check
git diff --name-only
git status --short --untracked-files=all
```

```text
PYTHONPATH=src python -m pytest tests/inspection/test_drafting_gate_packet.py -v
PYTHONPATH=src python -m pytest
find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
find . -depth -type d -name '__pycache__' -delete
find .pytest_cache -depth -delete
git diff --check
git diff --name-only
git status --short --untracked-files=all
git diff --exit-code HEAD -- <protected paths>
python - <<'PY'  # final seven-path, 12-hash, cleanup, privacy-artifact, and forbidden-output validator
```

## Canonical and snapshot validation

- Canonical Markdown parsing found exactly 37 unique ordered `SUB-001` through `SUB-037` rows.
- The snapshot has the exact 14-column schema and exactly 37 unique ordered `DGT-001` through `DGT-037` rows.
- Requirement ID, input/decision, current value, status, blocking stage, authority, responsible party, evidence, and notes reconcile exactly for every row after Markdown-cell parsing.
- Minimum-group membership matches the prescribed mappings exactly. The official/working-title, template/template-neutral, deadline/interim-schedule, and template-dependent identity/format alternatives remain `conditional`; direct decisions use `yes`; later-stage-only rows use `no`.
- All six minimum groups have direct human response requests and remain unresolved.

## Request, privacy, and negative fixtures

- The request has the exact heading and eight required ordered sections, followed by the six required groups in order.
- The paste-back block has all 22 required fields and each value is exactly `[human response required]`.
- The request distinguishes the working title from supervisor approval, selects no language/style/date/template, and states that drafting is blocked.
- Student identification numbers are marked sensitive, absent from the ordinary paste-back block, and not stored as a value. Restricted instructions/templates are requested through an approved restricted channel; product-image use requires provenance and permission.
- Eight temporary-fixture mutations all failed validation as required: omitted SUB row, altered copied value, removed minimum group, fabricated identity, preselected language, invented deadline, public student-ID request, and false drafting approval. Canonical files were not changed.

## Results and protected scope

- Initial focused: 13 collected and 13 passed in 0.30s; zero failures, skips, and xfails.
- Independent validator: `DRAFTING_GATE_VALIDATION=PASS canonical_requirements=37 snapshot_rows=37 minimum_groups=6 unresolved_minimum_groups=6 sensitive_fields=1 protected_files=12`.
- First post-change full suite: 1170 collected and 1170 passed in 30.79s; zero failures, skips, and xfails.
- `python -m compileall -q src tests scripts analysis` and both prescribed imports exited successfully.
- The accepted report registers, six SP-07 report assets, and `pyproject.toml` matched protected hashes. No dependency was added.

No human value was invented, selected, or approved. No report prose/source, human-filled decision file, personal-information file, downloaded template, PDF, presentation, diagram export, benchmark, accepted artifact change, archive, release, tag, commit, or push occurred. SP-08.2 report drafting was not started and remains blocked pending six authoritative human decision groups.

The final post-audit focused run passed 13/13 in 0.31s. The final full suite passed 1170/1170 in 30.55s. Both collected their stated counts and had zero failures, skips, and xfails. The eight negative cases were materialized under pytest temporary paths and did not modify canonical files. `git diff --check` passed; protected-path diff and SHA-256 comparison passed for five SP-08.1 registers, six SP-07 report assets, and `pyproject.toml`. Final status contains exactly the seven authorized paths. Cleanup removed pytest/Python caches and bytecode; no temporary Markdown/CSV fixture, validator comparison, orphaned `.tmp`, personal-information file, human-filled decision file, report source, PDF, presentation, diagram export, archive, release artifact, or repository-local environment remains. The final independent scope command printed `FINAL_GATE_SCOPE=PASS authorized_paths=7 protected_files=12 caches=0 temporary_files=0 forbidden_outputs=0`.

`READY FOR HUMAN REVIEW`
