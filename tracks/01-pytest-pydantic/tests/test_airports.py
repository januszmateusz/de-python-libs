import sqlite3
from collections.abc import Iterator
from contextlib import closing

import pytest


@pytest.fixture
def airport_db() -> Iterator[sqlite3.Connection]:
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE airports (code TEXT PRIMARY KEY, city TEXT)")
        conn.execute("INSERT INTO airports VALUES ('WAW', 'Warsaw'), ('KRK', 'Krakow')")
        print("\nSETUP")
        yield conn
        print("\nTEARDOWN")


def test_airport_db_returns_warsaw_for_waw(airport_db: sqlite3.Connection) -> None:
    cursor = airport_db.cursor()
    cursor.execute("SELECT city FROM airports WHERE code = ?", ("WAW",))
    row = cursor.fetchone()
    assert row == ("Warsaw",)
