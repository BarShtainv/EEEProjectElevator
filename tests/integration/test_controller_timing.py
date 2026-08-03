"""SP-06.7 event-driven scheduler and deterministic timing tests."""

from __future__ import annotations

import pytest

from elevator_access_sim import Controller, encode_frame
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.event_log import EventLog
from elevator_access_sim.models import (
    ClockError,
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
    StateInvariantError,
)


FRAME = encode_frame(1, 100)
RECORD = CredentialRecord(1, 100, True, 65535)


def make_controller(
    *,
    duration: int = 3000,
    timeout: int = 2000,
    enabled: bool = True,
) -> tuple[Controller, SimulatedClock, EventLog]:
    clock = SimulatedClock()
    log = EventLog()
    controller = Controller(clock, log)
    controller.initialize(
        SimulatorConfig(1, "PROJECT_WIEGAND_26", duration, timeout, enabled),
        [RECORD],
    )
    return controller, clock, log


def grant(controller: Controller, floor: int = 1) -> None:
    assert controller.submit(CredentialRequest(ReaderSource.LF, FRAME, floor)).result is Result.GRANTED


def test_no_op_and_future_advance_without_domain_event() -> None:
    controller, clock, _ = make_controller(enabled=False)
    first = controller.advance_to(0)
    second = controller.advance_to(5000)
    assert first.result is first.reason is None
    assert second.result is second.reason is None
    assert clock.now_ms() == 5000
    assert controller.events() == ()


@pytest.mark.parametrize("target", [-1, True, 1.0, "1", None, []])
def test_invalid_or_backward_target_preserves_all_state(target: object) -> None:
    controller, clock, _ = make_controller()
    controller.advance_to(10)
    before = (clock.now_ms(), controller.snapshot(), controller.events())
    with pytest.raises(ClockError):
        controller.advance_to(target)  # type: ignore[arg-type]
    assert (clock.now_ms(), controller.snapshot(), controller.events()) == before


@pytest.mark.parametrize("delta", [-1, True, 1.0, "1", None, []])
def test_invalid_delta_preserves_all_state(delta: object) -> None:
    controller, clock, _ = make_controller()
    before = (clock.now_ms(), controller.snapshot(), controller.events())
    with pytest.raises(ClockError):
        controller.advance_by(delta)  # type: ignore[arg-type]
    assert (clock.now_ms(), controller.snapshot(), controller.events()) == before


def test_advance_by_zero_and_normal_heartbeat_have_no_domain_outcome() -> None:
    controller, clock, _ = make_controller()
    assert controller.advance_by(0).result is None
    response = controller.advance_to(1000)
    assert response.result is response.reason is None
    assert clock.now_ms() == 1000
    assert controller.snapshot().watchdog_deadline_ms == 3000
    assert controller.events() == ()


def test_tst_tim_001_default_output_boundary_and_one_shot_timeout() -> None:
    controller, clock, _ = make_controller()
    grant(controller)
    assert controller.advance_to(2999).result is None
    assert controller.snapshot().active_floor == 1
    response = controller.advance_to(3000)
    assert clock.now_ms() == 3000
    assert (response.result, response.reason, response.state) == (
        Result.COMPLETED,
        Reason.OUTPUT_EXPIRED,
        ControllerState.IDLE,
    )
    assert response.output_snapshot.active_floor is None
    timeout = controller.events()[-1]
    assert timeout.event_type is EventType.OUTPUT_TIMEOUT
    assert timeout.timestamp_ms == 3000
    assert (timeout.reader_source, timeout.facility_code, timeout.credential_number, timeout.requested_floor) == (
        ReaderSource.LF,
        1,
        100,
        1,
    )
    assert controller.advance_to(3000).result is None
    assert controller.advance_to(3001).result is None
    assert sum(event.event_type is EventType.OUTPUT_TIMEOUT for event in controller.events()) == 1


def test_first_advance_after_output_deadline_processes_exact_due_time() -> None:
    controller, clock, _ = make_controller(enabled=False)
    grant(controller)
    response = controller.advance_to(10000)
    assert response.reason is Reason.OUTPUT_EXPIRED
    assert clock.now_ms() == 10000
    assert controller.events()[-1].timestamp_ms == 3000


def test_timeout_recovery_accepts_a_later_valid_request() -> None:
    controller, _, _ = make_controller()
    grant(controller)
    assert controller.advance_to(3000).reason is Reason.OUTPUT_EXPIRED
    response = controller.submit(CredentialRequest(ReaderSource.HF, FRAME, 16))
    assert (response.result, response.reason) == (Result.GRANTED, Reason.AUTHORIZED)
    assert response.output_snapshot.active_floor == 16


