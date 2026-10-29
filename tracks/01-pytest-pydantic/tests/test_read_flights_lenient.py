import logging

import pytest
from factories import MakeFlightsCsv

from flights.loader import read_flights_csv_lenient
from flights.models import Flight


@pytest.mark.integration
def test_read_flights_csv_lenient_skips_rows_with_invalid_delay(
    make_flights_csv: MakeFlightsCsv,
) -> None:
    path = make_flights_csv(
        [
            "LO123,WAW,KRK,ontime,0",
            "LO456,WAW,GDN,delayed,abc",
            "LO789,KRK,WAW,delayed,15",
        ]
    )

    flights = read_flights_csv_lenient(path)

    assert flights == [
        Flight(
            flight_number="LO123",
            origin="WAW",
            destination="KRK",
            status="ontime",
            delay_minutes=0,
        ),
        Flight(
            flight_number="LO789",
            origin="KRK",
            destination="WAW",
            status="delayed",
            delay_minutes=15,
        ),
    ]


@pytest.mark.integration
def test_read_flights_csv_lenient_logs_warning_with_line_number_for_invalid_delay(
    make_flights_csv: MakeFlightsCsv,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = make_flights_csv(
        [
            "LO123,WAW,KRK,ontime,0",
            "LO456,WAW,GDN,delayed,abc",
            "LO789,KRK,WAW,delayed,15",
        ]
    )

    with caplog.at_level(logging.WARNING, logger="flights.loader"):
        read_flights_csv_lenient(path)

    warnings = [
        record
        for record in caplog.records
        if record.levelno == logging.WARNING and record.name == "flights.loader"
    ]

    assert len(warnings) == 1
    assert "line 3 in" in warnings[0].getMessage()


@pytest.mark.integration
def test_read_flights_csv_lenient__logs_nothing_for_valid_file(
    make_flights_csv: MakeFlightsCsv,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = make_flights_csv(
        [
            "LO123,WAW,KRK,ontime,0",
            "LO456,WAW,GDN,delayed,10",
            "LO789,KRK,WAW,delayed,15",
        ]
    )

    with caplog.at_level(logging.WARNING, logger="flights.loader"):
        read_flights_csv_lenient(path)

    warnings = [
        record
        for record in caplog.records
        if record.levelno >= logging.WARNING and record.name == "flights.loader"
    ]

    assert warnings == []
