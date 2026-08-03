"""SP-06.5 logical output manager tests."""

import ast, inspect
from dataclasses import FrozenInstanceError
import pytest
import elevator_access_sim.outputs as module
from elevator_access_sim import OutputManager, SimulatedClock
from elevator_access_sim.models import StateInvariantError


def test_initial_state() -> None:
    m=OutputManager(); s=m.snapshot()
    assert len(s.channels)==16 and all(type(v) is bool and not v for v in s.channels)
    assert s.active_floor is None and s.expiry_ms is None and m.next_expiry_ms() is None and m.snapshot()==s


@pytest.mark.parametrize("floor", range(1,17))
def test_tst_out_001_all_floor_mapping(floor:int)->None:
    s=OutputManager().activate(floor,500,100)
    assert sum(s.channels)==1 and s.channels[floor-1] is True and s.active_floor==floor and s.expiry_ms==600


@pytest.mark.parametrize("duration", [100,3000,30000])
@pytest.mark.parametrize("now", [0,500,10**12])
def test_duration_arithmetic(now:int,duration:int)->None:
    assert OutputManager().activate(1,now,duration).expiry_ms==now+duration


@pytest.mark.parametrize("floor", [0,17,-1,True,1.0,"1",None,[],object()])
def test_invalid_floor_atomic(floor:object)->None:
    m=OutputManager(); before=m.snapshot()
    with pytest.raises(StateInvariantError):m.activate(floor,0,100) # type: ignore[arg-type]
    assert m.snapshot()==before


@pytest.mark.parametrize("now", [-1,True,1.0,"1",None,[]])
def test_invalid_time_atomic(now:object)->None:
    m=OutputManager(); before=m.snapshot()
    with pytest.raises(StateInvariantError):m.activate(1,now,100) # type: ignore[arg-type]
    assert m.snapshot()==before


@pytest.mark.parametrize("duration", [99,30001,-1,0,True,1.0,"100",None,[]])
def test_invalid_duration_atomic(duration:object)->None:
    m=OutputManager(); before=m.snapshot()
    with pytest.raises(StateInvariantError):m.activate(1,0,duration) # type: ignore[arg-type]
    assert m.snapshot()==before


def test_concurrent_activation_preserves_original()->None:
    m=OutputManager(); original=m.activate(1,0,3000)
    for args in ((2,1,100),(1,50,30000),(None,None,None)):
        with pytest.raises(StateInvariantError):m.activate(*args) # type: ignore[arg-type]
        assert m.snapshot()==original


def test_before_at_after_expiry_one_shot()->None:
    m=OutputManager(); m.activate(1,0,3000)
    assert not m.expire_if_due(0) and not m.expire_if_due(2999)
    assert m.expire_if_due(3000) and not m.expire_if_due(3000) and not m.expire_if_due(3001)
    assert m.snapshot().active_floor is None
    n=OutputManager(); n.activate(1,0,3000); assert n.expire_if_due(4000)


@pytest.mark.parametrize("now", [-1,True,1.0,"1",None,[],object()])
def test_invalid_expiry_time_preserves_active(now:object)->None:
    m=OutputManager(); before=m.activate(8,0,100)
    with pytest.raises(StateInvariantError):m.expire_if_due(now) # type: ignore[arg-type]
    assert m.snapshot()==before


@pytest.mark.parametrize("floor", [1,8,16])
def test_reset_cancels_timeout_and_snapshot_is_historical(floor:int)->None:
    m=OutputManager(); old=m.activate(floor,0,100); reset=m.reset()
    assert reset==m.snapshot() and m.next_expiry_ms() is None and not m.expire_if_due(100)
    assert old.active_floor==floor and m.reset()==reset
    with pytest.raises(FrozenInstanceError):old.active_floor=None # type: ignore[misc]


def test_simulated_clock_caller_and_import_scope()->None:
    c=SimulatedClock(); m=OutputManager(); m.activate(1,c.now_ms(),3000); c.advance_to(2999)
    assert not m.expire_if_due(c.now_ms()); c.advance_to(3000); assert m.expire_if_due(c.now_ms())
    tree=ast.parse(inspect.getsource(module)); assert {n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.level}=={"models"}
