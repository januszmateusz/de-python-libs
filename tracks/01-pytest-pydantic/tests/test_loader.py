from flights.loader import filter_active_flights
from flights.models import Flight

# FLIGHTS = [
#     Flight("LO123", "WAW", "KRK", "ACTIVE", 10),
#     Flight("LO456", "WAW", "GDN", "CANCELLED", 0),
#     Flight("FR789", "KRK", "WAW", "ACTIVE", 45),
# ]


# @pytest.fixture
# def mixed_flights() -> list[Flight]:
#     return FLIGHTS


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


def test_isolation(mixed_flights: list[Flight]) -> None:
    """Testuje, czy fixture mixed_flights jest izolowana między testami."""
    # Modyfika  cja mixed_flights w tym teście nie powinna wpływać na inne testy
    mixed_flights.append(Flight("FR999", "WAW", "GDN", "ACTIVE", 15))
    assert len(mixed_flights) == 4


# def test_isolation_final_check(mixed_flights: list[Flight]) -> None:
#     """Sprawdza, czy mixed_flights jest nadal w pierwotnym stanie po poprzednich testach."""
#     assert len(mixed_flights) == 3  # Powinno być 3 loty, jak w definicji fixture
