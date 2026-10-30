import logging

from flights.alerts import send_alert
from flights.delays import on_time_performance

logger = logging.getLogger(__name__)

OTP_TARGET = 0.8


def check_on_time_performance(delays: list[int], target: float = OTP_TARGET) -> float:
    """Liczy OTP; gdy spada poniżej celu, wysyła alert. Błąd alertu nie przerywa pipeline'u."""
    otp = on_time_performance(delays)
    if otp < target:
        try:
            send_alert(f"On-time performance {otp:.0%} is below target {target:.0%}")
        except Exception:
            logger.exception("Failed to send on-time performance alert")
    return otp
