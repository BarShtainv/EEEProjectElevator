# SP-06.11 Baseline Flake Repair Validation

## Starting state and environment

- Accepted commit: `64cfabc8e12dd4268a1ae888049783aaf0656364` on `main`.
- Initial status: clean; no conflicting user change was present.
- Python: 3.13.13.
- pip: 26.2.
- pytest: 9.1.1.
- External environment: the accepted repository-external project environment; no package was installed and no network access occurred.
- Imported module origin: `src/elevator_access_sim/config.py` in the current repository (observed absolute origin `/mnt/c/Users/Bar/Desktop/EEEProjectElevator/src/elevator_access_sim/config.py`).

The reported pre-SP-06.11 baseline collected 965 tests and produced 964 passes, one failure, zero skips, and zero xfails in 3.74 seconds. `tests/unit/test_config_files.py::test_pathlike_resolving_to_bytes_is_rejected_by_file_identity` failed while defining `BytesPath(os.PathLike[bytes])`, with `TypeError: 'str' object is not callable` reported from frozen `abc`; the node passed immediately afterward in isolation. That run changed no project file, and its generated caches were removed.

## Production and mutation inspection

The active `_read_startup_text` implementation was inspected from the repository module. It accepts only `str`/`os.PathLike`, calls `os.fspath`, rejects every result whose exact type is not `str`, and only then opens the path. It supplies `ConfigurationError` for the first file and `CredentialDataError` for the second. This matches the frozen production contract, so `src/elevator_access_sim/config.py` was not changed.

Searches covered tests that reference `builtins.open`, `os.fspath`, `os.PathLike`, `config_module`, `sys.modules`, `sys.path`, current-directory changes, and import caches. No test mutates `os.PathLike`, `os.fspath`, the working directory, or import caches. The relevant `builtins.open` and `config_module.load_config_json` patches use pytest's `monkeypatch` fixture and occur after the implicated node in the same module. The experiment module installs its separately named runner module in `sys.modules`; no evidence linked that action to the reported class-definition failure.

Before reproduction, generated `__pycache__`, `.pytest_cache`, `.pyc`, and `.pyo` artifacts were removed. No repository-local virtual environment was present, Git remained clean, and `PYTHONPATH=src python -B -c "import elevator_access_sim.config as c; print(c.__file__)"` resolved to the repository `src/` module.

## Pre-repair reproduction

The original failure was not reproduced after cache removal:

| Matrix | Result |
|---|---|
| failing node, 100 fresh `python -B` pytest interpreters | 100/100 passed; each run collected one test. |
| complete `tests/unit/test_config_files.py`, 30 fresh interpreters | 30/30 passed; each run passed 58 tests. |
| full suite, `PYTHONHASHSEED=1` | 965 passed in 3.33s. |
| full suite, `PYTHONHASHSEED=2` | 965 passed in 3.30s. |
| full suite, `PYTHONHASHSEED=3` | 965 passed in 3.26s. |
| full suite, `PYTHONHASHSEED=4` | 965 passed in 3.28s. |
| full suite, `PYTHONHASHSEED=5` | 965 passed in 3.26s. |

All five suites had zero failures, skips, and xfails. No differing observation was available for a failure-category diagnosis.

The exact root cause remains unresolved. Cache pollution, monkeypatch leakage, working-directory changes, and stale bytecode are not claimed as causes because reproduction did not prove any of them. The former test did contain an avoidable relative bytes-path dependency, but that dependency does not explain the observed failure during class construction and is not claimed as its cause.

## Deterministic hardening

Only `test_pathlike_resolving_to_bytes_is_rejected_by_file_identity` changed. Its `BytesPath.__fspath__` now returns `os.fsencode(tmp_path / "bytes-config.json")`; the file is not created. A `builtins.open` guard records any attempted call and fails immediately. The test invokes public `load_startup_files` with the still-valid credential path, then proves exact `ConfigurationError` identity, exact text `configuration file path must resolve to text`, and an empty open-call record.

The optional credential-path counterpart was not added. Public `load_startup_files` intentionally reads and validates the first configuration file before processing the second credential path, so a symmetric absolute assertion that no file I/O occurs would contradict the preserved production sequence.

## Post-repair validation

| Command or matrix | Exact result |
|---|---|
| direct repaired node with `-v` | 1 collected/passed in 0.19s; 0 failed/skipped/xfailed. |
| complete configuration-file module with `-v` | 58 collected/passed in 0.30s; 0 failed/skipped/xfailed. |
| repaired node, 100 fresh `python -B` interpreters | 100/100 runs passed. |
| complete configuration-file module, 30 fresh `python -B` interpreters | 30/30 runs passed; 58 tests per run. |
| repaired full suite, `PYTHONHASHSEED=1` | 965 passed in 3.24s. |
| repaired full suite, `PYTHONHASHSEED=2` | 965 passed in 3.26s. |
| repaired full suite, `PYTHONHASHSEED=3` | 965 passed in 3.28s. |
| repaired full suite, `PYTHONHASHSEED=4` | 965 passed in 3.23s. |
| repaired full suite, `PYTHONHASHSEED=5` | 965 passed in 3.40s. |
| final canonical `PYTHONPATH=src python -m pytest` after cache removal | 965 collected/passed in 3.64s; 0 failed/skipped/xfailed. |
| `python -m compileall -q src tests scripts` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "import elevator_access_sim"` | Exit 0 with no diagnostics. |
| `PYTHONPATH=src python -c "from elevator_access_sim import load_startup_files"` | Exit 0 with no diagnostics. |

Final cleanup removed generated Python/pytest caches and orphan bytecode. `git diff --check` passed. Changed-path and status review showed only `tests/unit/test_config_files.py`, this validation record, and `audit/file_change_ledger.md`. Production source, dependencies, unrelated tests, SP-06.11 documentation, optional features, inventory, traceability, and scalability artifacts remain unchanged. No commit or push occurred.

READY FOR HUMAN REVIEW
