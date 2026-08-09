# SP-08.2HR Baseline — Human-decision privacy, provenance, and partial-gate repair

Starting commit: `ba9756d09cbb7525a29ee5fb93baee9a5f75b9c1` on `main`. The accepted external environment used Python 3.13.13, pip 26.2, and pytest 9.1.1. Baseline collected 1170 tests; 1168 passed and two known gate-inspection failures exposed the overwritten snapshot and normalized historical assertions.

The starting commit changed five paths and introduced a sensitive student identifier into tracked content, overwrote the historical SP-08.2G snapshot, and changed historical tests. Current drafting blockers are supervisor authorization and a final deadline or accepted interim schedule. Protected SP-08.1/SP-07 paths remain outside this repair. Git history rewrite, force-push, commit, and push are deferred.
