"""SP-06.7 event-append failure policy across every controller path."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from elevator_access_sim import Controller, encode_frame
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.event_log import EventLog
from elevator_access_sim.models import (
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
)


FRAME = encode_frame(1, 100)
CONFIG = SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True)


def graph(records: list[CredentialRecord] | None = None) -> tuple[Controller, EventLog]:
    log = EventLog()
    controller = Controller(SimulatedClock(), log)
    controller.initialize(
        CONFIG,
        records if records is not None else [CredentialRecord(1, 100, True, 65535)],
    )
    return controller, log


def invalid_source() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    return controller, log, lambda: controller.submit(CredentialRequest("LF", FRAME, 1)), "idle"


def invalid_frame() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, (0,), 1)), "idle"


def unknown() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph([])
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1)), "idle"


def disabled() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph([CredentialRecord(1, 100, False, 65535)])
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1)), "idle"


def invalid_floor() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 17)), "idle"


def unauthorized() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph([CredentialRecord(1, 100, True, 0)])
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1)), "idle"


def grant() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    return controller, log, lambda: controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1)), "grant"


def busy() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    return controller, log, lambda: controller.submit(object()), "busy"  # type: ignore[arg-type]


def timeout() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    return controller, log, lambda: controller.advance_to(3000), "timeout"


def manual_reset() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    return controller, log, controller.manual_reset, "reset"


def watchdog_reset() -> tuple[Controller, EventLog, Callable[[], object], str]:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    controller.set_watchdog_service_suppressed(True)
    return controller, log, lambda: controller.advance_to(2000), "reset"


@pytest.mark.parametrize(
    "factory",
    [
        invalid_source,
        invalid_frame,
        unknown,
        disabled,
        invalid_floor,
        unauthorized,
        grant,
        busy,
        timeout,
        manual_reset,
        watchdog_reset,
    ],
    ids=[
        "invalid-source",
        "invalid-frame",
        "unknown",
        "disabled",
        "invalid-floor",
        "unauthorized",
        "grant",
        "busy",
        "output-timeout",
        "manual-reset",
        "watchdog-reset",
    ],
)
def test_tst_log_003_logging_failure_matrix_and_recovery(
    factory: Callable[[], tuple[Controller, EventLog, Callable[[], object], str]],
) -> None:
    controller, log, action, policy = factory()
    before_events = controller.events()
    before_snapshot = controller.snapshot()
    log.set_append_failure(True)

    response = action()

    assert response.result is Result.ERROR
    assert response.reason is Reason.LOGGING_ERROR
    assert response.logging_fault is True
    assert controller.events() == before_events
    assert response.latest_event_sequence == (before_events[-1].sequence_number if before_events else None)
    if policy in ("idle", "grant"):
        assert response.state is ControllerState.IDLE
        assert response.output_snapshot.active_floor is None
    elif policy == "busy":
        assert response.state is ControllerState.OUTPUT_ACTIVE
        assert response.output_snapshot.channels == before_snapshot.output_channels
        assert response.output_snapshot.expiry_ms == before_snapshot.output_expiry_ms
    elif policy in ("timeout", "reset"):
        assert response.state is ControllerState.IDLE
        assert response.output_snapshot.active_floor is None
        assert response.output_snapshot.expiry_ms is None

    log.set_append_failure(False)
    recovered = controller.manual_reset()
    expected_sequence = (before_events[-1].sequence_number if before_events else 0) + 1
    assert recovered.result is Result.RESET
    assert recovered.logging_fault is False
    assert recovered.latest_event_sequence == expected_sequence
    assert controller.events()[-1].sequence_number == expected_sequence
    assert not any(event.event_type is EventType.LOGGING_ERROR for event in controller.events())


def test_timeout_clears_output_before_attempting_event(monkeypatch: pytest.MonkeyPatch) -> None:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    observed: list[tuple[ControllerState, object, object]] = []
    original_append = log.append

    def append(draft):  # type: ignore[no-untyped-def]
        if draft.event_type is EventType.OUTPUT_TIMEOUT:
            snapshot = controller.snapshot()
            observed.append((snapshot.state, snapshot.active_floor, snapshot.output_expiry_ms))
        return original_append(draft)

    monkeypatch.setattr(log, "append", append)
    controller.advance_to(3000)
    assert observed == [(ControllerState.IDLE, None, None)]


@pytest.mark.parametrize("event_type", [EventType.MANUAL_RESET, EventType.WATCHDOG_RESET])
def test_reset_clears_output_before_attempting_event(
    event_type: EventType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    controller, log = graph()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    observed: list[tuple[ControllerState, object]] = []
    original_append = log.append

    def append(draft):  # type: ignore[no-untyped-def]
        if draft.event_type is event_type:
            observed.append((controller.snapshot().state, controller.snapshot().active_floor))
        return original_append(draft)

    monkeypatch.setattr(log, "append", append)
    if event_type is EventType.MANUAL_RESET:
        controller.manual_reset()
    else:
        controller.set_watchdog_service_suppressed(True)
        controller.advance_to(2000)
    assert observed == [(ControllerState.RESETTING, None)]


def test_no_op_does_not_clear_existing_logging_fault() -> None:
    controller, log = graph()
    log.set_append_failure(True)
    controller.submit(CredentialRequest("LF", FRAME, 1))
    log.set_append_failure(False)
    response = controller.advance_to(1)
    assert response.result is response.reason is None
    assert response.logging_fault is True
