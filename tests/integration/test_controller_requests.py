"""SP-06.7 end-to-end request coordination tests."""

from __future__ import annotations

import pytest

import elevator_access_sim.controller as controller_module
from elevator_access_sim import Controller, encode_frame
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.models import (
    AuthorizationDecision,
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventType,
    FrameValidation,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
    StateInvariantError,
)


CONFIG = SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True)
FRAME = encode_frame(1, 100)


def make_controller(
    records: list[CredentialRecord] | None = None,
    *,
    config: SimulatorConfig = CONFIG,
) -> Controller:
    controller = Controller(SimulatedClock())
    controller.initialize(
        config,
        records if records is not None else [CredentialRecord(1, 100, True, 65535)],
    )
    return controller


@pytest.mark.parametrize("source", [ReaderSource.LF, ReaderSource.HF])
def test_tst_src_001_successful_lf_and_hf_grants(source: ReaderSource) -> None:
    controller = make_controller()
    response = controller.submit(CredentialRequest(source, FRAME, 16))

    assert (response.result, response.reason, response.state) == (
        Result.GRANTED,
        Reason.AUTHORIZED,
        ControllerState.OUTPUT_ACTIVE,
    )
    assert response.output_snapshot.channels[15]
    assert sum(response.output_snapshot.channels) == 1
    assert response.output_snapshot.expiry_ms == 3000
    assert controller.events()[-1].reader_source is source


def test_tst_dat_003_same_frame_decodes_identically_for_both_sources() -> None:
    observations = []
    for source in (ReaderSource.LF, ReaderSource.HF):
        controller = make_controller()
        controller.submit(CredentialRequest(source, FRAME, 1))
        event = controller.events()[0]
        observations.append((event.facility_code, event.credential_number, event.requested_floor))
    assert observations == [(1, 100, 1), (1, 100, 1)]


@pytest.mark.parametrize("floor", range(1, 17))
def test_tst_out_002_all_sixteen_controller_grants(floor: int) -> None:
    controller = make_controller([CredentialRecord(1, 100, True, 1 << (floor - 1))])
    response = controller.submit(CredentialRequest(ReaderSource.LF, FRAME, floor))
    assert response.result is Result.GRANTED
    assert response.output_snapshot.channels[floor - 1]
    assert sum(response.output_snapshot.channels) == 1


@pytest.mark.parametrize("source", [1, 2, True, "LF", "HF", None, [], {}, object()])
def test_tst_src_002_invalid_source_has_null_context(source: object) -> None:
    controller = make_controller()
    response = controller.submit(CredentialRequest(source, object(), object()))
    event = controller.events()[0]
    assert (response.result, response.reason, response.state) == (
        Result.ERROR,
        Reason.INVALID_SOURCE,
        ControllerState.IDLE,
    )
    assert event.event_type is EventType.VALIDATION_ERROR
    assert (event.reader_source, event.facility_code, event.credential_number, event.requested_floor) == (None, None, None, None)
    assert response.output_snapshot.active_floor is None


@pytest.mark.parametrize(
    "frame",
    [None, object(), "0" * 26, (), (0,) * 25, (0,) * 27, (0,) * 12 + (2,) + (0,) * 13, (0,) * 12 + (True,) + (0,) * 13],
)
def test_invalid_frame_structures_map_context(frame: object) -> None:
    controller = make_controller()
    response = controller.submit(CredentialRequest(ReaderSource.HF, frame, 1))
    event = controller.events()[0]
    assert (response.result, response.reason) == (Result.ERROR, Reason.INVALID_FRAME)
    assert event.event_type is EventType.VALIDATION_ERROR
    assert event.reader_source is ReaderSource.HF
    assert (event.facility_code, event.credential_number, event.requested_floor) == (None, None, None)


@pytest.mark.parametrize("index", [0, 1, 13, 25])
def test_leading_and_trailing_parity_failures(index: int) -> None:
    corrupted = FRAME[:index] + (1 - FRAME[index],) + FRAME[index + 1 :]
    controller = make_controller()
    response = controller.submit(CredentialRequest(ReaderSource.LF, corrupted, 1))
    assert response.reason is Reason.PARITY_FAILURE
    assert controller.events()[0].event_type is EventType.VALIDATION_ERROR
    assert controller.events()[0].reader_source is ReaderSource.LF


