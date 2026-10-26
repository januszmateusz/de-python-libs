import sqlite3
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def airports_db_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Plik SQLite z tabelą airports (WAW, KRK) — budowany RAZ na sesję."""
    db_path = tmp_path_factory.mktemp("db_session") / "airports.db"
    print("\n[SESSION SETUP] Tworzenie i inicjalizacja bazy danych...")
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("CREATE TABLE airports (code TEXT PRIMARY KEY, city TEXT)")
        conn.execute("INSERT INTO airports VALUES ('WAW', 'Warsaw'), ('KRK', 'Krakow')")
        conn.commit()
    return db_path


@pytest.fixture
def airport_db(airports_db_path: Path) -> Iterator[sqlite3.Connection]:
    """Połączenie na test w jawnej transakcji; zmiany testu są wycofywane w teardownie."""
    with closing(sqlite3.connect(airports_db_path, isolation_level=None)) as conn:
        conn.execute("BEGIN")
        yield conn
        conn.rollback()


def test_airport_db_returns_warsaw_for_waw(airport_db: sqlite3.Connection) -> None:
    cursor = airport_db.cursor()
    cursor.execute("SELECT city FROM airports WHERE code = ?", ("WAW",))
    row = cursor.fetchone()
    assert row == ("Warsaw",)


def test_airport_insert_adds_airport(airport_db: sqlite3.Connection) -> None:
    """Test 1: Wstawia nowe lotnisko i sprawdza, że w tabeli są 3 pozycje."""
    airport_db.execute("INSERT INTO airports VALUES ('GDN', 'Gdansk')")

    cursor = airport_db.execute("SELECT COUNT(*) FROM airports")
    count = cursor.fetchone()[0]

    assert count == 3


def test_airport_has_two_seed_airports(airport_db: sqlite3.Connection) -> None:
    """Test 2: Sprawdza, że na start w tabeli są dokładnie 2 lotniska początkowe.

    Dzięki mechanizmowi `rollback` w fixturze `airport_db`, zmiany z poprzedniego
    testu (wstawienie 'GDN') nie wpłynęły na ten test.
    """
    cursor = airport_db.execute("SELECT COUNT(*) FROM airports")
    count = cursor.fetchone()[0]

    assert count == 2
