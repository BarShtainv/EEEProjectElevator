# SP-01 Baseline

- **Stage ID:** SP-01
- **Stage name:** Repository baseline and product-evidence preservation
- **Baseline observed:** 2026-07-24T13:56:19+03:00
- **Initial working directory:** `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`

## Selected project root

Selected root: `/mnt/c/Users/Bar/Desktop/EEEProjectElevator`.

It is correct because it is the current workspace, contains the project README, operating plan, source-material directories, and the Git top-level directory reported by `git rev-parse --show-toplevel`.

## Initial repository state

| Field | Observed value |
|---|---|
| Git repository | yes |
| Repository root | `/mnt/c/Users/Bar/Desktop/EEEProjectElevator` |
| Current branch | `main` |
| Current commit | `9e46275db11b6ffd8acec11f4470554bda781c86` |
| Recent commits | `9e46275 GeneralSources`; `d1643de Initial commit` |
| Initial `git status --short` | `?? prompt.txt` |
| Pre-existing task-relevant modified/untracked files | `prompt.txt` was untracked and contains the SP-01 instructions. It is protected and not modified by this stage. |

The baseline was not clean: Git reported the pre-existing untracked `prompt.txt`.

## Applicable instructions and canonical documentation

| Path | Role |
|---|---|
| `prompt.txt` | Task-specific SP-01 instructions; pre-existing and protected. |
| `final_engineering_project_plan.md` | Canonical durable project plan and stage acceptance criteria. |
| `general_purpose_evidence_gated_workflow_handbook_updated.md` | Project workflow guidance. |
| `README.md` | Existing repository overview. |

No `AGENTS.md`, `CONTRIBUTING.md`, `WORKFLOW.md`, or `PROJECT_PLAN.md` was found within the selected project root. No nearer instruction file applies to the created `audit/` or `evidence/` paths.

## Existing material at baseline

| Category | Paths or result |
|---|---|
| Major directories | `.git/`, `.agents/`, `.codex/`, `literature/`, `referenceProject/` |
| Canonical documentation | `README.md`, `final_engineering_project_plan.md`, `general_purpose_evidence_gated_workflow_handbook_updated.md` |
| Existing `audit/` directory | absent |
| Existing `evidence/` directory | absent |
| Product-evidence files, images, and snapshots | none found in the workspace |
| Technical source documents | Six PDFs in `literature/`; one PDF in `referenceProject/`; inventoried in `evidence/source_index.md` |

## Protected paths and material

- `prompt.txt` and all pre-existing tracked files.
- `literature/` and `referenceProject/` source PDFs.
- Any original product images, listing screenshots, or snapshots if later supplied.
- Both owner-supplied AliExpress URLs, preserved verbatim in `evidence/product_evidence.md`.
- Existing Git history and the `main` branch.

## Missing expected inputs, ambiguities, and risks

- The plan says three product images were available in a working context, but no image file exists in the baseline workspace.
- No listing text, screenshot, exported capture, seller statement, or readable product marking is locally available.
- Direct access to the canonical URL on 2026-07-24 returned a non-retryable error; no bypass was attempted.
- The exact manufacturer, model, revision, hardware, firmware, interface, and electrical characteristics remain unresolved.

## Task-created paths

The following paths did not exist at baseline and were created by SP-01 only: `audit/` and `evidence/` contents listed in `audit/file_change_ledger.md`.
