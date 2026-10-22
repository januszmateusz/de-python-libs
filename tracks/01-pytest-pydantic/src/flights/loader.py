import csv
from pathlib import Path

from flights.models import Flight


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
