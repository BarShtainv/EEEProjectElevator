# SP-06.2 Validation

## Environment and baseline gate

Commands were run from `/mnt/c/Users/Bar/Desktop/EEEProjectElevator` on branch `main` at starting and final HEAD `b449bed3300b341360964128b951df9b80b4fcf3`.

```text
$ source /home/bar/.venvs/eeeproject-elevator/bin/activate
$ python --version
Python 3.13.13

$ python -m pip --version
pip 26.2 from /home/bar/.venvs/eeeproject-elevator/lib/python3.13/site-packages/pip (python 3.13)

$ python -m pytest --version
pytest 9.1.1
```

No package was installed and no network was accessed.

The initial branch/commit/status, recent history, remote, package/test paths, environment, prior records, instructions, local-environment absence, and protected hashes were inspected. Initial `git status --short --untracked-files=all` was empty.

```text
$ PYTHONPATH=src python -m pytest
============================= test session starts ==============================
platform linux -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /mnt/c/Users/Bar/Desktop/EEEProjectElevator
configfile: pyproject.toml
testpaths: tests
collected 114 items

tests/unit/test_clock.py .......................                         [ 20%]
tests/unit/test_config.py .............................................. [ 60%]
............                                                             [ 71%]
tests/unit/test_models.py .................................              [100%]

============================= 114 passed in 0.37s ==============================
```

Baseline failed: 0. Skipped: 0. Xfailed: 0.

## Scoped Wiegand pytest

```text
$ PYTHONPATH=src python -m pytest tests/unit/test_wiegand.py -v
collecting ... collected 104 items
<104 verbose PASSED node results>
============================= 104 passed in 0.32s ==============================
```

Collected: 104. Passed: 104. Failed: 0. Skipped: 0. Xfailed: 0. Duration: 0.32 seconds. The initial scoped run passed; there were no failing test names or corrections.

The 104 cases include six independent canonical-vector cases, 24 separately collected corruption cases, valid-list acceptance, nine field round trips, 12 invalid containers, iterator non-consumption, ten invalid lengths, 11 invalid members, six decoder misuses, four parity-helper structural misuses, two false parity results, 16 encoder misuses, source independence, and module/API inspection.

## Full regression pytest

```text
$ PYTHONPATH=src python -m pytest
============================= test session starts ==============================
platform linux -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /mnt/c/Users/Bar/Desktop/EEEProjectElevator
configfile: pyproject.toml
testpaths: tests
collected 218 items

tests/unit/test_clock.py .......................                         [ 10%]
tests/unit/test_config.py .............................................. [ 31%]
............                                                             [ 37%]
tests/unit/test_models.py .................................              [ 52%]
tests/unit/test_wiegand.py ............................................. [ 72%]
...........................................................              [100%]

============================= 218 passed in 0.49s ==============================
```

Collected: 218. Passed: 218. Failed: 0. Skipped: 0. Xfailed: 0. Duration: 0.49 seconds. All previous 114 cases remain passing.

## Compile and import

```text
$ python -m compileall -q src tests
<no output; exit 0>

$ PYTHONPATH=src python -c "import elevator_access_sim"
<no output; exit 0>

$ PYTHONPATH=src python -c "from elevator_access_sim import encode_frame, decode_frame, validate_frame, has_valid_parity"
<no output; exit 0>
```

## Independent programmatic validation

The independent calculation used its own eight-bit and sixteen-bit format strings, parity sums, joins, slices, and integer decoding. It imported no private production helper.

```text
PUBLIC_FUNCTIONS=4 signatures=matched exports=matched
STATELESS_MODULE=yes PROJECT_IMPORTS=models PROHIBITED_IMPORTS=none
WV-001=00000000000000000000000001 decoded=0,0
WV-002=01111111111111111111111111 decoded=255,65535
WV-003=10000000100000000000000010 decoded=1,1
WV-004=10101010100010010001101001 decoded=85,4660
WV-005=10010101010101010101010101 decoded=42,43690
WV-006=10000000100000000011001000 decoded=1,100
INDEPENDENT_VECTORS=6 matched decoded
NEGATIVE_VECTOR_CORRUPTIONS=24 parity_failure
INVALID_CONTAINERS=12 invalid_frame
INVALID_LENGTHS=10 invalid_frame
INVALID_MEMBERS=11 invalid_frame
DECODER_MISUSE=6 StateInvariantError
ENCODER_MISUSE=16 CredentialDataError
ENCODED_BOUNDARIES=4 immutable_exact_binary_tuples
LF_HF_SOURCE_INDEPENDENCE=passed metadata_external
```

Focused AST/signature inspection confirms exact public annotations, no mutable module-level runtime value, only the reviewed `models` project import, no source/frequency parameter, and no import of configuration, clock, credentials, authorization, outputs, watchdog, event logging, controller, or CLI.

## Failure handling

Initial failures: none. Corrections after test execution: none. No canonical vector, field allocation, parity region, reason, or exception policy changed. No test was deleted, weakened, skipped, or marked xfail.

## Protected scope, cleanup, and Git

Requirements, register model, architecture, software design, test plan/inventory, implementation sequence, decision log, prior audit records, and all other protected paths match the baseline hashes. Test-inventory statuses remain design records.

```text
$ find . -path './.git' -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '*.pyc' \) -print
<no output; exit 0>

$ find . -path './.git' -prune -o -type f -name pyvenv.cfg -print
<no output; exit 0>

$ find src tests -type f | sort | rg '/(credentials|repository|authorization|event_log|outputs|watchdog|controller|cli|experiments|hardware|physical)\.py$'
<no output; exit 1 because no matching path exists>

$ git diff --name-only -- docs audit/stage_reports/subproject_06_01.md audit/validation/subproject_06_01_validation.md audit/stage_reports/subproject_06_01_repair.md audit/validation/subproject_06_01_repair_validation.md
<no output; exit 0>

$ git diff --check
<no output; exit 0>

$ git diff --name-only
audit/file_change_ledger.md
src/elevator_access_sim/__init__.py

$ git status --short --untracked-files=all
 M audit/file_change_ledger.md
 M src/elevator_access_sim/__init__.py
?? audit/baselines/subproject_06_02_baseline.md
?? audit/stage_reports/subproject_06_02.md
?? audit/validation/subproject_06_02_validation.md
?? src/elevator_access_sim/wiegand.py
?? tests/unit/test_wiegand.py

$ git rev-parse HEAD
b449bed3300b341360964128b951df9b80b4fcf3

$ git branch --show-current
main
```

`git diff --name-only` lists tracked changes; the status output also lists the five authorized new paths. The exact final change set is the seven paths authorized by SP-06.2.

No credential loader/repository, authorization, event logging, outputs, watchdog, controller, CLI, experiment, alternate profile, pulse timing, physical/RF adapter, network, database, thread, or async module was implemented. No commit or push occurred.

## Final outcome

READY FOR HUMAN REVIEW
