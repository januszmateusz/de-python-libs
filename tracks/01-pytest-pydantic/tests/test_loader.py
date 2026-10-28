import pytest

from flights.loader import filter_active_flights
from flights.models import Flight

# STATUS_CASE_BUG = pytest.mark.xfail(
#     reason="filter_active_flights compares status case-sensitively",
#     strict=True,
# )


def test_filter_active_flights_returns_only_active_flights(
    mixed_flights: list[Flight],
) -> None:
    result = filter_active_flights(mixed_flights)

    assert [f.flight_number for f in result] == ["LO123", "FR789"]


def test_filter_active_flights_returns_all_flights_when_none_cancelled() -> None:
    flights = [
        Flight("LO123", "WAW", "KRK", "ACTIVE", 10),
        Flight("LO456", "WAW", "GDN", "ACTIVE", 0),
        Flight("FR789", "KRK", "WAW", "ACTIVE", 45),
    ]

    result = filter_active_flights(flights)

    assert result == flights


def test_filter_active_flights_all_cancelled() -> None:
    flights = [
        Flight("LO123", "WAW", "KRK", "CANCELLED", 10),
        Flight("LO456", "WAW", "GDN", "CANCELLED", 0),
        Flight("FR789", "KRK", "WAW", "CANCELLED", 45),
    ]

    active_flights = filter_active_flights(flights)

    assert active_flights == []


@pytest.mark.parametrize(
    "status",
    [
        pytest.param("CANCELLED", id="uppercase_cancelled"),
        pytest.param("Cancelled", id="titlecase_cancelled"),
        pytest.param("cancelled", id="lowercase_cancelled"),
    ],
)
def test_filter_active_flights_removes_cancelled_flights(
    status: str,
) -> None:
    flights = [
        Flight(
            flight_number="LO123",
            origin="WAW",
            destination="KRK",
            status=status,
            delay_minutes=0,
        ),
    ]

    result = filter_active_flights(flights)

    assert result == []
