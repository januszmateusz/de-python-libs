import csv
from pathlib import Path

import pytest
from factories import FLIGHTS_HEADER, MakeFlightsCsv

from flights.models import Flight

pytest.register_assert_rewrite("helpers")


@pytest.fixture(scope="function")
def mixed_flights() -> list[Flight]:
    """Trzy loty: dwa aktywne (WAW, KRK) i jeden odwołany (WAW)."""
    return [
        Flight("LO123", "WAW", "KRK", "ACTIVE", 10),
        Flight("LO456", "WAW", "GDN", "CANCELLED", 0),
        Flight("FR789", "KRK", "WAW", "ACTIVE", 45),
    ]


@pytest.fixture
def make_flights_csv(tmp_path: Path) -> MakeFlightsCsv:
    """Fabryka: zapisuje w tmp_path plik CSV z nagłówkiem i podanymi surowymi wierszami."""

    def _make(
        rows: list[str],
        header: str = FLIGHTS_HEADER,
        filename: str = "flights.csv",
    ) -> Path:
        path = tmp_path / filename
        path.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
        return path

    return _make


@pytest.fixture(scope="session")
def reference_airports_csv(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Plik referencyjny lotnisk (tylko do odczytu) — tworzony raz na sesję."""
    session_dir = tmp_path_factory.mktemp("reference")
    file_path = session_dir / "airports.csv"

    headers = ["code", "city"]
    airports_data = [
        ["WAW", "Warszawa"],
        ["KRK", "Kraków"],
        ["GDN", "Gdańsk"],
    ]

    with file_path.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(airports_data)

    return file_path
