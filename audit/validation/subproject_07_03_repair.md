# SP-07.3R Validation — Catalog Semantics and Publication Rollback Repair

## Accepted state and baseline

| Gate | Exact result |
|---|---|
| Repository | `BarShtainv/EEEProjectElevator`, branch `main`, exact starting commit `a4f458ee8cf1065b5b45aff8403fdce248ab972d` |
| Initial state | Clean status, accepted recent history, no repository `AGENTS.md`, all SP-07.3 artifacts present |
| Environment | Python 3.13.13, pip 26.2, pytest 9.1.1 from `/home/bar/.venvs/eeeproject-elevator`; no installs or network |
| Cache cleanup | Removed only generated Python/pytest caches and bytecode |
| Baseline | `PYTHONPATH=src python -m pytest`: 1103 collected/passed in 23.66s; zero failures/skips/xfails |

Existing SP-07.3 baseline, stage, and validation records remain unchanged historical evidence.

## EXP-05 semantic repair

The integrated catalog inherited this historical planned question:

> What mixed controller request-processing host timing is present across 10, 100, 1000, and 10000 credentials, and which isolated measurements are still absent?

That wording was stale after the accepted isolated lookup and authorization evidence. Historical SP-07.1 remains unchanged, including its valid former gap. Only the integrated EXP-05 construction now uses exactly:

> What do the accepted mixed Controller.submit and isolated CredentialRepository.lookup and authorize host-software measurements show across 10, 100, 1000, and 10000 credentials within their stated operation boundaries and limitations?

An explicit semantic validator requires that exact question, all three operation names, all four sizes, boundaries, and limitations; rejects missing-evidence wording; preserves the EXP-05 ID/name/mapped IDs, complete-with-limit status, mixed and isolated evidence/artifacts, scope, and SP-07.4 action; and requires all six other rows to equal their historical content. A negative regression restoring the stale question fails validation.

## Publication rollback repair

The former publisher created backups immediately before each replacement, stopped rollback on the first restoration error, then unconditionally deleted all backups in `finally`. A failed restoration could therefore prevent remaining restorations and silently delete the only recovery copy while the propagated error could still imply preservation.

The repaired algorithm:

1. validates/builds all artifacts and stages every sibling temporary file;
2. preserves every existing destination before replacing any destination;
3. publishes in deterministic mapping order and validates published bytes;
4. after an `ArtifactError` or filesystem failure, attempts restoration for every replaced destination even after a restoration error;
5. collects bounded artifact keys, retains each failed restoration's backup, removes only safely unused/consumed backups and all staged new files;
6. raises exactly `artifact publication failed; existing outputs were preserved` after complete rollback;
7. otherwise raises `artifact publication failed; rollback incomplete; recovery backups retained: ...` with artifact keys and backup basenames only.

Unrelated programming exceptions are not relabeled as ordinary publication failures. No retries, sleeps, concurrency, or external transaction dependency was added.

The retained normal failure regression confirms all old bytes and zero temporary files. The new incomplete-rollback regression injects a fourth-output publication failure plus first-output restoration failure; restoration is attempted for all three replaced outputs, the other two restore, all five untouched outputs retain old bytes, the failed destination retains new bytes, exactly one original-byte backup remains, and all staged/other backups are absent. After disabling injection, that retained backup restores the destination and is consumed. The CLI regression returns 1 with exactly one relative, traceback-free `error: ... rollback incomplete ...` line and no false preservation claim.

## Tests, regeneration, and hashes

| Check | Exact result |
|---|---|
| Focused suite before regeneration | 29/29 passed in 0.88s; zero failures/skips/xfails |
| First repaired full suite | 1106/1106 passed in 22.74s; zero failures/skips/xfails |
| Official generation 1 | Exit 0; `completed: experiments=7 timing_groups=3 timing_rows=12 svg_figures=3 manifest_artifacts=8` |
| Official generation 2 | Exit 0 with the same completion line and byte-identical hashes |

Only the expected generated hashes changed:

- integrated catalog: `b86c084193ecf38cc70eb35bbac32a063266843bae724b3f4a58817d4a81db9a` → `9270a15ca480a78ade0e5685ca1dd41a246aa9b4e824cc5cd80304ca96916ff8`;
- manifest: `f4fe7d5181310d731919dea350abefe13d2c753948d1d40aa90d9f00e14816b1` → `69235fab571b97e00b54f4a8dd202e8331dadbf381dcd8caa0c2250f4ed44851`.

Unchanged generated hashes:

- integrated summary `95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c`;
- coverage table `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f`;
- correctness table `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224`;
- timing table `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811`;
- mixed SVG `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930`;
- lookup SVG `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096`;
- authorization SVG `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9`.

The separate standard-library validator did not import the generator and printed `INDEPENDENT_VALIDATION=PASS catalog=7 repaired_exp05=exact unchanged_artifacts=7 manifest=8 mixed=39000 isolated=24000`. It confirmed the historical question, repaired integrated question, six unchanged rows, question-only EXP-05 delta, unchanged quantitative totals/timing statistics/SVG bytes, updated manifest catalog hash, every remaining manifest hash, deterministic output, and all accepted-source bytes unchanged.

## Final validation and scope

| Check | Exact result |
|---|---|
| Final focused suite and rollback recovery | 29/29 passed in 0.91s; zero failures/skips/xfails. Dedicated recovery rerun: 1/1 passed in 0.26s (28 intentionally deselected); retained backup restored and consumed. |
| Final full suite | 1106 collected/passed in 24.19s; zero failures/skips/xfails |
| Compilation and imports | `python -m compileall -q src tests scripts analysis`, `import elevator_access_sim`, and `from elevator_access_sim import Controller` all exited 0 |
| Independent and deterministic checks | Repeated validator passed exact question, six rows, seven unchanged artifacts, eight manifest entries, and nine sources; two successive complete hash sets were identical |
| Git, protected scope, and cleanup | `git diff --check` passed; exact `main` and accepted HEAD; exactly six authorized paths; no caches, bytecode, `.tmp`/recovery files, local environment, raw input/timing collection, benchmark output, raster/report/release addition, or protected-path change |

No benchmark runner was executed. No accepted measurement, correctness data, configuration, historical SP-07.1 output, corrected SP-07.2 output, unchanged table/figure, simulator, report, presentation, release, SP-07.4, or Subproject-8 artifact changed. No commit or push occurred.

READY FOR HUMAN REVIEW
