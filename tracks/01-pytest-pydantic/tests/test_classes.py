from dataclasses import dataclass

import pytest

from flights.models import Flight


@dataclass(frozen=True)
class Route:
    origin: str
    destination: str


@pytest.fixture
def sample_route() -> Route:
    """Zwraca przykładową trasę WAW -> KRK."""
    return Route(origin="WAW", destination="KRK")


class TestRoute:
    def test_route_attributes(self, sample_route: Route) -> None:
        """Sprawdza poprawność pól w strukturze trasy."""
        assert sample_route.origin == "WAW"
        assert sample_route.destination == "KRK"

    def test_flights_matching_route(
        self, sample_route: Route, mixed_flights: list[Flight]
    ) -> None:
        """Weryfikuje, czy fixture mixed_flights zawiera lot pasujący do trasy."""
        matching_flights = [
            f
            for f in mixed_flights
            if f.origin == sample_route.origin
            and f.destination == sample_route.destination
        ]

        assert [f.flight_number for f in matching_flights] == ["LO123"]
