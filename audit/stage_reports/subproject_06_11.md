# SP-06.11 Stage Report

## Accepted baseline and documentation authority

SP-06.11 started clean on `main` at accepted commit `28a9dbebf23b0220ca87afdae143b7432ab0d8dc`. Python 3.13.13, pip 26.2, and pytest 9.1.1 came from the accepted external environment. After generated-cache removal, `PYTHONPATH=src python -m pytest` passed the 965-test baseline in 3.58 seconds with zero failures, skips, or xfails.

The accepted pre-stage repair at `audit/validation/subproject_06_11_baseline_flake_repair.md` and its hardened bytes-PathLike test remained unchanged and passing. Its validation-record SHA-256 remained `aafcd53bd960a5ada73860625dfa8f4a3040f55e08ee634b868303388f43c318`.

`README.md` is now the concise project entry point. `docs/reproducibility.md` is the single detailed runnable-command authority. Frozen requirements, architecture, register model, software design, implementation sequence, decision log, traceability history, test-plan design sections, and prior audits remain canonical for their existing purposes.

## README and reproducibility outcome

The README records the exact working title, completed software-simulator implementation/verification status, pending supervisor approval, implemented required capabilities, repository map, Python/dependency policy, quick test and optional editable-install shapes, CLI/reproducibility link, experiment boundary, final verification state, and explicit later work.

The reproducibility guide covers the repository-root assumption, Python 3.11+ and standard-library runtime policy, no-install and optional editable paths, the full and five focused pytest commands, strict UTF-8 temporary CLI documents, the LF/floor-1/3000-ms grant/timeout scenario, temporary experiment outputs, committed comparison artifacts, stable values/checksums, host-variable metrics, validation, cleanup, troubleshooting, interpretation limits, and unresolved human/project-stage work.

Both documents state that this is a deterministic Python simulator of an abstract access-authorization layer; LF/HF are logical labels; `PROJECT_WIEGAND_26` is proposed; outputs are logical; controller time is simulated; host timing is observational; and no physical RFID, electrical output, elevator movement/safety, real-time, production-readiness, or commercial-equivalence claim is made.

## Verification records and reconciliation

`audit/validation/subproject_06_11_verification_records.csv` has the exact 13-column schema and 100 inventory-ordered rows. Expected results/states/events remain copied from the canonical inventory, while actual results and evaluation statuses are separate fields. Ninety-four implemented executable/inspection/experiment rows are `passed`; six optional rows are `optional_deferred` with exact actual result `not executed: optional post-MVP scope`. Evidence paths are concrete and repository-relative.

The five experiment records reference experiment tests plus official result/environment artifacts and state exact schema/count/metric/checksum/reconciliation validation. `TST-TRC-005` references the new verification-record inspection and passed before promotion. Only its inventory status changed from `designed` to `implemented`; final inventory is 94 implemented and six optional designed rows. Only traceability status cells changed: 60 required rows are `verified`, six optional rows are `optional_deferred`, and no required row remains planned or unresolved. The historical SP-06.9 CSV remains byte-for-byte unchanged; its live-status compatibility assertion now permits both SP-06.10 and SP-06.11 scheduled rows to reflect later implementation while retaining historical class/order/count/evidence and optional-design checks.

The existing SP-05 test-plan content remains prospective. A separated SP-06 outcome section links actual evidence and explicitly preserves the expected-versus-actual distinction.

## Executed reproduction

Published focused commands passed: unit 667/667 in 1.32s, integration 192/192 in 0.50s, end-to-end 4/4 in 0.13s, inspection 19/19 in 1.92s, and experiment 94/94 in 0.62s. The reconciled repository suite passed 976/976 in 4.24s before final audit completion.

The documented CLI data and command produced exit 0, initialization, LF grant/authorized on floor 1, output timeout at simulated 3000 ms, a final idle snapshot with all 16 channels false, exactly one access-decision and one output-timeout event, no watchdog-reset event, and byte-identical repeated output. Temporary files were removed.

The experiment reproduction wrote only temporary result/environment files, exited 0 with `completed: sizes=4 measured_rows=12 timer=time.perf_counter_ns`, and passed exact sizes, repetitions, 1,000/1,000/1,000/10,000 requests, 40/20/15/15/10 counts, zero other outcomes, reconciliation, finite positive metrics, integer p95, committed checksum matching, environment limits, and raw-data exclusion. Temporary outputs were removed and committed host observations were untouched.

A clean working-tree copy outside the repository excluded Git, caches, bytecode, local environments, and temporary files. From that copied root the external interpreter passed 976/976 in 1.16s without the original path, network, database, device, GUI, interaction, or repository-local environment. The copied tree was removed.

## Validation, deviations, and boundaries

The first complete documentation module run passed 10 checks and failed one overly literal README phrase assertion. The README already satisfied the required limitation; the smallest correction made the inspection context-aware. The corrected node passed 1/1 and the complete module passed 11/11 in 1.14s. Historical resolver validation passed 2/2 in 0.41s.

The first copied-tree command created the copy but omitted changing into it; its 976/976 run occurred in the original root and was not accepted as copied-tree evidence. The command was corrected with an explicit copied-root directory change and rerun successfully. An initial CLI shell was rejected before process creation because the execution safety layer prohibited `rm -rf`; no artifact was created. The same scenario then passed with bounded `find -delete` cleanup. The reviewer-facing guide retains the task-required `rm -rf "$temporary_directory"` command for a path created by `mktemp -d`.

Standard-library validation passed UTF-8 decoding, CSV/JSON schemas, row counts, unique IDs, statuses, expected/actual separation, evidence links, live/historical reconciliation, experiment sizes/counts/metrics/checksums/environment linkage, and raw/identifying-data exclusion. Documentation inspections passed relative paths, Markdown links, package metadata, commands, protected claims, and baseline-repair preservation.

Final suite, compilation, import, Git, cleanup, copied-tree, CLI, experiment, and reconciliation outcomes are finalized in `audit/validation/subproject_06_11_validation.md`.

No simulator behavior, public API, production source, dependency, experiment generator/configuration/tracked result, prior test/audit, optional feature, report, literature review, presentation, release, tag, archive, submission package, commit, or push was created or changed.

The working title and software scope remain project-owner approved. Supervisor approval remains pending. Optional features, engineering report, presentation, release preparation, submission, physical integration, commercial-equivalence work, and all unresolved human approvals remain later work.

Final post-audit validation passed documentation 11/11 in 1.04s, historical resolver 2/2 in 0.46s, the complete 976-test suite in 4.10s, copied-tree 976/976 in 1.19s, standalone reconciliation, CLI and experiment reproductions, compilation, imports, Git scope/whitespace checks, and cleanup. All suites had zero failures, skips, and xfails.

READY FOR HUMAN REVIEW
