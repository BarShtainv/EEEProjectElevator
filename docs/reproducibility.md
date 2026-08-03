# Reproducibility

## Scope and audience

This is the canonical runnable-command guide for reviewers of the deterministic Python software simulator. It covers automated tests, one controlled CLI scenario, and regeneration of aggregate scalability observations. Commands assume the current directory is the repository root.

The simulator models an abstract access-authorization layer. LF and HF are logical reader-source labels only, `PROJECT_WIEGAND_26` is a proposed project profile, the 16 outputs are logical permission channels, and controller behavior uses simulated time. Host timing is observational.

## Python and dependency policy

Python 3.11 or later is supported. Runtime code uses only the Python standard library. pytest is the test dependency. No device, database, network service, GUI, or physical hardware is needed.

Use an external or otherwise controlled Python environment with pytest already available for offline verification. The project does not claim that packaging or test dependencies can be downloaded offline.

## Test setup paths

### No-install path

From the repository root:

```sh
PYTHONPATH=src python -m pytest
```

### Editable-install path

When setuptools and pytest are already available locally, an ordinary editable installation is optional:

```sh
python -m pip install -e ".[test]"
python -m pytest
```

The no-install path is the canonical repository validation command.

## Focused test commands

```sh
PYTHONPATH=src python -m pytest tests/unit
PYTHONPATH=src python -m pytest tests/integration
PYTHONPATH=src python -m pytest tests/end_to_end
PYTHONPATH=src python -m pytest tests/inspection
PYTHONPATH=src python -m pytest tests/experiment/test_run_experiments.py
```

All commands are noninteractive and require no network or device access.

## CLI demonstration

Create a temporary directory and write the two strict UTF-8 JSON documents with the standard library:

```sh
temporary_directory="$(mktemp -d)"
python - "$temporary_directory" <<'PY'
import json
import sys
from pathlib import Path

directory = Path(sys.argv[1])
configuration = {
    "schema_version": 1,
    "profile": "PROJECT_WIEGAND_26",
    "output_duration_ms": 3000,
    "watchdog_timeout_ms": 2000,
    "watchdog_enabled": True,
}
credentials = {
    "schema_version": 1,
    "credentials": [
        {
            "facility_code": 1,
            "credential_number": 100,
            "enabled": True,
            "floor_mask": 65535,
            "label": "demo-user",
        }
    ],
}
for name, value in (("config.json", configuration), ("credentials.json", credentials)):
    (directory / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        errors="strict",
    )
PY
```

Run one LF request for floor 1 with canonical frame `10000000100000000011001000`, then advance simulated time to 3000 ms:

```sh
PYTHONPATH=src python -m elevator_access_sim.cli \
  --config "$temporary_directory/config.json" \
  --credentials "$temporary_directory/credentials.json" \
  --source LF \
  --frame 10000000100000000011001000 \
  --floor 1 \
  --advance-to 3000
```

Expected stable behavior is successful initialization, a `granted`/`authorized` submission with logical floor 1 active, an `output_expired` advancement at simulated timestamp 3000, a final `idle` snapshot with all 16 output channels false, one access-decision event, one output-timeout event, and no watchdog-reset event. The output contains no host timing.

Remove the temporary documents afterward:

```sh
rm -rf "$temporary_directory"
```

## Scalability experiment regeneration

Regenerate into temporary outputs so the committed host observations are not overwritten:

```sh
temporary_directory="$(mktemp -d)"
PYTHONPATH=src python scripts/run_experiments.py \
  --config experiments/scalability_config.json \
  --results "$temporary_directory/scalability_results.json" \
  --environment "$temporary_directory/scalability_environment.json"
```

The committed comparison artifacts are:

- `experiments/scalability_config.json` — frozen generator/workload configuration;
- `results/scalability_results.json` — 12 aggregate measured rows;
- `results/scalability_environment.json` — bounded host and interpretation metadata.

### Stable values

