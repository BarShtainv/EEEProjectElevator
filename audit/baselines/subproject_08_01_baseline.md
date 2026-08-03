# SP-08.1 Baseline — Submission Gate and Report Evidence Architecture

- Repository `BarShtainv/EEEProjectElevator`, branch `main`, accepted starting commit `6ec20c1be8c0cbf64f4c04b695c343e59f75704e`.
- Initial `git status --short --untracked-files=all` was empty; no repository `AGENTS.md` was present.
- External environment: Python 3.13.13, pip 26.2, pytest 9.1.1; no installation or network access.
- Generated caches and bytecode only were removed before validation.
- Baseline: 1137 collected and 1137 passed in 26.78s; zero failures, skips, and xfails.
- SP-07.4R was accepted and its review summary, anomaly register, final ledger, source notes, and repair validation hashes matched the committed handoff.

## Principal report-evidence inputs

| Path | SHA-256 |
|---|---|
| `final_engineering_project_plan.md` | `fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33` |
| `README.md` | `55a9805251a3cebda92fd521fe2aaa938240ad9a497b90fe893943f7b03dfaf0` |
| `pyproject.toml` | `08ee535e4deae72e81a98efe380c158f97ed9ecafa6f21ee27b26455e0397e67` |
| `evidence/product_evidence.md` | `750b241c3400b88b82c5a78c50d2c75d7a636a632caccded3493ef51ec281361` |
| `evidence/assumptions_and_unknowns.md` | `d7b54357cb414f8df32f4d99684ac0e02146d6993341652cc3f15fe5ab578911` |
| `evidence/claim_evidence_matrix.csv` | `f8a4031d92a47e816f132456e1e68e145f8104689f83ec765e96e82730ab1d66` |
| `evidence/source_index.md` | `639907f1a611c0e47c5eb553e261b96e2ce7a1864e83f0fd3046eeba50f7c868` |
| `evidence/unresolved_sources.md` | `9c90e807990f24ccb7ce9f5088cecf0dc4b1d788aa06b26216baab846c013102` |
| `evidence/literature_notes.md` | `a9b0c3480e27fbe092fbe96b04bc954f7c7981f6eabc819cdc6cd33c0130de52` |
| `docs/methodology.md` | `a5b109d4f614e80de8fb66416748a0738afdef3e891a0bd151317e1c6f6c9a7c` |
| `docs/literature_review_outline.md` | `ffc4bb71ea1eaa960b3b1b00e31b39edadcddcbad416d116e0c02632f8b6bc0a` |
| `docs/requirements.md` | `9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d` |
| `docs/architecture.md` | `89ac9f0925fa0a29d2d690dc86e10ebec3223b20208158dfb6a1c95a19d2a4d5` |
| `docs/register_model.md` | `f2b836e963de52ccce035277b326601815b2928c1343ac80d3afe547c9106466` |
| `docs/software_design.md` | `82401d922484036bd1e011a6068dbef02f3b07bdbe355e9d1fc868e74fdf9476` |
| `docs/test_plan.md` | `8c8c28760d2ef28d23480896180eabcb81b4d187aa88abb697758e1bcfd325bf` |
| `docs/test_case_inventory.csv` | `ce97fca1b72521536ffc85a4fe22c7cb8cf26f3dbb4220e1db394667e9178601` |
| `docs/requirements_to_test_traceability.csv` | `e830fb840375e574d342073b285987b574fdaa76d80613e40d558f7b96bb2289` |
| `docs/architecture_to_requirements.csv` | `629c4e986e38aff724dc5cdbe8241232ede81c03c8c216fba60993102660f4b9` |
| `docs/decision_log.md` | `9f41034d1ceefb914f106b49e891937a14fdc903d08cd19d65fbda42a597d3ee` |
| `docs/reproducibility.md` | `573e17ddff8dd420f4882938a6a014f258cef4bdb9e591c68fedcdf988b3038e` |
| `data/results/sp07_report_artifact_manifest.json` | `69235fab571b97e00b54f4a8dd202e8331dadbf381dcd8caa0c2250f4ed44851` |
| `data/results/sp07_independent_review_summary.json` | `52a2f9ca0b13945e2cdbf7327c7d81d53512beedfe2c998a6be0b4c7d2c4ae1a` |
| `data/results/sp07_anomaly_register.csv` | `cafaddaef88faeeedecca6d312a2c71ebdc0cae339ca1b66143e5de2f4ca5d88` |
| `audit/validation/subproject_07_final_validation_ledger.csv` | `c0db9e213c7f2c2ddaf35baff3cc9f1a383c078de47cce03ed3aefee56f07745` |
| `docs/sp07_results_discussion_source_notes.md` | `6fbfdb192b9ce7b184b1901cf454d5de5e1d470302e288d41074d62a062281e6` |
| `audit/validation/subproject_07_04_validation.md` | `2e3c60c322975f0df833678768a92349995d49b9fd3978ecc2735005a2e038d6` |
| `audit/validation/subproject_07_04_repair.md` | `4d75d41c47fcc16ea6ea2e0db8888c1cafba9ebaabd1535ead4521ff87dc4d72` |

## Submission handoff

- Working title: project-owner-approved working value; supervisor approval pending.
- Supervisor approval: pending.
- University/department template: unavailable in the repository.
- Report language: unresolved.
- Original product capture: unavailable; product URLs only.
- Accepted report-ready quantitative assets: three CSV tables and three SVG figures, all matching `SP07_REPORT_ARTIFACTS_V1`.
- Authoritative unresolved inputs include official title, institution/program and identity fields, language, template/format, citation style, deadline/schedule, university rules, product-image permission, physical-component expectation, and defense/submission details.

Authorized paths are the five `report/` planning registers, `tests/inspection/test_report_preparation.py`, this baseline, `audit/stage_reports/subproject_08_01.md`, `audit/validation/subproject_08_01_validation.md`, and an appended `audit/file_change_ledger.md` section. All production code, existing tests/documents/evidence, SP-07 artifacts, literature/PDFs, report bibliography source, and Git history are protected.

SP-08.2 report source/prose, SP-08.3 presentation/demonstration/defense work, and SP-08.4 rendering/release/checksum/archive/tag work remain deferred pending the recorded human gates.
