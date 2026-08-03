# SP-06.9 Stage Report

## Outcome

SP-06.9 completed the required integration inventory without changing production behavior. Starting from clean `main` commit `9a6c448f71e887ac6c47d3a3436c0fe2a644e4e0`, the prescribed baseline passed 859/859 under Python 3.13.13, pip 26.2, and pytest 9.1.1. Final validation passed 871/871 with no failures, skips, or xfails.

## Gap analysis and evidence

The 100 inventory rows were compared in original order with all 66 requirement rows, all 66 traceability rows, 859 collected baseline nodes, current source/test paths, prior SP-06 validation records, and the frozen implementation sequence. Existing tests already proved the required LF/HF, Wiegand, credential, authorization, output, timing, watchdog, reset, logging, startup, CLI, replay, and fault behaviors. The only behavioral gap was a single-controller public flow proving each representative invalid source, frame, parity, and floor request can be followed immediately by a valid grant.

One parameterized end-to-end function added four collected recovery cases. Eight collected inspection tests now cover title/approval, scope and change control, mutable-state ownership and CLI thinness, dependency/environment isolation, UTF-8/repository-relative paths, contextual limitation claims, cross-file identifiers, and the complete machine-readable resolution. No duplicate recovery or fault test module was necessary.

Inventory resolution is:

- 67 `implemented_existing`;
- 3 `implemented_sp06_09`;
- 0 `inspection_existing`;
- 18 `inspection_sp06_09`;
- 5 `scheduled_sp06_10`;
- 1 `scheduled_sp06_11`;
- 6 `optional_deferred`;
- 0 `unresolved`.

At requirement level, 54 required requirements have passing current evidence, five required experiment/reporting requirements remain explicitly owned by SP-06.10, one required final verification-record requirement remains explicitly owned by SP-06.11, and six optional requirements remain Post-MVP. Every requirement and planned test reference resolves.

## Completed behavior matrix

Mapped public-flow evidence includes successful LF grant/expiry, successful HF grant, unknown/disabled/unauthorized denials, hostile busy precedence, invalid-source/frame/parity/floor recovery, timeout recovery, manual-reset recovery, and watchdog recovery. The 11-path append-failure matrix retains the frozen grant gate and denial/busy/timeout/manual/watchdog policy, consumes no sequence on failure, and does not fabricate a logging-error event after a failed append.

The passing matrix covers all five `Result` members, all 17 `Reason` members, all six `EventType` serialization values, all seven controller states, all 16 authorization mask bits, all 16 controller output bits, six canonical Wiegand vectors, and all 24 canonical single-bit corruptions. Existing tests also cover exact timeout boundaries, 3000/2000 and 30000/2000 scheduling, watchdog/output collision priority, independent suppression epochs, large/partitioned advance equivalence, deterministic replay/JSON Lines, strict startup configuration and UTF-8 files, atomic initialization, and all CLI exits and formatting.

## Canonical records and ownership

The inventory resolution CSV contains exactly 100 UTF-8 rows with the required nine columns and concrete nodes or later-stage references. After mapped evidence passed, 88 Task-9-owned inventory statuses changed from `designed` to `implemented`; 12 SP-06.10, SP-06.11, and optional rows remain `designed`. The requirements-to-test traceability file contained no broken identifier and was not changed.

SP-06.10 continues to own reproducible generation, aggregate result export, required 10/100/1,000/10,000 scalability runs, metrics, and experiment reporting. SP-06.11 continues to own final verification-record and reproducibility reconciliation. No experiment, performance timing, aggregate output, optional behavior, persistence, database, network, GUI, hardware, reader, physical output, or hardware-watchdog file was created.

## Validation and scope

Final scoped results were 4/4 end-to-end, 192/192 integration, and 8/8 inspection. Collection found 871 nodes; the full suite passed 871/871 in 2.68 seconds. A focused enum/state/floor/vector matrix passed 97/97. Standard-library parsing validated 100 inventory rows, 66 traceability rows, and 100 resolution rows. Compilation and all required imports exited successfully.

The first baseline attempt omitted the prompt-required `PYTHONPATH=src` and therefore failed collection with package import errors; no edit preceded the corrected prescribed 859/859 baseline. During test development, pytest 9 rejected the parameter name `request`, and two initial inspection phrases were more exact than the frozen documents; these tests were corrected before evidence gating. No production defect was found or corrected. Production source, frozen requirements/design/architecture/register/sequence/decision/evidence/literature content, prior tests/audits, dependency policy, and Git history remain protected. No commit or push occurred.

READY FOR HUMAN REVIEW

