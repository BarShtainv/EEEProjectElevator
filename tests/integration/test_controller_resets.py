"""SP-06.7 manual and watchdog reset preservation tests."""

from __future__ import annotations

import pytest

from elevator_access_sim import Controller, encode_frame
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.event_log import EventLog
from elevator_access_sim.models import (
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    DecodedCredential,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
)


FRAME = encode_frame(1, 100)
CONFIG = SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True)
RECORD = CredentialRecord(1, 100, True, 65535)


def active_controller() -> tuple[Controller, SimulatedClock, EventLog]:
    clock = SimulatedClock()
    log = EventLog()
    controller = Controller(clock, log)
    controller.initialize(CONFIG, [RECORD])
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    return controller, clock, log


def test_tst_rst_001_manual_reset_clears_runtime_and_preserves_owned_startup_data() -> None:
    controller, clock, _ = active_controller()
    clock.advance_to(500)
    config_identity = controller._config
    repository_identity = controller._repository
    prior = controller.events()

    response = controller.manual_reset()

    assert (response.result, response.reason, response.state) == (
        Result.RESET,
        Reason.MANUAL_REQUEST,
        ControllerState.IDLE,
    )
    assert clock.now_ms() == 500
    assert controller._config is config_identity
    assert controller._repository is repository_identity
    assert response.output_snapshot.active_floor is None
    assert controller.snapshot().watchdog_deadline_ms == 2500
    assert controller.events()[:-1] == prior
    assert controller.events()[-1].event_type is EventType.MANUAL_RESET
    assert controller.events()[-1].timestamp_ms == 500
    assert controller.events()[-1].sequence_number == 2
    assert (controller._request, controller._decoded, controller._selected_record, controller._decision, controller._active_context) == (None, None, None, None, None)


def test_manual_reset_cancels_timeout_and_allows_later_grant() -> None:
    controller, _, _ = active_controller()
    controller.manual_reset()
    controller.advance_to(3000)
    assert not any(event.event_type is EventType.OUTPUT_TIMEOUT for event in controller.events())
    assert controller.submit(CredentialRequest(ReaderSource.HF, FRAME, 16)).result is Result.GRANTED


def test_watchdog_reset_preserves_data_and_allows_later_grant() -> None:
    controller, clock, _ = active_controller()
    config_identity = controller._config
    repository_identity = controller._repository
    controller.set_watchdog_service_suppressed(True)
    response = controller.advance_to(2000)

    assert (response.result, response.reason) == (Result.RESET, Reason.WATCHDOG_TIMEOUT)
    assert clock.now_ms() == 2000
    assert controller._config is config_identity
    assert controller._repository is repository_identity
    assert controller.snapshot().watchdog_deadline_ms == 4000
    assert controller.submit(CredentialRequest(ReaderSource.HF, FRAME, 2)).result is Result.GRANTED


@pytest.mark.parametrize("target_state", list(ControllerState))
def test_tst_sta_001_manual_reset_from_every_valid_state(
    target_state: ControllerState,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    controller, clock, _ = active_controller()
    config_identity = controller._config
    repository_identity = controller._repository
    prior_events = controller.events()
    observed_states: list[ControllerState] = []
    original_append = controller._event_log.append

    def observing_append(draft):  # type: ignore[no-untyped-def]
        observed_states.append(controller._state)
        return original_append(draft)

    monkeypatch.setattr(controller._event_log, "append", observing_append)
    if target_state is not ControllerState.OUTPUT_ACTIVE:
        controller._outputs.reset()
        controller._active_context = None
    if target_state in (ControllerState.VALIDATING, ControllerState.LOOKUP, ControllerState.AUTHORIZING):
        controller._request = CredentialRequest(ReaderSource.LF, FRAME, 1)
    if target_state in (ControllerState.LOOKUP, ControllerState.AUTHORIZING):
        controller._decoded = DecodedCredential(1, 100)
    if target_state is ControllerState.AUTHORIZING:
        controller._selected_record = RECORD
    controller._state = target_state
    response = controller.manual_reset()

    assert observed_states == [ControllerState.RESETTING]
    assert response.state is ControllerState.IDLE
    assert response.reason is Reason.MANUAL_REQUEST
    assert controller.snapshot().active_floor is None
    assert controller._config is config_identity
    assert controller._repository is repository_identity
    assert clock.now_ms() == 0
    assert controller.events()[:-1] == prior_events
    assert controller.events()[-1].sequence_number == prior_events[-1].sequence_number + 1
    assert (controller._request, controller._decoded, controller._selected_record, controller._decision, controller._active_context) == (None, None, None, None, None)


def test_repeated_manual_resets_each_form_a_distinct_requested_reset() -> None:
    controller, _, _ = active_controller()
    first = controller.manual_reset()
    second = controller.manual_reset()
    assert first.reason is second.reason is Reason.MANUAL_REQUEST
    resets = [event for event in controller.events() if event.event_type is EventType.MANUAL_RESET]
    assert [event.sequence_number for event in resets] == [2, 3]


def test_reset_events_have_null_request_context() -> None:
    controller, _, _ = active_controller()
    controller.manual_reset()
    event = controller.events()[-1]
    assert (event.reader_source, event.facility_code, event.credential_number, event.requested_floor) == (None, None, None, None)

    controller.set_watchdog_service_suppressed(True)
    controller.advance_to(2000)
    event = controller.events()[-1]
    assert event.event_type is EventType.WATCHDOG_RESET
    assert (event.reader_source, event.facility_code, event.credential_number, event.requested_floor) == (None, None, None, None)
