"""SP-06.8 strict UTF-8 startup-file adapter tests."""

from __future__ import annotations

import inspect
import json
import os
from pathlib import Path

import pytest

import elevator_access_sim.config as config_module
from elevator_access_sim import load_startup_files
from elevator_access_sim.models import (
    ConfigurationError,
    CredentialDataError,
    CredentialRecord,
    DuplicateCredentialError,
    SimulatorConfig,
    StartupData,
)


CONFIG = {
    "schema_version": 1,
    "profile": "PROJECT_WIEGAND_26",
    "output_duration_ms": 3000,
    "watchdog_timeout_ms": 2000,
    "watchdog_enabled": True,
}


def credential(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "facility_code": 1,
        "credential_number": 100,
        "enabled": True,
        "floor_mask": 65535,
        "label": "demo-user",
    }
    value.update(changes)
    return value


def write_documents(
    tmp_path: Path,
    *,
    config: object = CONFIG,
    credentials: object | None = None,
) -> tuple[Path, Path]:
    config_path = tmp_path / "config.json"
    credentials_path = tmp_path / "credentials.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    document = {
        "schema_version": 1,
        "credentials": [credential()] if credentials is None else credentials,
    }
    credentials_path.write_text(
        json.dumps(document, ensure_ascii=False),
        encoding="utf-8",
    )
    return config_path, credentials_path


@pytest.mark.parametrize("path_kind", ["string", "pathlib"])
def test_valid_documented_files_and_path_types(tmp_path: Path, path_kind: str) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    paths = (
        (str(config_path), str(credentials_path))
        if path_kind == "string"
        else (config_path, credentials_path)
    )
    startup = load_startup_files(*paths)
    assert startup == StartupData(
        SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True),
        (CredentialRecord(1, 100, True, 65535, "demo-user"),),
    )


def test_empty_credentials_are_valid(tmp_path: Path) -> None:
    paths = write_documents(tmp_path, credentials=[])
    assert load_startup_files(*paths).credentials == ()


def test_unicode_label_and_order_are_preserved_exactly(tmp_path: Path) -> None:
    records = [
        credential(label=" משתמש "),
        credential(facility_code=2, credential_number=99, label="Δοκιμή"),
    ]
    paths = write_documents(tmp_path, credentials=records)
    loaded = load_startup_files(*paths)
    assert loaded.credentials == (
        CredentialRecord(1, 100, True, 65535, " משתמש "),
        CredentialRecord(2, 99, True, 65535, "Δοκιμή"),
    )


@pytest.mark.parametrize("duration", [100, 30000])
def test_configuration_duration_endpoints(tmp_path: Path, duration: int) -> None:
    paths = write_documents(tmp_path, config=CONFIG | {"output_duration_ms": duration})
    assert load_startup_files(*paths).config.output_duration_ms == duration


@pytest.mark.parametrize("timeout", [1, 4294967295])
def test_watchdog_timeout_endpoints(tmp_path: Path, timeout: int) -> None:
    paths = write_documents(tmp_path, config=CONFIG | {"watchdog_timeout_ms": timeout})
    assert load_startup_files(*paths).config.watchdog_timeout_ms == timeout


@pytest.mark.parametrize("kind", ["missing", "directory", "invalid-utf8", "malformed", "bom"])
def test_configuration_file_failures_keep_configuration_identity(tmp_path: Path, kind: str) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    if kind == "missing":
        config_path = tmp_path / "missing.json"
    elif kind == "directory":
        config_path = tmp_path
    elif kind == "invalid-utf8":
        config_path.write_bytes(b"\xff\xfe")
    elif kind == "malformed":
        config_path.write_text("{", encoding="utf-8")
    else:
        config_path.write_bytes(b"\xef\xbb\xbf" + json.dumps(CONFIG).encode("utf-8"))

    with pytest.raises(ConfigurationError, match="configuration"):
        load_startup_files(config_path, credentials_path)


@pytest.mark.parametrize("kind", ["missing", "directory", "invalid-utf8", "malformed"])
def test_credential_file_failures_keep_credential_identity(tmp_path: Path, kind: str) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    if kind == "missing":
        credentials_path = tmp_path / "missing.json"
    elif kind == "directory":
        credentials_path = tmp_path
    elif kind == "invalid-utf8":
        credentials_path.write_bytes(b"\x80")
    else:
        credentials_path.write_text("{", encoding="utf-8")

    with pytest.raises(CredentialDataError, match="credential") as error:
        load_startup_files(config_path, credentials_path)
    assert type(error.value) is CredentialDataError


@pytest.mark.parametrize(
    "document",
    [
        CONFIG | {"schema_version": 2},
        CONFIG | {"profile": "OTHER"},
        CONFIG | {"extra": 1},
        {key: value for key, value in CONFIG.items() if key != "profile"},
        CONFIG | {"output_duration_ms": 99},
        CONFIG | {"watchdog_timeout_ms": True},
        CONFIG | {"watchdog_enabled": 1},
    ],
)
def test_invalid_configuration_schema_never_defaults(tmp_path: Path, document: object) -> None:
    paths = write_documents(tmp_path, config=document)
    with pytest.raises(ConfigurationError):
        load_startup_files(*paths)


