def classify_delay(delay_minutes: int) -> str:
    """
    "early" < 0, "on_time" 0–14, "minor" 15–59,
    "major" 60–179, "severe" >= 180.
    ValueError, gdy delay_minutes < -120.
    """
    if delay_minutes < -120:
        raise ValueError("Delay cannot be less than -120 minutes.")
    elif delay_minutes < 0:
        return "early"
    elif delay_minutes <= 14:
        return "on_time"
    elif delay_minutes <= 59:
        return "minor"
    elif delay_minutes <= 179:
        return "major"
    else:
        return "severe"