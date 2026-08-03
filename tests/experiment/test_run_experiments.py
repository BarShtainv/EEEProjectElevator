"""SP-06.10 deterministic scalability runner tests."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import replace
import importlib.util
import json
import math
from pathlib import Path
import random
import sys

import pytest

from elevator_access_sim.credentials import CredentialRepository
from elevator_access_sim.models import ReaderSource


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "scripts" / "run_experiments.py"
CONFIG_PATH = ROOT / "experiments" / "scalability_config.json"
SPEC = importlib.util.spec_from_file_location("sp06_run_experiments", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def official_object() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def parse_object(value: object) -> object:
    return runner.parse_experiment_config(json.dumps(value))


def smoke_config() -> object:
    return replace(
        runner.load_experiment_config(CONFIG_PATH),
        configuration_id="SP06_SMOKE_V1",
        credential_counts=(10,),
        minimum_request_count=100,
        measured_repetitions=1,
    )


def aggregate_row(
    config: object,
    credential_count: int,
    repetition: int,
) -> dict[str, object]:
    request_count = max(config.minimum_request_count, credential_count)
    mix = config.mix()
    counts = {key: request_count * percent // 100 for key, percent in mix.items()}
    return {
        "credential_count": credential_count,
        "request_count": request_count,
        "repetition": repetition,
        "processed": request_count,
        "granted": counts["granted"],
        "denied_by_reason": {
            "unknown_credential": counts["unknown_credential"],
            "disabled_credential": counts["disabled_credential"],
            "unauthorized_floor": counts["unauthorized_floor"],
        },
        "validation_failures": counts["invalid_frame"],
        "validation_by_reason": {"invalid_frame": counts["invalid_frame"]},
        "other_outcomes": 0,
        "average_ns": 100.5 + repetition,
        "median_ns": 100 + repetition,
        "p95_ns": 200 + repetition,
        "throughput_cases_per_second": 1000000.0 + credential_count,
        "credential_checksum_sha256": runner.canonical_checksum(
            ["credentials", credential_count, config.seed]
        ),
        "request_checksum_sha256": runner.canonical_checksum(
            ["requests", credential_count, config.seed]
        ),
    }


def official_aggregate_rows(config: object) -> list[dict[str, object]]:
    return [
        aggregate_row(config, count, repetition)
        for count in config.credential_counts
        for repetition in range(1, config.measured_repetitions + 1)
    ]


def test_tst_rep_001_exact_official_configuration_parses_without_defaults() -> None:
    config = runner.load_experiment_config(CONFIG_PATH)
    assert config.configuration_id == "SP06_SCALABILITY_V1"
    assert config.workload_id == "MIXED_REQUESTS_V1"
    assert config.seed == 260516
    assert config.credential_counts == (10, 100, 1000, 10000)
    assert config.minimum_request_count == 1000
    assert (config.warmup_repetitions, config.measured_repetitions) == (1, 3)
    assert config.mix() == {
        "granted": 40,
        "unauthorized_floor": 20,
        "disabled_credential": 15,
        "unknown_credential": 15,
        "invalid_frame": 10,
    }


@pytest.mark.parametrize("text", ["[]", "null", "1", '"object"', "{", '{"x":NaN}'])
def test_configuration_rejects_nonobject_malformed_and_nonfinite_json(text: str) -> None:
    with pytest.raises(runner.ExperimentError):
        runner.parse_experiment_config(text)


@pytest.mark.parametrize(
    "text",
    [
        '{"schema_version":1,"schema_version":1}',
        '{"workload_mix_percent":{"granted":40,"granted":40}}',
    ],
)
def test_configuration_rejects_duplicate_members_at_any_level(text: str) -> None:
    with pytest.raises(runner.ExperimentError, match="duplicate JSON member"):
        runner.parse_experiment_config(text)


@pytest.mark.parametrize("field", list(runner.CONFIG_FIELDS))
def test_configuration_rejects_every_missing_field(field: str) -> None:
    value = official_object()
    value.pop(field)
    with pytest.raises(runner.ExperimentError, match="missing experiment field"):
        parse_object(value)


def test_configuration_rejects_unknown_fields() -> None:
    value = official_object()
    value["surprise"] = 1
    with pytest.raises(runner.ExperimentError, match="unknown experiment field"):
        parse_object(value)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("schema_version", True),
        ("seed", False),
        ("minimum_request_count", True),
        ("warmup_repetitions", True),
        ("measured_repetitions", False),
        ("output_duration_ms", True),
        ("watchdog_timeout_ms", False),
    ],
)
def test_configuration_rejects_boolean_as_integer(field: str, invalid: bool) -> None:
    value = official_object()
    value[field] = invalid
    with pytest.raises(runner.ExperimentError, match="must be an integer"):
        parse_object(value)


@pytest.mark.parametrize(
    "counts",
    [[], [0], [-1], [10, 10], [True], [1.0], [65537]],
)
def test_configuration_rejects_invalid_or_duplicate_counts(counts: object) -> None:
    value = official_object()
    value["configuration_id"] = "TEST_CONFIG"
    value["credential_counts"] = counts
    with pytest.raises(runner.ExperimentError):
        parse_object(value)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("minimum_request_count", 0),
        ("warmup_repetitions", 0),
        ("warmup_repetitions", 2),
        ("measured_repetitions", 0),
    ],
)
def test_configuration_rejects_invalid_counts_or_repetitions(field: str, invalid: int) -> None:
    value = official_object()
    value["configuration_id"] = "TEST_CONFIG"
    value[field] = invalid
    with pytest.raises(runner.ExperimentError):
        parse_object(value)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("profile", "OTHER"),
        ("output_duration_ms", 99),
        ("output_duration_ms", 30001),
        ("watchdog_timeout_ms", 0),
        ("watchdog_timeout_ms", 4294967296),
        ("watchdog_enabled", 0),
    ],
)
def test_configuration_rejects_invalid_simulator_values(field: str, invalid: object) -> None:
    value = official_object()
    value["configuration_id"] = "TEST_CONFIG"
    value[field] = invalid
    with pytest.raises(runner.ExperimentError):
        parse_object(value)


@pytest.mark.parametrize(
    "mutation",
    [
        {"granted": -1, "unauthorized_floor": 21},
        {"granted": 40.0},
        {"granted": True},
        {"granted": 39},
    ],
)
def test_configuration_rejects_invalid_percentages(mutation: dict[str, object]) -> None:
    value = official_object()
    value["configuration_id"] = "TEST_CONFIG"
    value["workload_mix_percent"].update(mutation)
    with pytest.raises(runner.ExperimentError):
        parse_object(value)


@pytest.mark.parametrize("change", ["missing", "unknown"])
def test_configuration_rejects_missing_or_unknown_category(change: str) -> None:
    value = official_object()
    value["configuration_id"] = "TEST_CONFIG"
    mix = value["workload_mix_percent"]
    if change == "missing":
        mix.pop("invalid_frame")
    else:
        mix["busy"] = 0
    with pytest.raises(runner.ExperimentError):
        parse_object(value)


def test_configuration_rejects_official_substitution_and_invalid_utf8(tmp_path: Path) -> None:
    value = official_object()
    value["measured_repetitions"] = 1
    with pytest.raises(runner.ExperimentError, match="must not be substituted"):
        parse_object(value)
    path = tmp_path / "config.json"
    path.write_bytes(b'\xff{"schema_version":1}')
    with pytest.raises(runner.ExperimentError, match="strict UTF-8"):
        runner.load_experiment_config(path)


@pytest.mark.parametrize(
    "substituted_mix",
    [
        {
            "granted": 39,
            "unauthorized_floor": 21,
            "disabled_credential": 15,
            "unknown_credential": 15,
            "invalid_frame": 10,
        },
        {
            "granted": 20,
            "unauthorized_floor": 20,
            "disabled_credential": 20,
            "unknown_credential": 20,
            "invalid_frame": 20,
        },
    ],
)
def test_official_configuration_rejects_positive_total_100_mix_substitution(
    substituted_mix: dict[str, int],
) -> None:
    value = official_object()
    value["workload_mix_percent"] = substituted_mix
    with pytest.raises(
        runner.ExperimentError,
        match="official configuration values must not be substituted",
    ):
        parse_object(value)


def test_nonofficial_bounded_configuration_retains_generic_mix_support() -> None:
    value = official_object()
    value.update(
        configuration_id="SP06_SMOKE_V1",
        credential_counts=[10],
        minimum_request_count=100,
        measured_repetitions=1,
        workload_mix_percent={
            "granted": 20,
            "unauthorized_floor": 20,
            "disabled_credential": 20,
            "unknown_credential": 20,
            "invalid_frame": 20,
        },
    )
    config = parse_object(value)
    assert config.mix() == value["workload_mix_percent"]


@pytest.mark.parametrize("credential_count", [10, 100, 1000, 10000])
def test_tst_rep_001_tst_scl_001_required_sizes_regenerate_exactly(
    credential_count: int,
) -> None:
    config = runner.load_experiment_config(CONFIG_PATH)
    global_state = random.getstate()
    first_records = runner.generate_credentials(config, credential_count)
    first_requests = runner.generate_requests(config, first_records)
    second_records = runner.generate_credentials(config, credential_count)
    second_requests = runner.generate_requests(config, second_records)

    assert random.getstate() == global_state
    assert first_records == second_records
    assert first_requests == second_requests
    assert runner.credential_checksum(first_records) == runner.credential_checksum(second_records)
    assert runner.request_checksum(first_requests) == runner.request_checksum(second_requests)
    assert len(first_records) == credential_count
    assert len(first_requests) == max(1000, credential_count)
    assert len({(record.facility_code, record.credential_number) for record in first_records}) == credential_count
    assert len(CredentialRepository.from_records(first_records)) == credential_count
    assert any(record.enabled and record.floor_mask == 65535 for record in first_records)
    assert any(record.enabled and record.floor_mask == 0 for record in first_records)
    assert any(not record.enabled for record in first_records)
    assert {request.request.reader_source for request in first_requests} == {
        ReaderSource.LF,
        ReaderSource.HF,
    }
    assert Counter(request.category for request in first_requests) == {
        category: len(first_requests) * percent // 100
        for category, percent in config.mix().items()
    }
    existing = {(record.facility_code, record.credential_number) for record in first_records}
    unknown_frames = [request.request.frame for request in first_requests if request.category == "unknown_credential"]
    assert all(frame[1:9] == (1,) * 8 for frame in unknown_frames)
    assert all(record.facility_code == 0 for record in first_records)
    assert all((255, number) not in existing for number in range(65536))


def test_tst_rep_001_different_seed_changes_request_checksum() -> None:
    config = runner.load_experiment_config(CONFIG_PATH)
    records = runner.generate_credentials(config, 100)
    requests = runner.generate_requests(config, records)
    changed = replace(config, seed=config.seed + 1, configuration_id="DIFFERENT_SEED")
    changed_records = runner.generate_credentials(changed, 100)
    changed_requests = runner.generate_requests(changed, changed_records)
    assert runner.request_checksum(requests) != runner.request_checksum(changed_requests)


def test_generated_records_requests_and_checksums_are_immutable_and_canonical() -> None:
    config = smoke_config()
    records = runner.generate_credentials(config, 10)
    requests = runner.generate_requests(config, records)
    assert isinstance(records, tuple) and isinstance(requests, tuple)
    assert len(runner.credential_checksum(records)) == 64
    assert len(runner.request_checksum(requests)) == 64
    assert runner.canonical_checksum({"null": None, "source": "LF"}) == runner.canonical_checksum(
        {"null": None, "source": "LF"}
    )


def test_tst_scl_001_bounded_generated_workload_matches_public_controller_outcomes() -> None:
    config = smoke_config()
    records = runner.generate_credentials(config, 10)
    requests = runner.generate_requests(config, records)
    row = runner.run_repetition(config, records, requests, 1)
    assert row["processed"] == 100
    assert row["granted"] == 40
    assert row["denied_by_reason"] == {
        "unknown_credential": 15,
        "disabled_credential": 15,
        "unauthorized_floor": 20,
    }
    assert row["validation_failures"] == 10
    assert row["validation_by_reason"] == {"invalid_frame": 10}
    assert row["other_outcomes"] == 0


@pytest.mark.parametrize(
    ("samples", "expected"),
    [
        ([7], 7),
        ([1, 9], 9),
        (list(range(1, 21)), 19),
        (list(range(1, 101)), 95),
        ([5, 1, 5, 2, 5], 5),
        ([100, 1, 50, 25], 100),
    ],
)
def test_tst_scl_002_nearest_rank_p95_no_interpolation(
    samples: list[int], expected: int
) -> None:
    assert runner.nearest_rank_p95(samples) == expected


@pytest.mark.parametrize("samples", [[], [True], [-1], [1.0], ["1"], None])
def test_nearest_rank_p95_rejects_invalid_samples(samples: object) -> None:
    with pytest.raises(runner.ExperimentError):
        runner.nearest_rank_p95(samples)


def test_tst_scl_002_fake_timer_metrics_and_reconciliation_are_exact() -> None:
    config = smoke_config()
    records = runner.generate_credentials(config, 10)
    requests = runner.generate_requests(config, records)
    timer_values: list[int] = []
    current = 0
    for elapsed in range(1, 101):
        timer_values.extend((current, current + elapsed))
        current += elapsed
    values = iter(timer_values)

    row = runner.run_repetition(config, records, requests, 1, timer=lambda: next(values))

    assert row["processed"] == 100
    assert row["average_ns"] == 50.5
    assert row["median_ns"] == 50.5
    assert row["p95_ns"] == 95
    assert row["throughput_cases_per_second"] == 100 * 1_000_000_000 / 5050
    assert row["processed"] == (
        row["granted"]
        + sum(row["denied_by_reason"].values())
        + row["validation_failures"]
        + row["other_outcomes"]
    )


@pytest.mark.parametrize("timer_values", [[1, 0], [True, 2], [0.0, 2], [1, 1]])
def test_repetition_rejects_invalid_or_nonpositive_total_timing(timer_values: list[object]) -> None:
    config = replace(smoke_config(), minimum_request_count=100)
    records = runner.generate_credentials(config, 10)
    requests = runner.generate_requests(config, records)
    repeated = iter(timer_values * len(requests))
    with pytest.raises(runner.ExperimentError):
        runner.run_repetition(config, records, requests, 1, timer=lambda: next(repeated))


def test_warmup_aggregate_is_discarded() -> None:
    config = smoke_config()
    calls = 2 * max(config.minimum_request_count, 10)
    current = 0
    values: list[int] = []
    for _ in range(calls):
        values.extend((current, current + 1))
        current += 1
    timer_values = iter(values)
    rows = runner.run_complete_experiment(config, timer=lambda: next(timer_values))
    assert len(rows) == 1
    assert rows[0]["repetition"] == 1


def test_tst_rep_002_tst_scl_003_official_shaped_results_and_environment_schema() -> None:
    config = runner.load_experiment_config(CONFIG_PATH)
    aggregates = official_aggregate_rows(config)
    environment = runner.collect_environment(config)
    results = runner.build_results_document(config, aggregates, environment)

    runner.validate_environment_document(environment, config)
    runner.validate_results_document(results, config, environment)
    assert tuple(results) == (
        "schema_version", "configuration_id", "workload_id", "seed", "timer", "results"
    )
    assert len(results["results"]) == 12
    assert Counter(row["credential_count"] for row in results["results"]) == {
        10: 3, 100: 3, 1000: 3, 10000: 3
    }
    assert all(tuple(row) == runner.RESULT_FIELDS for row in results["results"])
    assert tuple(environment) == runner.ENVIRONMENT_FIELDS
    assert environment["timer"] == "time.perf_counter_ns"
    assert environment == runner.collect_environment(config)
    assert environment["environment_id"].startswith("env-")
    serialized = json.dumps({"results": results, "environment": environment})
    for forbidden in ("username", "hostname", "/home/", "credentials\"", "requests\"", "timing_samples"):
        assert forbidden not in serialized


@pytest.mark.parametrize(
    "mutation",
    [
        lambda rows: rows.pop(),
        lambda rows: rows[0].update(other_outcomes=1),
        lambda rows: rows[0].update(p95_ns=1.5),
        lambda rows: rows[0].update(average_ns=float("nan")),
        lambda rows: rows[0].update(throughput_cases_per_second=0),
        lambda rows: rows[1].update(request_checksum_sha256="0" * 64),
    ],
)
def test_results_validation_rejects_schema_count_metric_and_checksum_faults(mutation) -> None:
    config = runner.load_experiment_config(CONFIG_PATH)
    rows = official_aggregate_rows(config)
    mutation(rows)
    with pytest.raises(runner.ExperimentError):
        runner.validate_aggregate_rows(rows, config)


def test_tst_rep_002_utf8_json_export_has_final_newline_and_replaces(tmp_path: Path) -> None:
    config = smoke_config()
    rows = [aggregate_row(config, 10, 1)]
    environment = runner.collect_environment(config)
    results = runner.build_results_document(config, rows, environment)
    results_path = tmp_path / "results.json"
    environment_path = tmp_path / "environment.json"
    results_path.write_text("old-results", encoding="utf-8")
    environment_path.write_text("old-environment", encoding="utf-8")

    runner.export_documents(results_path, environment_path, results, environment)

    assert results_path.read_bytes().endswith(b"\n")
    assert environment_path.read_bytes().endswith(b"\n")
    assert json.loads(results_path.read_text(encoding="utf-8")) == results
    assert json.loads(environment_path.read_text(encoding="utf-8")) == environment
    assert not list(tmp_path.glob("*.tmp"))
    assert not list(tmp_path.glob(".*.tmp"))


def test_export_prepublication_failure_preserves_both_existing_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_path = tmp_path / "results.json"
    environment_path = tmp_path / "environment.json"
    results_path.write_text("old-results", encoding="utf-8")
    environment_path.write_text("old-environment", encoding="utf-8")
    original = runner._write_temporary_json
    calls = 0

    def fail_second(destination: Path, document: object) -> Path:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise runner.ExperimentError("injected pre-publication failure")
        return original(destination, document)

    monkeypatch.setattr(runner, "_write_temporary_json", fail_second)
    with pytest.raises(runner.ExperimentError):
        runner.export_documents(results_path, environment_path, {"new": 1}, {"new": 2})
    assert results_path.read_text(encoding="utf-8") == "old-results"
    assert environment_path.read_text(encoding="utf-8") == "old-environment"
    assert not list(tmp_path.glob(".*.tmp"))


def test_handled_main_error_returns_one_without_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    result = runner.main(
        [
            "--config", str(invalid),
            "--results", str(tmp_path / "results.json"),
            "--environment", str(tmp_path / "environment.json"),
        ]
    )
    captured = capsys.readouterr()
    assert result == 1
    assert captured.out == ""
    assert captured.err.startswith("error: ")
    assert "Traceback" not in captured.err


def test_argparse_errors_exit_two() -> None:
    with pytest.raises(SystemExit) as outcome:
        runner.main([])
    assert outcome.value.code == 2


def test_structural_boundary_is_standard_library_offline_and_outside_production() -> None:
    source = RUNNER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    standard = {
        "__future__", "argparse", "collections", "dataclasses", "hashlib", "json", "math", "os",
        "pathlib", "platform", "random", "statistics", "sys", "tempfile", "time", "typing",
    }
    assert imported <= standard | {"elevator_access_sim"}
    assert not imported & {
        "socket", "requests", "httpx", "sqlite3", "tkinter", "serial", "RPi",
        "threading", "asyncio", "multiprocessing", "numpy", "pandas", "benchmark",
    }
    assert "sleep(" not in source
    assert "time.time(" not in source
    assert "perf_counter_ns" in source
    assert RUNNER_PATH.parent == ROOT / "scripts"
    assert not (ROOT / "src" / "elevator_access_sim" / "experiments.py").exists()
    assert all(path.stat().st_size < 1_000_000 for path in (ROOT / "experiments").glob("*"))
