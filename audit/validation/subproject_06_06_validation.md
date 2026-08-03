# SP-06.6 Validation

```text
Baseline: 488 collected/passed, 0 failed/skipped/xfailed in 1.24s
Output closure: 71 collected/passed, 0 failed/skipped/xfailed in 0.35s
Initial watchdog: 66 collected/passed, 0 failed/skipped/xfailed in 0.28s
Initial full: 562 collected/passed, 0 failed/skipped/xfailed in 1.40s
Final watchdog after suppressed-service precedence correction: 66/66 in 0.29s
Final full: 562/562 in 1.19s
compileall: exit 0; package import: exit 0; Watchdog import: exit 0
```

Validated constructor endpoints/Boolean traps; interval formula; enabled/disabled schedules; direct service and suppression; exact heartbeat consumption; normal/suppressed same-time priority; one-shot early/exact/late expiry; reinitialization/new epochs; 3000/30000 normal schedules; invalid-call atomicity; models-only import scope; and both SP-06.5 closure cases. No test was skipped or weakened.

The first green suite did not expose that suppressed direct `service` at the deadline must return false before normal expired-service validation. Inspection identified it; the condition order was corrected and a same-deadline assertion added. Final suites pass.

Final cleanup removed caches. Git whitespace, protected paths, absence of controller/later modules and repository-local environments, unchanged HEAD/branch, and exact authorized status were checked. No commit or push occurred.

```text
$ git diff --check
<no output; exit 0>
$ git diff --name-only
audit/file_change_ledger.md
src/elevator_access_sim/__init__.py
tests/unit/test_outputs.py
$ git status --short --untracked-files=all
 M audit/file_change_ledger.md
 M src/elevator_access_sim/__init__.py
 M tests/unit/test_outputs.py
?? audit/baselines/subproject_06_06_baseline.md
?? audit/stage_reports/subproject_06_06.md
?? audit/validation/subproject_06_06_validation.md
?? src/elevator_access_sim/watchdog.py
?? tests/unit/test_watchdog.py
$ git rev-parse HEAD
c75475ee886a73dfc33c272c1e4c524d475dbbf8
$ git branch --show-current
main
```

READY FOR HUMAN REVIEW
