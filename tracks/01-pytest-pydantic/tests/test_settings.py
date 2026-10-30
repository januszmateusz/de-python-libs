import re

import pytest

from flights.settings import (
    DEFAULT_ON_TIME_THRESHOLD,
    ENV_ON_TIME_THRESHOLD,
    get_on_time_threshold,
)


def test_get_on_time_threshold_returns_default_when_variable_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENV_ON_TIME_THRESHOLD, raising=False)

    assert get_on_time_threshold() == DEFAULT_ON_TIME_THRESHOLD


def test_get_on_time_threshold_reads_value_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_ON_TIME_THRESHOLD, "30")

    result = get_on_time_threshold()

    assert result == 30


@pytest.mark.parametrize(
    "raw_value",
    [
        pytest.param("abc", id="not_a_number"),
        pytest.param("0", id="zero"),
        pytest.param("-1", id="negative"),
        pytest.param("15.5", id="fractional"),
    ],
)
def test_get_on_time_threshold_raises_for_invalid_value(
    monkeypatch: pytest.MonkeyPatch,
    raw_value: str,
) -> None:
    monkeypatch.setenv(ENV_ON_TIME_THRESHOLD, raw_value)

    with pytest.raises(ValueError, match=re.escape(f"got {raw_value!r}")):
        get_on_time_threshold()