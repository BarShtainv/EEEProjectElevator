"""Strict simulator-configuration parsing."""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

from .models import ConfigurationError, SimulatorConfig


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

