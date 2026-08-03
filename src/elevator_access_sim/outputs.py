"""Atomic logical output ownership with deterministic timeout evaluation."""

from .models import OutputSnapshot, StateInvariantError


_INACTIVE = OutputSnapshot((False,) * 16, None, None)


def _time(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise StateInvariantError(f"{field} must be a nonnegative integer")
    return value


class OutputManager:
    def __init__(self) -> None:
        self._snapshot = _INACTIVE

    def activate(self, floor: int, now_ms: int, duration_ms: int) -> OutputSnapshot:
        if self._snapshot.active_floor is not None:
            raise StateInvariantError("an output is already active")
        if type(floor) is not int or not 1 <= floor <= 16:
            raise StateInvariantError("floor must be an integer from 1 to 16")
        now = _time(now_ms, "now_ms")
        if type(duration_ms) is not int or not 100 <= duration_ms <= 30000:
            raise StateInvariantError("duration_ms must be an integer from 100 to 30000")
        candidate = OutputSnapshot(tuple(i == floor - 1 for i in range(16)), floor, now + duration_ms)
        self._snapshot = candidate
        return candidate

    def next_expiry_ms(self) -> int | None:
        return self._snapshot.expiry_ms

    def expire_if_due(self, now_ms: int) -> bool:
        now = _time(now_ms, "now_ms")
        expiry = self._snapshot.expiry_ms
        if expiry is None or now < expiry:
            return False
        self._snapshot = _INACTIVE
        return True

    def reset(self) -> OutputSnapshot:
        self._snapshot = _INACTIVE
        return self._snapshot

    def snapshot(self) -> OutputSnapshot:
        return self._snapshot
