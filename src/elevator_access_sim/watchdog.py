"""Deterministic logical watchdog scheduling primitives."""

from .models import StateInvariantError


def _time(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise StateInvariantError(f"{field} must be a nonnegative integer")
    return value


class Watchdog:
    def __init__(self, enabled: bool, timeout_ms: int, now_ms: int) -> None:
        if type(enabled) is not bool:
            raise StateInvariantError("enabled must be a Boolean")
        if type(timeout_ms) is not int or not 1 <= timeout_ms <= 4294967295:
            raise StateInvariantError("timeout_ms is invalid")
        now = _time(now_ms, "now_ms")
        self._enabled = enabled
        self._timeout = timeout_ms
        self._interval = max(1, timeout_ms // 2)
        self._suppressed = False
        self._emitted = False
        self._last_service = now
        self._deadline = now + timeout_ms if enabled else None
        self._next_heartbeat = now + self._interval if enabled else None

    def heartbeat_interval_ms(self) -> int:
        return self._interval

    def next_heartbeat_ms(self) -> int | None:
        return self._next_heartbeat

    def expiry_deadline_ms(self) -> int | None:
        return self._deadline

    def set_service_suppressed(self, suppressed: bool) -> None:
        if type(suppressed) is not bool:
            raise StateInvariantError("suppressed must be a Boolean")
        self._suppressed = suppressed

    def service(self, now_ms: int) -> bool:
        now = _time(now_ms, "now_ms")
        if not self._enabled:
            return False
        if self._emitted:
            raise StateInvariantError("expired epoch requires reinitialization")
        if now < self._last_service:
            raise StateInvariantError("service time moved backward")
        if self._suppressed:
            return False
        if self._deadline is None or now >= self._deadline:
            raise StateInvariantError("cannot service an expired epoch")
        self._last_service = now
        self._deadline = now + self._timeout
        self._next_heartbeat = now + self._interval
        return True

    def process_heartbeat(self, now_ms: int) -> bool:
        now = _time(now_ms, "now_ms")
        if not self._enabled:
            return False
        if self._emitted or self._next_heartbeat is None:
            raise StateInvariantError("no heartbeat is scheduled")
        if now != self._next_heartbeat:
            raise StateInvariantError("heartbeat time is not exactly due")
        if self._suppressed:
            self._next_heartbeat = now + self._interval
            return False
        self._last_service = now
        self._deadline = now + self._timeout
        self._next_heartbeat = now + self._interval
        return True

    def expiry_request_if_due(self, now_ms: int) -> bool:
        now = _time(now_ms, "now_ms")
        if not self._enabled or self._deadline is None or self._emitted:
            return False
        if now < self._deadline:
            return False
        self._emitted = True
        self._next_heartbeat = None
        return True

    def reinitialize(self, now_ms: int) -> None:
        now = _time(now_ms, "now_ms")
        self._suppressed = False
        self._emitted = False
        self._last_service = now
        self._deadline = now + self._timeout if self._enabled else None
        self._next_heartbeat = now + self._interval if self._enabled else None
