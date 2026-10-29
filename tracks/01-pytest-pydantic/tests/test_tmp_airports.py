from pathlib import Path

import pytest


@pytest.mark.integration
def test_reference_airports_contains_main_hubs(
    reference_airports_csv: Path,
) -> None:
    """Test 1: Sprawdza, czy plik zawiera kluczowe kody lotnisk."""
    content = reference_airports_csv.read_text(encoding="utf-8")

    assert "WAW" in content
    assert "KRK" in content
    assert "GDN" in content


@pytest.mark.integration
def test_reference_airports_structure(reference_airports_csv: Path) -> None:
    """Test 2: Sprawdza nagłówek oraz liczbę wierszy w pliku referencyjnym."""
    lines = reference_airports_csv.read_text(encoding="utf-8").splitlines()

    # Nagłówek + 3 lotniska = 4 linie
    assert lines[0] == "code,city"
    assert len(lines) == 4
    assert "Warszawa" in lines[1]
