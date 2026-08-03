"""Missing required public-flow evidence for SP-06.9."""

from __future__ import annotations

import pytest

from elevator_access_sim import Controller, encode_frame
from elevator_access_sim.clock import SimulatedClock
from elevator_access_sim.models import (
    ControllerState,
    CredentialRecord,
    CredentialRequest,
    EventType,
    ReaderSource,
    Reason,
    Result,
    SimulatorConfig,
)


FRAME = encode_frame(1, 100)
CONFIG = SimulatorConfig(1, "PROJECT_WIEGAND_26", 3000, 2000, True)
RECORD = CredentialRecord(1, 100, True, 65535)


def _controller() -> Controller:
    controller = Controller(SimulatedClock())
    response = controller.initialize(CONFIG, [RECORD])
    assert response.state is ControllerState.IDLE
    return controller


@pytest.mark.parametrize(
    ("invalid_request", "reason"),
    [
        pytest.param(CredentialRequest("LF", FRAME, 1), Reason.INVALID_SOURCE, id="invalid-source"),
        pytest.param(CredentialRequest(ReaderSource.LF, FRAME[:-1], 1), Reason.INVALID_FRAME, id="invalid-frame"),
        pytest.param(
            CredentialRequest(ReaderSource.LF, (1 - FRAME[0],) + FRAME[1:], 1),
            Reason.PARITY_FAILURE,
            id="parity-failure",
        ),
        pytest.param(CredentialRequest(ReaderSource.LF, FRAME, 17), Reason.INVALID_FLOOR, id="invalid-floor"),
    ],
)
def test_tst_e2e_004_tst_rst_004_tst_nfr_003_invalid_input_then_valid_grant(
    invalid_request: CredentialRequest,
    reason: Reason,
) -> None:
    controller = _controller()

    rejected = controller.submit(invalid_request)
    recovered = controller.submit(CredentialRequest(ReaderSource.HF, FRAME, 16))

    assert (rejected.result, rejected.reason, rejected.state) == (
        Result.ERROR,
        reason,
        ControllerState.IDLE,
    )
    assert rejected.output_snapshot.active_floor is None
    assert (recovered.result, recovered.reason, recovered.state) == (
        Result.GRANTED,
        Reason.AUTHORIZED,
        ControllerState.OUTPUT_ACTIVE,
    )
    assert recovered.output_snapshot.active_floor == 16
    assert [event.event_type for event in controller.events()] == [
        EventType.VALIDATION_ERROR,
        EventType.ACCESS_DECISION,
    ]
    assert [event.sequence_number for event in controller.events()] == [1, 2]
