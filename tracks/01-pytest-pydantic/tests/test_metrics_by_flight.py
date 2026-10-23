import pytest

from flights import delays
from flights.loader import filter_active_flights
from flights.models import Flight


def test_average_delay_of_active_flights_ignores_cancelled(
    mixed_flights: list[Flight],
) -> None:
    active_delays = [f.delay_minutes for f in filter_active_flights(mixed_flights)]

    result = delays.average_delay(active_delays)

    assert result == pytest.approx(27.5)