@pytest.mark.parametrize("floor", [None, True, 0, 17, object()])
def test_unknown_credential_precedes_floor_validation(floor: object) -> None:
    controller = make_controller([])
    response = controller.submit(CredentialRequest(ReaderSource.LF, FRAME, floor))
    event = controller.events()[0]
    assert (response.result, response.reason) == (Result.DENIED, Reason.UNKNOWN_CREDENTIAL)
    assert (event.facility_code, event.credential_number, event.requested_floor) == (1, 100, None)


@pytest.mark.parametrize("floor", [None, True, 0, 17, object()])
def test_disabled_credential_precedes_floor_validation(floor: object) -> None:
    controller = make_controller([CredentialRecord(1, 100, False, 65535)])
    response = controller.submit(CredentialRequest(ReaderSource.HF, FRAME, floor))
    event = controller.events()[0]
    assert (response.result, response.reason) == (Result.DENIED, Reason.DISABLED_CREDENTIAL)
    assert (event.facility_code, event.credential_number, event.requested_floor) == (1, 100, None)


@pytest.mark.parametrize("floor", [None, True, 0, 17, -1, 1.0, "1", [], {}])
def test_invalid_floor_for_known_enabled_record(floor: object) -> None:
    controller = make_controller()
    response = controller.submit(CredentialRequest(ReaderSource.LF, FRAME, floor))
    event = controller.events()[0]
    assert (response.result, response.reason) == (Result.ERROR, Reason.INVALID_FLOOR)
    assert event.event_type is EventType.VALIDATION_ERROR
    assert (event.facility_code, event.credential_number, event.requested_floor) == (1, 100, None)


@pytest.mark.parametrize("floor", range(1, 17))
def test_clear_permission_bit_denies_without_activation(floor: int) -> None:
    controller = make_controller([CredentialRecord(1, 100, True, 0)])
    response = controller.submit(CredentialRequest(ReaderSource.HF, FRAME, floor))
    event = controller.events()[0]
    assert (response.result, response.reason) == (Result.DENIED, Reason.UNAUTHORIZED_FLOOR)
    assert event.requested_floor == floor
    assert response.output_snapshot.active_floor is None


def test_invalid_and_denied_requests_are_recoverable() -> None:
    controller = make_controller()
    assert controller.submit(CredentialRequest("LF", FRAME, 1)).reason is Reason.INVALID_SOURCE
    assert controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 17)).reason is Reason.INVALID_FLOOR
    assert controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1)).result is Result.GRANTED
    assert [event.sequence_number for event in controller.events()] == [1, 2, 3]


def test_busy_precedes_type_and_hostile_attribute_inspection(monkeypatch: pytest.MonkeyPatch) -> None:
    controller = make_controller()
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    original = controller.snapshot()
    calls: list[str] = []

    class Hostile:
        def __getattribute__(self, name: str) -> object:
            calls.append(name)
            raise AssertionError("request inspected")

    monkeypatch.setattr(controller_module, "validate_frame", lambda value: (_ for _ in ()).throw(AssertionError("frame called")))
    monkeypatch.setattr(controller_module, "authorize", lambda *args: (_ for _ in ()).throw(AssertionError("authorize called")))
    assert controller._repository is not None
    monkeypatch.setattr(controller._repository, "lookup", lambda key: (_ for _ in ()).throw(AssertionError("lookup called")))
    monkeypatch.setattr(controller._outputs, "activate", lambda *args: (_ for _ in ()).throw(AssertionError("activate called")))
    response = controller.submit(Hostile())  # type: ignore[arg-type]

    assert calls == []
    assert (response.result, response.reason, response.state) == (
        Result.DENIED,
        Reason.CONTROLLER_BUSY,
        ControllerState.OUTPUT_ACTIVE,
    )
    assert response.output_snapshot == controller._outputs.snapshot()
    assert controller.snapshot().output_channels == original.output_channels
    assert controller.snapshot().output_expiry_ms == original.output_expiry_ms
    busy = controller.events()[-1]
    assert (busy.reader_source, busy.facility_code, busy.credential_number, busy.requested_floor) == (None, None, None, None)


def test_idle_non_request_is_invariant_error_without_change() -> None:
    controller = make_controller()
    before = controller.snapshot()
    with pytest.raises(StateInvariantError):
        controller.submit(object())  # type: ignore[arg-type]
    assert controller.snapshot() == before
    assert controller.events() == ()


