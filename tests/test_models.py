import pytest
from pydantic import ValidationError

from de_python_libs.models import FlightEvent


def test_valid_event_normalizes_icao24():
    e = FlightEvent(
        flight_id="LO123",
        icao24="48AE21",
        event_type="departure",
        event_ts="2026-09-27T10:00:00Z",
    )
    assert e.icao24 == "48ae21"


def test_invalid_icao24_raises():
    with pytest.raises(ValidationError):
        FlightEvent(
            flight_id="LO123",
            icao24="XYZ",
            event_type="departure",
            event_ts="2026-09-27T10:00:00Z",
        )
