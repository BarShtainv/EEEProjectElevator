# SP-06.1R Repair Validation

## Baseline

Commands were run from `/mnt/c/Users/Bar/Desktop/EEEProjectElevator` on branch `main` at starting and final HEAD `b155165f279f88699517998e877248bfa62e4a70`.

```text
$ git status --short --untracked-files=all
<no output; exit 0>

$ python --version
Python 3.13.13

$ python -m pytest --version
/home/bar/miniforge3/bin/python: No module named pytest
<exit 1>
```

The base environment reproduced the historical blocker. The dedicated external path `/home/bar/.venvs/eeeproject-elevator` did not initially exist.

## External environment creation

```text
$ python -m venv /home/bar/.venvs/eeeproject-elevator
<no output; exit 0>
```

```text
$ source /home/bar/.venvs/eeeproject-elevator/bin/activate
$ python -m pip install --upgrade pip
Requirement already satisfied: pip in /home/bar/.venvs/eeeproject-elevator/lib/python3.13/site-packages (26.0.1)
Collecting pip
  Downloading pip-26.2-py3-none-any.whl.metadata (4.6 kB)
Downloading pip-26.2-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 7.7 MB/s  0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 26.0.1
    Uninstalling pip-26.0.1:
      Successfully uninstalled pip-26.0.1
Successfully installed pip-26.2
```

```text
$ python -m pip install "pytest>=7"
Collecting pytest>=7
  Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting iniconfig>=1.0.1 (from pytest>=7)
  Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
Collecting packaging>=22 (from pytest>=7)
  Downloading packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest>=7)
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pygments>=2.7.2 (from pytest>=7)
  Downloading pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 9.6 MB/s  0:00:00
Installing collected packages: pygments, pluggy, packaging, iniconfig, pytest

Successfully installed iniconfig-2.3.0 packaging-26.2 pluggy-1.6.0 pygments-2.20.0 pytest-9.1.1
```

No global package or Miniforge base package was changed. No pytest-cov, linter, formatter, type checker, documentation tool, framework, or runtime dependency was installed.

## Tool versions

```text
$ python --version
Python 3.13.13

$ python -m pip --version
pip 26.2 from /home/bar/.venvs/eeeproject-elevator/lib/python3.13/site-packages/pip (python 3.13)

$ python -m pytest --version
pytest 9.1.1
```

## Final scoped pytest execution

