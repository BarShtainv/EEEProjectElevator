"""SP-06.3 pure authorization tests."""

import ast
import inspect

import pytest

import elevator_access_sim.authorization as module
from elevator_access_sim import authorize
from elevator_access_sim.models import AuthorizationDecision, CredentialRecord, DecodedCredential, Reason, Result, StateInvariantError


DECODED = DecodedCredential(1, 100)


def record(enabled: object = True, mask: object = 65535, facility: object = 1, credential: object = 100, label: object = None) -> CredentialRecord:
    return CredentialRecord(facility, credential, enabled, mask, label)  # type: ignore[arg-type]


@pytest.mark.parametrize("floor", [1, None, True, "1", []])
def test_tst_aut_001_unknown_precedes_floor_validation(floor: object) -> None:
    assert authorize(DECODED, None, floor) == AuthorizationDecision(Result.DENIED, Reason.UNKNOWN_CREDENTIAL, DECODED, None, None)


@pytest.mark.parametrize("floor", [1, None, True, "1", {}])
def test_tst_aut_002_disabled_precedes_floor_validation(floor: object) -> None:
    disabled = record(False, 0)
    assert authorize(DECODED, disabled, floor) == AuthorizationDecision(Result.DENIED, Reason.DISABLED_CREDENTIAL, DECODED, disabled, None)


@pytest.mark.parametrize("floor", [0, 17, -1, True, 1.0, "1", None, [], {}, object()])
def test_tst_aut_003_invalid_floor(floor: object) -> None:
    selected = record()
    assert authorize(DECODED, selected, floor) == AuthorizationDecision(Result.ERROR, Reason.INVALID_FLOOR, DECODED, selected, None)


@pytest.mark.parametrize("floor", range(1, 17))
def test_tst_aut_004_every_single_set_bit_grants(floor: int) -> None:
    selected = record(mask=1 << (floor - 1))
    assert authorize(DECODED, selected, floor) == AuthorizationDecision(Result.GRANTED, Reason.AUTHORIZED, DECODED, selected, floor)


@pytest.mark.parametrize("floor", range(1, 17))
def test_tst_aut_005_clear_bit_and_neighbor_bits_deny(floor: int) -> None:
    neighbor = 1 << (floor % 16)
    selected = record(mask=neighbor)
    assert authorize(DECODED, selected, floor) == AuthorizationDecision(Result.DENIED, Reason.UNAUTHORIZED_FLOOR, DECODED, selected, floor)


@pytest.mark.parametrize("floor", range(1, 17))
def test_all_mask_grants_and_zero_mask_denies(floor: int) -> None:
    assert authorize(DECODED, record(mask=65535), floor).reason is Reason.AUTHORIZED
    assert authorize(DECODED, record(mask=0), floor).reason is Reason.UNAUTHORIZED_FLOOR


@pytest.mark.parametrize("decoded", [None, (1, 100), DecodedCredential(True, 100), DecodedCredential(-1, 100), DecodedCredential(1, False), DecodedCredential(1, 65536)])
def test_malformed_decoded_raises(decoded: object) -> None:
    with pytest.raises(StateInvariantError): authorize(decoded, None, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("selected", [object(), record(enabled=1), record(mask=-1), record(mask=True), record(label=""), record(label="\ud800"), record(facility=2), record(credential=101)])
def test_malformed_or_mismatched_record_raises(selected: object) -> None:
    with pytest.raises(StateInvariantError): authorize(DECODED, selected, 1)  # type: ignore[arg-type]


def test_authorization_is_pure_and_imports_only_models() -> None:
    selected = record(mask=1)
    before = (DECODED, selected)
    authorize(DECODED, selected, 1)
    assert before == (DECODED, selected)
    tree = ast.parse(inspect.getsource(module))
    assert {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.level} == {"models"}
    assert not any(isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Attribute) for node in ast.walk(tree))
