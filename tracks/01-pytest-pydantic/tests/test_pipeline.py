from unittest.mock import create_autospec

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
