# SP-06.8 Validation

## Environment and test commands

```text
Repository: /mnt/c/Users/Bar/Desktop/EEEProjectElevator
Branch: main
Starting HEAD: 6ad56143718c5c3dacaa9d6af746cdf80b03dc54
Python: 3.13.13
pip: 26.2
pytest: 9.1.1

Baseline `PYTHONPATH=src python -m pytest`: 759 collected/passed, 0 failed/skipped/xfailed in 1.95s
File adapter `PYTHONPATH=src python -m pytest tests/unit/test_config_files.py -v`: 58 passed in 0.32s
CLI `PYTHONPATH=src python -m pytest tests/integration/test_cli.py -v`: 42 passed in 0.28s
Full suite `PYTHONPATH=src python -m pytest`: 859 collected/passed, 0 failed/skipped/xfailed in 1.86s
```

## File-adapter evidence

- Valid ASCII and Unicode documents load through string and `pathlib.Path` paths; empty records, stable order, preserved label content, duration 100/30000, and watchdog 1/4294967295 pass.
- Explicit strict UTF-8 rejects invalid bytes. A UTF-8 BOM is not stripped and reaches normal JSON rejection. No locale or replacement decoding exists.
- Missing paths, directories, ordinary permission/read failures, malformed JSON, duplicate members, unsupported schema/profile, unknown/missing fields, wrong types/ranges, and invalid labels retain configuration versus credential exception identity.
- A duplicate composite key raises exact `DuplicateCredentialError`, not its generic base type.
- Boolean, bytes, `None`, numeric, collection, arbitrary object, and PathLike-to-bytes values are rejected at the correct file boundary.
- A valid first file followed by an invalid second file produces no `StartupData`; the existing four JSON text-loader signatures and behavior remain unchanged.

## CLI evidence

- Parser tests prove both file arguments required, request fields all-or-none, advance modes mutually exclusive, and argparse integer conversion/exit 2 for floor/time syntax.
- Exact LF and HF grants pass; the exact 26 frame characters reach `Controller.submit` as a 26-member zero/one tuple. Lowercase source, short/nonbinary/parity-invalid frame, invalid floor, unauthorized, unknown, and disabled outcomes are delegated and remain process exit 0.
- Normal grant/advance returns output timeout at 3000. Manual reset occurs after request/advance. Suppression is applied before advancement and causes one idle or active watchdog reset at 2000 with no colliding output timeout.
- Every executed response line contains deterministic compact JSON. Final snapshot has the exact nine keys, exactly 16 Boolean channels, explicit nulls, and lowercase state. Events retain nine keys, explicit nulls, uppercase source, and lowercase event/result/reason. Repeated runs are byte-identical.
- Configuration/credential missing-file, duplicate-key, negative-time, controller-initialization, and logging failures return 1 with stable `error: ` stderr and no traceback. Normal access denial remains 0; syntax errors remain 2.
- AST/TOML inspection confirms only approved imports, no lookup/parity/field/mask/output/watchdog/event policy, no direct manager construction, no normal filesystem write, no global mutable runtime state, no wall clock/sleep/thread/async/network/database/GUI/hardware/subprocess, one console entry, no dependency change, and no CLI-helper package-root export.

## Real temporary-file smoke

Executed with the current external Python and `PYTHONPATH=src`:

```text
python -m elevator_access_sim.cli \
  --config /tmp/elevator-access-sim-sp06.8-v29Hnp/config.json \
  --credentials /tmp/elevator-access-sim-sp06.8-v29Hnp/credentials.json \
  --source LF \
  --frame 10000000100000000011001000 \
  --floor 1 \
  --advance-to 3000
```

Exit status was 0. Output contained `INITIALIZE` success, `SUBMIT` granted/authorized with floor 1 expiry 3000, `ADVANCE` completed/output_expired, an idle inactive `SNAPSHOT`, sequence-1 access-decision grant at timestamp 0, and sequence-2 output-timeout at timestamp 3000. No watchdog-reset event or external service/device/database/persistent output occurred. The temporary directory was removed and was never added to the repository.

## Final technical and scope validation

Executed `python -m compileall -q src tests`; package, `load_startup_files`, and all four CLI imports; signature/UTF-8/formatter/parser/delegation programmatic checks; `git diff --check`; changed-path/status review; protected SHA-256 comparison; cache cleanup; local-environment inspection; branch and HEAD checks. All passed.

Exactly the ten SP-06.8 ledger paths changed. Requirements, register model, architecture/diagrams, software design, test plan/inventory, implementation sequence, traceability, prior audits, domain models/managers/controller, existing tests, evidence/literature/PDF/bibliography/product/project/workflow material, dependency values, and Git history remained unchanged. No experiment, scalability, persistence, mutable administration, database/network/GUI/hardware/physical/additional-profile/optional-policy path was created. No repository-local virtual environment exists. No commit or push occurred.

READY FOR HUMAN REVIEW
