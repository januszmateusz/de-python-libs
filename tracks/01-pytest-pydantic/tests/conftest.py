import pytest

from flights.models import Flight

pytest.register_assert_rewrite("helpers")


@pytest.fixture
def mixed_flights() -> list[Flight]:
    """Trzy loty: dwa aktywne (WAW, KRK) i jeden odwołany (WAW)."""
    return [
        Flight("LO123", "WAW", "KRK", "ACTIVE", 10),
        Flight("LO456", "WAW", "GDN", "CANCELLED", 0),
        Flight("FR789", "KRK", "WAW", "ACTIVE", 45),
    ]
