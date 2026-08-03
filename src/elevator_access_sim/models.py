"""Shared immutable values and exceptions for the software-only simulator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class _CanonicalIntEnum(IntEnum):
    """Integer enum with explicit canonical text serialization."""

    def to_text(self) -> str:
        return self.name.lower()


class ReaderSource(_CanonicalIntEnum):
    LF = 1
    HF = 2

    def to_text(self) -> str:
        return self.name


class ControllerState(_CanonicalIntEnum):
    RESETTING = 0
    INITIALIZING = 1
    IDLE = 2
    VALIDATING = 3
    LOOKUP = 4
    AUTHORIZING = 5
    OUTPUT_ACTIVE = 6


class EventType(_CanonicalIntEnum):
    ACCESS_DECISION = 1
    VALIDATION_ERROR = 2
    OUTPUT_TIMEOUT = 3
    MANUAL_RESET = 4
    WATCHDOG_RESET = 5
    LOGGING_ERROR = 6


class Result(_CanonicalIntEnum):
    GRANTED = 1
    DENIED = 2
    ERROR = 3
    COMPLETED = 4
    RESET = 5


class Reason(_CanonicalIntEnum):
    AUTHORIZED = 1
    UNKNOWN_CREDENTIAL = 2
    DISABLED_CREDENTIAL = 3
    UNAUTHORIZED_FLOOR = 4
    INVALID_SOURCE = 5
    INVALID_FRAME = 6
    PARITY_FAILURE = 7
    INVALID_FLOOR = 8
    CONTROLLER_BUSY = 9
    OUTPUT_EXPIRED = 10
    MANUAL_REQUEST = 11
    WATCHDOG_TIMEOUT = 12
    INVALID_CONFIGURATION = 13
    INVALID_CREDENTIAL_RECORD = 14
    DUPLICATE_CREDENTIAL = 15
    REPOSITORY_INITIALIZATION_FAILURE = 16
    LOGGING_ERROR = 17


class ElevatorAccessSimError(Exception):
    """Base exception for exceptional simulator conditions."""


class ConfigurationError(ElevatorAccessSimError):
    """Raised when startup configuration is invalid."""


class CredentialDataError(ElevatorAccessSimError):
    """Raised when trusted credential data is invalid."""


class DuplicateCredentialError(CredentialDataError):
    """Raised when an ordered credential key is duplicated."""


class ClockError(ElevatorAccessSimError):
    """Raised for invalid simulated-clock operations."""


class EventLogError(ElevatorAccessSimError):
    """Raised for exceptional event-log infrastructure failures."""


class StateInvariantError(ElevatorAccessSimError):
    """Raised when an impossible internal state is constructed."""


@dataclass(frozen=True, slots=True)
class CredentialRequest:
    reader_source: object
    frame: object
    requested_floor: object


@dataclass(frozen=True, slots=True)
class DecodedCredential:
    facility_code: int
    credential_number: int


@dataclass(frozen=True, slots=True)
class CredentialKey:
    facility_code: int
    credential_number: int


@dataclass(frozen=True, slots=True)
class CredentialRecord:
    facility_code: int
    credential_number: int
    enabled: bool
    floor_mask: int
    label: str | None = None


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    result: Result
    reason: Reason
    decoded_credential: DecodedCredential | None = None
    selected_record: CredentialRecord | None = None
    selected_floor: int | None = None


@dataclass(frozen=True, slots=True)
class EventDraft:
    timestamp_ms: int
    event_type: EventType
    reader_source: ReaderSource | None
    facility_code: int | None
    credential_number: int | None
    requested_floor: int | None
    result: Result
    reason: Reason


@dataclass(frozen=True, slots=True)
class EventRecord:
    sequence_number: int
    timestamp_ms: int
    event_type: EventType
    reader_source: ReaderSource | None
    facility_code: int | None
    credential_number: int | None
    requested_floor: int | None
    result: Result
    reason: Reason


@dataclass(frozen=True, slots=True)
class SimulatorConfig:
    schema_version: int
    profile: str
    output_duration_ms: int
    watchdog_timeout_ms: int
    watchdog_enabled: bool


def _require_optional_nonnegative_integer(value: int | None, field: str) -> None:
    if value is not None and (type(value) is not int or value < 0):
        raise StateInvariantError(f"{field} must be a nonnegative integer or None")


def _validate_output_snapshot(
    channels: tuple[bool, ...],
    active_floor: int | None,
    expiry_ms: int | None,
) -> None:
    if not isinstance(channels, tuple):
        raise StateInvariantError("output channels must be an immutable tuple")
    if len(channels) != 16:
        raise StateInvariantError("output channels must contain exactly 16 values")
    if any(type(value) is not bool for value in channels):
        raise StateInvariantError("every output channel must be a Boolean")

    active_indexes = [index for index, value in enumerate(channels) if value]
    if len(active_indexes) > 1:
        raise StateInvariantError("at most one output channel may be active")

    if not active_indexes:
        if active_floor is not None or expiry_ms is not None:
            raise StateInvariantError("inactive outputs require no active floor or expiry")
        return

    if type(active_floor) is not int or not 1 <= active_floor <= 16:
        raise StateInvariantError("active floor must be an integer from 1 through 16")
    if active_floor != active_indexes[0] + 1:
        raise StateInvariantError("active floor must match the active output channel")
    if type(expiry_ms) is not int or expiry_ms < 0:
        raise StateInvariantError("active output expiry must be a nonnegative integer")


@dataclass(frozen=True, slots=True)
class OutputSnapshot:
    channels: tuple[bool, ...]
    active_floor: int | None
    expiry_ms: int | None

    def __post_init__(self) -> None:
        _validate_output_snapshot(self.channels, self.active_floor, self.expiry_ms)


@dataclass(frozen=True, slots=True)
class ControllerResponse:
    result: Result | None
    reason: Reason | None
    state: ControllerState
    latest_event_sequence: int | None
    output_snapshot: OutputSnapshot
    logging_fault: bool


@dataclass(frozen=True, slots=True)
class ControllerSnapshot:
    state: ControllerState
    output_channels: tuple[bool, ...]
    active_floor: int | None
    output_expiry_ms: int | None
    watchdog_deadline_ms: int | None
    initialized: bool
    configuration_valid: bool
    repository_ready: bool
    latest_event_sequence: int | None

    def __post_init__(self) -> None:
        if not isinstance(self.state, ControllerState):
            raise StateInvariantError("controller state must be a ControllerState")
        for field, value in (
            ("initialized", self.initialized),
            ("configuration_valid", self.configuration_valid),
            ("repository_ready", self.repository_ready),
        ):
            if type(value) is not bool:
                raise StateInvariantError(f"{field} must be a Boolean")
        _validate_output_snapshot(
            self.output_channels,
            self.active_floor,
            self.output_expiry_ms,
        )
        _require_optional_nonnegative_integer(
            self.watchdog_deadline_ms,
            "watchdog deadline",
        )
        if self.latest_event_sequence is not None and (
            type(self.latest_event_sequence) is not int
            or self.latest_event_sequence < 1
        ):
            raise StateInvariantError(
                "latest event sequence must be a positive integer or None"
            )


@dataclass(frozen=True, slots=True)
class FrameValidation:
    ok: bool
    reason: Reason | None
    decoded: DecodedCredential | None


@dataclass(frozen=True, slots=True)
class RepositoryLookup:
    record: CredentialRecord | None


@dataclass(frozen=True, slots=True)
class LogAppendOutcome:
    record: EventRecord | None
    logging_fault: bool


@dataclass(frozen=True, slots=True)
class StartupData:
    config: SimulatorConfig
    credentials: tuple[CredentialRecord, ...]

