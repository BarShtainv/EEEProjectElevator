# SP-06.3 Validation

## Commands and results

Repository: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`; branch `main`; HEAD `4dfd4b2ae0d369c0d45755e9595ac197b1276d67`.

```text
$ python --version
Python 3.13.13
$ python -m pip --version
pip 26.2 from /home/bar/.venvs/eeeproject-elevator/lib/python3.13/site-packages/pip (python 3.13)
$ python -m pytest --version
pytest 9.1.1

$ PYTHONPATH=src python -m pytest
collected 218 items
============================= 218 passed in 0.59s ==============================

$ PYTHONPATH=src python -m pytest tests/unit/test_credential_config.py tests/unit/test_credentials.py tests/unit/test_authorization.py -v
collecting ... collected 149 items
<149 verbose PASSED node results>
============================= 149 passed in 0.47s ==============================

$ PYTHONPATH=src python -m pytest
collected 367 items
============================= 367 passed in 0.79s ==============================

$ python -m compileall -q src tests
<no output; exit 0>
$ PYTHONPATH=src python -c "import elevator_access_sim"
<no output; exit 0>
$ PYTHONPATH=src python -c "from elevator_access_sim import CredentialRepository, authorize, load_credentials_json, load_startup_json"
<no output; exit 0>
```

Baseline/scoped/full failures: 0. Skipped: 0. Xfailed: 0. Initial failing names and corrections: none.

## Focused results

Credential cases passed for exact field sets, documented/empty/Unicode/omitted-label inputs, endpoint and Boolean validation, malformed/duplicate JSON, labels, order, late atomic failure, colliding sums, duplicate ordered keys, and startup exception identity. Repository cases passed for empty/multiple/order/length/known/unknown/collision/duplicates, invalid positions and fields, malformed sequences, immutable observation, and trusted lookup misuse.

```text
PUBLIC_EXPORTS=4 signatures=matched
JSON_SCHEMA=exact EMPTY=valid ORDER=preserved ENDPOINTS=passed BOOL_TRAPS=rejected LABELS=enforced
DUPLICATE_JSON=CredentialDataError DUPLICATE_KEY=DuplicateCredentialError
REPOSITORY=immutable_observation ORDERED_COLLISION_KEYS=distinct UNKNOWN=None
FLOOR_MATRIX=grants:16 denials:16 mapping=bit_floor_minus_1
PRECEDENCE=unknown,disabled,before_floor INVALID_FLOOR=error
authorization.py_PROJECT_IMPORTS=['models']
credentials.py_PROJECT_IMPORTS=['models']
```

Authorization arguments remained unchanged. No output/logger/clock/Wiegand/controller/hardware import exists in authorization; no later module was created.

## Final Git and cleanup

```text
$ find . -path './.git' -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '*.pyc' -o -name pyvenv.cfg \) -print
<no output; exit 0>
$ find src tests -type f | sort | rg '/(event_log|outputs|watchdog|controller|cli|experiments|persistence|database|hardware|physical)\.py$'
<no output; no matching path>
$ git diff --name-only -- docs <prior-audit-paths>
<no output; exit 0>
$ git diff --check
<no output; exit 0>
$ git diff --name-only
audit/file_change_ledger.md
src/elevator_access_sim/__init__.py
src/elevator_access_sim/config.py
$ git status --short --untracked-files=all
 M audit/file_change_ledger.md
 M src/elevator_access_sim/__init__.py
 M src/elevator_access_sim/config.py
?? audit/baselines/subproject_06_03_baseline.md
?? audit/stage_reports/subproject_06_03.md
?? audit/validation/subproject_06_03_validation.md
?? src/elevator_access_sim/authorization.py
?? src/elevator_access_sim/credentials.py
?? tests/unit/test_authorization.py
?? tests/unit/test_credential_config.py
?? tests/unit/test_credentials.py
$ git rev-parse HEAD
4dfd4b2ae0d369c0d45755e9595ac197b1276d67
$ git branch --show-current
main
```

Tracked diff names plus authorized untracked records total exactly eleven allowed paths. Protected baseline hashes remain unchanged.

No commit or push occurred.

## Final outcome

READY FOR HUMAN REVIEW
