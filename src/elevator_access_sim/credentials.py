"""Validated in-memory credential repository."""

from __future__ import annotations

from collections.abc import Sequence

from .models import (
    CredentialDataError,
    CredentialKey,
    CredentialRecord,
    DuplicateCredentialError,
    RepositoryLookup,
    StateInvariantError,
)


def _require_integer(value: object, field: str, maximum: int) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise CredentialDataError(f"{field} must be an integer from 0 to {maximum}")
    return value


def _require_label(value: object) -> str | None:
    if value is None:
        return None
    if type(value) is not str or not value.strip():
        raise CredentialDataError("label must be a nonempty non-whitespace string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise CredentialDataError("label must be valid UTF-8 text") from exc
    return value


def _validated_record(value: object) -> CredentialRecord:
    if not isinstance(value, CredentialRecord):
        raise CredentialDataError("every repository item must be a CredentialRecord")
    facility = _require_integer(value.facility_code, "facility_code", 255)
    credential = _require_integer(
        value.credential_number,
        "credential_number",
        65535,
    )
    if type(value.enabled) is not bool:
        raise CredentialDataError("enabled must be a Boolean")
    floor_mask = _require_integer(value.floor_mask, "floor_mask", 65535)
    label = _require_label(value.label)
    return CredentialRecord(facility, credential, value.enabled, floor_mask, label)


def _record_key(record: CredentialRecord) -> CredentialKey:
    return CredentialKey(record.facility_code, record.credential_number)


class CredentialRepository:
    """Immutable record observation with private ordered-key lookup state."""

    def __init__(
        self,
        records: tuple[CredentialRecord, ...],
        index: dict[CredentialKey, CredentialRecord],
    ) -> None:
        self._records = records
        self._index = index

    @classmethod
    def from_records(
        cls,
        records: Sequence[CredentialRecord],
    ) -> CredentialRepository:
        """Validate and atomically construct a repository from a finite sequence."""

        if isinstance(records, (str, bytes, bytearray)) or not isinstance(
            records,
            Sequence,
        ):
            raise CredentialDataError("records must be a finite record sequence")

        validated: list[CredentialRecord] = []
        index: dict[CredentialKey, CredentialRecord] = {}
        for value in records:
            record = _validated_record(value)
            key = _record_key(record)
            if key in index:
                raise DuplicateCredentialError(
                    f"duplicate credential key: ({key.facility_code}, {key.credential_number})"
                )
            validated.append(record)
            index[key] = record
        return cls(tuple(validated), index)

    def lookup(self, key: CredentialKey) -> RepositoryLookup:
        """Return the matching record or a normal empty lookup outcome."""

        if not isinstance(key, CredentialKey):
            raise StateInvariantError("lookup key must be a CredentialKey")
        if type(key.facility_code) is not int or not 0 <= key.facility_code <= 255:
            raise StateInvariantError("lookup facility_code is invalid")
        if (
            type(key.credential_number) is not int
            or not 0 <= key.credential_number <= 65535
        ):
            raise StateInvariantError("lookup credential_number is invalid")
        return RepositoryLookup(self._index.get(key))

    def records(self) -> tuple[CredentialRecord, ...]:
        """Return records in their validated input order."""

        return self._records

    def __len__(self) -> int:
        return len(self._records)
