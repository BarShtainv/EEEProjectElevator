# SP-06.8 Stage Report

Accepted clean baseline `6ad56143718c5c3dacaa9d6af746cdf80b03dc54` on `main`; Python 3.13.13, pip 26.2, pytest 9.1.1; baseline 759/759 in 1.95s. The external environment `/home/bar/.venvs/eeeproject-elevator` was reused without installation or network access.

Added and exported `load_startup_files(config_path, credentials_path)`. It accepts text strings and `os.PathLike[str]`, rejects unsupported/bytes/Boolean/scalar/collection paths, reads each file explicitly with `encoding="utf-8", errors="strict"`, then delegates both texts to the unchanged atomic `load_startup_json`. It uses no default, fallback encoding, BOM stripping, normalization, mutation, cache, or partial return.

Configuration path/read/decode/JSON failures retain `ConfigurationError`; credential equivalents retain `CredentialDataError`; duplicate composite keys retain exact `DuplicateCredentialError`. Messages are concise and identify the relevant file category without platform exception text. Valid Unicode labels and input order are preserved.

Implemented the four reviewed CLI APIs: `build_parser`, `run`, `format_snapshot`, and `format_event`. Required config/credential paths have no fallback. Source/frame/floor are all-or-none; advance-to/by are exclusive; floor/time conversion belongs to argparse. Exact `LF`/`HF` adapt to their enum, other text remains raw invalid source. Frame characters map only `0`/`1`; all others are preserved for controller validation.

Execution order is parse, strict file load, fresh zero clock/controller, initialize, optional suppression, optional request, optional advance, optional manual reset, final snapshot, then successful events. Every domain action delegates to the public `Controller`; the CLI performs no Wiegand decode/parity/field logic, lookup, authorization, mask, output, watchdog scheduling, reset preservation, event construction, or sequencing.

Every executed operation prints a deterministic compact JSON response line. Snapshot formatting uses the exact nine-field order and 16 JSON Booleans. Event formatting uses the exact existing nine-field order, explicit nulls, uppercase LF/HF, and lowercase state/event/result/reason text. `ensure_ascii=False`, compact separators, and stable insertion order are used.

Valid demonstrations and modeled grants/denials/validation/timeouts/resets return 0. File/UTF-8/schema/duplicate-key/controller-startup/clock/logging failures return 1 with one `error: ` stderr line and no traceback. Argparse syntax errors retain code 2. Formatter programmer misuse raises `StateInvariantError`.

Final tests: startup files 58/58 in 0.32s; CLI 42/42 in 0.28s; full regression 859/859 in 1.86s. No failures, skips, or xfails occurred. A real `python -m elevator_access_sim.cli` smoke with temporary documented inputs exited 0, displayed an LF grant, expired it at 3000, ended idle/inactive, produced one access-decision and one output-timeout event, produced no watchdog reset, and left no temporary data.

Compilation and package/adapter/CLI imports passed. Public signatures, explicit UTF-8, TOML console metadata, deterministic JSON, delegation structure, protected hashes/paths, cleanup, repository-local-environment absence, whitespace, status, branch, and unchanged HEAD passed final validation. No protected domain source, existing test, frozen engineering/traceability record, prior audit, or Git history changed.

SP-06.9 integration-inventory consolidation and all experiment/scalability, persistence, network/database, GUI, hardware/physical, additional-profile, and optional-policy work remain deferred. No deviation, commit, or push occurred.

READY FOR HUMAN REVIEW
