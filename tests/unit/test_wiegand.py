"""Focused tests for the proposed PROJECT_WIEGAND_26 codec."""

from __future__ import annotations

import ast
import inspect
from collections.abc import Iterator

import pytest

import elevator_access_sim.wiegand as wiegand_module
from elevator_access_sim import (
    decode_frame,
    encode_frame,
    has_valid_parity,
    validate_frame,
)
from elevator_access_sim.models import (
    CredentialDataError,
    CredentialRequest,
    DecodedCredential,
    FrameValidation,
    ReaderSource,
    Reason,
    StateInvariantError,
)


VECTORS = (
    ("WV-001", 0, 0, "00000000000000000000000001"),
    ("WV-002", 255, 65535, "01111111111111111111111111"),
    ("WV-003", 1, 1, "10000000100000000000000010"),
    ("WV-004", 85, 4660, "10101010100010010001101001"),
    ("WV-005", 42, 43690, "10010101010101010101010101"),
    ("WV-006", 1, 100, "10000000100000000011001000"),
)


def _bits(bit_string: str) -> tuple[int, ...]:
    return tuple(0 if character == "0" else 1 for character in bit_string)


def _independent_reference(
    facility_code: int,
    credential_number: int,
) -> tuple[str, tuple[int, int]]:
    facility = f"{facility_code:08b}"
    credential = f"{credential_number:016b}"
    leading_data = facility + credential[:4]
    trailing_data = credential[4:]
    leading_parity = str(sum(int(bit) for bit in leading_data) % 2)
    trailing_parity = str(1 - sum(int(bit) for bit in trailing_data) % 2)
    complete = leading_parity + facility + credential + trailing_parity
    decoded = (int(complete[1:9], 2), int(complete[9:25], 2))
    return complete, decoded


def _flip(frame: tuple[int, ...], index: int) -> tuple[int, ...]:
    return frame[:index] + (1 - frame[index],) + frame[index + 1 :]


@pytest.mark.parametrize(
    ("vector_id", "facility", "credential", "documented"),
    VECTORS,
    ids=[vector[0] for vector in VECTORS],
)
def test_tst_wie_006_fixed_vectors_are_independently_verified_and_round_trip(
    vector_id: str,
    facility: int,
    credential: int,
    documented: str,
) -> None:
    del vector_id
    independently_calculated, independently_decoded = _independent_reference(
        facility,
        credential,
    )
    frame = _bits(documented)

    assert independently_calculated == documented
    assert independently_decoded == (facility, credential)
    assert len(frame) == 26
    assert all(type(bit) is int and bit in (0, 1) for bit in frame)
    assert sum(frame[0:13]) % 2 == 0
    assert sum(frame[13:26]) % 2 == 1
    assert has_valid_parity(frame) is True

    expected = DecodedCredential(facility, credential)
    assert validate_frame(frame) == FrameValidation(True, None, expected)
    assert decode_frame(frame) == expected
    assert encode_frame(facility, credential) == frame
    assert decode_frame(encode_frame(facility, credential)) == expected


