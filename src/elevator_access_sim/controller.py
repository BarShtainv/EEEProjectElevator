"""Deterministic coordination of the simulator's reviewed domain managers."""

from __future__ import annotations

from collections.abc import Sequence

from .authorization import authorize
from .clock import SimulatedClock
from .credentials import CredentialRepository
from .event_log import EventLog
from .models import (
    AuthorizationDecision,
    ClockError,
    ConfigurationError,
    ControllerResponse,
    ControllerSnapshot,
    ControllerState,
    CredentialDataError,
    CredentialKey,
    CredentialRecord,
    CredentialRequest,
    DecodedCredential,
    DuplicateCredentialError,
    EventDraft,
    EventLogError,
    EventRecord,
    EventType,
    FrameValidation,
    LogAppendOutcome,
    ReaderSource,
    Reason,
    RepositoryLookup,
    Result,
    SimulatorConfig,
    StateInvariantError,
)
from .outputs import OutputManager
from .watchdog import Watchdog
from .wiegand import validate_frame


_ActiveContext = tuple[
    ReaderSource | None,
    int | None,
    int | None,
    int | None,
]


class Controller:
    """Compose validation, authorization, output, watchdog, and event behavior."""

    def __init__(
        self,
        clock: SimulatedClock,
        event_log: EventLog | None = None,
    ) -> None:
        if not isinstance(clock, SimulatedClock):
            raise StateInvariantError("clock must be a SimulatedClock")
        if event_log is not None and not isinstance(event_log, EventLog):
            raise StateInvariantError("event_log must be an EventLog or None")

        self._clock = clock
        self._event_log = EventLog() if event_log is None else event_log
        self._state = ControllerState.RESETTING
        self._config: SimulatorConfig | None = None
        self._repository: CredentialRepository | None = None
        self._outputs = OutputManager()
        self._watchdog: Watchdog | None = None
        self._initialized = False
        self._configuration_valid = False
        self._repository_ready = False
        self._logging_fault = False
        self._request: CredentialRequest | None = None
        self._decoded: DecodedCredential | None = None
        self._selected_record: CredentialRecord | None = None
        self._decision: AuthorizationDecision | None = None
        self._active_context: _ActiveContext | None = None

    def initialize(
        self,
        config: SimulatorConfig,
        credentials: Sequence[CredentialRecord],
    ) -> ControllerResponse:
        """Clear startup state and atomically publish validated candidates."""

        self._state = ControllerState.RESETTING
        self._outputs.reset()
        self._clear_transients()
        self._event_log.clear_startup()
        self._config = None
        self._repository = None
        self._watchdog = None
        self._initialized = False
        self._configuration_valid = False
        self._repository_ready = False
        self._logging_fault = False
        self._state = ControllerState.INITIALIZING

        try:
            candidate_config = self._validated_config(config)
        except ConfigurationError:
            return self._startup_failure(Reason.INVALID_CONFIGURATION)

        try:
            candidate_repository = CredentialRepository.from_records(credentials)
        except DuplicateCredentialError:
            return self._startup_failure(Reason.DUPLICATE_CREDENTIAL)
        except CredentialDataError:
            return self._startup_failure(Reason.INVALID_CREDENTIAL_RECORD)
        except StateInvariantError:
            raise
        except Exception:
            return self._startup_failure(Reason.REPOSITORY_INITIALIZATION_FAILURE)

        candidate_watchdog = Watchdog(
            candidate_config.watchdog_enabled,
            candidate_config.watchdog_timeout_ms,
            self._clock.now_ms(),
        )
        self._config = candidate_config
        self._repository = candidate_repository
        self._watchdog = candidate_watchdog
        self._configuration_valid = True
        self._repository_ready = True
        self._initialized = True
        self._state = ControllerState.IDLE
        return self._response()

    def submit(self, request: CredentialRequest) -> ControllerResponse:
        """Process one request with busy precedence and fail-closed logging."""

        self._require_operational()
        output = self._outputs.snapshot()
        if output.active_floor is not None or self._state is ControllerState.OUTPUT_ACTIVE:
            self._state = ControllerState.OUTPUT_ACTIVE
            outcome = self._append_event(
                EventType.ACCESS_DECISION,
                Result.DENIED,
                Reason.CONTROLLER_BUSY,
            )
            if outcome.logging_fault:
                return self._response(Result.ERROR, Reason.LOGGING_ERROR)
            return self._response(Result.DENIED, Reason.CONTROLLER_BUSY)

        if not isinstance(request, CredentialRequest):
            raise StateInvariantError("request must be a CredentialRequest")
        if self._state is not ControllerState.IDLE:
            raise StateInvariantError("idle request processing requires IDLE state")

        self._state = ControllerState.VALIDATING
        self._request = request
        source = request.reader_source
        if type(source) is not ReaderSource or source not in (
            ReaderSource.LF,
            ReaderSource.HF,
        ):
            return self._complete_idle_event(
                EventType.VALIDATION_ERROR,
                Result.ERROR,
                Reason.INVALID_SOURCE,
            )

        validation = validate_frame(request.frame)
        if not isinstance(validation, FrameValidation):
            raise StateInvariantError("validate_frame returned an invalid outcome")
        if not validation.ok:
            if validation.decoded is not None or validation.reason not in (
                Reason.INVALID_FRAME,
                Reason.PARITY_FAILURE,
            ):
                raise StateInvariantError("validate_frame returned an impossible failure")
            return self._complete_idle_event(
                EventType.VALIDATION_ERROR,
                Result.ERROR,
                validation.reason,
                source,
            )
        if validation.reason is not None or not isinstance(
            validation.decoded,
            DecodedCredential,
        ):
            raise StateInvariantError("successful validation requires decoded data")

        decoded = validation.decoded
        self._decoded = decoded
        self._state = ControllerState.LOOKUP
        repository = self._repository
        if repository is None:
            raise StateInvariantError("repository disappeared during processing")
        lookup = repository.lookup(
            CredentialKey(decoded.facility_code, decoded.credential_number)
        )
        if not isinstance(lookup, RepositoryLookup):
            raise StateInvariantError("repository returned an invalid lookup outcome")
        record = lookup.record
        if record is None:
            return self._complete_idle_event(
                EventType.ACCESS_DECISION,
                Result.DENIED,
                Reason.UNKNOWN_CREDENTIAL,
                source,
                decoded.facility_code,
                decoded.credential_number,
            )
        if not isinstance(record, CredentialRecord):
            raise StateInvariantError("repository returned an invalid record")
        if (
            record.facility_code != decoded.facility_code
            or record.credential_number != decoded.credential_number
            or type(record.enabled) is not bool
        ):
            raise StateInvariantError("repository returned an inconsistent record")
        self._selected_record = record
        if not record.enabled:
            return self._complete_idle_event(
                EventType.ACCESS_DECISION,
                Result.DENIED,
                Reason.DISABLED_CREDENTIAL,
                source,
                decoded.facility_code,
                decoded.credential_number,
            )

        self._state = ControllerState.AUTHORIZING
        decision = authorize(decoded, record, request.requested_floor)
        if not isinstance(decision, AuthorizationDecision):
            raise StateInvariantError("authorize returned an invalid decision")
        self._decision = decision
        self._validate_decision(decision, decoded, record)

        if decision.reason is Reason.INVALID_FLOOR:
            return self._complete_idle_event(
                EventType.VALIDATION_ERROR,
                Result.ERROR,
                Reason.INVALID_FLOOR,
                source,
                decoded.facility_code,
                decoded.credential_number,
            )
        if decision.reason is Reason.UNAUTHORIZED_FLOOR:
            return self._complete_idle_event(
                EventType.ACCESS_DECISION,
                Result.DENIED,
                Reason.UNAUTHORIZED_FLOOR,
                source,
                decoded.facility_code,
                decoded.credential_number,
                decision.selected_floor,
            )

        selected_floor = decision.selected_floor
        if decision.reason is not Reason.AUTHORIZED or type(selected_floor) is not int:
            raise StateInvariantError("authorize returned an impossible grant")
        outcome = self._append_event(
            EventType.ACCESS_DECISION,
            Result.GRANTED,
            Reason.AUTHORIZED,
            source,
            decoded.facility_code,
            decoded.credential_number,
            selected_floor,
        )
        if outcome.logging_fault:
            self._state = ControllerState.IDLE
            self._clear_request_transients()
            return self._response(Result.ERROR, Reason.LOGGING_ERROR)

        config = self._config
        if config is None:
            raise StateInvariantError("configuration disappeared during processing")
        self._outputs.activate(
            selected_floor,
            self._clock.now_ms(),
            config.output_duration_ms,
        )
        self._active_context = (
            source,
            decoded.facility_code,
            decoded.credential_number,
            selected_floor,
        )
        self._clear_request_transients()
        self._state = ControllerState.OUTPUT_ACTIVE
        return self._response(Result.GRANTED, Reason.AUTHORIZED)

    def advance_to(self, target_ms: int) -> ControllerResponse:
        """Advance logical time by jumping only between due domain timestamps."""

        self._require_operational()
        current = self._clock.now_ms()
        if type(target_ms) is not int or target_ms < 0:
            raise ClockError("target_ms must be a nonnegative integer")
        if target_ms < current:
            raise ClockError("target_ms cannot be earlier than current time")

        last_result: Result | None = None
        last_reason: Reason | None = None
        while True:
            current = self._clock.now_ms()
            due_times = self._due_times(current)
            bounded = [timestamp for timestamp in due_times if timestamp <= target_ms]
            if not bounded:
                if current < target_ms:
                    self._clock.advance_to(target_ms)
                break

            due = min(bounded)
            if current < due:
                self._clock.advance_to(due)
            now = self._clock.now_ms()
            watchdog = self._watchdog
            if watchdog is None:
                raise StateInvariantError("watchdog disappeared during advancement")

            if watchdog.next_heartbeat_ms() == now:
                heartbeat_result = watchdog.process_heartbeat(now)
                if type(heartbeat_result) is not bool:
                    raise StateInvariantError("watchdog returned an invalid heartbeat outcome")
                next_heartbeat = watchdog.next_heartbeat_ms()
                if next_heartbeat is not None and next_heartbeat <= now:
                    raise StateInvariantError("watchdog did not consume the due heartbeat")

            deadline = watchdog.expiry_deadline_ms()
            if deadline is not None and deadline <= now:
                expiry_requested = watchdog.expiry_request_if_due(now)
                if type(expiry_requested) is not bool:
                    raise StateInvariantError("watchdog returned an invalid expiry outcome")
                if expiry_requested:
                    response = self._watchdog_reset()
                    last_result, last_reason = response.result, response.reason
                    continue
                raise StateInvariantError("due watchdog expiry produced no request")

            expiry = self._outputs.next_expiry_ms()
            if expiry is not None and expiry <= now:
                context = self._timeout_context()
                if not self._outputs.expire_if_due(now):
                    raise StateInvariantError("due output did not expire")
                self._state = ControllerState.IDLE
                self._active_context = None
                outcome = self._append_event(
                    EventType.OUTPUT_TIMEOUT,
                    Result.COMPLETED,
                    Reason.OUTPUT_EXPIRED,
                    *context,
                )
                if outcome.logging_fault:
                    last_result, last_reason = Result.ERROR, Reason.LOGGING_ERROR
                else:
                    last_result, last_reason = Result.COMPLETED, Reason.OUTPUT_EXPIRED

        return self._response(last_result, last_reason)

    def advance_by(self, delta_ms: int) -> ControllerResponse:
        """Advance by an exact nonnegative logical-time delta."""

        self._require_operational()
        if type(delta_ms) is not int or delta_ms < 0:
            raise ClockError("delta_ms must be a nonnegative integer")
        return self.advance_to(self._clock.now_ms() + delta_ms)

    def manual_reset(self) -> ControllerResponse:
        """Complete a runtime reset while preserving validated startup state."""

        self._require_operational()
        return self._perform_reset(
            EventType.MANUAL_RESET,
            Reason.MANUAL_REQUEST,
        )

    def set_watchdog_service_suppressed(
        self,
        suppressed: bool,
    ) -> ControllerResponse:
        """Set the reviewed deterministic watchdog fault control."""

        self._require_operational()
        watchdog = self._watchdog
        if watchdog is None:
            raise StateInvariantError("watchdog disappeared")
        watchdog.set_service_suppressed(suppressed)
        return self._response()

    def snapshot(self) -> ControllerSnapshot:
        """Return a fresh immutable observation without processing due work."""

        output = self._outputs.snapshot()
        deadline = (
            None if self._watchdog is None else self._watchdog.expiry_deadline_ms()
        )
        return ControllerSnapshot(
            self._state,
            output.channels,
            output.active_floor,
            output.expiry_ms,
            deadline,
            self._initialized,
            self._configuration_valid,
            self._repository_ready,
            self._event_log.latest_sequence(),
        )

    def events(self) -> tuple[EventRecord, ...]:
        """Return successful events in event-log sequence order."""

        return self._event_log.records()

    @staticmethod
    def _validated_config(value: object) -> SimulatorConfig:
        if not isinstance(value, SimulatorConfig):
            raise ConfigurationError("config must be a SimulatorConfig")
        if type(value.schema_version) is not int or value.schema_version != 1:
            raise ConfigurationError("schema_version must be integer 1")
        if type(value.profile) is not str or value.profile != "PROJECT_WIEGAND_26":
            raise ConfigurationError("profile is invalid")
        if (
            type(value.output_duration_ms) is not int
            or not 100 <= value.output_duration_ms <= 30000
        ):
            raise ConfigurationError("output_duration_ms is invalid")
        if (
            type(value.watchdog_timeout_ms) is not int
            or not 1 <= value.watchdog_timeout_ms <= 4294967295
        ):
            raise ConfigurationError("watchdog_timeout_ms is invalid")
        if type(value.watchdog_enabled) is not bool:
            raise ConfigurationError("watchdog_enabled is invalid")
        return value

    def _require_operational(self) -> None:
        if not (
            self._initialized
            and self._configuration_valid
            and self._repository_ready
            and self._config is not None
            and self._repository is not None
            and self._watchdog is not None
        ):
            raise StateInvariantError("controller is not initialized")

    def _response(
        self,
        result: Result | None = None,
        reason: Reason | None = None,
    ) -> ControllerResponse:
        return ControllerResponse(
            result,
            reason,
            self._state,
            self._event_log.latest_sequence(),
            self._outputs.snapshot(),
            self._logging_fault,
        )

    def _append_event(
        self,
        event_type: EventType,
        result: Result,
        reason: Reason,
        reader_source: ReaderSource | None = None,
        facility_code: int | None = None,
        credential_number: int | None = None,
        requested_floor: int | None = None,
    ) -> LogAppendOutcome:
        draft = EventDraft(
            self._clock.now_ms(),
            event_type,
            reader_source,
            facility_code,
            credential_number,
            requested_floor,
            result,
            reason,
        )
        try:
            record = self._event_log.append(draft)
        except EventLogError:
            self._logging_fault = True
            return LogAppendOutcome(None, True)
        self._logging_fault = False
        return LogAppendOutcome(record, False)

    def _startup_failure(self, reason: Reason) -> ControllerResponse:
        outcome = self._append_event(
            EventType.VALIDATION_ERROR,
            Result.ERROR,
            reason,
        )
        if outcome.logging_fault:
            return self._response(Result.ERROR, Reason.LOGGING_ERROR)
        return self._response(Result.ERROR, reason)

    def _complete_idle_event(
        self,
        event_type: EventType,
        result: Result,
        reason: Reason,
        reader_source: ReaderSource | None = None,
        facility_code: int | None = None,
        credential_number: int | None = None,
        requested_floor: int | None = None,
    ) -> ControllerResponse:
        outcome = self._append_event(
            event_type,
            result,
            reason,
            reader_source,
            facility_code,
            credential_number,
            requested_floor,
        )
        self._state = ControllerState.IDLE
        self._clear_request_transients()
        if outcome.logging_fault:
            return self._response(Result.ERROR, Reason.LOGGING_ERROR)
        return self._response(result, reason)

    @staticmethod
    def _validate_decision(
        decision: AuthorizationDecision,
        decoded: DecodedCredential,
        record: CredentialRecord,
    ) -> None:
        if decision.decoded_credential != decoded or decision.selected_record != record:
            raise StateInvariantError("authorization decision context is inconsistent")
        valid = (
            (
                decision.result is Result.ERROR
                and decision.reason is Reason.INVALID_FLOOR
                and decision.selected_floor is None
            )
            or (
                decision.result is Result.DENIED
                and decision.reason is Reason.UNAUTHORIZED_FLOOR
                and type(decision.selected_floor) is int
                and 1 <= decision.selected_floor <= 16
            )
            or (
                decision.result is Result.GRANTED
                and decision.reason is Reason.AUTHORIZED
                and type(decision.selected_floor) is int
                and 1 <= decision.selected_floor <= 16
            )
        )
        if not valid:
            raise StateInvariantError("authorize returned an impossible outcome")

    def _due_times(self, current_ms: int) -> tuple[int, ...]:
        watchdog = self._watchdog
        if watchdog is None:
            raise StateInvariantError("watchdog disappeared during advancement")
        candidates = (
            watchdog.next_heartbeat_ms(),
            watchdog.expiry_deadline_ms(),
            self._outputs.next_expiry_ms(),
        )
        due: list[int] = []
        for timestamp in candidates:
            if timestamp is None:
                continue
            if type(timestamp) is not int or timestamp < current_ms:
                raise StateInvariantError("scheduled due time is stale or invalid")
            due.append(timestamp)
        return tuple(due)

    def _timeout_context(self) -> _ActiveContext:
        if self._active_context is not None:
            return self._active_context
        return (None, None, None, self._outputs.snapshot().active_floor)

    def _watchdog_reset(self) -> ControllerResponse:
        return self._perform_reset(
            EventType.WATCHDOG_RESET,
            Reason.WATCHDOG_TIMEOUT,
        )

    def _perform_reset(
        self,
        event_type: EventType,
        reason: Reason,
    ) -> ControllerResponse:
        self._state = ControllerState.RESETTING
        self._outputs.reset()
        self._clear_transients()
        outcome = self._append_event(event_type, Result.RESET, reason)
        watchdog = self._watchdog
        if watchdog is None:
            raise StateInvariantError("watchdog disappeared during reset")
        watchdog.reinitialize(self._clock.now_ms())
        self._state = ControllerState.IDLE
        if outcome.logging_fault:
            return self._response(Result.ERROR, Reason.LOGGING_ERROR)
        return self._response(Result.RESET, reason)

    def _clear_request_transients(self) -> None:
        self._request = None
        self._decoded = None
        self._selected_record = None
        self._decision = None

    def _clear_transients(self) -> None:
        self._clear_request_transients()
        self._active_context = None
