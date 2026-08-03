"""Focused tests for SP-06.1 simulator configuration."""

import json

import pytest

from elevator_access_sim.config import default_config, load_config_json
from elevator_access_sim.models import ConfigurationError, SimulatorConfig


DOCUMENTED = {
    "schema_version": 1,
    "profile": "PROJECT_WIEGAND_26",
    "output_duration_ms": 3000,
    "watchdog_timeout_ms": 2000,
    "watchdog_enabled": True,
}


def encoded(**changes: object) -> str:
    value = DOCUMENTED | changes
    return json.dumps(value)


def test_tst_cfg_001_exact_documented_json() -> None:
    assert load_config_json(json.dumps(DOCUMENTED)) == SimulatorConfig(
        schema_version=1,
        profile="PROJECT_WIEGAND_26",
        output_duration_ms=3000,
        watchdog_timeout_ms=2000,
        watchdog_enabled=True,
    )


def test_tst_cfg_001_default_config() -> None:
    assert default_config() == load_config_json(json.dumps(DOCUMENTED))


@pytest.mark.parametrize("value", [100, 30000], ids=["minimum", "maximum"])
def test_tst_tim_002_output_duration_endpoints(value: int) -> None:
    assert load_config_json(encoded(output_duration_ms=value)).output_duration_ms == value


@pytest.mark.parametrize("value", [1, 4294967295], ids=["minimum", "maximum"])
def test_tst_cfg_002_watchdog_timeout_endpoints(value: int) -> None:
    assert load_config_json(encoded(watchdog_timeout_ms=value)).watchdog_timeout_ms == value


@pytest.mark.parametrize("value", [99, 30001, -1, True, 100.0, "100", None])
def test_tst_tim_002_rejects_invalid_output_duration(value: object) -> None:
    with pytest.raises(ConfigurationError, match="output_duration_ms"):
        load_config_json(encoded(output_duration_ms=value))


@pytest.mark.parametrize("value", [0, 4294967296, -1, True, 1.0, "1", None])
def test_tst_cfg_002_rejects_invalid_watchdog_timeout(value: object) -> None:
    with pytest.raises(ConfigurationError, match="watchdog_timeout_ms"):
        load_config_json(encoded(watchdog_timeout_ms=value))


@pytest.mark.parametrize("value", [True, 1.0, "1", None])
def test_tst_cfg_003_rejects_invalid_schema_version(value: object) -> None:
    with pytest.raises(ConfigurationError, match="schema_version"):
        load_config_json(encoded(schema_version=value))


@pytest.mark.parametrize("value", [False, 0, 1, "true", None, [], {}])
def test_tst_cfg_003_requires_actual_watchdog_boolean(value: object) -> None:
    if value is False:
        assert load_config_json(encoded(watchdog_enabled=value)).watchdog_enabled is False
    else:
        with pytest.raises(ConfigurationError, match="watchdog_enabled"):
            load_config_json(encoded(watchdog_enabled=value))


def test_tst_cfg_003_rejects_missing_field() -> None:
    value = DOCUMENTED.copy()
    del value["profile"]
    with pytest.raises(ConfigurationError, match="missing.*profile"):
        load_config_json(json.dumps(value))


def test_tst_cfg_003_rejects_unknown_field() -> None:
    with pytest.raises(ConfigurationError, match="unknown.*extra"):
        load_config_json(encoded(extra=1))


def test_tst_cfg_003_rejects_duplicate_json_member() -> None:
    text = (
        '{"schema_version":1,"profile":"PROJECT_WIEGAND_26",'
        '"output_duration_ms":3000,"output_duration_ms":100,'
        '"watchdog_timeout_ms":2000,"watchdog_enabled":true}'
    )
    with pytest.raises(ConfigurationError, match="duplicate.*output_duration_ms"):
        load_config_json(text)


@pytest.mark.parametrize("text", ["{", "", "not-json"])
def test_tst_cfg_003_rejects_malformed_json(text: str) -> None:
    with pytest.raises(ConfigurationError, match="malformed"):
        load_config_json(text)


def test_tst_cfg_003_rejects_unsupported_schema_version() -> None:
    with pytest.raises(ConfigurationError, match="schema_version"):
        load_config_json(encoded(schema_version=2))


def test_tst_cfg_003_rejects_unsupported_profile() -> None:
    with pytest.raises(ConfigurationError, match="profile"):
        load_config_json(encoded(profile="OTHER"))


@pytest.mark.parametrize("text", ["[]", "null", "true", "1", '"value"'])
def test_tst_cfg_003_rejects_wrong_top_level_type(text: str) -> None:
    with pytest.raises(ConfigurationError, match="object"):
        load_config_json(text)


@pytest.mark.parametrize("value", [1, None, "true", [], {}])
def test_tst_cfg_003_rejects_wrong_profile_or_boolean_field_types(value: object) -> None:
    field = "profile" if value in (1, None, [], {}) else "watchdog_enabled"
    text = encoded(**{field: value})
    with pytest.raises(ConfigurationError, match=field):
        load_config_json(text)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_tst_cfg_003_rejects_nonfinite_constants(constant: str) -> None:
    text = json.dumps(DOCUMENTED).replace("3000", constant, 1)
    with pytest.raises(ConfigurationError, match="non-finite"):
        load_config_json(text)


@pytest.mark.parametrize("value", [None, b"{}", 1, {}, []])
def test_load_config_json_requires_string_input(value: object) -> None:
    with pytest.raises(ConfigurationError, match="string"):
        load_config_json(value)  # type: ignore[arg-type]


def test_tst_cfg_005_failed_parse_is_atomic_and_does_not_change_defaults() -> None:
    before = default_config()
    with pytest.raises(ConfigurationError):
        load_config_json(encoded(output_duration_ms=99))
    after = default_config()
    assert before == after

