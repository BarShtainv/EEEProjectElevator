"""Deterministic monotonic simulated time."""

from __future__ import annotations

from typing import Protocol

from .models import ClockError


class Clock(Protocol):
    def now_ms(self) -> int: ...


def _require_nonnegative_integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ClockError(f"{field} must be a nonnegative integer")
    return value


class SimulatedClock:
    """A clock that owns only a nonnegative logical millisecond value."""

    def __init__(self, start_ms: int = 0) -> None:
        self._now_ms = _require_nonnegative_integer(start_ms, "start_ms")

    def now_ms(self) -> int:
        return self._now_ms

    def advance_by(self, delta_ms: int) -> int:
        delta = _require_nonnegative_integer(delta_ms, "delta_ms")
        target = self._now_ms + delta
        self._now_ms = target
        return self._now_ms

    def advance_to(self, target_ms: int) -> int:
        target = _require_nonnegative_integer(target_ms, "target_ms")
        if target < self._now_ms:
            raise ClockError("target_ms cannot be earlier than current time")
        self._now_ms = target
        return self._now_ms

