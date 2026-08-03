"""Strict simulator-configuration parsing."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from typing import Any

from .credentials import _record_key, _validated_record
from .models import (
    ConfigurationError,
    CredentialDataError,
    CredentialRecord,
    DuplicateCredentialError,
    SimulatorConfig,
    StartupData,
)


_CONFIG_FIELDS = frozenset(
    {
        "schema_version",
        "profile",
        "output_duration_ms",
        "watchdog_timeout_ms",
        "watchdog_enabled",
    }
)
_PROFILE = "PROJECT_WIEGAND_26"
_CREDENTIAL_TOP_FIELDS = frozenset({"schema_version", "credentials"})
_CREDENTIAL_REQUIRED_FIELDS = frozenset(
    {"facility_code", "credential_number", "enabled", "floor_mask"}
)
_CREDENTIAL_FIELDS = _CREDENTIAL_REQUIRED_FIELDS | {"label"}


def default_config() -> SimulatorConfig:
    """Return the documented immutable simulator defaults."""

    return SimulatorConfig(
        schema_version=1,
        profile=_PROFILE,
        output_duration_ms=3000,
        watchdog_timeout_ms=2000,
        watchdog_enabled=True,
    )


def _object_without_duplicates(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ConfigurationError(f"duplicate configuration field: {key}")
        value[key] = item
    return value


def _reject_nonfinite(value: str) -> None:
    raise ConfigurationError(f"non-finite numeric value is not allowed: {value}")


def _credential_object_without_duplicates(
    pairs: Iterable[tuple[str, Any]],
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise CredentialDataError(f"duplicate credential JSON member: {key}")
        value[key] = item
    return value


def _reject_credential_nonfinite(value: str) -> None:
    raise CredentialDataError(f"non-finite credential value is not allowed: {value}")


def _require_exact_integer(value: object, field: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ConfigurationError(
            f"{field} must be an integer from {minimum} to {maximum}"
        )
    return value


def load_config_json(text: str) -> SimulatorConfig:
    """Parse and atomically validate the complete version-1 configuration object."""

    if not isinstance(text, str):
        raise ConfigurationError("configuration JSON must be a string")

    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_constant=_reject_nonfinite,
        )
    except ConfigurationError:
        raise
    except (json.JSONDecodeError, RecursionError, UnicodeError) as exc:
        raise ConfigurationError("malformed configuration JSON") from exc

    if not isinstance(value, dict):
        raise ConfigurationError("configuration JSON must contain an object")

    actual_fields = set(value)
    unknown_fields = sorted(actual_fields - _CONFIG_FIELDS)
    if unknown_fields:
        raise ConfigurationError(
            f"unknown configuration field: {unknown_fields[0]}"
        )
    missing_fields = sorted(_CONFIG_FIELDS - actual_fields)
    if missing_fields:
        raise ConfigurationError(
            f"missing configuration field: {missing_fields[0]}"
        )

    schema_version = _require_exact_integer(
        value["schema_version"],
        "schema_version",
        1,
        1,
    )
    profile = value["profile"]
    if type(profile) is not str or profile != _PROFILE:
        raise ConfigurationError(f"profile must be '{_PROFILE}'")
    output_duration_ms = _require_exact_integer(
        value["output_duration_ms"],
        "output_duration_ms",
        100,
        30000,
    )
    watchdog_timeout_ms = _require_exact_integer(
        value["watchdog_timeout_ms"],
        "watchdog_timeout_ms",
        1,
        4294967295,
    )
    watchdog_enabled = value["watchdog_enabled"]
    if type(watchdog_enabled) is not bool:
        raise ConfigurationError("watchdog_enabled must be a Boolean")

    return SimulatorConfig(
        schema_version=schema_version,
        profile=profile,
        output_duration_ms=output_duration_ms,
        watchdog_timeout_ms=watchdog_timeout_ms,
        watchdog_enabled=watchdog_enabled,
    )


def load_credentials_json(text: str) -> tuple[CredentialRecord, ...]:
    """Parse and atomically validate the version-1 credential document."""

    if not isinstance(text, str):
        raise CredentialDataError("credential JSON must be a string")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_credential_object_without_duplicates,
            parse_constant=_reject_credential_nonfinite,
        )
    except CredentialDataError:
        raise
    except (json.JSONDecodeError, RecursionError, UnicodeError) as exc:
        raise CredentialDataError("malformed credential JSON") from exc
    if not isinstance(value, dict):
        raise CredentialDataError("credential JSON must contain an object")

    actual_fields = set(value)
    unknown = sorted(actual_fields - _CREDENTIAL_TOP_FIELDS)
    missing = sorted(_CREDENTIAL_TOP_FIELDS - actual_fields)
    if unknown:
        raise CredentialDataError(f"unknown credential top-level field: {unknown[0]}")
    if missing:
        raise CredentialDataError(f"missing credential top-level field: {missing[0]}")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise CredentialDataError("credential schema_version must be integer 1")
    entries = value["credentials"]
    if not isinstance(entries, list):
        raise CredentialDataError("credentials must be an array")

    records: list[CredentialRecord] = []
    keys = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise CredentialDataError(f"credential entry {index} must be an object")
        entry_fields = set(entry)
        unknown = sorted(entry_fields - _CREDENTIAL_FIELDS)
        missing = sorted(_CREDENTIAL_REQUIRED_FIELDS - entry_fields)
        if unknown:
            raise CredentialDataError(f"unknown credential field: {unknown[0]}")
        if missing:
            raise CredentialDataError(f"missing credential field: {missing[0]}")
        if "label" in entry and entry["label"] is None:
            raise CredentialDataError("present label cannot be null")
        record = _validated_record(
            CredentialRecord(
                entry["facility_code"],
                entry["credential_number"],
                entry["enabled"],
                entry["floor_mask"],
                entry.get("label"),
            )
        )
        key = _record_key(record)
        if key in keys:
            raise DuplicateCredentialError(
                f"duplicate credential key: ({key.facility_code}, {key.credential_number})"
            )
        records.append(record)
        keys.add(key)
    return tuple(records)


def load_startup_json(config_text: str, credentials_text: str) -> StartupData:
    """Atomically validate both startup documents and preserve error identity."""

    config = load_config_json(config_text)
    credentials = load_credentials_json(credentials_text)
    return StartupData(config, credentials)


def _read_startup_text(
    path_value: object,
    kind: str,
    error_type: type[ConfigurationError] | type[CredentialDataError],
) -> str:
    if not isinstance(path_value, (str, os.PathLike)):
        raise error_type(f"{kind} file path must be a string or PathLike")
    try:
        path = os.fspath(path_value)
    except (TypeError, ValueError, OSError) as exc:
        raise error_type(f"{kind} file path is invalid") from exc
    if type(path) is not str:
        raise error_type(f"{kind} file path must resolve to text")
    try:
        with open(path, "r", encoding="utf-8", errors="strict") as stream:
            return stream.read()
    except (OSError, UnicodeError, ValueError) as exc:
        raise error_type(f"{kind} file could not be read as strict UTF-8") from exc


def load_startup_files(
    config_path: str | os.PathLike[str],
    credentials_path: str | os.PathLike[str],
) -> StartupData:
    """Strictly read both UTF-8 startup files and atomically parse them."""

    config_text = _read_startup_text(
        config_path,
        "configuration",
        ConfigurationError,
    )
    credentials_text = _read_startup_text(
        credentials_path,
        "credential",
        CredentialDataError,
    )
    return load_startup_json(config_text, credentials_text)
