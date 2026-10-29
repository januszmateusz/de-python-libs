import re

import pytest
from factories import MakeFlightsCsv

from flights.loader import read_flights_csv
from flights.models import Flight


@pytest.mark.integration
def test_read_flights_returns_flights_for_valid_file(
    make_flights_csv: MakeFlightsCsv,
) -> None:
    """Poprawny plik z wierszami danych -> zwraca listę obiektów Flight."""
    csv_file = make_flights_csv(
        [
            "LO123,WAW,JFK,On Time,0",
            "LH456,FRA,LHR,Delayed,45",
            "BA789,LHR,LAX,Cancelled,120",
        ]
    )

    result = read_flights_csv(csv_file)

    expected = [
        Flight(
            flight_number="LO123",
            origin="WAW",
            destination="JFK",
            status="On Time",
            delay_minutes=0,
        ),
        Flight(
            flight_number="LH456",
            origin="FRA",
            destination="LHR",
            status="Delayed",
            delay_minutes=45,
        ),
        Flight(
            flight_number="BA789",
            origin="LHR",
            destination="LAX",
            status="Cancelled",
            delay_minutes=120,
        ),
    ]

    assert result == expected


@pytest.mark.integration
def test_read_flights_returns_empty_list_for_header_only_file(
    make_flights_csv: MakeFlightsCsv,
) -> None:
    """Plik z samym nagłówkiem -> zwraca pustą listę."""
    csv_file = make_flights_csv([])

    result = read_flights_csv(csv_file)

    assert result == []


@pytest.mark.integration
def test_read_flights_raises_for_non_integer_delay(
    make_flights_csv: MakeFlightsCsv,
) -> None:
    """Wiersz z delay_minutes = 'XYZ' -> rzuca ValueError (testowane z match)."""
    csv_file = make_flights_csv(["LO123,WAW,JFK,On Time,XYZ"])

    with pytest.raises(ValueError, match=re.escape("invalid literal for int()")):
        read_flights_csv(csv_file)


@pytest.mark.integration
def test_read_flights_raises_for_missing_flight_number_column(
    make_flights_csv: MakeFlightsCsv,
) -> None:
    """Plik bez kolumny flight_number -> rzuca KeyError."""
    csv_file = make_flights_csv(
        ["WAW,JFK,ACTIVE,0"],
        header="origin,destination,status,delay_minutes",
    )

    with pytest.raises(KeyError, match="flight_number"):
        read_flights_csv(csv_file)
