# SP-06.2 Stage Report

## Baseline and environment

- Repository root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`
- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `b449bed3300b341360964128b951df9b80b4fcf3` (`Step_6.1`)
- Starting status: clean
- External environment: `/home/bar/.venvs/eeeproject-elevator`
- Python: `3.13.13`
- pip: `26.2`
- pytest: `9.1.1`
- Baseline record: `audit/baselines/subproject_06_02_baseline.md`

The pre-edit regression collected 114 tests and passed all 114 in 0.37 seconds. The accepted SP-06.1 and SP-06.1R records were present, no conflicting user change existed, and no dependency or environment change was needed.

## Wiegand API and representation

Created the stateless `src/elevator_access_sim/wiegand.py` module with the four reviewed public functions:

```python
def validate_frame(frame: object) -> FrameValidation: ...
def decode_frame(frame: tuple[int, ...]) -> DecodedCredential: ...
def encode_frame(facility_code: int, credential_number: int) -> tuple[int, ...]: ...
def has_valid_parity(frame: tuple[int, ...]) -> bool: ...
```

The package root explicitly exports all four while retaining every SP-06.1 export. The module imports only reviewed model types/exceptions and owns no mutable runtime state.

The canonical internal frame is an immutable tuple of exactly 26 exact `int` members valued 0 or 1. The external validator accepts only tuples/lists, converts valid lists to tuples internally, rejects all other containers without consuming iterators, and applies container, length, member, leading-parity, trailing-parity, then decode checks in that order. Malformed external values return `invalid_frame`; parity failures return `parity_failure`; neither path raises.

## Fields, parity, encoding, and decoding

Facility bits 2–9 and credential bits 10–25 are encoded and decoded most-significant bit first. Facility values are exact integers 0–255 and credential values exact integers 0–65535; Boolean and every other invalid trusted encoder value raise `CredentialDataError` without truncation or coercion.

The leading bit is calculated so Python slice `frame[0:13]` contains an even number of ones. The trailing bit is calculated so `frame[13:26]` contains an odd number. Trusted decoder structural/parity misuse raises `StateInvariantError`; the parity helper raises the same exception only for structural misuse and returns `False` for structurally valid parity failures.

## Canonical and negative vectors

All six reviewed strings were independently recalculated in the test module, matched exactly, passed both parity equations, encoded exactly, decoded to their specified fields, and round-tripped:

```text
WV-001  00000000000000000000000001  -> (0, 0)
WV-002  01111111111111111111111111  -> (255, 65535)
WV-003  10000000100000000000000010  -> (1, 1)
WV-004  10101010100010010001101001  -> (85, 4660)
WV-005  10010101010101010101010101  -> (42, 43690)
WV-006  10000000100000000011001000  -> (1, 100)
```

For every vector, independent flips at documentation bits 1, 26, 2, and 14 produced 24 `parity_failure` outcomes, no decoded value, a false parity-helper result, and a trusted-decoder invariant exception.

## Invalid input and source independence

Tests cover 12 unsupported container kinds, non-consumption of an arbitrary iterator, tuple/list lengths 0, 1, 25, 27, and 52, and 11 representative non-binary member types. All external cases return `FrameValidation(False, Reason.INVALID_FRAME, None)` without exception. Six decoder misuse cases raise `StateInvariantError`; structural parity-helper misuse raises `StateInvariantError`; and 16 encoder misuse cases raise `CredentialDataError`.

Identical immutable frames stored in LF and HF `CredentialRequest` values validate and decode identically. No public codec function accepts source/frequency metadata, and no bit represents or infers reader source.

## Tests and validation

Created `tests/unit/test_wiegand.py` with 104 collected pytest cases covering TST-WIE-001–008, TST-DAT-001–002, and the Wiegand-only portion of TST-DAT-003. Inventory statuses remain unchanged.

- Scoped: 104 collected, 104 passed, 0 failed, 0 skipped, 0 xfailed in 0.32 seconds.
- Full regression: 218 collected, 218 passed, 0 failed, 0 skipped, 0 xfailed in 0.49 seconds.
- Compilation: `python -m compileall -q src tests` passed with no output.
- Package import: passed with no output.
- Four-function package import: passed with no output.
- Independent API/vector/corruption/malformed/boundary/source checks: passed.

There were no test failures and no corrective iteration. No test was weakened, skipped, or marked xfail.

## Scope, deferred work, and deviations

Protected requirements, register model, architecture, software design, test plan/inventory, implementation sequence, decision log, traceability, evidence, literature/source PDFs, bibliography, product material, prior audit records, project plan, workflow handbook, and Git history remain unchanged and hash-verified.

SP-06.3 credential JSON loading, credential repository, and authorization remain deferred. No pulse timing, physical/RF behavior, alternate profile/length, event logger, output, watchdog, controller, CLI, experiment, hardware adapter, network, database, thread, or async behavior was added. There were no scope or design deviations. No dependency was installed, no network was accessed, and no commit or push occurred.

## Exact readiness state

READY FOR HUMAN REVIEW