def test_processing_state_at_collaborator_boundaries(monkeypatch: pytest.MonkeyPatch) -> None:
    controller = make_controller()
    original_validate = controller_module.validate_frame
    original_authorize = controller_module.authorize
    repository = controller._repository
    assert repository is not None
    original_lookup = repository.lookup
    seen: list[ControllerState] = []

    def validating(frame: object) -> FrameValidation:
        seen.append(controller.snapshot().state)
        return original_validate(frame)

    def lookup(key: object):  # type: ignore[no-untyped-def]
        seen.append(controller.snapshot().state)
        return original_lookup(key)  # type: ignore[arg-type]

    def authorizing(*args: object) -> AuthorizationDecision:
        seen.append(controller.snapshot().state)
        return original_authorize(*args)  # type: ignore[arg-type]

    monkeypatch.setattr(controller_module, "validate_frame", validating)
    monkeypatch.setattr(repository, "lookup", lookup)
    monkeypatch.setattr(controller_module, "authorize", authorizing)
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    assert seen == [ControllerState.VALIDATING, ControllerState.LOOKUP, ControllerState.AUTHORIZING]


def test_successful_grant_append_precedes_activation(monkeypatch: pytest.MonkeyPatch) -> None:
    controller = make_controller()
    original_append = controller._event_log.append
    original_activate = controller._outputs.activate
    order: list[str] = []

    def append(draft):  # type: ignore[no-untyped-def]
        assert controller.snapshot().state is ControllerState.AUTHORIZING
        assert controller.snapshot().active_floor is None
        order.append("append")
        return original_append(draft)

    def activate(*args):  # type: ignore[no-untyped-def]
        order.append("activate")
        return original_activate(*args)

    monkeypatch.setattr(controller._event_log, "append", append)
    monkeypatch.setattr(controller._outputs, "activate", activate)
    controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    assert order == ["append", "activate"]


def test_activation_invariant_after_successful_append_propagates_without_log_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    controller = make_controller()
    monkeypatch.setattr(
        controller._outputs,
        "activate",
        lambda *args: (_ for _ in ()).throw(StateInvariantError("injected activation defect")),
    )
    with pytest.raises(StateInvariantError, match="activation defect"):
        controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
    assert len(controller.events()) == 1
    assert controller.events()[0].reason is Reason.AUTHORIZED
    assert controller.snapshot().active_floor is None


@pytest.mark.parametrize(
    "lookup_outcome",
    [
        object(),
        controller_module.RepositoryLookup(object()),
        controller_module.RepositoryLookup(CredentialRecord(2, 100, True, 65535)),
        controller_module.RepositoryLookup(CredentialRecord(1, 100, 1, 65535)),
    ],
)
def test_invalid_repository_outcomes_raise_invariant(
    monkeypatch: pytest.MonkeyPatch,
    lookup_outcome: object,
) -> None:
    controller = make_controller()
    assert controller._repository is not None
    monkeypatch.setattr(controller._repository, "lookup", lambda key: lookup_outcome)
    with pytest.raises(StateInvariantError):
        controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))


@pytest.mark.parametrize(
    "validation",
    [
        object(),
        FrameValidation(True, None, None),
        FrameValidation(True, Reason.INVALID_FRAME, None),
        FrameValidation(False, Reason.AUTHORIZED, None),
        FrameValidation(False, Reason.INVALID_FRAME, controller_module.DecodedCredential(1, 100)),
    ],
)
def test_invalid_frame_collaborator_outcomes_raise_invariant(
    monkeypatch: pytest.MonkeyPatch,
    validation: object,
) -> None:
    controller = make_controller()
    monkeypatch.setattr(controller_module, "validate_frame", lambda frame: validation)
    with pytest.raises(StateInvariantError):
        controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))


@pytest.mark.parametrize(
    "decision",
    [
        object(),
        AuthorizationDecision(Result.GRANTED, Reason.AUTHORIZED, None, None, 1),
        AuthorizationDecision(Result.DENIED, Reason.UNKNOWN_CREDENTIAL, None, None, None),
        AuthorizationDecision(Result.GRANTED, Reason.AUTHORIZED, controller_module.DecodedCredential(1, 100), CredentialRecord(1, 100, True, 65535), None),
    ],
)
def test_invalid_authorization_collaborator_outcomes_raise_invariant(
    monkeypatch: pytest.MonkeyPatch,
    decision: object,
) -> None:
    controller = make_controller()
    monkeypatch.setattr(controller_module, "authorize", lambda *args: decision)
    with pytest.raises(StateInvariantError):
        controller.submit(CredentialRequest(ReaderSource.LF, FRAME, 1))
