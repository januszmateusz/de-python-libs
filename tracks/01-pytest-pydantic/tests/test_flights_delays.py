import pytest

from flights import delays


@pytest.mark.parametrize(
    ("delay_minutes", "expected"),
    [
        (-120, "early"),
        (-1, "early"),
        (0, "on_time"),
        (14, "on_time"),
        (15, "minor"),
        (59, "minor"),
        (60, "major"),
        (179, "major"),
        (180, "severe"),
    ],
)
def test_classify_delay_returns_category_at_boundaries(
    delay_minutes: int, expected: str
) -> None:
    assert delays.classify_delay(delay_minutes) == expected


@pytest.mark.parametrize(
    "delay_minutes",
    [
        -121,
        -500,
    ],
)
def test_classify_delay_raises_for_delay_below_minus_120(delay_minutes: int) -> None:
    with pytest.raises(ValueError, match="below allowed minimum"):
        delays.classify_delay(delay_minutes)


@pytest.mark.parametrize(
    ("delays_list", "expected"),
    [
        pytest.param(
            [10, 20, 30],
            20.0,
            id="mean_is_whole_number",
        ),
        pytest.param(
            [10, 20, 25],
            18.333,
            id="mean_is_fractional",
        ),
    ],
)
def test_average_delay_returns_expected_mean(
    delays_list: list[int],
    expected: float,
) -> None:
    result = delays.average_delay(delays_list)

    assert result == pytest.approx(expected, rel=1e-3)


def test_average_delay_raises_for_empty_list() -> None:
    delays_list: list[int] = []
    with pytest.raises(ValueError, match="empty list"):
        delays.average_delay(delays_list)


@pytest.mark.parametrize(
    ("delays_list", "expected"),
    [
        pytest.param([0, 10, 20, 30], 0.5, id="half_of_flights_on_time"),
        pytest.param([14, 15], 0.5, id="boundary_14_on_time_15_late"),
        pytest.param([0, 5, 10, 14], 1.0, id="all_flights_on_time_at_14_minute_limit"),
        pytest.param([15, 60, 200], 0.0, id="all_flights_late_from_15_minutes"),
    ],
)
def test_on_time_performance_returns_expected_ratio(
    delays_list: list[int], expected: float
) -> None:
    result = delays.on_time_performance(delays_list)

    assert result == pytest.approx(expected)


def test_on_time_performance_raises_for_empty_list() -> None:
    delays_list: list[int] = []
    with pytest.raises(ValueError, match="empty list"):
        delays.on_time_performance(delays_list)
