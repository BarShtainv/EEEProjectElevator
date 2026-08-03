"""Focused tests for SP-06.1 shared models."""

from dataclasses import FrozenInstanceError

import pytest

from elevator_access_sim.models import (
    ControllerSnapshot,
    ControllerState,
    CredentialKey,
    CredentialRequest,
    EventType,
    OutputSnapshot,
    ReaderSource,
    Reason,
    Result,
    StateInvariantError,
)


INACTIVE = (False,) * 16


def test_tst_src_001_reader_source_values_and_uppercase_serialization() -> None:
    assert {member.name: member.value for member in ReaderSource} == {"LF": 1, "HF": 2}
    assert [member.to_text() for member in ReaderSource] == ["LF", "HF"]


def test_fixed_enum_names_numbers_and_lowercase_serialization() -> None:
    assert {member.name: member.value for member in ControllerState} == {
        "RESETTING": 0,
        "INITIALIZING": 1,
        "IDLE": 2,
        "VALIDATING": 3,
        "LOOKUP": 4,
        "AUTHORIZING": 5,
        "OUTPUT_ACTIVE": 6,
    }
    assert {member.name: member.value for member in EventType} == {
        "ACCESS_DECISION": 1,
        "VALIDATION_ERROR": 2,
        "OUTPUT_TIMEOUT": 3,
        "MANUAL_RESET": 4,
        "WATCHDOG_RESET": 5,
        "LOGGING_ERROR": 6,
    }
    assert {member.name: member.value for member in Result} == {
        "GRANTED": 1,
        "DENIED": 2,
        "ERROR": 3,
        "COMPLETED": 4,
        "RESET": 5,
    }
    assert {member.name: member.value for member in Reason} == {
        "AUTHORIZED": 1,
        "UNKNOWN_CREDENTIAL": 2,
        "DISABLED_CREDENTIAL": 3,
        "UNAUTHORIZED_FLOOR": 4,
        "INVALID_SOURCE": 5,
        "INVALID_FRAME": 6,
        "PARITY_FAILURE": 7,
        "INVALID_FLOOR": 8,
        "CONTROLLER_BUSY": 9,
        "OUTPUT_EXPIRED": 10,
        "MANUAL_REQUEST": 11,
        "WATCHDOG_TIMEOUT": 12,
        "INVALID_CONFIGURATION": 13,
        "INVALID_CREDENTIAL_RECORD": 14,
        "DUPLICATE_CREDENTIAL": 15,
        "REPOSITORY_INITIALIZATION_FAILURE": 16,
        "LOGGING_ERROR": 17,
    }
    for enum_type in (ControllerState, EventType, Result, Reason):
        assert all(member.to_text() == member.name.lower() for member in enum_type)


def test_zero_is_only_a_controller_state_value_not_a_null_enum_member() -> None:
    assert ControllerState(0) is ControllerState.RESETTING
    for enum_type in (ReaderSource, EventType, Result, Reason):
        with pytest.raises(ValueError):
            enum_type(0)


def test_frozen_dataclass_rejects_mutation() -> None:
    key = CredentialKey(1, 100)
    with pytest.raises(FrozenInstanceError):
        key.facility_code = 2  # type: ignore[misc]


def test_tst_crd_001_credential_key_is_an_ordered_pair() -> None:
    assert CredentialKey(1, 100) != CredentialKey(2, 99)
    assert len({CredentialKey(1, 100), CredentialKey(2, 99)}) == 2


def test_credential_request_accepts_unvalidated_raw_boundary_values() -> None:
    request = CredentialRequest(
        reader_source={"invalid": "source"},
        frame=None,
        requested_floor=True,
    )
    assert request.reader_source == {"invalid": "source"}
    assert request.frame is None
    assert request.requested_floor is True


def test_tst_out_004_inactive_output_snapshot_is_valid() -> None:
    assert OutputSnapshot(INACTIVE, None, None).channels == INACTIVE


@pytest.mark.parametrize("floor", [1, 8, 16])
def test_tst_out_004_one_active_output_matches_floor(floor: int) -> None:
    channels = tuple(index == floor - 1 for index in range(16))
    snapshot = OutputSnapshot(channels, floor, 0)
    assert snapshot.active_floor == floor


@pytest.mark.parametrize(
    ("channels", "floor", "expiry"),
    [
        ((False,) * 15, None, None),
        ((False,) * 17, None, None),
        (tuple([False] * 15 + [0]), None, None),
        (tuple([True, True] + [False] * 14), 1, 10),
        (INACTIVE, 1, None),
        (INACTIVE, None, 10),
        (tuple([True] + [False] * 15), 2, 10),
    ],
)
def test_tst_out_004_rejects_invalid_output_shape_or_relationship(
    channels: tuple[bool, ...],
    floor: int | None,
    expiry: int | None,
) -> None:
    with pytest.raises(StateInvariantError):
        OutputSnapshot(channels, floor, expiry)


def test_output_snapshot_rejects_mutable_channel_collection() -> None:
    with pytest.raises(StateInvariantError):
        OutputSnapshot([False] * 16, None, None)  # type: ignore[arg-type]


@pytest.mark.parametrize("floor", [0, 17, -1, True, 1.0, "1"])
def test_output_snapshot_rejects_invalid_active_floor(floor: object) -> None:
    channels = (True,) + (False,) * 15
    with pytest.raises(StateInvariantError):
        OutputSnapshot(channels, floor, 10)  # type: ignore[arg-type]


@pytest.mark.parametrize("expiry", [-1, True, 1.0, "10", None])
def test_output_snapshot_rejects_invalid_active_expiry(expiry: object) -> None:
    channels = (True,) + (False,) * 15
    with pytest.raises(StateInvariantError):
        OutputSnapshot(channels, 1, expiry)  # type: ignore[arg-type]


def test_controller_snapshot_applies_output_invariants() -> None:
    with pytest.raises(StateInvariantError):
        ControllerSnapshot(
            state=ControllerState.OUTPUT_ACTIVE,
            output_channels=(True, True) + (False,) * 14,
            active_floor=1,
            output_expiry_ms=10,
            watchdog_deadline_ms=20,
            initialized=True,
            configuration_valid=True,
            repository_ready=True,
            latest_event_sequence=1,
        )


@pytest.mark.parametrize("value", [True, -1, 1.0])
def test_controller_snapshot_rejects_boolean_or_invalid_integer_traps(value: object) -> None:
    with pytest.raises(StateInvariantError):
        ControllerSnapshot(
            state=ControllerState.IDLE,
            output_channels=INACTIVE,
            active_floor=None,
            output_expiry_ms=None,
            watchdog_deadline_ms=value,  # type: ignore[arg-type]
            initialized=True,
            configuration_valid=True,
            repository_ready=True,
            latest_event_sequence=None,
        )