```text
$ PYTHONPATH=src python -m pytest tests/unit/test_models.py tests/unit/test_config.py tests/unit/test_clock.py -v
============================= test session starts ==============================
platform linux -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- /home/bar/.venvs/eeeproject-elevator/bin/python
cachedir: .pytest_cache
rootdir: /mnt/c/Users/Bar/Desktop/EEEProjectElevator
configfile: pyproject.toml
collecting ... collected 114 items

tests/unit/test_models.py::test_tst_src_001_reader_source_values_and_uppercase_serialization PASSED [  0%]
tests/unit/test_models.py::test_fixed_enum_names_numbers_and_lowercase_serialization PASSED [  1%]
tests/unit/test_models.py::test_zero_is_only_a_controller_state_value_not_a_null_enum_member PASSED [  2%]
tests/unit/test_models.py::test_frozen_dataclass_rejects_mutation PASSED [  3%]
tests/unit/test_models.py::test_tst_crd_001_credential_key_is_an_ordered_pair PASSED [  4%]
tests/unit/test_models.py::test_credential_request_accepts_unvalidated_raw_boundary_values PASSED [  5%]
tests/unit/test_models.py::test_tst_out_004_inactive_output_snapshot_is_valid PASSED [  6%]
tests/unit/test_models.py::test_tst_out_004_one_active_output_matches_floor[1] PASSED [  7%]
tests/unit/test_models.py::test_tst_out_004_one_active_output_matches_floor[8] PASSED [  7%]
tests/unit/test_models.py::test_tst_out_004_one_active_output_matches_floor[16] PASSED [  8%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels0-None-None] PASSED [  9%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels1-None-None] PASSED [ 10%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels2-None-None] PASSED [ 11%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels3-1-10] PASSED [ 12%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels4-1-None] PASSED [ 13%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels5-None-10] PASSED [ 14%]
tests/unit/test_models.py::test_tst_out_004_rejects_invalid_output_shape_or_relationship[channels6-2-10] PASSED [ 14%]
tests/unit/test_models.py::test_output_snapshot_rejects_mutable_channel_collection PASSED [ 15%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[0] PASSED [ 16%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[17] PASSED [ 17%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[-1] PASSED [ 18%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[True] PASSED [ 19%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[1.0] PASSED [ 20%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_floor[1] PASSED [ 21%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_expiry[-1] PASSED [ 21%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_expiry[True] PASSED [ 22%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_expiry[1.0] PASSED [ 23%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_expiry[10] PASSED [ 24%]
tests/unit/test_models.py::test_output_snapshot_rejects_invalid_active_expiry[None] PASSED [ 25%]
tests/unit/test_models.py::test_controller_snapshot_applies_output_invariants PASSED [ 26%]
tests/unit/test_models.py::test_controller_snapshot_rejects_boolean_or_invalid_integer_traps[True] PASSED [ 27%]
tests/unit/test_models.py::test_controller_snapshot_rejects_boolean_or_invalid_integer_traps[-1] PASSED [ 28%]
tests/unit/test_models.py::test_controller_snapshot_rejects_boolean_or_invalid_integer_traps[1.0] PASSED [ 28%]
tests/unit/test_config.py::test_tst_cfg_001_exact_documented_json PASSED [ 29%]
tests/unit/test_config.py::test_tst_cfg_001_default_config PASSED        [ 30%]
tests/unit/test_config.py::test_tst_tim_002_output_duration_endpoints[minimum] PASSED [ 31%]
tests/unit/test_config.py::test_tst_tim_002_output_duration_endpoints[maximum] PASSED [ 32%]
tests/unit/test_config.py::test_tst_cfg_002_watchdog_timeout_endpoints[minimum] PASSED [ 33%]
tests/unit/test_config.py::test_tst_cfg_002_watchdog_timeout_endpoints[maximum] PASSED [ 34%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[99] PASSED [ 35%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[30001] PASSED [ 35%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[-1] PASSED [ 36%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[True] PASSED [ 37%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[100.0] PASSED [ 38%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[100] PASSED [ 39%]
tests/unit/test_config.py::test_tst_tim_002_rejects_invalid_output_duration[None] PASSED [ 40%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[0] PASSED [ 41%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[4294967296] PASSED [ 42%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[-1] PASSED [ 42%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[True] PASSED [ 43%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[1.0] PASSED [ 44%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[1] PASSED [ 45%]
tests/unit/test_config.py::test_tst_cfg_002_rejects_invalid_watchdog_timeout[None] PASSED [ 46%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_invalid_schema_version[True] PASSED [ 47%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_invalid_schema_version[1.0] PASSED [ 48%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_invalid_schema_version[1] PASSED [ 49%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_invalid_schema_version[None] PASSED [ 50%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[False] PASSED [ 50%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[0] PASSED [ 51%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[1] PASSED [ 52%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[true] PASSED [ 53%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[None] PASSED [ 54%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[value5] PASSED [ 55%]
tests/unit/test_config.py::test_tst_cfg_003_requires_actual_watchdog_boolean[value6] PASSED [ 56%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_missing_field PASSED [ 57%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_unknown_field PASSED [ 57%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_duplicate_json_member PASSED [ 58%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_malformed_json[{] PASSED [ 59%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_malformed_json[] PASSED [ 60%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_malformed_json[not-json] PASSED [ 61%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_unsupported_schema_version PASSED [ 62%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_unsupported_profile PASSED [ 63%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_top_level_type[[]] PASSED [ 64%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_top_level_type[null] PASSED [ 64%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_top_level_type[true] PASSED [ 65%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_top_level_type[1] PASSED [ 66%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_top_level_type["value"] PASSED [ 67%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types[1] PASSED [ 68%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types[None] PASSED [ 69%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types[true] PASSED [ 70%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types[value3] PASSED [ 71%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types[value4] PASSED [ 71%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_nonfinite_constants[NaN] PASSED [ 72%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_nonfinite_constants[Infinity] PASSED [ 73%]
tests/unit/test_config.py::test_tst_cfg_003_rejects_nonfinite_constants[-Infinity] PASSED [ 74%]
tests/unit/test_config.py::test_load_config_json_requires_string_input[None] PASSED [ 75%]
tests/unit/test_config.py::test_load_config_json_requires_string_input[{}] PASSED [ 76%]
tests/unit/test_config.py::test_load_config_json_requires_string_input[1] PASSED [ 77%]
tests/unit/test_config.py::test_load_config_json_requires_string_input[value3] PASSED [ 78%]
tests/unit/test_config.py::test_load_config_json_requires_string_input[value4] PASSED [ 78%]
tests/unit/test_config.py::test_tst_cfg_005_failed_parse_is_atomic_and_does_not_change_defaults PASSED [ 79%]
tests/unit/test_clock.py::test_tst_tim_003_clock_starts_at_zero_by_default PASSED [ 80%]
tests/unit/test_clock.py::test_tst_tim_003_clock_accepts_valid_nonzero_start PASSED [ 81%]
tests/unit/test_clock.py::test_tst_tim_003_advance_by_zero_is_idempotent PASSED [ 82%]
tests/unit/test_clock.py::test_tst_tim_003_advance_by_positive_delta PASSED [ 83%]
tests/unit/test_clock.py::test_tst_tim_003_advance_to_equal_time_is_idempotent PASSED [ 84%]
tests/unit/test_clock.py::test_tst_tim_003_advance_to_later_time PASSED  [ 85%]
tests/unit/test_clock.py::test_tst_tim_003_rejects_invalid_start[-1] PASSED [ 85%]
tests/unit/test_clock.py::test_tst_tim_003_rejects_invalid_start[True] PASSED [ 86%]
tests/unit/test_clock.py::test_tst_tim_003_rejects_invalid_start[1.0] PASSED [ 87%]
tests/unit/test_clock.py::test_tst_tim_003_rejects_invalid_start[1] PASSED [ 88%]
tests/unit/test_clock.py::test_tst_tim_003_rejects_invalid_start[None] PASSED [ 89%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_delta_does_not_change_time[-1] PASSED [ 90%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_delta_does_not_change_time[True] PASSED [ 91%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_delta_does_not_change_time[1.0] PASSED [ 92%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_delta_does_not_change_time[1] PASSED [ 92%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_delta_does_not_change_time[None] PASSED [ 93%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[24] PASSED [ 94%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[-1] PASSED [ 95%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[True] PASSED [ 96%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[25.0] PASSED [ 97%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[25] PASSED [ 98%]
tests/unit/test_clock.py::test_tst_tim_003_rejected_target_does_not_change_time[None] PASSED [ 99%]
tests/unit/test_clock.py::test_clock_has_no_wall_clock_sleep_thread_or_async_dependency PASSED [100%]

============================= 114 passed in 0.35s ==============================
```

