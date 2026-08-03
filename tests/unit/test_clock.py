"""Focused tests for SP-06.1 simulated monotonic time."""

import ast
import inspect

import pytest

import elevator_access_sim.clock as clock_module
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.models import ClockError


def test_tst_tim_003_clock_starts_at_zero_by_default() -> None:
    assert SimulatedClock().now_ms() == 0


def test_tst_tim_003_clock_accepts_valid_nonzero_start() -> None:
    assert SimulatedClock(25).now_ms() == 25


def test_tst_tim_003_advance_by_zero_is_idempotent() -> None:
    clock = SimulatedClock(25)
    assert clock.advance_by(0) == 25
    assert clock.now_ms() == 25


def test_tst_tim_003_advance_by_positive_delta() -> None:
    clock = SimulatedClock(25)
    assert clock.advance_by(10) == 35
    assert clock.now_ms() == 35


def test_tst_tim_003_advance_to_equal_time_is_idempotent() -> None:
    clock = SimulatedClock(25)
    assert clock.advance_to(25) == 25
    assert clock.now_ms() == 25


def test_tst_tim_003_advance_to_later_time() -> None:
    clock = SimulatedClock(25)
    assert clock.advance_to(100) == 100
    assert clock.now_ms() == 100


@pytest.mark.parametrize("value", [-1, True, 1.0, "1", None])
def test_tst_tim_003_rejects_invalid_start(value: object) -> None:
    with pytest.raises(ClockError, match="start_ms"):
        SimulatedClock(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [-1, True, 1.0, "1", None])
def test_tst_tim_003_rejected_delta_does_not_change_time(value: object) -> None:
    clock = SimulatedClock(25)
    with pytest.raises(ClockError, match="delta_ms"):
        clock.advance_by(value)  # type: ignore[arg-type]
    assert clock.now_ms() == 25


@pytest.mark.parametrize("value", [24, -1, True, 25.0, "25", None])
def test_tst_tim_003_rejected_target_does_not_change_time(value: object) -> None:
    clock = SimulatedClock(25)
    with pytest.raises(ClockError, match="target_ms"):
        clock.advance_to(value)  # type: ignore[arg-type]
    assert clock.now_ms() == 25


def test_clock_has_no_wall_clock_sleep_thread_or_async_dependency() -> None:
    tree = ast.parse(inspect.getsource(clock_module))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
    assert imported_roots.isdisjoint({"time", "threading", "asyncio"})
    assert not any(
        isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id == "sleep")
            or (isinstance(node.func, ast.Attribute) and node.func.attr == "sleep")
        )
        for node in ast.walk(tree)
    )

