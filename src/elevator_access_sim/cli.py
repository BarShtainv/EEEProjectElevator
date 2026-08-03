"""Thin deterministic offline command-line adapter for the simulator."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from .clock import SimulatedClock
from .config import load_startup_files
from .controller import Controller
from .models import (
    ClockError,
    ConfigurationError,
    ControllerResponse,
    ControllerSnapshot,
    CredentialDataError,
    CredentialRequest,
    EventRecord,
    ReaderSource,
    Reason,
    StateInvariantError,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the controlled single-scenario command-line parser."""

    parser = argparse.ArgumentParser(
        prog="elevator-access-sim",
        description="Run one deterministic offline elevator-access simulation.",
    )
    parser.add_argument("--config", required=True, metavar="PATH")
    parser.add_argument("--credentials", required=True, metavar="PATH")
    parser.add_argument("--source", metavar="SOURCE")
    parser.add_argument("--frame", metavar="FRAME")
    parser.add_argument("--floor", type=int, metavar="FLOOR")
    parser.add_argument("--suppress-watchdog", action="store_true")
    advancement = parser.add_mutually_exclusive_group()
    advancement.add_argument("--advance-to", type=int, metavar="MS")
    advancement.add_argument("--advance-by", type=int, metavar="MS")
    parser.add_argument("--manual-reset", action="store_true")
    return parser


def format_snapshot(snapshot: ControllerSnapshot) -> str:
    """Serialize one immutable controller snapshot in frozen field order."""

    if not isinstance(snapshot, ControllerSnapshot):
        raise StateInvariantError("snapshot must be a ControllerSnapshot")
    value = {
        "state": snapshot.state.to_text(),
        "output_channels": snapshot.output_channels,
        "active_floor": snapshot.active_floor,
        "output_expiry_ms": snapshot.output_expiry_ms,
        "watchdog_deadline_ms": snapshot.watchdog_deadline_ms,
        "initialized": snapshot.initialized,
        "configuration_valid": snapshot.configuration_valid,
        "repository_ready": snapshot.repository_ready,
        "latest_event_sequence": snapshot.latest_event_sequence,
    }
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def format_event(event: EventRecord) -> str:
    """Serialize one immutable event using the reviewed nine-field schema."""

    if not isinstance(event, EventRecord):
        raise StateInvariantError("event must be an EventRecord")
    value = {
        "sequence_number": event.sequence_number,
        "timestamp_ms": event.timestamp_ms,
        "event_type": event.event_type.to_text(),
        "reader_source": (
            None if event.reader_source is None else event.reader_source.to_text()
        ),
        "facility_code": event.facility_code,
        "credential_number": event.credential_number,
        "requested_floor": event.requested_floor,
        "result": event.result.to_text(),
        "reason": event.reason.to_text(),
    }
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _format_response(response: ControllerResponse) -> str:
    value = {
        "result": None if response.result is None else response.result.to_text(),
        "reason": None if response.reason is None else response.reason.to_text(),
        "state": response.state.to_text(),
        "latest_event_sequence": response.latest_event_sequence,
        "logging_fault": response.logging_fault,
        "active_floor": response.output_snapshot.active_floor,
        "output_expiry_ms": response.output_snapshot.expiry_ms,
    }
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _source_value(value: str) -> ReaderSource | str:
    if value == "LF":
        return ReaderSource.LF
    if value == "HF":
        return ReaderSource.HF
    return value


def _frame_value(value: str) -> tuple[object, ...]:
    return tuple(
        0 if character == "0" else 1 if character == "1" else character
        for character in value
    )


def _print_response(label: str, response: ControllerResponse) -> None:
    print(f"{label} {_format_response(response)}")


def _logging_failed(response: ControllerResponse) -> bool:
    return response.reason is Reason.LOGGING_ERROR


def _write_error(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)


def run(argv: Sequence[str] | None = None) -> int:
    """Run one deterministic startup and optional controlled operation sequence."""

    parser = build_parser()
    arguments = parser.parse_args(argv)
    request_values = (arguments.source, arguments.frame, arguments.floor)
    supplied = tuple(value is not None for value in request_values)
    if any(supplied) and not all(supplied):
        parser.error("--source, --frame, and --floor must be supplied together")

    try:
        startup = load_startup_files(arguments.config, arguments.credentials)
    except (ConfigurationError, CredentialDataError) as exc:
        _write_error(str(exc))
        return 1

    clock = SimulatedClock(0)
    controller = Controller(clock)
    initialization = controller.initialize(startup.config, startup.credentials)
    _print_response("INITIALIZE", initialization)
    if initialization.result is not None:
        reason = initialization.reason
        _write_error(
            "controller initialization failed"
            if reason is None
            else f"controller initialization failed: {reason.to_text()}"
        )
        return 1

    if arguments.suppress_watchdog:
        suppression = controller.set_watchdog_service_suppressed(True)
        _print_response("SUPPRESSION", suppression)
        if _logging_failed(suppression):
            _write_error("event logging failed")
            return 1

    if all(supplied):
        request = CredentialRequest(
            _source_value(arguments.source),
            _frame_value(arguments.frame),
            arguments.floor,
        )
        submitted = controller.submit(request)
        _print_response("SUBMIT", submitted)
        if _logging_failed(submitted):
            _write_error("event logging failed")
            return 1

    try:
        if arguments.advance_to is not None:
            advanced = controller.advance_to(arguments.advance_to)
            _print_response("ADVANCE", advanced)
            if _logging_failed(advanced):
                _write_error("event logging failed")
                return 1
        elif arguments.advance_by is not None:
            advanced = controller.advance_by(arguments.advance_by)
            _print_response("ADVANCE", advanced)
            if _logging_failed(advanced):
                _write_error("event logging failed")
                return 1
    except ClockError as exc:
        _write_error(str(exc))
        return 1

    if arguments.manual_reset:
        reset = controller.manual_reset()
        _print_response("MANUAL_RESET", reset)
        if _logging_failed(reset):
            _write_error("event logging failed")
            return 1

    print(f"SNAPSHOT {format_snapshot(controller.snapshot())}")
    for event in controller.events():
        print(f"EVENT {format_event(event)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