Exact result: collected 114; passed 114; failed 0; skipped 0; xfailed 0; duration 0.35 seconds.

## Final full-suite pytest execution

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

============================= 114 passed in 0.31s ==============================
```

Exact result: collected 114; passed 114; failed 0; skipped 0; xfailed 0; duration 0.31 seconds.

## Compilation and import

```text
$ python -m compileall -q src tests
<no output; exit 0>

$ PYTHONPATH=src python -c "import elevator_access_sim"
<no output; exit 0>
```

## Focused implementation inspection

```text
PYPROJECT_PARSE=passed
REQUIRES_PYTHON=>=3.11
RUNTIME_DEPENDENCIES=0
OPTIONAL_TEST=['pytest>=7']
PACKAGE_DISCOVERY=['src']
FROZEN_SLOTTED_RECORDS=15
REVIEWED_API_EXPORTS=31
CREDENTIAL_LOADING=absent
CLOCK_PROHIBITED_IMPORTS=none
LATER_STAGE_MODULE_SCAN=<no output>
```

The first read-only metadata helper assumed a nonexistent `tool.setuptools.package-dir` key and exited with `KeyError: 'package-dir'`. Inspection of the actual TOML showed `tool.setuptools.packages.find.where = ["src"]`; the corrected helper then passed as shown above. This was a validation-helper mistake, not a pytest, source, test, compile, or import defect, and it caused no repository change.

## Failures and corrections

Initial pytest failures: none. Final pytest failures: none. Production corrections: none. Test corrections: none. No test was skipped or marked xfail to bypass a defect, and no custom harness replaced real pytest execution.

## Git, scope, and cleanup

The final exact Git commands and outputs are recorded below after creation of all four authorized repair records.

```text
$ find . -path './.git' -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '*.pyc' \) -print
<no output; exit 0>

$ find . -path './.git' -prune -o -type f -name pyvenv.cfg -print
<no output; exit 0>

$ find src tests -type f | sort | rg '/(wiegand|credentials|repository|authorization|event_log|outputs|watchdog|controller|cli|experiments)\.py$'
<no output; exit 1 because no matching path exists>

$ git diff --check
<no output; exit 0>

$ git diff --name-only
audit/file_change_ledger.md

$ git status --short --untracked-files=all
 M audit/file_change_ledger.md
?? audit/baselines/subproject_06_01_repair_baseline.md
?? audit/stage_reports/subproject_06_01_repair.md
?? audit/validation/subproject_06_01_repair_validation.md

$ git rev-parse HEAD
b155165f279f88699517998e877248bfa62e4a70

$ git branch --show-current
main
```

`git diff --name-only` reports tracked changes only; the status output supplies the three authorized untracked repair records. Source, test, and original-record SHA-256 values exactly match the repair baseline.

The original blocked SP-06.1 stage report and validation are unchanged. Source/test hashes match the repair baseline. No later-stage module, repository-local environment, or retained cache exists. No commit or push occurred.

## Final outcome

READY FOR HUMAN REVIEW
