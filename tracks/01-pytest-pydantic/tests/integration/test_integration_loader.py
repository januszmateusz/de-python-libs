from flights.loader import filter_active_flights
from flights.models import Flight


def test_filter_active_flights_returns_only_active_flights(
    mixed_flights: list[Flight],
) -> None:
    result = filter_active_flights(mixed_flights)

    assert [f.flight_number for f in result] == ["LO321", "LO654", "LO987"]
