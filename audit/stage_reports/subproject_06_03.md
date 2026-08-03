# SP-06.3 Stage Report

## Baseline and environment

SP-06.3 began clean on `main` at `4dfd4b2ae0d369c0d45755e9595ac197b1276d67` in `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`. The external environment was `/home/bar/.venvs/eeeproject-elevator`: Python 3.13.13, pip 26.2, pytest 9.1.1. The pre-edit suite collected 218 and passed 218 in 0.59 seconds.

## Credential data and startup

`load_credentials_json` accepts only a string containing exactly schema version 1 and a credential array. It rejects duplicate JSON members at every object level, malformed/non-object input, unknown/missing fields, wrong types/ranges, Boolean integer traps, invalid/null/empty/whitespace/unencodable labels, and non-object entries with `CredentialDataError`. It preserves accepted Unicode labels and record order, returns an immutable tuple, accepts an empty array, and publishes no partial result. Duplicate ordered `(facility_code, credential_number)` keys raise `DuplicateCredentialError`; equal arithmetic sums remain distinct.

`load_startup_json` validates configuration first, credentials second, returns immutable `StartupData` only after both pass, and preserves `ConfigurationError`, `CredentialDataError`, and `DuplicateCredentialError` identities.

## Repository and authorization

`CredentialRepository.from_records` accepts finite sequences, validates every frozen record locally, rejects malformed structures/records and duplicate ordered keys, then publishes an ordered tuple and private key index. `records()` is immutable and ordered; length is stable; known lookup returns its record; a valid unknown key returns `RepositoryLookup(None)`; malformed trusted keys raise `StateInvariantError`.

Pure `authorize` validates decoded data, returns unknown before floor handling, validates a supplied matching record, returns disabled before floor handling, then validates floor 1–16 and checks `1 << (floor - 1)`. Invalid floor is `error/invalid_floor`; clear bit is `denied/unauthorized_floor`; set bit is `granted/authorized`. Trusted decoded/record/key mismatch defects raise `StateInvariantError`. All 16 set-bit and clear-bit mappings passed, including floor 1→bit 0 and floor 16→bit 15.

## Validation and scope

- Scoped: 149 collected, 149 passed, 0 failed/skipped/xfailed in 0.47s.
- Full: 367 collected, 367 passed, 0 failed/skipped/xfailed in 0.79s; all previous 218 remain passing.
- Compile and both required imports: passed with no output.
- Independent schema/repository/precedence/16-floor/API/import checks: passed.
- Initial failures and corrections: none.

Protected engineering documents, inventory statuses, prior audit records, and Git history remain unchanged and hash-verified. No event log, output, timeout, watchdog, controller, reset, CLI, experiment, persistence/database/network, role/time policy, or hardware behavior was added. SP-06.4 event logging remains deferred. No dependency/network action, commit, or push occurred. Deviations: none.

## Exact readiness state

READY FOR HUMAN REVIEW
