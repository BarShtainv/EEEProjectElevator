"""SP-06.3 credential JSON and startup loading tests."""

import json

import pytest

from elevator_access_sim import load_credentials_json, load_startup_json
from elevator_access_sim.models import (
    ConfigurationError,
    CredentialDataError,
    CredentialRecord,
    DuplicateCredentialError,
)


CONFIG = json.dumps({"schema_version": 1, "profile": "PROJECT_WIEGAND_26", "output_duration_ms": 3000, "watchdog_timeout_ms": 2000, "watchdog_enabled": True})


def document(records: list[object], **changes: object) -> str:
    return json.dumps({"schema_version": 1, "credentials": records} | changes)


def record(**changes: object) -> dict[str, object]:
    return {"facility_code": 1, "credential_number": 100, "enabled": True, "floor_mask": 65535, "label": "demo-user"} | changes


def test_tst_cfg_004_documented_empty_omitted_unicode_and_order() -> None:
    assert load_credentials_json(document([])) == ()
    values = [record(facility_code=0, credential_number=0, floor_mask=0, label=" משתמש "), record(facility_code=255, credential_number=65535, enabled=False, floor_mask=65535)]
    parsed = load_credentials_json(document(values))
    assert parsed[0] == CredentialRecord(0, 0, True, 0, " משתמש ")
    assert parsed[1].label == "demo-user"
    omitted = record(); del omitted["label"]
    assert load_credentials_json(document([omitted]))[0].label is None


@pytest.mark.parametrize("field,value", [("facility_code", -1), ("facility_code", 256), ("facility_code", True), ("credential_number", -1), ("credential_number", 65536), ("credential_number", False), ("floor_mask", -1), ("floor_mask", 65536), ("floor_mask", True), ("enabled", 1), ("enabled", "true")])
def test_tst_crd_002_invalid_fields(field: str, value: object) -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json(document([record(**{field: value})]))


@pytest.mark.parametrize("label", [None, "", "   ", 1, [], "\ud800"])
def test_invalid_present_labels(label: object) -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json(document([record(label=label)]))


@pytest.mark.parametrize("text", ["{", "[]", "null", "1", '"x"', '{"schema_version":1,"credentials":NaN}'])
def test_malformed_or_nonobject_documents(text: str) -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json(text)


@pytest.mark.parametrize("value", [None, 1, b"{}", {}, []])
def test_nonstring_input(value: object) -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json(value)  # type: ignore[arg-type]


def test_duplicate_members_and_composite_keys_are_distinct_errors() -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json('{"schema_version":1,"schema_version":1,"credentials":[]}')
    with pytest.raises(CredentialDataError):
        load_credentials_json('{"schema_version":1,"credentials":[{"facility_code":1,"facility_code":2,"credential_number":100,"enabled":true,"floor_mask":1}]}')
    with pytest.raises(DuplicateCredentialError):
        load_credentials_json(document([record(), record(label="second")]))
    assert len(load_credentials_json(document([record(), record(facility_code=2, credential_number=99)]))) == 2


@pytest.mark.parametrize("payload", [{"credentials": []}, {"schema_version": 1}, {"schema_version": 1, "credentials": [], "extra": 1}, {"schema_version": 2, "credentials": []}, {"schema_version": True, "credentials": []}, {"schema_version": 1, "credentials": {}}, {"schema_version": 1, "credentials": [1]}])
def test_top_level_and_entry_schema_errors(payload: dict[str, object]) -> None:
    with pytest.raises(CredentialDataError):
        load_credentials_json(json.dumps(payload))


def test_missing_and_unknown_record_fields_and_late_failure_are_atomic() -> None:
    missing = record(); del missing["enabled"]
    with pytest.raises(CredentialDataError): load_credentials_json(document([missing]))
    with pytest.raises(CredentialDataError): load_credentials_json(document([record(extra=1)]))
    before = load_credentials_json(document([record()]))
    with pytest.raises(CredentialDataError): load_credentials_json(document([record(), record(facility_code=2), record(facility_code=3, floor_mask=-1)]))
    assert before == (CredentialRecord(1, 100, True, 65535, "demo-user"),)


def test_tst_cfg_005_startup_success_and_error_identity() -> None:
    startup = load_startup_json(CONFIG, document([record()]))
    assert startup.credentials[0].credential_number == 100
    with pytest.raises(ConfigurationError): load_startup_json("{}", document([]))
    with pytest.raises(CredentialDataError) as error: load_startup_json(CONFIG, "{")
    assert type(error.value) is CredentialDataError
    with pytest.raises(DuplicateCredentialError): load_startup_json(CONFIG, document([record(), record()]))
