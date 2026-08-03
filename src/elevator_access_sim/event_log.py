"""Deterministic in-memory event recording and JSON Lines export."""

from __future__ import annotations

import json

from .models import EventDraft, EventLogError, EventRecord, EventType, ReaderSource, Reason, Result, StateInvariantError


def _optional_integer(value: object, field: str, minimum: int, maximum: int) -> None:
    if value is not None and (type(value) is not int or not minimum <= value <= maximum):
        raise StateInvariantError(f"{field} is invalid")


def _validate_draft(value: object) -> EventDraft:
    if not isinstance(value, EventDraft):
        raise StateInvariantError("draft must be an EventDraft")
    if type(value.timestamp_ms) is not int or value.timestamp_ms < 0:
        raise StateInvariantError("timestamp_ms is invalid")
    if not isinstance(value.event_type, EventType):
        raise StateInvariantError("event_type is invalid")
    if value.reader_source is not None and not isinstance(value.reader_source, ReaderSource):
        raise StateInvariantError("reader_source is invalid")
    _optional_integer(value.facility_code, "facility_code", 0, 255)
    _optional_integer(value.credential_number, "credential_number", 0, 65535)
    _optional_integer(value.requested_floor, "requested_floor", 1, 16)
    if not isinstance(value.result, Result):
        raise StateInvariantError("result is invalid")
    if not isinstance(value.reason, Reason):
        raise StateInvariantError("reason is invalid")
    return value


class EventLog:
    """Own successful immutable events and their contiguous sequence numbers."""

    def __init__(self) -> None:
        self._records: list[EventRecord] = []
        self._next_sequence = 1
        self._latest_timestamp: int | None = None
        self._append_failure = False

    def append(self, draft: EventDraft) -> EventRecord:
        if self._append_failure:
            raise EventLogError("injected event append failure")
        trusted = _validate_draft(draft)
        if self._latest_timestamp is not None and trusted.timestamp_ms < self._latest_timestamp:
            raise StateInvariantError("event timestamp cannot move backward")
        record = EventRecord(self._next_sequence, trusted.timestamp_ms, trusted.event_type, trusted.reader_source, trusted.facility_code, trusted.credential_number, trusted.requested_floor, trusted.result, trusted.reason)
        self._records.append(record)
        self._next_sequence += 1
        self._latest_timestamp = trusted.timestamp_ms
        return record

    def set_append_failure(self, enabled: bool) -> None:
        if type(enabled) is not bool:
            raise StateInvariantError("append failure flag must be a Boolean")
        self._append_failure = enabled

    def records(self) -> tuple[EventRecord, ...]:
        return tuple(self._records)

    def latest_sequence(self) -> int | None:
        return self._records[-1].sequence_number if self._records else None

    def clear_startup(self) -> None:
        self._records.clear()
        self._next_sequence = 1
        self._latest_timestamp = None
        self._append_failure = False

    def to_jsonl(self) -> str:
        lines = []
        for record in self._records:
            value = {
                "sequence_number": record.sequence_number,
                "timestamp_ms": record.timestamp_ms,
                "event_type": record.event_type.to_text(),
                "reader_source": None if record.reader_source is None else record.reader_source.to_text(),
                "facility_code": record.facility_code,
                "credential_number": record.credential_number,
                "requested_floor": record.requested_floor,
                "result": record.result.to_text(),
                "reason": record.reason.to_text(),
            }
            lines.append(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        return "\n".join(lines)
