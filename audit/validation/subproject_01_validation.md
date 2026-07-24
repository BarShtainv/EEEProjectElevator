# SP-01 Validation

## Commands run

| Check | Command or method | Result |
|---|---|---|
| Workspace and Git baseline | `pwd`; `git rev-parse --show-toplevel`; `git branch --show-current`; `git rev-parse HEAD`; `git status --short`; `git log -5 --oneline` | Root confirmed; initial branch `main`; commit `9e46275db11b6ffd8acec11f4470554bda781c86`; initial status `?? prompt.txt`. |
| Instruction/document inventory | Shallow `find`, `rg --files`, and direct reads of applicable files | Required plan and workflow documents read; no local `AGENTS.md`, `CONTRIBUTING.md`, `WORKFLOW.md`, or `PROJECT_PLAN.md` found. |
| Product-evidence inventory | Filename and media inventory outside `.git/` | No local product images, snapshots, listing exports, or seller statements found. |
| URL access | Non-authenticated direct open of canonical AliExpress URL | Non-retryable access error; no content preserved and no bypass attempted. |
| Source inventory | Shallow `find` of `literature/` and `referenceProject/`; SHA-256 calculation | Seven PDFs indexed; no broad literature analysis performed. |
| Required files | `find audit evidence -maxdepth 4 -type f -print | sort` | All eight required SP-01 files exist. |
| Markdown readability | UTF-8 decode check | Passed. |
| CSV validation | Inline Python standard-library `csv` check | Passed; expected header and nine columns in every row. |
| Image hash comparisons | Search for product-image source/copy pairs | Not applicable: no image source or copy exists. |
| Whitespace | `git diff --check` | Passed. |
| Changed-path review | `git diff --name-only` and `git status --short` | No tracked-file diff; new allowed files are untracked, alongside pre-existing `prompt.txt`. |
| Forbidden-path review | Compare created paths against SP-01 allowed paths | Passed: no forbidden path modified. |
| Unsupported-assertion review | Manual search/review for `STM32`, `STM32F103`, `ARM`, `relay`, `Wiegand`, `125 kHz`, `13.56 MHz`, `voltage`, `current`, and `elevator control` in evidence files | Passed: no unsupported claim connects these terms to the commercial product. |

## Relevant command outputs

Initial Git status was:

```text
?? prompt.txt
```

Initial recent history was:

```text
9e46275 GeneralSources
d1643de Initial commit
```

## Required-file checks

The following required files are present:

- `audit/baseline.md`
- `audit/file_change_ledger.md`
- `audit/stage_reports/subproject_01.md`
- `audit/validation/subproject_01_validation.md`
- `evidence/product_evidence.md`
- `evidence/assumptions_and_unknowns.md`
- `evidence/claim_evidence_matrix.csv`
- `evidence/source_index.md`

The required empty evidence directories also exist: `evidence/images/` and `evidence/snapshots/`.

## Final Git status

Final checks completed on 2026-07-24. `git diff --name-only` produced no output because all SP-01 artifacts are new and untracked. `git diff --check` produced no output, indicating no whitespace errors in tracked diffs. Final `git status --short` was:

```text
?? audit/
?? evidence/
?? prompt.txt
```

`prompt.txt` is the pre-existing task instruction file. `audit/` and `evidence/` are the new, allowed SP-01 paths. No tracked or forbidden path was modified.

## Unresolved validation issues

- Image-copy hash comparisons are not applicable until original product images are supplied.
- No listing-content assertion can be validated until a listing capture, screenshot, export, or accessible public page is available.
