"""SP-06.7 controller construction and atomic initialization tests."""

from __future__ import annotations

import ast
import inspect

import pytest

import elevator_access_sim.controller as controller_module
from elevator_access_sim import Controller
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.event_log import EventLog
from elevator_access_sim.models import (
    ControllerState,
    CredentialDataError,
    CredentialRecord,
    EventDraft,
    EventLogError,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
    StateInvariantError,
)


def config(**changes: object) -> SimulatorConfig:
    values: dict[str, object] = {
        "schema_version": 1,
        "profile": "PROJECT_WIEGAND_26",
        "output_duration_ms": 3000,
        "watchdog_timeout_ms": 2000,
        "watchdog_enabled": True,
    }
    values.update(changes)
    return SimulatorConfig(**values)  # type: ignore[arg-type]


def record(**changes: object) -> CredentialRecord:
    values: dict[str, object] = {
        "facility_code": 1,
        "credential_number": 100,
        "enabled": True,
        "floor_mask": 65535,
        "label": None,
    }
    values.update(changes)
    return CredentialRecord(**values)  # type: ignore[arg-type]


def test_constructor_validates_dependencies_without_mutation() -> None:
    clock = SimulatedClock(25)
    event_log = EventLog()
    event_log.append(
        EventDraft(25, EventType.MANUAL_RESET, None, None, None, None, Result.RESET, Reason.MANUAL_REQUEST)
    )
    controller = Controller(clock, event_log)

    assert clock.now_ms() == 25
    assert controller.events() == event_log.records()
    assert controller.snapshot().state is ControllerState.RESETTING
    assert controller.snapshot().initialized is False
    assert controller.snapshot().watchdog_deadline_ms is None
    assert controller.snapshot().active_floor is None


@pytest.mark.parametrize("clock", [None, 0, True, object()])
def test_constructor_rejects_non_simulated_clocks(clock: object) -> None:
    with pytest.raises(StateInvariantError):
        Controller(clock)  # type: ignore[arg-type]


@pytest.mark.parametrize("event_log", [0, True, object(), []])
def test_constructor_rejects_invalid_event_logs(event_log: object) -> None:
    with pytest.raises(StateInvariantError):
        Controller(SimulatedClock(), event_log)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        {"output_duration_ms": 100},
        {"output_duration_ms": 30000},
        {"watchdog_timeout_ms": 1},
        {"watchdog_timeout_ms": 4294967295},
        {"watchdog_enabled": False},
    ],
)
def test_valid_configuration_endpoints_and_watchdog_modes(changes: dict[str, object]) -> None:
    controller = Controller(SimulatedClock())
    response = controller.initialize(config(**changes), [])
    snapshot = controller.snapshot()

    assert response.result is response.reason is None
    assert response.state is ControllerState.IDLE
    assert snapshot.initialized and snapshot.configuration_valid and snapshot.repository_ready
    assert snapshot.watchdog_deadline_ms == (
        None if changes.get("watchdog_enabled") is False else changes.get("watchdog_timeout_ms", 2000)
    )
    assert controller.events() == ()


def test_valid_multiple_credentials_publish_together() -> None:
    controller = Controller(SimulatedClock())
    values = [record(), record(facility_code=2, credential_number=99, enabled=False)]
    response = controller.initialize(config(), values)

    assert response.state is ControllerState.IDLE
    assert controller._config == config()
    assert controller._repository is not None
    assert controller._repository.records() == tuple(values)


@pytest.mark.parametrize(
    "value",
    [
        None,
        object(),
        config(schema_version=2),
        config(schema_version=True),
        config(profile="OTHER"),
        config(profile=1),
        config(output_duration_ms=99),
        config(output_duration_ms=30001),
        config(output_duration_ms=True),
        config(watchdog_timeout_ms=0),
        config(watchdog_timeout_ms=4294967296),
        config(watchdog_timeout_ms=True),
        config(watchdog_enabled=1),
    ],
)
def test_invalid_programmatic_configuration_is_mapped_atomically(value: object) -> None:
    controller = Controller(SimulatedClock())
    response = controller.initialize(value, [])  # type: ignore[arg-type]

    assert response.result is Result.ERROR
    assert response.reason is Reason.INVALID_CONFIGURATION
    assert response.state is ControllerState.INITIALIZING
    assert controller._config is controller._repository is controller._watchdog is None
    assert not controller.snapshot().initialized
    assert controller.events()[0].event_type is EventType.VALIDATION_ERROR
    assert controller.events()[0].reader_source is None


@pytest.mark.parametrize(
    "credentials",
    [
        object(),
        "records",
        [object()],
        [record(facility_code=-1)],
        [record(enabled=1)],
    ],
)
def test_malformed_credential_sequence_or_record_maps_reason(credentials: object) -> None:
    controller = Controller(SimulatedClock())
    response = controller.initialize(config(), credentials)  # type: ignore[arg-type]
    assert (response.result, response.reason, response.state) == (
        Result.ERROR,
        Reason.INVALID_CREDENTIAL_RECORD,
        ControllerState.INITIALIZING,
    )
    assert controller._config is controller._repository is controller._watchdog is None