def test_default_3000_2000_heartbeat_priority_prevents_watchdog_reset() -> None:
    controller, _, _ = make_controller()
    grant(controller)
    controller.advance_to(2999)
    response = controller.advance_to(3000)
    assert response.reason is Reason.OUTPUT_EXPIRED
    assert [event.event_type for event in controller.events()] == [
        EventType.ACCESS_DECISION,
        EventType.OUTPUT_TIMEOUT,
    ]
    assert controller.snapshot().watchdog_deadline_ms == 5000


def test_long_30000_2000_output_uses_heartbeats_and_expires_once() -> None:
    controller, _, _ = make_controller(duration=30000)
    grant(controller, 16)
    response = controller.advance_to(30000)
    assert (response.result, response.reason) == (Result.COMPLETED, Reason.OUTPUT_EXPIRED)
    assert controller.events()[-1].timestamp_ms == 30000
    assert sum(event.event_type is EventType.WATCHDOG_RESET for event in controller.events()) == 0
    assert sum(event.event_type is EventType.OUTPUT_TIMEOUT for event in controller.events()) == 1


@pytest.mark.parametrize("active", [False, True])
def test_suppressed_watchdog_resets_once_at_2000(active: bool) -> None:
    controller, clock, _ = make_controller()
    if active:
        grant(controller)
    controller.set_watchdog_service_suppressed(True)
    assert controller.advance_to(1999).result is None
    response = controller.advance_to(2000)
    assert clock.now_ms() == 2000
    assert (response.result, response.reason, response.state) == (
        Result.RESET,
        Reason.WATCHDOG_TIMEOUT,
        ControllerState.IDLE,
    )
    assert controller.snapshot().active_floor is None
    assert controller.snapshot().watchdog_deadline_ms == 4000
    assert controller.advance_to(2000).result is None
    assert sum(event.event_type is EventType.WATCHDOG_RESET for event in controller.events()) == 1


def test_watchdog_output_collision_resets_and_cancels_timeout() -> None:
    controller, _, _ = make_controller(duration=2000, timeout=2000)
    grant(controller)
    controller.set_watchdog_service_suppressed(True)
    response = controller.advance_to(2000)
    assert response.reason is Reason.WATCHDOG_TIMEOUT
    assert controller.snapshot().active_floor is None
    assert [event.event_type for event in controller.events()] == [
        EventType.ACCESS_DECISION,
        EventType.WATCHDOG_RESET,
    ]
    assert controller.advance_to(3000).result is None


def test_second_deliberately_suppressed_epoch_is_independent() -> None:
    controller, _, _ = make_controller()
    controller.set_watchdog_service_suppressed(True)
    assert controller.advance_to(2000).reason is Reason.WATCHDOG_TIMEOUT
    controller.set_watchdog_service_suppressed(True)
    assert controller.advance_to(3999).result is None
    assert controller.advance_to(4000).reason is Reason.WATCHDOG_TIMEOUT
    assert controller.advance_to(4000).result is None
    resets = [event for event in controller.events() if event.event_type is EventType.WATCHDOG_RESET]
    assert [event.timestamp_ms for event in resets] == [2000, 4000]


def run_partition_scenario(
    boundaries: list[int],
    *,
    duration: int = 3000,
    suppress: bool = False,
) -> tuple[object, object, object]:
    controller, clock, log = make_controller(duration=duration)
    grant(controller)
    if suppress:
        controller.set_watchdog_service_suppressed(True)
    response = None
    for boundary in boundaries:
        response = controller.advance_to(boundary)
    return response, controller.snapshot(), (controller.events(), log.to_jsonl(), clock.now_ms())


@pytest.mark.parametrize(
    "duration,final,partition,suppress",
    [
        (3000, 3000, [999, 1000, 1999, 2000, 2999, 3000], False),
        (3000, 2000, [1, 999, 1000, 1999, 2000], True),
        (30000, 30000, list(range(1000, 30001, 1000)), False),
    ],
)
def test_large_and_partitioned_advances_are_equivalent(
    duration: int,
    final: int,
    partition: list[int],
    suppress: bool,
) -> None:
    large = run_partition_scenario([final], duration=duration, suppress=suppress)
    small = run_partition_scenario(partition, duration=duration, suppress=suppress)
    assert large == small


def test_deterministic_replay_including_json_lines() -> None:
    schedule = [500, 1000, 1999, 2000, 2500, 3000]
    first = run_partition_scenario(schedule)
    second = run_partition_scenario(schedule)
    assert first == second


def test_snapshot_does_not_process_due_events() -> None:
    controller, clock, _ = make_controller(enabled=False)
    grant(controller)
    clock.advance_to(3000)
    before_events = controller.events()
    snapshot = controller.snapshot()
    assert snapshot.active_floor == 1
    assert controller.events() == before_events


def test_stale_internal_due_marker_raises_invariant() -> None:
    controller, clock, _ = make_controller(enabled=False)
    grant(controller)
    clock.advance_to(4000)
    before = controller.snapshot()
    with pytest.raises(StateInvariantError, match="stale"):
        controller.advance_to(5000)
    assert controller.snapshot() == before
