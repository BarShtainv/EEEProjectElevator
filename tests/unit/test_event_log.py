"""SP-06.4 EventLog tests."""

import ast
import inspect
import json
from dataclasses import FrozenInstanceError

import pytest

import elevator_access_sim.event_log as module
from elevator_access_sim import EventLog
from elevator_access_sim.models import EventDraft, EventLogError, EventRecord, EventType, ReaderSource, Reason, Result, StateInvariantError


def draft(timestamp: object = 0, event_type: object = EventType.ACCESS_DECISION, source: object = ReaderSource.LF, facility: object = 1, credential: object = 100, floor: object = 1, result: object = Result.GRANTED, reason: object = Reason.AUTHORIZED) -> EventDraft:
    return EventDraft(timestamp, event_type, source, facility, credential, floor, result, reason)  # type: ignore[arg-type]


def test_initial_append_order_immutability_and_equal_timestamps() -> None:
    log = EventLog()
    assert log.records() == () and log.latest_sequence() is None and log.to_jsonl() == ""
    first = log.append(draft())
    second = log.append(draft(0, EventType.VALIDATION_ERROR, None, None, None, None, Result.ERROR, Reason.INVALID_FRAME))
    third = log.append(draft(5))
    assert [item.sequence_number for item in log.records()] == [1, 2, 3]
    assert log.latest_sequence() == 3 and first.timestamp_ms == second.timestamp_ms == 0 and third.timestamp_ms == 5
    observed = log.records() + (first,)
    assert len(observed) == 4 and len(log.records()) == 3
    with pytest.raises(FrozenInstanceError): first.timestamp_ms = 9  # type: ignore[misc]


@pytest.mark.parametrize("event_type", list(EventType))
def test_all_event_types_serialize_lowercase(event_type: EventType) -> None:
    log = EventLog(); log.append(draft(event_type=event_type))
    assert json.loads(log.to_jsonl())["event_type"] == event_type.name.lower()


@pytest.mark.parametrize("source", [ReaderSource.LF, ReaderSource.HF, None])
def test_sources_serialize_uppercase_or_null(source: ReaderSource | None) -> None:
    log = EventLog(); log.append(draft(source=source))
    assert json.loads(log.to_jsonl())["reader_source"] == (None if source is None else source.name)


@pytest.mark.parametrize("result", list(Result))
def test_all_results_serialize_lowercase(result: Result) -> None:
    log = EventLog(); log.append(draft(result=result))
    assert json.loads(log.to_jsonl())["result"] == result.name.lower()


@pytest.mark.parametrize("reason", list(Reason))
def test_all_reasons_serialize_lowercase(reason: Reason) -> None:
    log = EventLog(); log.append(draft(reason=reason))
    assert json.loads(log.to_jsonl())["reason"] == reason.name.lower()


def test_jsonl_exact_keys_nulls_compact_order_and_stability() -> None:
    log = EventLog(); log.append(draft(source=None, facility=None, credential=None, floor=None))
    text = log.to_jsonl(); value = json.loads(text)
    assert list(value) == ["sequence_number", "timestamp_ms", "event_type", "reader_source", "facility_code", "credential_number", "requested_floor", "result", "reason"]
    assert [value[key] for key in ("reader_source", "facility_code", "credential_number", "requested_floor")] == [None] * 4
    assert " " not in text and "\n" not in text and log.to_jsonl() == text and log.latest_sequence() == 1


def test_failure_injection_is_atomic_contiguous_and_clear_resets_all() -> None:
    log = EventLog(); old = log.append(draft(5)); log.set_append_failure(True)
    for _ in range(2):
        with pytest.raises(EventLogError): log.append(draft(6))
    assert log.records() == (old,) and log.latest_sequence() == 1
    log.set_append_failure(False); assert log.append(draft(6)).sequence_number == 2
    log.set_append_failure(True); historical = log.records(); log.clear_startup()
    assert log.records() == () and log.latest_sequence() is None and len(historical) == 2
    assert log.append(draft(0)).sequence_number == 1


@pytest.mark.parametrize("enabled", [0, 1, None, "true", []])
def test_invalid_failure_flags(enabled: object) -> None:
    with pytest.raises(StateInvariantError): EventLog().set_append_failure(enabled)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [object(), draft(-1), draft(True), draft(event_type=1), draft(source="LF"), draft(facility=-1), draft(facility=True), draft(credential=65536), draft(credential=False), draft(floor=0), draft(floor=True), draft(result=1), draft(reason=1)])
def test_invalid_drafts_are_atomic(bad: object) -> None:
    log = EventLog()
    with pytest.raises(StateInvariantError): log.append(bad)  # type: ignore[arg-type]
    assert log.records() == () and log.latest_sequence() is None


def test_backward_timestamp_fails_without_gap_and_equal_passes() -> None:
    log = EventLog(); log.append(draft(5))
    with pytest.raises(StateInvariantError): log.append(draft(4))
    assert log.append(draft(5)).sequence_number == 2


@pytest.mark.parametrize("event_type,result,reason", [(EventType.OUTPUT_TIMEOUT, Result.COMPLETED, Reason.OUTPUT_EXPIRED), (EventType.MANUAL_RESET, Result.RESET, Reason.MANUAL_REQUEST), (EventType.WATCHDOG_RESET, Result.RESET, Reason.WATCHDOG_TIMEOUT), (EventType.LOGGING_ERROR, Result.ERROR, Reason.LOGGING_ERROR)])
def test_representative_event_kinds(event_type: EventType, result: Result, reason: Reason) -> None:
    assert EventLog().append(draft(event_type=event_type, source=None, facility=None, credential=None, floor=None, result=result, reason=reason)).event_type is event_type


def test_structure_and_import_scope() -> None:
    tree = ast.parse(inspect.getsource(module))
    imports = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.level}
    assert imports == {"models"}
    assert not any(isinstance(n, ast.Import) and any(a.name != "json" for a in n.names) for n in ast.walk(tree))