def test_duplicate_composite_key_has_distinct_startup_reason() -> None:
    controller = Controller(SimulatedClock())
    response = controller.initialize(config(), [record(), record(label="duplicate")])
    assert response.reason is Reason.DUPLICATE_CREDENTIAL
    assert controller.events()[0].reason is Reason.DUPLICATE_CREDENTIAL


def test_unexpected_repository_exception_maps_without_partial_publication(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenRepository:
        @classmethod
        def from_records(cls, records: object) -> object:
            del records
            raise RuntimeError("injected infrastructure failure")

    monkeypatch.setattr(controller_module, "CredentialRepository", BrokenRepository)
    controller = Controller(SimulatedClock())
    response = controller.initialize(config(), [])
    assert response.reason is Reason.REPOSITORY_INITIALIZATION_FAILURE
    assert controller._config is controller._repository is controller._watchdog is None


def test_repository_invariant_is_not_converted(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenRepository:
        @classmethod
        def from_records(cls, records: object) -> object:
            del records
            raise StateInvariantError("impossible")

    monkeypatch.setattr(controller_module, "CredentialRepository", BrokenRepository)
    with pytest.raises(StateInvariantError, match="impossible"):
        Controller(SimulatedClock()).initialize(config(), [])


def test_startup_logging_failure_maps_logging_error_without_sequence() -> None:
    class FailingLog(EventLog):
        def append(self, draft: EventDraft):  # type: ignore[no-untyped-def]
            del draft
            raise EventLogError("startup append failed")

    controller = Controller(SimulatedClock(), FailingLog())
    response = controller.initialize(config(schema_version=2), [])
    assert (response.result, response.reason, response.logging_fault) == (
        Result.ERROR,
        Reason.LOGGING_ERROR,
        True,
    )
    assert response.latest_event_sequence is None
    assert controller.events() == ()


def test_corrected_initialization_after_failure_clears_error_event() -> None:
    controller = Controller(SimulatedClock())
    assert controller.initialize(config(schema_version=2), []).reason is Reason.INVALID_CONFIGURATION
    response = controller.initialize(config(), [record()])
    assert response.result is response.reason is None
    assert response.latest_event_sequence is None
    assert controller.events() == ()


def test_reinitialize_clears_prior_active_runtime_and_startup_log() -> None:
    from elevator_access_sim import CredentialRequest, encode_frame

    controller = Controller(SimulatedClock())
    controller.initialize(config(), [record()])
    controller.submit(CredentialRequest(ReaderSource.LF, encode_frame(1, 100), 1))
    assert controller.snapshot().active_floor == 1

    response = controller.initialize(config(watchdog_enabled=False), [])
    assert response.state is ControllerState.IDLE
    assert response.output_snapshot.active_floor is None
    assert controller.events() == ()
    assert controller.snapshot().watchdog_deadline_ms is None


@pytest.mark.parametrize(
    "method,args",
    [
        ("submit", (object(),)),
        ("advance_to", (0,)),
        ("advance_by", (0,)),
        ("manual_reset", ()),
        ("set_watchdog_service_suppressed", (False,)),
    ],
)
def test_operational_methods_require_successful_initialization(method: str, args: tuple[object, ...]) -> None:
    controller = Controller(SimulatedClock())
    before = controller.snapshot()
    with pytest.raises(StateInvariantError):
        getattr(controller, method)(*args)
    assert controller.snapshot() == before


def test_public_signatures_exports_and_structural_scope() -> None:
    from elevator_access_sim import Controller as ExportedController

    assert ExportedController is Controller
    expected = {
        "initialize": ("self", "config", "credentials"),
        "submit": ("self", "request"),
        "advance_to": ("self", "target_ms"),
        "advance_by": ("self", "delta_ms"),
        "manual_reset": ("self",),
        "set_watchdog_service_suppressed": ("self", "suppressed"),
        "snapshot": ("self",),
        "events": ("self",),
    }
    for name, parameters in expected.items():
        assert tuple(inspect.signature(getattr(Controller, name)).parameters) == parameters
    assert not hasattr(Controller, "force_state")
    assert not hasattr(Controller, "set_state")

    tree = ast.parse(inspect.getsource(controller_module))
    project_imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.level
    }
    assert project_imports == {
        "authorization",
        "clock",
        "credentials",
        "event_log",
        "models",
        "outputs",
        "watchdog",
        "wiegand",
    }
    forbidden = {"time", "datetime", "threading", "asyncio", "pathlib", "socket"}
    assert not any(
        isinstance(node, (ast.Import, ast.ImportFrom))
        and any(alias.name.split(".")[0] in forbidden for alias in node.names)
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
    )
