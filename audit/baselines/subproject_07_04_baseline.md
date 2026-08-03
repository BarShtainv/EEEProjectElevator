# SP-07.4 Baseline — Independent Quantitative Claim Review

- Repository `BarShtainv/EEEProjectElevator`, clean `main`, accepted commit `7b6ad373014e047ac454d11578f18a017d462057`.
- No repository `AGENTS.md`; external environment `/home/bar/.venvs/eeeproject-elevator` used without installs or network.
- Python 3.13.13; pip 26.2; pytest 9.1.1.
- Generated caches/bytecode only were removed before validation.
- Baseline: 1106 collected and 1106 passed in 24.13s; zero failures, skips, and xfails.

## Canonical review inputs and SHA-256

| Path | SHA-256 |
|---|---|
| `final_engineering_project_plan.md` | `fd761e0e9d8b1db9c52e16234762019ff9a8deaeeb1722ae110219ae4ef15e33` |
| `docs/requirements.md` | `9a29af817336f73a8f2ecf4a0b9731fdd32765fd8f2bed2ad3b78003085a202d` |
| `docs/test_case_inventory.csv` | `ce97fca1b72521536ffc85a4fe22c7cb8cf26f3dbb4220e1db394667e9178601` |
| `docs/requirements_to_test_traceability.csv` | `e830fb840375e574d342073b285987b574fdaa76d80613e40d558f7b96bb2289` |
| `audit/validation/subproject_06_11_verification_records.csv` | `623032dabefa0cd983812527ab09ba719a00998f1d3e6204ecea5fbe17da4e42` |
| `data/results/sp07_experiment_catalog.csv` | `c9a8568d1c64988aa694f6d9ad64578fac922ed1df8325c5b109d4ff1986f1cb` |
| `data/results/sp07_quantitative_summary.json` | `dc168fec1b5f5cb018fd9be818c4c27a7015317ded36e52a4a2079dd070a9cc0` |
| `experiments/scalability_config.json` | `93ec68084c3b07c9badbb4e2f5d150d962fb8dceae7b4f092eb7909331491921` |
| `results/scalability_results.json` | `009381bf10bc74042b02abc4a12fe0a04b29437de3288b868f04d4cce1addc4f` |
| `results/scalability_environment.json` | `ed91091102ab910ceb28cc99f5bc9d7124d0b673261b65d476f5a91cbb8de4ba` |
| `audit/validation/subproject_06_10_validation.md` | `e6dc96bb105bf1af02ee170faf0c541f5a72f8e69686cfcfa6aca67f0d57f8d5` |
| `experiments/isolated_operations_config.json` | `6668ba4b744ef2a708dbdc471457751535370d4baba2d9754ec8589c1e299838` |
| `data/results/sp07_isolated_operation_results.json` | `9d8edd077439a12000cc560c615208dff0f381a5b77f3c8474b3b92b4e540bdf` |
| `data/results/sp07_isolated_operation_environment.json` | `106eba0f338b2cbb215dbbd7536d2814985843856b650b749a983710ad55f7ec` |
| `audit/validation/subproject_07_02_timing_boundary_repair.md` | `1524a88db09641bd5f31a0411341d0e0e9b454ff2502ea99948fefc50879ef90` |
| `data/results/sp07_experiment_catalog_integrated.csv` | `9270a15ca480a78ade0e5685ca1dd41a246aa9b4e824cc5cd80304ca96916ff8` |
| `data/results/sp07_quantitative_summary_integrated.json` | `95f532d8c6a03603df93c1324c5f0bcb5ed0b21fea6a8defba472ec7114d670c` |
| `data/results/sp07_table_experiment_coverage.csv` | `f7aef89308e316dbfabb94f166b488294271fcf2a9c66c3e2631a5b4546ec78f` |
| `data/results/sp07_table_correctness.csv` | `2ee80a42df288fef0bdd2357fb09a562ddd364c18a7b25259e7c29d8b7b84224` |
| `data/results/sp07_table_timing_summary.csv` | `5c777e8f77b0c5e06f44e5c0a0b810e464dff663dfa2bfd47f9d18e09eaf0811` |
| `docs/figures/sp07_mixed_controller_average_ns.svg` | `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930` |
| `docs/figures/sp07_lookup_average_ns.svg` | `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096` |
| `docs/figures/sp07_authorization_average_ns.svg` | `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9` |
| `data/results/sp07_report_artifact_manifest.json` | `69235fab571b97e00b54f4a8dd202e8331dadbf381dcd8caa0c2250f4ed44851` |
| `audit/validation/subproject_07_01_validation.md` | `675bb96506ef931c0ec2e26f15cf1ce3d61fe23540ff703d5c6ffbed83cfbd1e` |
| `audit/validation/subproject_07_01_repair.md` | `a4b14d0d7eed99c8049b2b2cf6b6ecfb2af9a1396db8b5016000f194c7dc6da6` |
| `audit/validation/subproject_07_02_validation.md` | `9849892b76a383b2b411b6cd46227e6d6d6741a92611c53f4f1d1c107d6a9775` |
| `audit/validation/subproject_07_03_validation.md` | `896a6d38b952f18e73ba2dda1dbd4e94e869ae7bc65d49f0b52a729d405d6a9d` |
| `audit/validation/subproject_07_03_repair.md` | `e0d00c7b948ffbb3836836807437ee610dd8f3f7d966baf4ec9723814c6b0b9b` |

The accepted manifest is `SP07_REPORT_ARTIFACTS_V1`, with nine sources and eight nonrecursive generated artifacts. Accepted counts are seven experiments, 22 correctness rows, 12 timing rows, and three SVGs.

Only the independent review script, four review outputs, focused tests, this baseline, SP-07.4 stage/validation records, and an appended ledger section are authorized. Every measurement, table, figure, manifest, catalog, summary, simulator/test/governance artifact, prior audit, and report/presentation path is protected.

Independence requires standard-library parsing and recalculation without importing existing analysis, experiment, or simulator code. Known threats include one host, three repetitions, no raw samples/pooled inference, unequal mixed request counts, differing operation boundaries, deterministic constructed correctness workloads, timing variation/non-monotonicity, absent branch coverage, and no physical/real-time/safety/commercial evidence. Subproject 8 remains deferred.
