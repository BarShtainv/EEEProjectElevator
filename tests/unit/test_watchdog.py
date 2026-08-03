"""SP-06.6 deterministic watchdog tests."""

import ast, inspect
import pytest
import elevator_access_sim.watchdog as module
from elevator_access_sim import Watchdog
from elevator_access_sim.models import StateInvariantError


@pytest.mark.parametrize("timeout,interval", [(1,1),(2,1),(3,1),(4,2),(5,2),(2000,1000),(4294967295,2147483647)])
def test_formula_and_enabled_initial_state(timeout:int, interval:int)->None:
    w=Watchdog(True,timeout,10); assert w.heartbeat_interval_ms()==interval
    assert w.next_heartbeat_ms()==10+interval and w.expiry_deadline_ms()==10+timeout


def test_disabled_behavior()->None:
    w=Watchdog(False,2000,0); assert w.heartbeat_interval_ms()==1000
    assert w.next_heartbeat_ms() is None and w.expiry_deadline_ms() is None
    assert not w.service(0) and not w.process_heartbeat(0) and not w.expiry_request_if_due(9999)


@pytest.mark.parametrize("enabled", [0,1,"true",None,[],object()])
def test_invalid_enabled(enabled:object)->None:
    with pytest.raises(StateInvariantError):Watchdog(enabled,1,0) # type: ignore[arg-type]


@pytest.mark.parametrize("timeout", [0,-1,4294967296,True,1.0,"1",None,[]])
def test_invalid_timeout(timeout:object)->None:
    with pytest.raises(StateInvariantError):Watchdog(True,timeout,0) # type: ignore[arg-type]


@pytest.mark.parametrize("now", [-1,True,1.0,"1",None,[],object()])
def test_invalid_constructor_time(now:object)->None:
    with pytest.raises(StateInvariantError):Watchdog(True,1,now) # type: ignore[arg-type]


def test_direct_service_and_suppression()->None:
    w=Watchdog(True,2000,0); assert w.service(500)
    assert w.expiry_deadline_ms()==2500 and w.next_heartbeat_ms()==1500
    assert w.service(500); w.set_service_suppressed(True); before=(w.expiry_deadline_ms(),w.next_heartbeat_ms())
    assert not w.service(600) and before==(w.expiry_deadline_ms(),w.next_heartbeat_ms())
    assert not w.service(2500) and before==(w.expiry_deadline_ms(),w.next_heartbeat_ms())


def test_exact_heartbeat_normal_and_scheduler_misuse()->None:
    w=Watchdog(True,2000,0)
    with pytest.raises(StateInvariantError):w.process_heartbeat(999)
    assert w.process_heartbeat(1000); assert w.expiry_deadline_ms()==3000 and w.next_heartbeat_ms()==2000
    with pytest.raises(StateInvariantError):w.process_heartbeat(1000)


def test_timeout_one_same_timestamp_priority()->None:
    normal=Watchdog(True,1,0); assert normal.process_heartbeat(1); assert normal.expiry_deadline_ms()==2; assert not normal.expiry_request_if_due(1)
    suppressed=Watchdog(True,1,0); suppressed.set_service_suppressed(True)
    assert not suppressed.process_heartbeat(1); assert suppressed.expiry_request_if_due(1); assert not suppressed.expiry_request_if_due(1); assert suppressed.next_heartbeat_ms() is None


def test_default_suppressed_expiry_and_new_epoch()->None:
    w=Watchdog(True,2000,0); w.set_service_suppressed(True)
    assert not w.process_heartbeat(1000) and not w.expiry_request_if_due(1000)
    assert not w.process_heartbeat(2000) and w.expiry_request_if_due(2000) and not w.expiry_request_if_due(2000)
    with pytest.raises(StateInvariantError):w.service(2000)
    w.reinitialize(2000); assert w.next_heartbeat_ms()==3000 and w.expiry_deadline_ms()==4000
    assert w.process_heartbeat(3000)


def test_normal_schedules_through_3000_and_30000()->None:
    w=Watchdog(True,2000,0)
    for timestamp in range(1000,30001,1000):
        assert w.process_heartbeat(timestamp); assert not w.expiry_request_if_due(timestamp)


@pytest.mark.parametrize("value", [0,1,"true",None,[]])
def test_invalid_suppression_flag(value:object)->None:
    with pytest.raises(StateInvariantError):Watchdog(True,1,0).set_service_suppressed(value) # type: ignore[arg-type]


@pytest.mark.parametrize("value", [-1,True,1.0,"1",None,[]])
@pytest.mark.parametrize("method", ["service","process_heartbeat","expiry_request_if_due","reinitialize"])
def test_invalid_method_times(value:object,method:str)->None:
    w=Watchdog(True,2000,0); before=(w.next_heartbeat_ms(),w.expiry_deadline_ms())
    with pytest.raises(StateInvariantError):getattr(w,method)(value)
    assert before==(w.next_heartbeat_ms(),w.expiry_deadline_ms())


def test_service_expired_and_backward_preserve()->None:
    w=Watchdog(True,2000,100); before=(w.next_heartbeat_ms(),w.expiry_deadline_ms())
    with pytest.raises(StateInvariantError):w.service(99)
    with pytest.raises(StateInvariantError):w.service(2100)
    assert before==(w.next_heartbeat_ms(),w.expiry_deadline_ms())


def test_late_expiry_one_shot_and_reinitialize_failure()->None:
    w=Watchdog(True,10,0); assert not w.expiry_request_if_due(9); assert w.expiry_request_if_due(20); deadline=w.expiry_deadline_ms()
    assert not w.expiry_request_if_due(21) and w.expiry_deadline_ms()==deadline
    with pytest.raises(StateInvariantError):w.reinitialize(-1)
    assert w.expiry_deadline_ms()==deadline and w.next_heartbeat_ms() is None


def test_import_scope()->None:
    tree=ast.parse(inspect.getsource(module)); assert {n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.level}=={"models"}
