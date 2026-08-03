# SP-06.8 Baseline

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Accepted starting commit: `6ad56143718c5c3dacaa9d6af746cdf80b03dc54`
- Initial status: clean (`git status --short --untracked-files=all` produced no output)
- Accepted records: SP-06.1 through SP-06.7 baselines, reports, and validations are present.
- Environment: Python 3.13.13; pip 26.2; pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`.
- Baseline command: `PYTHONPATH=src python -m pytest`
- Baseline result: 759 collected, 759 passed, 0 failed, 0 skipped, 0 xfailed in 1.95s.

## Reviewed contracts

Existing text APIs are `default_config()`, `load_config_json(text)`, `load_credentials_json(text)`, and `load_startup_json(config_text, credentials_text)`. They strictly validate complete schema-version-1 JSON, retain credential order, reject duplicate members/keys and invalid values without defaults, and preserve distinct configuration, credential-data, and duplicate-key exceptions.

The existing controller owns all domain processing through `initialize`, `submit`, time advancement, suppression, reset, snapshot, and event observation. The reviewed CLI API is `build_parser()`, `run(argv=None)`, `format_snapshot(snapshot)`, and `format_event(event)`. The adapter may translate exact source labels and CLI characters to raw request fields but must delegate every validation, authorization, output, watchdog, reset, and event decision to `Controller`.

Authorized paths are `config.py`, package exports, `cli.py`, `pyproject.toml`, the two new SP-06.8 test modules, this baseline, the SP-06.8 stage/validation records, and the file-change ledger. Protected paths include every domain manager/model/controller, all existing tests, frozen engineering and traceability documents, prior audit records, project/workflow material, evidence/literature/product artifacts, requirements/dependency values other than the single reviewed console entry, and Git history. SHA-256 values were recorded for protected sources, documents, prior records, and existing tests before edits.

SP-06.9 integration-inventory consolidation and all experiments, scalability, persistence, networking, databases, GUI, hardware, physical behavior, optional profiles, and optional authorization work remain deferred.
