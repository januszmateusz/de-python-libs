import pytest

from flights.models import Flight


@pytest.fixture
def mixed_flights() -> list[Flight]:
    """Trzy loty: trzy aktywne loty z RZE."""
    return [
        Flight("LO321", "RZE", "KRK", "ACTIVE", 0),
        Flight("LO654", "RZE", "GDN", "ACTIVE", 5),
        Flight("LO987", "RZE", "WAW", "ACTIVE", 25),
    ]
