from pathlib import Path
from typing import Protocol

FLIGHTS_HEADER = "flight_number,origin,destination,status,delay_minutes"


class MakeFlightsCsv(Protocol):
    """Typ fabryki zapisującej plik CSV z lotami z surowych wierszy."""

    def __call__(
        self,
        rows: list[str],
        header: str = FLIGHTS_HEADER,
        filename: str = "flights.csv",
    ) -> Path: ...
