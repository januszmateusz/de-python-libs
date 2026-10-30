import os

ENV_ON_TIME_THRESHOLD = "FLIGHTS_ON_TIME_THRESHOLD"
DEFAULT_ON_TIME_THRESHOLD = 15


def get_on_time_threshold() -> int:
    """Próg punktualności w minutach ze zmiennej środowiskowej (domyślnie 15)."""
    raw = os.environ.get(ENV_ON_TIME_THRESHOLD)
    if raw is None:
        return DEFAULT_ON_TIME_THRESHOLD

    error = f"{ENV_ON_TIME_THRESHOLD} must be a positive integer, got {raw!r}"
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(error) from None
    if value <= 0:
        raise ValueError(error)
    return value
