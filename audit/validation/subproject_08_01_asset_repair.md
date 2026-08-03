# SP-08.1R Validation — Canonical Report-Diagram Asset Coverage Repair

## Accepted handoff and baseline

- Repository: `BarShtainv/EEEProjectElevator`; branch: `main`.
- Accepted starting commit and unchanged HEAD: `2dfca70fc896762d5c1238af0d8e3ff8b1760ba0`.
- Initial working tree: clean; no conflicting user changes and no repository `AGENTS.md` were present.
- External environment: Python 3.13.13, pip 26.2, pytest 9.1.1 from `$HOME/.venvs/eeeproject-elevator`; no dependency installation or network access occurred.
- Generated caches and bytecode only were removed before the baseline.
- Baseline: 1153 collected and 1153 passed in 26.29s; zero failures, skips, and xfails.
- The existing SP-08.1 baseline, stage report, and validation report remain unchanged historical records.

## Defect and bounded repair

The accepted 16-row asset register included three of the seven Mermaid sources referenced by `docs/architecture.md`: `docs/figures/top_level_architecture.mmd`, `docs/figures/controller_state_machine.mmd`, and `docs/figures/data_flow.mmd`. It omitted four canonical sources also required by the architecture and proposed by the report outline:

| Asset ID | Appended canonical path | Chapter | Preserved boundary |
|---|---|---:|---|
| `AST-017` | `docs/figures/system_context.mmd` | 2 | Logical LF/HF labels and abstract permission outputs only; no physical reader, elevator interface, safety behavior, or commercial equivalence. |
| `AST-018` | `docs/figures/firmware_architecture.mmd` | 7 | Project simulator module responsibilities only; no commercial firmware, MCU selection, or hardware execution. |
| `AST-019` | `docs/figures/reset_sequence.mmd` | 7 | Simulated startup/manual/watchdog reset behavior only; no physical fail-safe or safety-certification result. |
| `AST-020` | `docs/figures/watchdog_sequence.mmd` | 7 | Simulated monotonic time only; no MCU-watchdog equivalence, real-time, reliability, or physical-safety result. |

All four are `diagram` assets with repository-relative, resolving source artifacts and `needs_export` status. AST-017 permits export only after report format, language, and rendering method approval; AST-018 through AST-020 permit later controlled export only. The original AST-001 through AST-016 field sequence has SHA-256 `cf6705e29eafd44e2796978984b6df0630e60d568a37fa721ded6dff09614ed3` under the regression serialization and remains unchanged. The final register has exactly 20 ordered rows.

## Reconciliation and protected evidence

- Independent parsing found exactly the expected seven unique `docs/figures/*.mmd` paths in `docs/architecture.md`; each exists and is registered exactly once.
- Every explicit Mermaid path in `report/report_outline.md` is registered. Its proposed system-context, top-level, firmware/responsibility, data-flow, state-machine, reset, and watchdog content all reconcile with the seven registered sources.
- All Mermaid rows use `asset_type=diagram` and `readiness_status=needs_export`; all interpretation limits and source-artifact paths are nonempty and resolve.
- No SVG, PNG, PDF, JPEG, WebP, BMP, or TIFF counterpart exists for any canonical Mermaid source. No diagram content changed and no diagram was rendered.
- The product-image row remains `missing`; no image or permission state changed.
- The accepted SP-07 report assets remain byte-identical to `SP07_REPORT_ARTIFACTS_V1`:
  - coverage table `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f`;
  - correctness table `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224`;
  - timing table `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811`;
  - mixed-controller SVG `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930`;
  - lookup SVG `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096`;
  - authorization SVG `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9`.
- The submission register, report outline, claim-source matrix, and bibliography-readiness register match their accepted HEAD bytes. Twenty-five unresolved human/unavailable entries still block SP-08.2.

## Validation evidence

- Focused inspection: 20 collected and 20 passed in 0.49s; zero failures, skips, and xfails. Coverage includes exact 20-row order, the immutable original-row digest, exact repair rows, independently parsed architecture references, outline references, technical boundaries, source resolution, export absence, duplicate prevention, and removal of each of the seven registrations.
- Independent standard-library validation imported no test module and printed: `ASSET_REPAIR_VALIDATION=PASS total_assets=20 mermaid_assets=7 sp07_accepted_assets=6 missing_canonical_diagrams=0 duplicate_paths=0`.
- First post-repair full suite: 1157 collected and 1157 passed in 25.53s; zero failures, skips, and xfails.
- Python compilation and imports: `python -m compileall -q src tests scripts analysis`, `import elevator_access_sim`, and `from elevator_access_sim import Controller` exited successfully.
- `git diff --check` passed. Initial scope inspection showed only the two implementation paths before this audit was added.

The post-audit focused rerun collected 20 and passed 20 in 0.43s. The final full suite collected 1157 and passed 1157 in 25.57s. Both had zero failures, skips, and xfails.

## Scope, cleanup, and readiness

SP-08.1R changed only the asset register, its inspection tests, this repair record, and the appended file-change ledger section. It did not alter production source, canonical diagrams, accepted SP-07 artifacts, quantitative data, requirements, architecture, report outline, claim or bibliography registers, dependency metadata, or historical audits. It did not run a benchmark, draft report prose, create report source, render/export a diagram, create a PDF/presentation/archive/release artifact, begin SP-08.2, commit, or push.

Final cleanup removed `.pytest_cache/`, all `__pycache__/` directories, and all `*.pyc`/`*.pyo` files. No temporary CSV fixture, validator/comparison file, or orphaned `.tmp` file remained. Final Git scope contains exactly the four authorized paths recorded in the ledger; `git diff --check`, protected-path comparison, and untracked-file inspection pass. No repository-local environment, diagram export, report source, PDF, presentation, archive, or release artifact was created.

Human resolution remains required for at least report language, university/department template or explicit template-neutral drafting authorization, official or approved working title, student and supervisor identities, citation style, and submission deadline/interim schedule. Product imagery additionally requires an original preserved source, provenance, and reproduction permission.

`READY FOR HUMAN REVIEW`
