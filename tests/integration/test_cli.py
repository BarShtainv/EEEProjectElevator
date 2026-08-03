"""SP-06.8 thin offline CLI integration and formatting tests."""

from __future__ import annotations

import argparse
import ast
import inspect
import json
import tomllib
from pathlib import Path

import pytest

import elevator_access_sim
import elevator_access_sim.cli as cli_module
from elevator_access_sim import Controller, SimulatedClock, encode_frame
from elevator_access_sim.cli import build_parser, format_event, format_snapshot, run
from elevator_access_sim.models import (
    ControllerResponse,
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventRecord,
    EventType,
    OutputSnapshot,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
    StateInvariantError,
)


FRAME = "10000000100000000011001000"
CONFIG = {
    "schema_version": 1,
    "profile": "PROJECT_WIEGAND_26",
    "output_duration_ms": 3000,
    "watchdog_timeout_ms": 2000,
    "watchdog_enabled": True,
}


def record(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "facility_code": 1,
        "credential_number": 100,
        "enabled": True,
        "floor_mask": 65535,
        "label": "demo-user",
    }
    value.update(changes)
    return value


def files(
    tmp_path: Path,
    *,
    config: dict[str, object] | None = None,
    records: list[dict[str, object]] | None = None,
) -> tuple[Path, Path]:
    config_path = tmp_path / "config.json"
    credentials_path = tmp_path / "credentials.json"
    config_path.write_text(json.dumps(CONFIG if config is None else config), encoding="utf-8")
    credentials_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "credentials": [record()] if records is None else records,
            }
        ),
        encoding="utf-8",
    )
    return config_path, credentials_path


def argv(paths: tuple[Path, Path], *extra: str) -> list[str]:
    return ["--config", str(paths[0]), "--credentials", str(paths[1]), *extra]


def parse_lines(text: str) -> list[tuple[str, dict[str, object]]]:
    parsed = []
    for line in text.splitlines():
        label, payload = line.split(" ", 1)
        parsed.append((label, json.loads(payload)))
    return parsed


