from unittest.mock import Mock, create_autospec

import logging
import pytest

from flights import pipeline
from flights.alerts import send_alert

# 4 z 5 lotów punktualnych (< 15 min) → OTP = 0.8 (dokładnie na celu)
DELAYS_AT_TARGET = [0, 5, 10, 14, 30]
# 1 z 4 punktualny → OTP = 0.25
DELAYS_BELOW_TARGET = [0, 20, 30, 45]
# wszystkie punktualne → OTP = 1.0
DELAYS_ABOVE_TARGET = [0, 0, 5, 10, 14]


def test_check_on_time_performance_sends_alert_when_below_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    alert = create_autospec(send_alert)

    monkeypatch.setattr(pipeline, "send_alert", alert)

    result = pipeline.check_on_time_performance(DELAYS_BELOW_TARGET)

    assert result == pytest.approx(0.25)

    alert.assert_called_once_with(
        "On-time performance 25% is below target 80%"
    )


@pytest.mark.parametrize(
    "delays",
    [
        pytest.param(DELAYS_ABOVE_TARGET, id="above_target"),
        pytest.param(DELAYS_AT_TARGET, id="exactly_at_target"),
    ],
)
def test_check_on_time_performance_sends_no_alert_when_target_met(
    monkeypatch: pytest.MonkeyPatch,
    delays: list[int],
) -> None:
    alert = create_autospec(send_alert)

    monkeypatch.setattr(pipeline, "send_alert", alert)

    pipeline.check_on_time_performance(delays)

    alert.assert_not_called()


def test_check_on_time_performance_survives_alert_failure(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    alert = create_autospec(send_alert)
    alert.side_effect = ConnectionError("webhook unreachable")
    monkeypatch.setattr(pipeline, "send_alert", alert)

    with caplog.at_level(logging.ERROR, logger="flights.pipeline"):
        result = pipeline.check_on_time_performance(DELAYS_BELOW_TARGET)

    assert result == pytest.approx(0.25)

    alert.assert_called_once()

    errors = [
        record
        for record in caplog.records
        if record.name == "flights.pipeline" and record.levelno >= logging.ERROR
    ]

    assert len(errors) == 1   
    assert errors[0].exc_info is not None
    assert errors[0].exc_info[0] is ConnectionError

def test_check_otp(monkeypatch):
    monkeypatch.setattr("flights.pipeline.on_time_performance", Mock(return_value=0.5))
    alert = Mock()
    monkeypatch.setattr("flights.pipeline.send_alert", alert)

    result = pipeline.check_on_time_performance([1, 2, 3])

    assert result == 0.5
    alert.assert_called()


