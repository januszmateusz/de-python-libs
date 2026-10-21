ON_TIME_THRESHOLD_MINUTES = 15
"""Lot jest punktualny, gdy opóźnienie < 15 min (standard branżowy A15)."""


def classify_delay(delay_minutes: int) -> str:
    """
    "early" < 0, "on_time" 0–14, "minor" 15–59,
    "major" 60–179, "severe" >= 180.
    ValueError, gdy delay_minutes < -120.
    """
    if delay_minutes < -120:
        raise ValueError(f"Delay ({delay_minutes}) is below allowed minimum (-120).")
    elif delay_minutes < 0:
        return "early"
    elif delay_minutes < ON_TIME_THRESHOLD_MINUTES:
        return "on_time"
    elif delay_minutes <= 59:
        return "minor"
    elif delay_minutes <= 179:
        return "major"
    else:
        return "severe"


def average_delay(delays: list[int]) -> float:
    """Średnie opóźnienie w minutach. ValueError dla pustej listy."""
    if not delays:
        raise ValueError("Cannot compute average delay of an empty list.")
    return sum(delays) / len(delays)


def on_time_performance(delays: list[int]) -> float:
    """
    Odsetek lotów punktualnych (OTP) jako ułamek 0.0–1.0.
    Lot jest punktualny, gdy opóźnienie < ON_TIME_THRESHOLD_MINUTES.
    ValueError dla pustej listy.
    """
    if not delays:
        raise ValueError("Cannot compute on-time performance of an empty list.")
    on_time_count = sum(1 for delay in delays if delay < ON_TIME_THRESHOLD_MINUTES)
    return on_time_count / len(delays)