def test_duplicate_configuration_member_is_rejected(tmp_path: Path) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    config_path.write_text(
        '{"schema_version":1,"profile":"PROJECT_WIEGAND_26",'
        '"output_duration_ms":3000,"output_duration_ms":100,'
        '"watchdog_timeout_ms":2000,"watchdog_enabled":true}',
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError, match="duplicate"):
        load_startup_files(config_path, credentials_path)


@pytest.mark.parametrize(
    "records",
    [
        [credential(floor_mask=-1)],
        [credential(enabled=1)],
        [credential(label="")],
        [credential(extra=1)],
    ],
)
def test_invalid_credential_fields_preserve_identity(tmp_path: Path, records: object) -> None:
    paths = write_documents(tmp_path, credentials=records)
    with pytest.raises(CredentialDataError):
        load_startup_files(*paths)


@pytest.mark.parametrize(
    "document",
    [
        {"schema_version": 2, "credentials": []},
        {"credentials": []},
        {"schema_version": 1},
        {"schema_version": 1, "credentials": [], "extra": 1},
        {"schema_version": 1, "credentials": {}},
    ],
)
def test_invalid_credential_top_level_schema_is_delegated(
    tmp_path: Path,
    document: dict[str, object],
) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    credentials_path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(CredentialDataError):
        load_startup_files(config_path, credentials_path)


def test_duplicate_credential_json_member_is_rejected(tmp_path: Path) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    credentials_path.write_text(
        '{"schema_version":1,"credentials":[],"credentials":[]}',
        encoding="utf-8",
    )
    with pytest.raises(CredentialDataError, match="duplicate"):
        load_startup_files(config_path, credentials_path)


def test_duplicate_credential_key_retains_subclass_identity(tmp_path: Path) -> None:
    paths = write_documents(
        tmp_path,
        credentials=[credential(), credential(label="second")],
    )
    with pytest.raises(DuplicateCredentialError) as error:
        load_startup_files(*paths)
    assert type(error.value) is DuplicateCredentialError


@pytest.mark.parametrize("value", [True, False, b"path", None, 1, 1.0, [], {}, object()])
def test_invalid_configuration_path_arguments(tmp_path: Path, value: object) -> None:
    _, credentials_path = write_documents(tmp_path)
    with pytest.raises(ConfigurationError, match="configuration file path"):
        load_startup_files(value, credentials_path)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, False, b"path", None, 1, 1.0, [], {}, object()])
def test_invalid_credential_path_arguments(tmp_path: Path, value: object) -> None:
    config_path, _ = write_documents(tmp_path)
    with pytest.raises(CredentialDataError, match="credential file path"):
        load_startup_files(config_path, value)  # type: ignore[arg-type]


def test_pathlike_resolving_to_bytes_is_rejected_by_file_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class BytesPath(os.PathLike[bytes]):
        def __fspath__(self) -> bytes:
            return os.fsencode(tmp_path / "bytes-config.json")

    _, credentials_path = write_documents(tmp_path)
    opened: list[object] = []

    def unexpected_open(path: object, *args: object, **kwargs: object) -> object:
        opened.append(path)
        raise AssertionError("bytes PathLike must be rejected before file I/O")

    monkeypatch.setattr("builtins.open", unexpected_open)

    with pytest.raises(ConfigurationError) as error:
        load_startup_files(BytesPath(), credentials_path)  # type: ignore[arg-type]

    assert type(error.value) is ConfigurationError
    assert str(error.value) == "configuration file path must resolve to text"
    assert opened == []


def test_ordinary_read_failures_have_stable_wrapped_messages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    original_open = open

    def failing_open(path: object, *args: object, **kwargs: object):
        if os.fspath(path) == os.fspath(config_path):
            raise PermissionError("platform-specific detail")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", failing_open)
    with pytest.raises(
        ConfigurationError,
        match="^configuration file could not be read as strict UTF-8$",
    ):
        load_startup_files(config_path, credentials_path)


def test_second_file_failure_returns_no_partial_startup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path, credentials_path = write_documents(tmp_path)
    credentials_path.write_text("{", encoding="utf-8")
    calls: list[str] = []
    original = config_module.load_config_json

    def observed(text: str) -> SimulatorConfig:
        calls.append("configuration-validated")
        return original(text)

    monkeypatch.setattr(config_module, "load_config_json", observed)
    with pytest.raises(CredentialDataError):
        load_startup_files(config_path, credentials_path)
    assert calls == ["configuration-validated"]


def test_existing_text_loader_signatures_and_behavior_are_unchanged() -> None:
    assert tuple(inspect.signature(config_module.load_config_json).parameters) == ("text",)
    assert tuple(inspect.signature(config_module.load_credentials_json).parameters) == ("text",)
    assert tuple(inspect.signature(config_module.load_startup_json).parameters) == (
        "config_text",
        "credentials_text",
    )
    config_text = json.dumps(CONFIG)
    credentials_text = json.dumps({"schema_version": 1, "credentials": []})
    assert config_module.load_startup_json(config_text, credentials_text) == StartupData(
        SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True),
        (),
    )
