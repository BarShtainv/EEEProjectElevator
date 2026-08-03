"""Stateless validation and codec for the proposed PROJECT_WIEGAND_26 profile."""

from __future__ import annotations

from .models import (
    CredentialDataError,
    DecodedCredential,
    FrameValidation,
    Reason,
    StateInvariantError,
)


_FRAME_LENGTH = 26
_FACILITY_WIDTH = 8
_CREDENTIAL_WIDTH = 16


def _is_binary_bit(value: object) -> bool:
    return type(value) is int and value in (0, 1)


def _require_structural_frame(frame: object) -> tuple[int, ...]:
    if not isinstance(frame, tuple):
        raise StateInvariantError("frame must be an immutable tuple")
    if len(frame) != _FRAME_LENGTH:
        raise StateInvariantError("frame must contain exactly 26 bits")
    if any(not _is_binary_bit(bit) for bit in frame):
        raise StateInvariantError("every frame member must be exact integer 0 or 1")
    return frame


def _has_leading_parity(frame: tuple[int, ...]) -> bool:
    return sum(frame[0:13]) % 2 == 0


def _has_trailing_parity(frame: tuple[int, ...]) -> bool:
    return sum(frame[13:26]) % 2 == 1


def _bits_to_integer(bits: tuple[int, ...]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _decode_fields(frame: tuple[int, ...]) -> DecodedCredential:
    return DecodedCredential(
        facility_code=_bits_to_integer(frame[1:9]),
        credential_number=_bits_to_integer(frame[9:25]),
    )


def validate_frame(frame: object) -> FrameValidation:
    """Validate an external complete frame and decode it when valid."""

    if not isinstance(frame, (tuple, list)):
        return FrameValidation(False, Reason.INVALID_FRAME, None)
    if len(frame) != _FRAME_LENGTH:
        return FrameValidation(False, Reason.INVALID_FRAME, None)
    if any(not _is_binary_bit(bit) for bit in frame):
        return FrameValidation(False, Reason.INVALID_FRAME, None)

    canonical = tuple(frame)
    if not _has_leading_parity(canonical):
        return FrameValidation(False, Reason.PARITY_FAILURE, None)
    if not _has_trailing_parity(canonical):
        return FrameValidation(False, Reason.PARITY_FAILURE, None)
    return FrameValidation(True, None, _decode_fields(canonical))


def decode_frame(frame: tuple[int, ...]) -> DecodedCredential:
    """Decode a structurally and parity-valid trusted frame."""

    canonical = _require_structural_frame(frame)
    if not _has_leading_parity(canonical) or not _has_trailing_parity(canonical):
        raise StateInvariantError("trusted frame parity is invalid")
    return _decode_fields(canonical)


def encode_frame(
    facility_code: int,
    credential_number: int,
) -> tuple[int, ...]:
    """Encode trusted field values as one immutable PROJECT_WIEGAND_26 frame."""

    if type(facility_code) is not int or not 0 <= facility_code <= 255:
        raise CredentialDataError("facility_code must be an integer from 0 to 255")
    if type(credential_number) is not int or not 0 <= credential_number <= 65535:
        raise CredentialDataError(
            "credential_number must be an integer from 0 to 65535"
        )

    facility_bits = tuple(
        (facility_code >> shift) & 1
        for shift in range(_FACILITY_WIDTH - 1, -1, -1)
    )
    credential_bits = tuple(
        (credential_number >> shift) & 1
        for shift in range(_CREDENTIAL_WIDTH - 1, -1, -1)
    )
    leading_data = facility_bits + credential_bits[:4]
    trailing_data = credential_bits[4:]
    leading_parity = sum(leading_data) % 2
    trailing_parity = 1 - (sum(trailing_data) % 2)
    return (
        (leading_parity,)
        + facility_bits
        + credential_bits
        + (trailing_parity,)
    )


def has_valid_parity(frame: tuple[int, ...]) -> bool:
    """Return whether a structurally valid trusted frame passes both regions."""

    canonical = _require_structural_frame(frame)
    return _has_leading_parity(canonical) and _has_trailing_parity(canonical)
