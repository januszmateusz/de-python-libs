import re
from pathlib import Path

import pytest

from flights.loader import read_flights_csv
from flights.models import Flight


def test_read_flights_returns_flights_for_valid_file(tmp_path: Path) -> None:
    """Poprawny plik z wierszami danych -> zwraca listę obiektów Flight."""
    csv_file = tmp_path / "flights.csv"
    csv_file.write_text(
        "flight_number,origin,destination,status,delay_minutes\n"
        "LO123,WAW,JFK,On Time,0\n"
        "LH456,FRA,LHR,Delayed,45\n"
        "BA789,LHR,LAX,Cancelled,120\n",
        encoding="utf-8",
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


def test_read_flights_returns_empty_list_for_header_only_file(tmp_path: Path) -> None:
    """Plik z samym nagłówkiem -> zwraca pustą listę."""
    csv_file = tmp_path / "flights.csv"
    csv_file.write_text(
        "flight_number,origin,destination,status,delay_minutes",
        encoding="utf-8",
    )

    result = read_flights_csv(csv_file)

    assert result == []


def test_read_flights_raises_for_non_integer_delay(tmp_path: Path) -> None:
    """Wiersz z delay_minutes = 'XYZ' -> rzuca ValueError (testowane z match)."""
    csv_file = tmp_path / "flights.csv"
    csv_file.write_text(
        "flight_number,origin,destination,status,delay_minutes\n"
        "LO123,WAW,JFK,On Time,XYZ\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=re.escape("invalid literal for int()")):
        read_flights_csv(csv_file)


def test_read_flights_raises_for_missing_flight_number_column(tmp_path: Path) -> None:
    """Plik bez kolumny flight_number -> rzuca KeyError."""
    csv_file = tmp_path / "flights.csv"
    csv_file.write_text(
        "origin,destination,status,delay_minutes\nWAW,JFK,On Time,0\n",
        encoding="utf-8",
    )

    with pytest.raises(KeyError, match="flight_number"):
        read_flights_csv(csv_file)