def test_public_signatures_and_parser_creation() -> None:
    assert tuple(inspect.signature(build_parser).parameters) == ()
    assert tuple(inspect.signature(run).parameters) == ("argv",)
    assert tuple(inspect.signature(format_snapshot).parameters) == ("snapshot",)
    assert tuple(inspect.signature(format_event).parameters) == ("event",)
    parser = build_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.prog == "elevator-access-sim"


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["--config", "x"],
        ["--credentials", "x"],
    ],
)
def test_required_file_arguments_are_usage_errors(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        run(arguments)
    assert error.value.code == 2


@pytest.mark.parametrize(
    "partial",
    [
        ("--source", "LF"),
        ("--frame", FRAME),
        ("--floor", "1"),
        ("--source", "LF", "--frame", FRAME),
        ("--source", "LF", "--floor", "1"),
        ("--frame", FRAME, "--floor", "1"),
    ],
)
def test_incomplete_request_group_is_usage_error(tmp_path: Path, partial: tuple[str, ...]) -> None:
    with pytest.raises(SystemExit) as error:
        run(argv(files(tmp_path), *partial))
    assert error.value.code == 2


def test_advancement_options_are_mutually_exclusive(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as error:
        run(argv(files(tmp_path), "--advance-to", "1", "--advance-by", "1"))
    assert error.value.code == 2


@pytest.mark.parametrize(
    "extra",
    [
        ("--source", "LF", "--frame", FRAME, "--floor", "not-an-integer"),
        ("--advance-to", "not-an-integer"),
        ("--advance-by", "not-an-integer"),
    ],
)
def test_floor_and_time_syntax_use_argparse_integer_conversion(
    tmp_path: Path,
    extra: tuple[str, ...],
) -> None:
    with pytest.raises(SystemExit) as error:
        run(argv(files(tmp_path), *extra))
    assert error.value.code == 2


def test_valid_startup_without_request_prints_final_idle_snapshot(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert run(argv(files(tmp_path))) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    lines = parse_lines(captured.out)
    assert [label for label, _ in lines] == ["INITIALIZE", "SNAPSHOT"]
    assert lines[0][1]["result"] is None and lines[0][1]["reason"] is None
    snapshot = lines[1][1]
    assert snapshot["state"] == "idle"
    assert snapshot["active_floor"] is None
    assert snapshot["latest_event_sequence"] is None
    assert snapshot["output_channels"] == [False] * 16


@pytest.mark.parametrize("source", ["LF", "HF"])
def test_lf_and_hf_grants_preserve_source_text(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    source: str,
) -> None:
    status = run(argv(files(tmp_path), "--source", source, "--frame", FRAME, "--floor", "16"))
    assert status == 0
    lines = parse_lines(capsys.readouterr().out)
    submit = next(value for label, value in lines if label == "SUBMIT")
    event = next(value for label, value in lines if label == "EVENT")
    assert (submit["result"], submit["reason"], submit["state"]) == (
        "granted",
        "authorized",
        "output_active",
    )
    assert event["reader_source"] == source
    assert event["facility_code"] == 1 and event["credential_number"] == 100


def test_exact_frame_characters_are_delivered_without_field_interpretation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[object] = []
    original = Controller.submit

    def submit(self: Controller, request: CredentialRequest) -> ControllerResponse:
        observed.append(request.frame)
        return original(self, request)

    monkeypatch.setattr(Controller, "submit", submit)
    assert run(argv(files(tmp_path), "--source", "LF", "--frame", FRAME, "--floor", "1")) == 0
    capsys.readouterr()
    assert observed == [tuple(int(character) for character in FRAME)]


@pytest.mark.parametrize(
    "extra,reason,event_type",
    [
        (("--source", "lf", "--frame", FRAME, "--floor", "1"), "invalid_source", "validation_error"),
        (("--source", "LF", "--frame", FRAME[:-1], "--floor", "1"), "invalid_frame", "validation_error"),
        (("--source", "LF", "--frame", FRAME[:10] + "2" + FRAME[11:], "--floor", "1"), "invalid_frame", "validation_error"),
        (("--source", "LF", "--frame", ("0" if FRAME[0] == "1" else "1") + FRAME[1:], "--floor", "1"), "parity_failure", "validation_error"),
        (("--source", "LF", "--frame", FRAME, "--floor", "17"), "invalid_floor", "validation_error"),
    ],
)
def test_invalid_request_domain_outcomes_remain_exit_zero(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    extra: tuple[str, ...],
    reason: str,
    event_type: str,
) -> None:
    assert run(argv(files(tmp_path), *extra)) == 0
    captured = capsys.readouterr()
    lines = parse_lines(captured.out)
    submit = next(value for label, value in lines if label == "SUBMIT")
    event = next(value for label, value in lines if label == "EVENT")
    assert submit["reason"] == reason
    assert event["event_type"] == event_type
    assert captured.err == ""


@pytest.mark.parametrize(
    "records,floor,reason",
    [
        ([record(floor_mask=0)], "1", "unauthorized_floor"),
        ([], "1", "unknown_credential"),
        ([record(enabled=False)], "1", "disabled_credential"),
    ],
)
def test_modeled_denials_are_process_success(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    records: list[dict[str, object]],
    floor: str,
    reason: str,
) -> None:
    paths = files(tmp_path, records=records)
    assert run(argv(paths, "--source", "HF", "--frame", FRAME, "--floor", floor)) == 0
    lines = parse_lines(capsys.readouterr().out)
    submit = next(value for label, value in lines if label == "SUBMIT")
    assert (submit["result"], submit["reason"]) == ("denied", reason)


def test_normal_output_timeout_sequence(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    status = run(
        argv(
            files(tmp_path),
            "--source", "LF", "--frame", FRAME, "--floor", "1",
            "--advance-to", "3000",
        )
    )
    assert status == 0
    lines = parse_lines(capsys.readouterr().out)
    assert [label for label, _ in lines] == ["INITIALIZE", "SUBMIT", "ADVANCE", "SNAPSHOT", "EVENT", "EVENT"]
    assert lines[2][1]["reason"] == "output_expired"
    assert lines[3][1]["state"] == "idle"
    assert lines[3][1]["active_floor"] is None
    assert [value["event_type"] for label, value in lines if label == "EVENT"] == ["access_decision", "output_timeout"]


def test_manual_reset_occurs_after_request_and_time_advance(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    status = run(
        argv(
            files(tmp_path),
            "--source", "LF", "--frame", FRAME, "--floor", "1",
            "--advance-by", "500", "--manual-reset",
        )
    )
    assert status == 0
    lines = parse_lines(capsys.readouterr().out)
    labels = [label for label, _ in lines]
    assert labels[:5] == ["INITIALIZE", "SUBMIT", "ADVANCE", "MANUAL_RESET", "SNAPSHOT"]
    assert lines[3][1]["reason"] == "manual_request"
    reset_event = [value for label, value in lines if label == "EVENT"][-1]
    assert reset_event["event_type"] == "manual_reset" and reset_event["timestamp_ms"] == 500


@pytest.mark.parametrize("active", [False, True])
def test_idle_and_active_watchdog_suppression_reset(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    active: bool,
) -> None:
    extra = ["--suppress-watchdog"]
    if active:
        extra += ["--source", "LF", "--frame", FRAME, "--floor", "1"]
    extra += ["--advance-to", "2000"]
    assert run(argv(files(tmp_path), *extra)) == 0
    lines = parse_lines(capsys.readouterr().out)
    labels = [label for label, _ in lines]
    assert labels.index("SUPPRESSION") < labels.index("ADVANCE")
    advanced = next(value for label, value in lines if label == "ADVANCE")
    snapshot = next(value for label, value in lines if label == "SNAPSHOT")
    events = [value for label, value in lines if label == "EVENT"]
    assert (advanced["result"], advanced["reason"]) == ("reset", "watchdog_timeout")
    assert snapshot["state"] == "idle" and snapshot["active_floor"] is None
    assert events[-1]["event_type"] == "watchdog_reset"
    assert not any(event["event_type"] == "output_timeout" for event in events)


def test_snapshot_and_event_formatters_are_exact_json_and_deterministic() -> None:
    controller = Controller(SimulatedClock())
    controller.initialize(
        SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True),
        [CredentialRecord(1, 100, True, 65535)],
    )
    controller.submit(CredentialRequest(ReaderSource.HF, encode_frame(1, 100), 1))
    snapshot_text = format_snapshot(controller.snapshot())
    event_text = format_event(controller.events()[0])
    snapshot = json.loads(snapshot_text)
    event = json.loads(event_text)

    assert list(snapshot) == [
        "state", "output_channels", "active_floor", "output_expiry_ms",
        "watchdog_deadline_ms", "initialized", "configuration_valid",
        "repository_ready", "latest_event_sequence",
    ]
    assert len(snapshot["output_channels"]) == 16
    assert all(type(value) is bool for value in snapshot["output_channels"])
    assert list(event) == [
        "sequence_number", "timestamp_ms", "event_type", "reader_source",
        "facility_code", "credential_number", "requested_floor", "result", "reason",
    ]
    assert event["reader_source"] == "HF"
    assert (event["event_type"], event["result"], event["reason"]) == (
        "access_decision", "granted", "authorized"
    )
    assert format_snapshot(controller.snapshot()) == snapshot_text
    assert format_event(controller.events()[0]) == event_text
    assert "\n" not in snapshot_text and "\n" not in event_text


def test_explicit_nulls_in_snapshot_and_event_formatting() -> None:
    controller = Controller(SimulatedClock())
    controller.initialize(SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, False), [])
    snapshot = json.loads(format_snapshot(controller.snapshot()))
    assert snapshot["active_floor"] is snapshot["output_expiry_ms"] is snapshot["watchdog_deadline_ms"] is None
    event = EventRecord(1, 0, EventType.MANUAL_RESET, None, None, None, None, Result.RESET, Reason.MANUAL_REQUEST)
    parsed = json.loads(format_event(event))
    assert parsed["reader_source"] is parsed["facility_code"] is parsed["credential_number"] is parsed["requested_floor"] is None


@pytest.mark.parametrize("formatter,value", [(format_snapshot, object()), (format_event, object())])
def test_formatter_misuse_raises_invariant(formatter: object, value: object) -> None:
    with pytest.raises(StateInvariantError):
        formatter(value)  # type: ignore[operator]


def test_repeated_runs_produce_identical_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    arguments = argv(files(tmp_path), "--source", "LF", "--frame", FRAME, "--floor", "1", "--advance-to", "3000")
    assert run(arguments) == 0
    first = capsys.readouterr()
    assert run(arguments) == 0
    second = capsys.readouterr()
    assert first == second


@pytest.mark.parametrize("which", ["configuration", "credential"])
def test_file_errors_return_one_without_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    which: str,
) -> None:
    paths = files(tmp_path)
    selected = (
        (tmp_path / "missing-config.json", paths[1])
        if which == "configuration"
        else (paths[0], tmp_path / "missing-credentials.json")
    )
    assert run(argv(selected)) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith(f"error: {which}")
    assert "Traceback" not in captured.err


def test_duplicate_key_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    paths = files(tmp_path, records=[record(), record(label="duplicate")])
    assert run(argv(paths)) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("error: duplicate credential key")
    assert "Traceback" not in captured.err


def test_negative_logical_time_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(argv(files(tmp_path), "--advance-to", "-1")) == 1
    captured = capsys.readouterr()
    assert parse_lines(captured.out)[0][0] == "INITIALIZE"
    assert captured.err.startswith("error: target_ms")
    assert "Traceback" not in captured.err


def test_logging_error_response_returns_one(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingController(Controller):
        def initialize(self, config, credentials):  # type: ignore[no-untyped-def]
            response = super().initialize(config, credentials)
            self._event_log.set_append_failure(True)
            return response

    monkeypatch.setattr(cli_module, "Controller", FailingController)
    status = run(argv(files(tmp_path), "--source", "LF", "--frame", FRAME, "--floor", "1"))
    assert status == 1
    captured = capsys.readouterr()
    submit = next(value for label, value in parse_lines(captured.out) if label == "SUBMIT")
    assert submit["reason"] == "logging_error"
    assert captured.err == "error: event logging failed\n"


def test_controller_initialization_response_failure_returns_one(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = Controller.initialize

    def initialize(self: Controller, config: object, credentials: object) -> ControllerResponse:
        original(self, config, credentials)  # type: ignore[arg-type]
        return ControllerResponse(
            Result.ERROR,
            Reason.INVALID_CONFIGURATION,
            ControllerState.INITIALIZING,
            None,
            OutputSnapshot((False,) * 16, None, None),
            False,
        )

    monkeypatch.setattr(Controller, "initialize", initialize)
    assert run(argv(files(tmp_path))) == 1
    captured = capsys.readouterr()
    assert "invalid_configuration" in captured.err
    assert "Traceback" not in captured.err


def test_cli_structure_and_package_metadata_remain_thin_and_offline() -> None:
    source = Path(cli_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported <= {
        "__future__", "argparse", "json", "sys", "collections",
        "clock", "config", "controller", "models",
    }
    forbidden = {
        "time", "datetime", "threading", "asyncio", "socket", "sqlite3",
        "subprocess", "tkinter", "serial", "requests",
    }
    assert imported.isdisjoint(forbidden)
    assert all(token not in source for token in (
        "CredentialRepository", "authorize(", "decode_frame", "floor_mask",
        "OutputManager", "Watchdog(", "EventDraft", "sequence_number =",
        "open(", "write_text", "write_bytes", "sleep(",
    ))
    mutable_nodes = (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)
    assert not any(
        isinstance(node, (ast.Assign, ast.AnnAssign))
        and isinstance(node.value, mutable_nodes)
        for node in tree.body
    )

    assert hasattr(elevator_access_sim, "load_startup_files")
    assert not hasattr(elevator_access_sim, "build_parser")
    assert not hasattr(elevator_access_sim, "format_snapshot")
    metadata = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["scripts"] == {
        "elevator-access-sim": "elevator_access_sim.cli:run"
    }
    assert metadata["project"]["dependencies"] == []
    assert metadata["project"]["version"] == "0.1.0"