- Schema version 1, configuration ID `SP06_SCALABILITY_V1`, workload ID `MIXED_REQUESTS_V1`, and seed 260516.
- Credential sizes 10, 100, 1,000, and 10,000.
- Request counts 1,000, 1,000, 1,000, and 10,000 respectively.
- One unmeasured warm-up and three measured rows per size, giving 12 measured rows.
- Exact workload mix: 40% granted, 20% unauthorized floor, 15% disabled credential, 15% unknown credential, and 10% invalid frame.
- Zero other outcomes and exact processed-count reconciliation.
- Identical generated-input checksum pair across repetitions of the same size:

| Size | Credential SHA-256 | Request SHA-256 |
|---:|---|---|
| 10 | `e6b71173d03d5aa5a6529afb86f62a0db1c39057a8cfc208bc90ff06330beaee` | `93dbc8c1f8fe624fad47c9e8a13d02f814bd6a0166777923719fb35456ab30b8` |
| 100 | `2dbe74a204c5968756397ce3531a835f8f1a122e542048eb4ac8a1aba0077e3f` | `c08bf3b836778aede71c75ace428bc7de76fab0f31828cda40e8ff208313a0da` |
| 1,000 | `decf95c5b5002df2d80219c5b5a0adcad49c4956f9476ac7ad5c363649e1f87d` | `625b9c80bdf6c2fd1ce0a2b45d8692ca347dc2e4377070cf7c7b7ba6be740d76` |
| 10,000 | `2c859c5b59825058c02ac7d6ae98e05632d35318f08e1937317aa9ac85fb2b1d` | `c1ff8a6c7e6d63bfb50b323ee2d217ceddc7a2943927c88022464244f06eb55b` |

### Host-variable values

Average, median, observed nearest-rank p95 nanoseconds, throughput, and host/environment identity may differ across valid runs. Only `Controller.submit` is timed with `time.perf_counter_ns`; generation, initialization, simulated output-expiry cleanup, validation, environment capture, and export are outside the timed interval. Do not expect identical nanosecond values and do not apply a pass/fail performance threshold.

### Result validation

Parse both temporary JSON documents with strict UTF-8. Confirm four sizes, repetitions 1–3 per size, 12 rows, the request counts and workload outcomes above, zero other outcomes, finite positive metrics, integer positive p95, same-size checksum stability, and one environment ID shared by every row and the environment document. Confirm no raw credentials, raw requests, events, or timing-sample arrays are exported.

Remove temporary experiment outputs afterward:

```sh
rm -rf "$temporary_directory"
```

## Deterministic and variable boundaries

Simulator domain behavior, generated logical inputs, outcome counts, event order, simulated timestamps, schema identifiers, and same-configuration checksums are deterministic. Host wall duration and `perf_counter_ns` measurements are observational and variable.

These results describe one Python software model. They do not establish compatibility with a physical RFID reader, electrical output correctness, elevator movement or safety behavior, certification, field reliability, production readiness, real-time guarantees, or commercial-controller equivalence.

## Cleanup

The procedures above create only temporary directories. Remove each only after confirming that its value came from `mktemp -d`:

```sh
rm -rf "$temporary_directory"
```

Normal verification may also generate `.pytest_cache`, `__pycache__`, `.pyc`, and `.pyo` caches. They are disposable and are not required for reproduction. Do not delete tracked result or audit files.

## Troubleshooting

- `ModuleNotFoundError: elevator_access_sim`: run from the repository root and retain `PYTHONPATH=src`, or use the editable-install path.
- `No module named pytest`: use a controlled environment where pytest is already available; offline execution cannot fetch a missing dependency.
- Configuration or credential startup error: preserve strict UTF-8, exact schema version 1 fields, integer ranges, and JSON Boolean values.
- Different experiment timing: compare schemas, counts, checksums, and recorded environment; host timing is expected to vary.

## Human and project-stage limitations

The working title and software-model scope are project-owner approved, but supervisor approval remains pending. Optional features remain deferred. The engineering report, presentation, release preparation, university submission, human approvals, and any physical or commercial-equivalence work are separate later activities and are not completed by these procedures.
