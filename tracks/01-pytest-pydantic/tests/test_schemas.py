from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from flights.models import Flight
from flights.schemas import FlightRecord


def valid_row() -> dict[str, Any]:
    """Poprawny wiersz jak z csv.DictReader — wszystkie wartości są tekstem."""
    return {
        "flight_number": "LO123",
        "origin": "WAW",
        "destination": "KRK",
        "status": "ACTIVE",
        "delay_minutes": "10",
        "scheduled_departure": "2026-11-18T10:30:00Z",
    }


def test_flight_record_converts_text_values_to_declared_types() -> None:
    record = FlightRecord.model_validate(valid_row())

    assert record.delay_minutes == 10
    assert record.scheduled_departure == datetime(2026, 11, 18, 10, 30, tzinfo=UTC)


def test_flight_record_reports_all_errors_at_once() -> None:
    row = valid_row()
    row["delay_minutes"] = "abc"
    del row["destination"]

    with pytest.raises(ValidationError) as exc_info:
        FlightRecord.model_validate(row)

    errors = exc_info.value.errors()
    assert {(e["loc"], e["type"]) for e in errors} == {
        (("delay_minutes",), "int_parsing"),
        (("destination",), "missing"),
    }


def test_dataclass_does_not_validate_types() -> None:
    """Demonstracja: dataclass przyjmuje dowolną wartość mimo adnotacji typu."""
    flight = Flight("LO123", "WAW", "KRK", "ACTIVE", "abc")  # type: ignore[arg-type]

    assert flight.delay_minutes == "abc"


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        pytest.param("10", 10, id="numeric_text"),
        pytest.param(10.0, 10, id="float_without_fraction"),
        pytest.param("-120", -120, id="negative_numeric_text"),
    ],
)
def test_flight_record_lax_mode_accepts_lossless_conversions(
    raw_value: object, expected: int
) -> None:
    row = valid_row()
    row["delay_minutes"] = raw_value

    record = FlightRecord.model_validate(row)

    assert record.delay_minutes == expected


@pytest.mark.parametrize(
    ("raw_value", "error_type"),
    [
        pytest.param("abc", "int_parsing", id="text"),
        pytest.param(10.5, "int_from_float", id="float_with_fraction"),
        pytest.param("10.5", "int_parsing", id="text_with_fraction"),
        pytest.param(None, "int_type", id="none"),
    ],
)
def test_flight_record_lax_mode_rejects_lossy_or_invalid_values(
    raw_value: object, error_type: str
) -> None:
    row = valid_row()
    row["delay_minutes"] = raw_value

    with pytest.raises(ValidationError) as exc_info:
        FlightRecord.model_validate(row)

    assert len(exc_info.value.errors()) == 1
    error = exc_info.value.errors()[0]
    assert error["loc"] == ("delay_minutes",)
    assert error["type"] == error_type


def test_flight_record_lax_mode_rejects_number_for_text_field() -> None:
    row = valid_row()
    row["flight_number"] = 123

    with pytest.raises(ValidationError) as exc_info:
        FlightRecord.model_validate(row)

    assert len(exc_info.value.errors()) == 1
    error = exc_info.value.errors()[0]
    assert error["loc"] == ("flight_number",)
    assert error["type"] == "string_type"


def test_flight_record_strict_mode_rejects_csv_text() -> None:
    with pytest.raises(ValidationError) as exc_info:
        FlightRecord.model_validate(valid_row(), strict=True)

    failed_fields = {e["loc"] for e in exc_info.value.errors()}
    # W strict nie przechodzą pola nie-tekstowe podane jako tekst: int i datetime
    assert failed_fields == {
        ("delay_minutes",),
        ("scheduled_departure",),
    }


def test_flight_record_gate_defaults_to_none_when_missing() -> None:
    record = FlightRecord.model_validate(valid_row())  # valid_row() nie ma klucza "gate"

    assert record.gate is None


def test_flight_record_keeps_empty_csv_cell_as_empty_string() -> None:
    row = valid_row()
    row["gate"] = ""  # pusta komórka CSV

    record = FlightRecord.model_validate(row)

    assert record.gate == ""

#   delay_minutes "-121"            -> greater_than_equal
#   origin "waw"                    -> string_pattern_mismatch
#   origin "WARS"                   -> string_pattern_mismatch
#   scheduled_departure bez strefy  -> timezone_aware
#   destination "123"               -> string_pattern_mismatch
@pytest.mark.parametrize(
    ("field", "raw_value"),
    [
        pytest.param("delay_minutes", "-121", id="delay_below_minimum"),
        pytest.param("origin", "waw", id="lowercase_airport_code"),
        pytest.param("origin", "WARS", id="four_letter_airport_code"),
        pytest.param("scheduled_departure", "2026-11-18T10:30:00", id="naive_datetime"),
        # TODO: dodaj jeden własny przypadek naruszenia reguły (inny niż powyższe)
        pytest.param("destination", "123", id="numeric_airport_code"),
    ],
)
def test_flight_record_rejects_business_rule_violations(field: str, raw_value: object) -> None:
    row = valid_row()
    row[field] = raw_value

    with pytest.raises(ValidationError) as exc_info:
        FlightRecord.model_validate(row)

    errors = exc_info.value.errors()

    assert len(errors) == 1
    assert errors[0]["loc"] == (field,)
