# Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller

## Project identity

This repository contains the completed implementation and automated verification package for a deterministic Python software simulator of an abstract access-authorization layer. The working title and software scope are project-owner approved; supervisor approval remains pending.

The model is software-only. LF and HF are logical reader-source labels, `PROJECT_WIEGAND_26` is a proposed project profile, and the 16 outputs are logical permission channels. The repository does not model a physical RFID reader, electrical outputs, elevator movement, or any safety function, and it establishes no equivalence with a commercial controller.

## Implemented capabilities

- Strict validation, parity checking, encoding, and decoding for the proposed `PROJECT_WIEGAND_26` profile.
- LF/HF logical source metadata retained independently of credential bits.
- Strictly validated in-memory credential repository and 16-floor mask authorization.
- At most one active logical output, deterministic simulated timeout, and simulated controller time.
- Simulated watchdog service suppression, fault injection, reset, and recovery.
- Immutable event records, atomic sequence ownership, and deterministic JSON Lines export.
- Strict UTF-8 configuration and credential startup files.
- Thin offline command-line demonstration.
- Deterministic scalability generation and aggregate host-timing runner.
- Unit, integration, end-to-end, inspection, and experiment verification.

Optional profiles, additional authorization policies, persistence, enhanced interfaces, physical adapters, and extra experiment sizes remain deferred post-MVP work.

## Repository map

- [Requirements](docs/requirements.md), [architecture](docs/architecture.md), and [logical register model](docs/register_model.md)
- [Python software design](docs/software_design.md) and [test plan](docs/test_plan.md)
- [Reproducibility instructions](docs/reproducibility.md)
- [Simulator package](src/elevator_access_sim/) and [automated tests](tests/)
- [Official scalability configuration](experiments/scalability_config.json)
- [Aggregate scalability results](results/scalability_results.json) and [recorded environment](results/scalability_environment.json)
- [Audit records](audit/)

## Requirements

- Python 3.11 or later.
- pytest for running the test suite.
- No runtime dependencies beyond the Python standard library.
- No device, database, network service, GUI, or physical hardware is required.

Normal simulator execution is offline. Installation commands can only use packaging and test dependencies already available locally unless a separately authorized network-enabled setup is used.

## Quick test

From the repository root, without installation:

```sh
PYTHONPATH=src python -m pytest
```

Optional editable installation:

```sh
python -m pip install -e ".[test]"
python -m pytest
```

## CLI quick start

The CLI accepts strict configuration and credential JSON files:

```sh
PYTHONPATH=src python -m elevator_access_sim.cli --config CONFIG_PATH --credentials CREDENTIALS_PATH
```

Use the complete temporary-file grant/timeout procedure in [the reproducibility instructions](docs/reproducibility.md#cli-demonstration).

## Experiments

The deterministic runner is [scripts/run_experiments.py](scripts/run_experiments.py). Its official configuration is [experiments/scalability_config.json](experiments/scalability_config.json), with seed 260516, credential sizes 10, 100, 1,000, and 10,000, one warm-up, and three measured repetitions per size. Only `Controller.submit` is host-timed.

Committed host observations are stored in [results/scalability_results.json](results/scalability_results.json), with the bounded environment and interpretation record in [results/scalability_environment.json](results/scalability_environment.json). Timing varies across hosts and runs. No performance threshold, real-time guarantee, or physical-performance inference exists.

## Verification status

Final SP-06.11 validation passed 976 tests with zero failures, skips, or xfails. The live test inventory contains 94 implemented required/MVP rows and six designed optional rows. All 60 required requirements are verified; six optional requirements remain explicitly deferred. The canonical execution record is [audit/validation/subproject_06_11_validation.md](audit/validation/subproject_06_11_validation.md).

## Limitations and pending work

Passing software tests demonstrates conformance of this Python implementation to the proposed project model under controlled inputs. It does not demonstrate physical RFID compatibility, electrical behavior, elevator control, safety, certification, field reliability, production readiness, real-time behavior, or commercial-controller equivalence.

Supervisor approval and other human approvals remain unresolved. Optional features, the engineering report, presentation, release preparation, university submission, and any physical-scope work are separate later activities; this repository does not claim those deliverables are finished.
