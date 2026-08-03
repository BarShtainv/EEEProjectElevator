"""SP-07.2 isolated lookup and authorization experiment tests."""

from __future__ import annotations

import argparse
import ast
import dataclasses
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
from types import ModuleType

import pytest

from elevator_access_sim.authorization import authorize
from elevator_access_sim.credentials import CredentialRepository
from elevator_access_sim.models import AuthorizationDecision, Reason, Result


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "analysis/run_experiments.py"
CONFIGURATION = ROOT / "experiments/isolated_operations_config.json"


@pytest.fixture(scope="module")
def experiment() -> ModuleType:
    spec = importlib.util.spec_from_file_location("sp07_isolated_runner", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def config(experiment: ModuleType):
    return experiment.load_experiment_config(CONFIGURATION)


def _official_object() -> dict[str, object]:
    return json.loads(CONFIGURATION.read_text(encoding="utf-8"))


def _parse_changed(experiment: ModuleType, mutation: object) -> None:
    value = _official_object()
    assert callable(mutation)
    mutation(value)
    experiment.parse_experiment_config(json.dumps(value))


class StepTimer:
    def __init__(self, step: int = 2) -> None:
        self.value = 0
        self.step = step
        self.calls = 0

    def __call__(self) -> int:
        current = self.value
        self.value += self.step
        self.calls += 1
        return current


def _generated(experiment: ModuleType, config: object, count: int):
    records = experiment.generate_credentials(config, count)
    lookup = experiment.generate_lookup_cases(config, records)
    authorization = experiment.generate_authorization_cases(config, records)
    return records, lookup, authorization


def test_exact_official_configuration_parses(experiment: ModuleType, config: object) -> None:
    assert config.schema_version == 1
    assert config.configuration_id == "SP07_ISOLATED_OPERATIONS_V1"
    assert config.workload_id == "LOOKUP_AUTHORIZATION_MATRIX_V1"
    assert config.seed == 270516
    assert config.credential_counts == (10, 100, 1000, 10000)
    assert config.case_count_per_repetition == 1000
    assert config.warmup_repetitions == 1 and config.measured_repetitions == 3


def test_invalid_utf8_configuration_is_rejected(experiment: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_bytes(b"\xff")
    with pytest.raises(experiment.ExperimentError, match="strict UTF-8"):
        experiment.load_experiment_config(path)


@pytest.mark.parametrize(
    "text,match",
    [
        ("{", "not valid JSON"),
        ('{"schema_version":1,"schema_version":1}', "duplicate JSON member"),
        ("[]", "JSON object"),
    ],
)
def test_malformed_duplicate_and_wrong_root_configuration_rejected(
    experiment: ModuleType, text: str, match: str
) -> None:
    with pytest.raises(experiment.ExperimentError, match=match):
        experiment.parse_experiment_config(text)


@pytest.mark.parametrize(
    "mutation,match",
    [
        (lambda value: value.pop("seed"), "missing experiment field"),
        (lambda value: value.__setitem__("unknown", 1), "unknown experiment field"),
        (lambda value: value.__setitem__("schema_version", True), "must be an integer"),
        (lambda value: value.__setitem__("schema_version", 2), "must not be substituted"),
        (lambda value: value.__setitem__("configuration_id", "other"), "must not be substituted"),
        (lambda value: value.__setitem__("workload_id", "other"), "must not be substituted"),
        (lambda value: value.__setitem__("seed", 1), "must not be substituted"),
        (lambda value: value.__setitem__("credential_counts", [100, 10, 1000, 10000]), "must not be substituted"),
        (lambda value: value.__setitem__("credential_counts", [10, 100, 1000]), "must not be substituted"),
        (lambda value: value.__setitem__("credential_counts", [10, 100, 1000, 1000]), "must not be substituted"),
        (lambda value: value.__setitem__("case_count_per_repetition", 0), "at least 1"),
        (lambda value: value.__setitem__("case_count_per_repetition", 950), "must not be substituted"),
        (lambda value: value.__setitem__("warmup_repetitions", 2), "must not be substituted"),
        (lambda value: value.__setitem__("measured_repetitions", 2), "must not be substituted"),
        (lambda value: value["credential_pool_percent"].pop("disabled"), "missing credential_pool category"),
        (lambda value: value["lookup_mix_percent"].__setitem__("other", 1), "unknown lookup_mix category"),
        (lambda value: value["authorization_mix_percent"].__setitem__("authorized", True), "must be an integer"),
        (lambda value: value["lookup_mix_percent"].__setitem__("hit", 0), "at least 1"),
        (lambda value: value["credential_pool_percent"].__setitem__("enabled_all_floors", -1), "at least 1"),
        (lambda value: value["authorization_mix_percent"].__setitem__("authorized", 39), "total exactly 100"),
        (lambda value: (value["lookup_mix_percent"].__setitem__("hit", 60), value["lookup_mix_percent"].__setitem__("miss", 40)), "must not be substituted"),
    ],
)
def test_every_official_configuration_substitution_or_defect_is_rejected(
    experiment: ModuleType, mutation: object, match: str
) -> None:
    with pytest.raises(experiment.ExperimentError, match=match):
        _parse_changed(experiment, mutation)


@pytest.mark.parametrize("count", [10, 100, 1000, 10000])
def test_credentials_are_exact_unique_deterministic_and_seed_sensitive(
    experiment: ModuleType, config: object, count: int
) -> None:
    state = random.getstate()
    records = experiment.generate_credentials(config, count)
    assert random.getstate() == state
    assert len(records) == len({(item.facility_code, item.credential_number) for item in records}) == count
    assert [item.credential_number for item in records] == list(range(count))
    assert all(item.facility_code == 1 and item.label is None for item in records)
    assert sum(item.enabled and item.floor_mask == 65535 for item in records) == count * 60 // 100
    assert sum(item.enabled and item.floor_mask == 0 for item in records) == count * 20 // 100
    assert sum(not item.enabled and item.floor_mask == 65535 for item in records) == count * 20 // 100
    assert CredentialRepository.from_records(records).records() == records
    regenerated = experiment.generate_credentials(config, count)
    assert regenerated == records
    assert experiment.credential_checksum(regenerated) == experiment.credential_checksum(records)
    changed = dataclasses.replace(config, seed=config.seed + 1)
    changed_records = experiment.generate_credentials(changed, count)
    assert changed_records != records
    assert experiment.credential_checksum(changed_records) != experiment.credential_checksum(records)


@pytest.mark.parametrize("count", [10, 100, 1000, 10000])
def test_lookup_cases_are_exact_immutable_deterministic_and_noncolliding(
    experiment: ModuleType, config: object, count: int
) -> None:
    records, cases, _ = _generated(experiment, config, count)
    assert len(cases) == 1000
    assert sum(case.expected_label == "hit" for case in cases) == 500
    assert sum(case.expected_label == "miss" for case in cases) == 500
    repository = CredentialRepository.from_records(records)
    for case in cases:
        found = repository.lookup(case.key).record
        assert (found is not None) == (case.expected_label == "hit")
        if case.expected_label == "miss":
            assert case.key.facility_code == 255
    assert experiment.generate_lookup_cases(config, records) == cases
    assert experiment.lookup_case_checksum(experiment.generate_lookup_cases(config, records)) == experiment.lookup_case_checksum(cases)
    with pytest.raises(dataclasses.FrozenInstanceError):
        cases[0].expected_label = "miss"  # type: ignore[misc]


@pytest.mark.parametrize("count", [10, 100, 1000, 10000])
def test_authorization_cases_are_exact_immutable_deterministic_and_correct(
    experiment: ModuleType, config: object, count: int
) -> None:
    records, _, cases = _generated(experiment, config, count)
    assert len(records) == count and len(cases) == 1000
    expected = {
        "granted_authorized": 400,
        "denied_unauthorized_floor": 200,
        "denied_disabled_credential": 150,
        "denied_unknown_credential": 150,
        "error_invalid_floor": 100,
    }
    assert {label: sum(case.expected_label == label for case in cases) for label in expected} == expected
    for case in cases:
        decision = authorize(case.decoded, case.record, case.requested_floor)
        assert experiment.classify_authorization(decision) == case.expected_label
        if case.expected_label == "error_invalid_floor":
            assert case.requested_floor in (0, 17)
        else:
            assert 1 <= case.requested_floor <= 16
        if case.expected_label == "denied_unknown_credential":
            assert case.record is None and case.decoded.facility_code == 255
    assert experiment.generate_authorization_cases(config, records) == cases
    with pytest.raises(dataclasses.FrozenInstanceError):
        cases[0].requested_floor = 3  # type: ignore[misc]


def test_case_sequences_and_checksums_change_with_seed(
    experiment: ModuleType, config: object
) -> None:
    records, lookup, authorization_cases = _generated(experiment, config, 100)
    changed = dataclasses.replace(config, seed=config.seed + 1)
    changed_records, changed_lookup, changed_authorization = _generated(experiment, changed, 100)
    assert (
        experiment.lookup_case_checksum(lookup)
        != experiment.lookup_case_checksum(changed_lookup)
    )
    assert (
        experiment.authorization_case_checksum(authorization_cases)
        != experiment.authorization_case_checksum(changed_authorization)
    )
    assert records != changed_records


def test_lookup_and_authorization_diagonal_confusion_matrices(experiment: ModuleType) -> None:
    lookup_expected = ["hit"] * 500 + ["miss"] * 500
    lookup = experiment.build_confusion_summary(lookup_expected, lookup_expected, experiment.OPERATIONS[0])
    assert lookup["confusion_matrix"] == {
        "hit": {"hit": 500, "miss": 0},
        "miss": {"hit": 0, "miss": 500},
    }
    assert lookup["correct_count"] == 1000 and lookup["mismatch_count"] == 0
    assert lookup["correct_grant_count"] is None and lookup["incorrect_grant_count"] is None

    expected = (
        ["granted_authorized"] * 400
        + ["denied_unauthorized_floor"] * 200
        + ["denied_disabled_credential"] * 150
        + ["denied_unknown_credential"] * 150
        + ["error_invalid_floor"] * 100
    )
    authorization_summary = experiment.build_confusion_summary(
        expected, expected, experiment.OPERATIONS[1]
    )
    assert authorization_summary["correct_grant_count"] == 400
    assert authorization_summary["correct_denial_count"] == 500
    assert authorization_summary["correct_error_count"] == 100
    assert authorization_summary["incorrect_grant_count"] == 0
    assert authorization_summary["incorrect_denial_count"] == 0
    assert authorization_summary["other_mismatch_count"] == 0


@pytest.mark.parametrize(
    "expected,actual,field",
    [
        ("denied_unknown_credential", "granted_authorized", "incorrect_grant_count"),
        ("granted_authorized", "denied_disabled_credential", "incorrect_denial_count"),
        ("error_invalid_floor", "other", "other_mismatch_count"),
    ],
)
def test_every_authorization_mismatch_class_is_counted(
    experiment: ModuleType, expected: str, actual: str, field: str
) -> None:
    summary = experiment.build_confusion_summary([expected], [actual], experiment.OPERATIONS[1])
    assert summary["correct_count"] == 0 and summary["mismatch_count"] == 1
    assert summary[field] == 1
    assert sum(
        summary[name]
        for name in ("incorrect_grant_count", "incorrect_denial_count", "other_mismatch_count")
    ) == 1


@pytest.mark.parametrize(
    "samples,expected",
    [
        ([7], 7),
        ([1, 9], 9),
        (list(range(1, 21)), 19),
        (list(range(1, 101)), 95),
        ([4, 4, 4, 4], 4),
        ([9, 1, 7, 3, 5], 9),
    ],
)
def test_nearest_rank_p95_exact_cases(
    experiment: ModuleType, samples: list[int], expected: int
) -> None:
    assert experiment.nearest_rank_p95(samples) == expected


@pytest.mark.parametrize("samples", [[], [True], [-1], [1.5], "123"])
def test_nearest_rank_rejects_invalid_timer_samples(
    experiment: ModuleType, samples: object
) -> None:
    with pytest.raises(experiment.ExperimentError, match="p95 samples"):
        experiment.nearest_rank_p95(samples)


def test_fake_timer_lookup_and_authorization_metrics_are_exact(
    experiment: ModuleType, config: object
) -> None:
    records, lookup_cases, authorization_cases = _generated(experiment, config, 10)
    lookup_timer = StepTimer(2)
    lookup = experiment.run_lookup_repetition(records, lookup_cases, 1, timer=lookup_timer)
    assert lookup_timer.calls == 2000
    assert lookup["processed"] == 1000
    assert lookup["average_ns"] == lookup["median_ns"] == lookup["p95_ns"] == 2
    assert lookup["throughput_cases_per_second"] == 500_000_000
    assert lookup["expected_outcomes"] == lookup["actual_outcomes"] == {"hit": 500, "miss": 500}

    authorization_timer = StepTimer(4)
    authorization_row = experiment.run_authorization_repetition(
        authorization_cases, 10, 1, timer=authorization_timer
    )
    assert authorization_timer.calls == 2000
    assert authorization_row["processed"] == 1000
    assert authorization_row["average_ns"] == authorization_row["median_ns"] == authorization_row["p95_ns"] == 4
    assert authorization_row["throughput_cases_per_second"] == 250_000_000
    assert authorization_row["mismatch_count"] == 0


def test_timed_regions_exclude_construction_and_classification(
    experiment: ModuleType,
    config: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, lookup_cases, authorization_cases = _generated(experiment, config, 10)
    events: list[str] = []
    real_repository = experiment.CredentialRepository

    class ObservedRepository:
        @classmethod
        def from_records(cls, values):
            events.append("repository construction")
            return cls(real_repository.from_records(values))

        def __init__(self, repository):
            self.repository = repository

        def lookup(self, key):
            events.append("lookup")
            return self.repository.lookup(key)

    real_lookup_classifier = experiment.classify_lookup
    monkeypatch.setattr(experiment, "CredentialRepository", ObservedRepository)
    monkeypatch.setattr(
        experiment,
        "classify_lookup",
        lambda outcome, key: (events.append("classify"), real_lookup_classifier(outcome, key))[1],
    )
    timer = lambda: (events.append("timer"), len(events))[1]
    experiment.run_lookup_repetition(records, lookup_cases[:1], 1, timer=timer)
    assert events == ["repository construction", "timer", "lookup", "timer", "classify"]

    events.clear()
    real_authorize = experiment.authorize
    real_auth_classifier = experiment.classify_authorization
    monkeypatch.setattr(
        experiment,
        "authorize",
        lambda decoded, record, floor: (
            events.append("authorize"), real_authorize(decoded, record, floor)
        )[1],
    )
    monkeypatch.setattr(
        experiment,
        "classify_authorization",
        lambda decision: (events.append("classify"), real_auth_classifier(decision))[1],
    )
    experiment.run_authorization_repetition(authorization_cases[:1], 10, 1, timer=timer)
    assert events == ["timer", "authorize", "timer", "classify"]


def test_ast_proves_direct_call_timing_boundaries() -> None:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "_timer_sample" not in functions

    def assignment(function: ast.FunctionDef, name: str) -> tuple[int, ast.Assign]:
        loop = next(node for node in function.body if isinstance(node, ast.For))
        for index, statement in enumerate(loop.body):
            if (
                isinstance(statement, ast.Assign)
                and len(statement.targets) == 1
                and isinstance(statement.targets[0], ast.Name)
                and statement.targets[0].id == name
            ):
                return index, statement
        raise AssertionError(f"missing assignment to {name}")

    def direct_call(statement: ast.Assign) -> ast.Call:
        assert isinstance(statement.value, ast.Call)
        return statement.value

    for name in ("run_lookup_repetition", "run_authorization_repetition"):
        function = functions[name]
        assert not any(isinstance(node, ast.Lambda) for node in ast.walk(function))
        assert not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_timer_sample"
            for node in ast.walk(function)
        )

    lookup = functions["run_lookup_repetition"]
    lookup_loop_index = next(
        index for index, node in enumerate(lookup.body) if isinstance(node, ast.For)
    )
    repository_index = next(
        index
        for index, node in enumerate(lookup.body)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "from_records"
            for call in ast.walk(node)
            if isinstance(call, ast.Call)
        )
    )
    assert repository_index < lookup_loop_index
    key_index, _ = assignment(lookup, "key")
    lookup_start_index, lookup_start = assignment(lookup, "start")
    lookup_call_index, lookup_outcome = assignment(lookup, "outcome")
    lookup_end_index, lookup_end = assignment(lookup, "end")
    lookup_classify_index, lookup_label = assignment(lookup, "actual_label")
    assert key_index < lookup_start_index < lookup_call_index < lookup_end_index
    assert lookup_end_index < lookup_classify_index
    assert isinstance(direct_call(lookup_start).func, ast.Name)
    assert direct_call(lookup_start).func.id == "timer"  # type: ignore[union-attr]
    lookup_target = direct_call(lookup_outcome)
    assert isinstance(lookup_target.func, ast.Attribute)
    assert isinstance(lookup_target.func.value, ast.Name)
    assert (lookup_target.func.value.id, lookup_target.func.attr) == ("repository", "lookup")
    assert [argument.id for argument in lookup_target.args if isinstance(argument, ast.Name)] == ["key"]
    assert isinstance(direct_call(lookup_end).func, ast.Name)
    assert direct_call(lookup_end).func.id == "timer"  # type: ignore[union-attr]
    assert isinstance(direct_call(lookup_label).func, ast.Name)
    assert direct_call(lookup_label).func.id == "classify_lookup"  # type: ignore[union-attr]

    authorization = functions["run_authorization_repetition"]
    field_indices = [assignment(authorization, name)[0] for name in ("decoded", "record", "requested_floor")]
    auth_start_index, auth_start = assignment(authorization, "start")
    auth_call_index, auth_decision = assignment(authorization, "decision")
    auth_end_index, auth_end = assignment(authorization, "end")
    auth_classify_index, auth_label = assignment(authorization, "actual_label")
    assert max(field_indices) < auth_start_index < auth_call_index < auth_end_index
    assert auth_end_index < auth_classify_index
    assert isinstance(direct_call(auth_start).func, ast.Name)
    assert direct_call(auth_start).func.id == "timer"  # type: ignore[union-attr]
    auth_target = direct_call(auth_decision)
    assert isinstance(auth_target.func, ast.Name) and auth_target.func.id == "authorize"
    assert [argument.id for argument in auth_target.args if isinstance(argument, ast.Name)] == [
        "decoded", "record", "requested_floor"
    ]
    assert isinstance(direct_call(auth_end).func, ast.Name)
    assert direct_call(auth_end).func.id == "timer"  # type: ignore[union-attr]
    assert isinstance(direct_call(auth_label).func, ast.Name)
    assert direct_call(auth_label).func.id == "classify_authorization"  # type: ignore[union-attr]


def test_complete_fake_timer_run_has_24_measured_rows_and_no_warmups(
    experiment: ModuleType, config: object
) -> None:
    timer = StepTimer(3)
    rows = experiment.run_complete_experiment(config, timer=timer)
    assert len(rows) == 24
    assert [(row["operation"], row["credential_count"], row["repetition"]) for row in rows] == [
        (operation, count, repetition)
        for operation in experiment.OPERATIONS
        for count in config.credential_counts
        for repetition in (1, 2, 3)
    ]
    assert timer.calls == 4 * 2 * 4 * 1000 * 2
    assert all(row["average_ns"] == row["median_ns"] == row["p95_ns"] == 3 for row in rows)


@pytest.fixture(scope="module")
def official_documents(experiment: ModuleType, config: object):
    rows = experiment.run_complete_experiment(config, timer=StepTimer(5))
    environment = experiment.collect_environment(config)
    results = experiment.build_results_document(config, rows, environment)
    return rows, results, environment


def test_result_schema_order_counts_matrices_checksums_and_aggregates(
    experiment: ModuleType, config: object, official_documents: tuple[object, object, object]
) -> None:
    rows, results, environment = official_documents
    experiment.validate_results_document(results, config, environment)
    assert tuple(results) == experiment.RESULT_DOCUMENT_FIELDS
    assert results["operations"] == list(experiment.OPERATIONS)
    assert len(results["results"]) == 24
    assert all(tuple(row) == experiment.RESULT_FIELDS for row in results["results"])
    lookup = [row for row in results["results"] if row["operation"] == experiment.OPERATIONS[0]]
    authorization_rows = [
        row for row in results["results"] if row["operation"] == experiment.OPERATIONS[1]
    ]
    assert sum(row["processed"] for row in lookup) == 12000
    assert sum(row["actual_outcomes"]["hit"] for row in lookup) == 6000
    assert sum(row["actual_outcomes"]["miss"] for row in lookup) == 6000
    assert sum(row["correct_count"] for row in lookup) == 12000
    assert sum(row["mismatch_count"] for row in lookup) == 0
    assert sum(row["processed"] for row in authorization_rows) == 12000
    assert sum(row["correct_grant_count"] for row in authorization_rows) == 4800
    assert sum(row["correct_denial_count"] for row in authorization_rows) == 6000
    assert sum(row["correct_error_count"] for row in authorization_rows) == 1200
    assert sum(row["incorrect_grant_count"] for row in authorization_rows) == 0
    assert sum(row["incorrect_denial_count"] for row in authorization_rows) == 0
    assert sum(row["other_mismatch_count"] for row in authorization_rows) == 0
    assert all(row["actual_outcomes"]["other"] == 0 for row in authorization_rows)
    assert len({row["environment_id"] for row in results["results"]}) == 1
    for row in results["results"]:
        assert row["processed"] == row["correct_count"] == 1000
        assert row["mismatch_count"] == 0
        assert type(row["p95_ns"]) is int
        assert all(
            math.isfinite(row[field]) and row[field] > 0
            for field in ("average_ns", "median_ns", "p95_ns", "throughput_cases_per_second")
        )
    text = json.dumps(results).lower()
    for forbidden in (
        '"records"', '"cases"', '"samples"', '"decoded_inputs"',
        '"selected_records"', '"controller_snapshots"',
    ):
        assert forbidden not in text


def test_environment_schema_id_definitions_limits_and_identity_boundary(
    experiment: ModuleType, config: object, official_documents: tuple[object, object, object]
) -> None:
    _, _, environment = official_documents
    experiment.validate_environment_document(environment, config)
    assert tuple(environment) == experiment.ENVIRONMENT_FIELDS
    assert environment["operation_definitions"] == experiment.OPERATION_DEFINITIONS
    assert environment["interpretation_limits"] == list(experiment.INTERPRETATION_LIMITS)
    assert experiment.collect_environment(config)["environment_id"] == environment["environment_id"]
    text = json.dumps(environment).lower()
    for required in (
        "python software operations", "timer overhead", "repository construction",
        "trusted-key validation", "authorization rows exclude", "database servers",
        "no real-time target", "physical rfid", "safety", "commercial-equivalence",
    ):
        assert required in text
    for forbidden in (
        '"username"', '"hostname"', '"home"', '"repository_path"',
        '"virtual_environment"', '"executable"', "/home/", "/mnt/", "c:\\users\\",
    ):
        assert forbidden not in text


def test_successful_atomic_publication_writes_both_documents(
    experiment: ModuleType,
    official_documents: tuple[object, object, object],
    tmp_path: Path,
) -> None:
    _, results, environment = official_documents
    results_path = tmp_path / "results.json"
    environment_path = tmp_path / "environment.json"
    experiment.publish_documents(results_path, environment_path, results, environment)
    assert json.loads(results_path.read_text(encoding="utf-8")) == results
    assert json.loads(environment_path.read_text(encoding="utf-8")) == environment
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob(".*.tmp"))


