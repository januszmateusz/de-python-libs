import csv
import logging
from pathlib import Path

from flights.models import Flight

logger = logging.getLogger(__name__)


def read_flights_csv(path: Path) -> list[Flight]:
    """Wczytuje loty z CSV z nagłówkiem; konwertuje delay_minutes na int."""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [
            Flight(
                flight_number=row["flight_number"],
                origin=row["origin"],
                destination=row["destination"],
                status=row["status"],
                delay_minutes=int(row["delay_minutes"]),
            )
            for row in reader
        ]


def filter_active_flights(flights: list[Flight]) -> list[Flight]:
    """Zwraca loty, które nie zostały odwołane."""
    return [f for f in flights if f.status != "CANCELLED"]


def read_flights_csv_lenient(path: Path) -> list[Flight]:
    """
    Wczytuje loty z CSV, pomijając wiersze z nieprawidłowym delay_minutes.
    Każdy pominięty wiersz jest logowany jako WARNING z numerem linii w pliku.
    """
    flights: list[Flight] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):
            try:
                delay = int(row["delay_minutes"])
            except ValueError:
                logger.warning(
                    "Skipping line %d in %s: invalid delay_minutes %r",
                    line_number,
                    path.name,
                    row["delay_minutes"],
                )
                continue
            flights.append(
                Flight(
                    flight_number=row["flight_number"],
                    origin=row["origin"],
                    destination=row["destination"],
                    status=row["status"],
                    delay_minutes=delay,
                )
            )
    return flights