@pytest.mark.parametrize(
    ("index", "corruption"),
    (
        (0, "documentation-bit-1-leading-parity"),
        (25, "documentation-bit-26-trailing-parity"),
        (1, "documentation-bit-2-leading-data"),
        (13, "documentation-bit-14-trailing-data"),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.parametrize(
    ("vector_id", "facility", "credential", "documented"),
    VECTORS,
    ids=[vector[0] for vector in VECTORS],
)
def test_tst_wie_004_005_all_24_single_bit_corruptions_fail_parity(
    vector_id: str,
    facility: int,
    credential: int,
    documented: str,
    index: int,
    corruption: str,
) -> None:
    del vector_id, facility, credential, corruption
    corrupted = _flip(_bits(documented), index)
    assert validate_frame(corrupted) == FrameValidation(
        False,
        Reason.PARITY_FAILURE,
        None,
    )
    assert has_valid_parity(corrupted) is False
    with pytest.raises(StateInvariantError, match="parity"):
        decode_frame(corrupted)


def test_validate_frame_accepts_a_valid_list_at_the_external_boundary() -> None:
    frame = list(_bits(VECTORS[-1][3]))
    assert validate_frame(frame) == FrameValidation(
        True,
        None,
        DecodedCredential(1, 100),
    )


@pytest.mark.parametrize(
    ("facility", "credential"),
    (
        (0, 0),
        (255, 65535),
        (0, 65535),
        (255, 0),
        (1, 100),
        (17, 257),
        (42, 43690),
        (85, 4660),
        (213, 54321),
    ),
)
def test_tst_wie_008_encoder_boundaries_and_fixed_round_trips(
    facility: int,
    credential: int,
) -> None:
    frame = encode_frame(facility, credential)
    assert isinstance(frame, tuple)
    assert len(frame) == 26
    assert all(type(bit) is int and bit in (0, 1) for bit in frame)
    assert has_valid_parity(frame) is True
    assert decode_frame(frame) == DecodedCredential(facility, credential)


@pytest.mark.parametrize(
    "frame",
    (
        None,
        1,
        1.0,
        True,
        "0" * 26,
        b"0" * 26,
        bytearray(26),
        {"frame": (0,) * 26},
        {0, 1},
        (bit for bit in (0,) * 26),
        iter((0,) * 26),
        object(),
    ),
    ids=(
        "none",
        "integer",
        "float",
        "boolean",
        "string",
        "bytes",
        "bytearray",
        "mapping",
        "set",
        "generator",
        "iterator",
        "object",
    ),
)
def test_tst_wie_007_invalid_containers_return_invalid_frame(frame: object) -> None:
    assert validate_frame(frame) == FrameValidation(False, Reason.INVALID_FRAME, None)


def test_validate_frame_does_not_consume_an_arbitrary_iterator() -> None:
    frame: Iterator[int] = iter((0,) * 26)
    assert validate_frame(frame).reason is Reason.INVALID_FRAME
    assert next(frame) == 0


@pytest.mark.parametrize("container", [tuple, list], ids=["tuple", "list"])
@pytest.mark.parametrize("length", [0, 1, 25, 27, 52])
def test_tst_wie_001_002_invalid_lengths_return_invalid_frame(
    container: type[tuple[int, ...]] | type[list[int]],
    length: int,
) -> None:
    frame = container([0] * length)
    assert validate_frame(frame) == FrameValidation(False, Reason.INVALID_FRAME, None)


@pytest.mark.parametrize(
    "member",
    [-1, 2, True, False, None, "0", "1", 0.0, 1.0, [], object()],
    ids=(
        "negative",
        "two",
        "true",
        "false",
        "none",
        "string-zero",
        "string-one",
        "float-zero",
        "float-one",
        "empty-collection",
        "object",
    ),
)
def test_tst_wie_003_non_binary_members_return_invalid_frame(member: object) -> None:
    frame = (0,) * 12 + (member,) + (0,) * 13
    assert validate_frame(frame) == FrameValidation(False, Reason.INVALID_FRAME, None)


@pytest.mark.parametrize(
    "frame",
    (
        list(_bits(VECTORS[0][3])),
        (0,) * 25,
        (0,) * 12 + (2,) + (0,) * 13,
        (0,) * 12 + (True,) + (0,) * 13,
        _flip(_bits(VECTORS[0][3]), 0),
        _flip(_bits(VECTORS[0][3]), 25),
    ),
    ids=(
        "list",
        "invalid-length",
        "invalid-member",
        "boolean-member",
        "leading-parity",
        "trailing-parity",
    ),
)
def test_decode_frame_rejects_trusted_api_misuse(frame: object) -> None:
    with pytest.raises(StateInvariantError):
        decode_frame(frame)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "frame",
    (
        [0] * 26,
        (0,) * 25,
        (0,) * 12 + (2,) + (0,) * 13,
        (0,) * 12 + (True,) + (0,) * 13,
    ),
    ids=("list", "invalid-length", "invalid-member", "boolean-member"),
)
def test_has_valid_parity_rejects_structural_misuse(frame: object) -> None:
    with pytest.raises(StateInvariantError):
        has_valid_parity(frame)  # type: ignore[arg-type]


@pytest.mark.parametrize("index", [0, 25], ids=["leading", "trailing"])
def test_has_valid_parity_returns_false_for_structural_frame_with_bad_parity(
    index: int,
) -> None:
    assert has_valid_parity(_flip(_bits(VECTORS[0][3]), index)) is False


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("facility", -1),
        ("facility", 256),
        ("credential", -1),
        ("credential", 65536),
        ("facility", True),
        ("credential", False),
        ("facility", 1.0),
        ("credential", 1.0),
        ("facility", "1"),
        ("credential", "1"),
        ("facility", None),
        ("credential", None),
        ("facility", []),
        ("credential", []),
        ("facility", {}),
        ("credential", {}),
    ),
)
def test_encode_frame_rejects_invalid_trusted_values(
    field: str,
    value: object,
) -> None:
    facility = value if field == "facility" else 1
    credential = value if field == "credential" else 100
    with pytest.raises(CredentialDataError):
        encode_frame(facility, credential)  # type: ignore[arg-type]


def test_tst_dat_003_same_frame_is_independent_of_lf_hf_metadata() -> None:
    frame = _bits(VECTORS[-1][3])
    lf_request = CredentialRequest(ReaderSource.LF, frame, 1)
    hf_request = CredentialRequest(ReaderSource.HF, frame, 1)

    assert lf_request.frame is hf_request.frame
    assert lf_request.reader_source is ReaderSource.LF
    assert hf_request.reader_source is ReaderSource.HF
    assert validate_frame(lf_request.frame) == validate_frame(hf_request.frame)
    assert decode_frame(frame) == DecodedCredential(1, 100)


def test_wiegand_module_is_stateless_and_has_only_reviewed_dependencies() -> None:
    tree = ast.parse(inspect.getsource(wiegand_module))
    project_imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.level > 0
    }
    mutable_global_values = (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp)

    assert project_imports == {"models"}
    assert not any(
        isinstance(node, (ast.Assign, ast.AnnAssign))
        and isinstance(node.value, mutable_global_values)
        for node in tree.body
    )
    assert set(inspect.signature(validate_frame).parameters) == {"frame"}
    assert set(inspect.signature(decode_frame).parameters) == {"frame"}
    assert tuple(inspect.signature(encode_frame).parameters) == (
        "facility_code",
        "credential_number",
    )
    assert set(inspect.signature(has_valid_parity).parameters) == {"frame"}
