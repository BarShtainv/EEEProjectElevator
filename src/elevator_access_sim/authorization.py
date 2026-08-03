"""Pure credential and floor authorization decisions."""

from __future__ import annotations

from .models import (
    AuthorizationDecision,
    CredentialRecord,
    DecodedCredential,
    Reason,
    Result,
    StateInvariantError,
)


def _require_integer(value: object, field: str, maximum: int) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise StateInvariantError(f"trusted {field} is invalid")
    return value


def _validate_decoded(value: object) -> DecodedCredential:
    if not isinstance(value, DecodedCredential):
        raise StateInvariantError("decoded must be a DecodedCredential")
    _require_integer(value.facility_code, "facility_code", 255)
    _require_integer(value.credential_number, "credential_number", 65535)
    return value


def _validate_record(value: object) -> CredentialRecord:
    if not isinstance(value, CredentialRecord):
        raise StateInvariantError("record must be a CredentialRecord or None")
    _require_integer(value.facility_code, "record facility_code", 255)
    _require_integer(value.credential_number, "record credential_number", 65535)
    if type(value.enabled) is not bool:
        raise StateInvariantError("trusted record enabled value is invalid")
    _require_integer(value.floor_mask, "record floor_mask", 65535)
    if value.label is not None:
        if type(value.label) is not str or not value.label.strip():
            raise StateInvariantError("trusted record label is invalid")
        try:
            value.label.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise StateInvariantError("trusted record label is invalid") from exc
    return value


def authorize(
    decoded: DecodedCredential,
    record: CredentialRecord | None,
    requested_floor: object,
) -> AuthorizationDecision:
    """Return the frozen pure authorization outcome in precedence order."""

    trusted_decoded = _validate_decoded(decoded)
    if record is None:
        return AuthorizationDecision(
            Result.DENIED,
            Reason.UNKNOWN_CREDENTIAL,
            trusted_decoded,
            None,
            None,
        )

    trusted_record = _validate_record(record)
    if (
        trusted_record.facility_code != trusted_decoded.facility_code
        or trusted_record.credential_number != trusted_decoded.credential_number
    ):
        raise StateInvariantError("record key does not match decoded credential")
    if not trusted_record.enabled:
        return AuthorizationDecision(
            Result.DENIED,
            Reason.DISABLED_CREDENTIAL,
            trusted_decoded,
            trusted_record,
            None,
        )
    if type(requested_floor) is not int or not 1 <= requested_floor <= 16:
        return AuthorizationDecision(
            Result.ERROR,
            Reason.INVALID_FLOOR,
            trusted_decoded,
            trusted_record,
            None,
        )
    if trusted_record.floor_mask & (1 << (requested_floor - 1)) == 0:
        return AuthorizationDecision(
            Result.DENIED,
            Reason.UNAUTHORIZED_FLOOR,
            trusted_decoded,
            trusted_record,
            requested_floor,
        )
    return AuthorizationDecision(
        Result.GRANTED,
        Reason.AUTHORIZED,
        trusted_decoded,
        trusted_record,
        requested_floor,
    )