def test_second_replacement_failure_restores_both_old_outputs(
    experiment: ModuleType,
    official_documents: tuple[object, object, object],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, results, environment = official_documents
    results_path = tmp_path / "results.json"
    environment_path = tmp_path / "environment.json"
    results_path.write_bytes(b"old results")
    environment_path.write_bytes(b"old environment")
    original_replace = experiment.os.replace
    calls = 0

    def fail_second(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected second replacement failure")
        original_replace(source, destination)

    monkeypatch.setattr(experiment.os, "replace", fail_second)
    with pytest.raises(experiment.ExperimentError, match="preserved"):
        experiment.publish_documents(results_path, environment_path, results, environment)
    assert results_path.read_bytes() == b"old results"
    assert environment_path.read_bytes() == b"old environment"
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob(".*.tmp"))


def test_handled_cli_failure_is_one_line_and_preserves_outputs(
    experiment: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    bad_config = tmp_path / "bad.json"
    bad_config.write_text("{}", encoding="utf-8")
    results = tmp_path / "results.json"
    environment = tmp_path / "environment.json"
    results.write_bytes(b"old results")
    environment.write_bytes(b"old environment")
    assert experiment.main(
        ["--config", str(bad_config), "--results", str(results), "--environment", str(environment)]
    ) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert len(output.err.splitlines()) == 1 and output.err.startswith("error: ")
    assert "Traceback" not in output.err
    assert results.read_bytes() == b"old results"
    assert environment.read_bytes() == b"old environment"


def test_argparse_returns_two_and_all_three_arguments_are_required(
    experiment: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as raised:
        experiment.main([])
    assert raised.value.code == 2
    assert "required" in capsys.readouterr().err
    actions = [action for action in experiment.build_argument_parser()._actions if action.option_strings]
    assert {action.dest for action in actions if action.required} == {"config", "results", "environment"}


def test_structural_boundary_uses_only_standard_library_and_public_operations() -> None:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    imports: set[str] = set()
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            imported_names.update(alias.asname or alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
            imported_names.update(alias.asname or alias.name for alias in node.names)
    assert imports <= {
        "__future__", "argparse", "collections", "dataclasses", "hashlib", "json", "math",
        "os", "pathlib", "platform", "random", "statistics", "sys", "tempfile", "time",
        "elevator_access_sim",
    }
    assert imports.isdisjoint(
        {"numpy", "pandas", "matplotlib", "requests", "urllib", "socket", "sqlite3",
         "threading", "asyncio", "multiprocessing", "subprocess"}
    )
    assert "Controller" not in imported_names
    assert "encode_frame" not in imported_names
    source = SCRIPT.read_text(encoding="utf-8")
    assert "scripts.run_experiments" not in source
    assert "time.sleep" not in source
    assert "Controller.submit" not in source
