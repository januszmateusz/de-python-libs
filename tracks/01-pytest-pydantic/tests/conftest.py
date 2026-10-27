import csv
from pathlib import Path

import pytest
from factories import FLIGHTS_HEADER, MakeFlightsCsv

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


@pytest.fixture
def make_flights_csv(
    tmp_path: Path,
    line_ending: str,
) -> MakeFlightsCsv:
    """Fabryka: zapisuje w tmp_path plik CSV z nagłówkiem i podanymi surowymi wierszami."""

    def _make_flights_csv(
        rows: list[str],
        header: str = FLIGHTS_HEADER,
        filename: str = "flights.csv",
    ) -> Path:
        path = tmp_path / filename
        content = line_ending.join([header, *rows]) + line_ending
        path.write_text(content, encoding="utf-8", newline="")
        return path

    return _make_flights_csv


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


@pytest.fixture(params=["\n", "\r\n"], ids=["LF", "CRLF"])
def line_ending(request: pytest.FixtureRequest) -> str:
    """Koniec linii w generowanych plikach CSV: LF i CRLF (każdy zależny test uruchamia się dwukrotnie)."""
    return str(request.param)
