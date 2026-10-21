import pytest

from flights import delays


def test_classify_delay_raises_for_delay_below_minus_120() -> None:
    delay_minutes = -121
    with pytest.raises(ValueError, match="below allowed minimum"):
        delays.classify_delay(delay_minutes)


def test_classify_delay_returns_early_at_minus_120() -> None:
    delay_minutes = -120
    result = delays.classify_delay(delay_minutes)
    assert result == "early"


def test_classify_delay_returns_early_for_minus_1() -> None:
    delay_minutes = -1
    result = delays.classify_delay(delay_minutes)
    assert result == "early"


def test_classify_delay_returns_on_time_for_zero_delay() -> None:
    delay_minutes = 0
    result = delays.classify_delay(delay_minutes)
    assert result == "on_time"


def test_classify_delay_returns_on_time_for_14_minutes_delay() -> None:
    delay_minutes = 14
    result = delays.classify_delay(delay_minutes)
    assert result == "on_time"


def test_classify_delay_returns_minor_for_15_minutes_delay() -> None:
    delay_minutes = 15
    result = delays.classify_delay(delay_minutes)
    assert result == "minor"


def test_classify_delay_returns_minor_for_59_minutes_delay() -> None:
    delay_minutes = 59
    result = delays.classify_delay(delay_minutes)
    assert result == "minor"


def test_classify_delay_returns_major_for_60_minutes_delay() -> None:
    delay_minutes = 60
    result = delays.classify_delay(delay_minutes)
    assert result == "major"


def test_classify_delay_returns_major_for_179_minutes_delay() -> None:
    delay_minutes = 179
    result = delays.classify_delay(delay_minutes)
    assert result == "major"


def test_classify_delay_returns_severe_for_180_minutes_delay() -> None:
    delay_minutes = 180
    result = delays.classify_delay(delay_minutes)
    assert result == "severe"


def test_average_delay_returns_mean_for_whole_number_result() -> None:
    delays_list = [10, 20, 30]
    result = delays.average_delay(delays_list)
    assert result == pytest.approx(20.0)


def test_average_delay_returns_mean_for_fractional_result() -> None:
    delays_list = [10, 20, 25]
    result = delays.average_delay(delays_list)
    assert result == pytest.approx(18.333, rel=1e-3)


def test_average_delay_raises_for_empty_list() -> None:
    delays_list: list[int] = []
    with pytest.raises(ValueError, match="empty list"):
        delays.average_delay(delays_list)


def test_on_time_performance_returns_half_when_two_of_four_on_time() -> None:
    delays_list = [0, 10, 20, 30]
    result = delays.on_time_performance(delays_list)
    assert result == pytest.approx(0.5)


def test_on_time_performance_treats_14_minutes_as_on_time_and_15_as_late() -> None:
    delays_list = [14, 15]
    result = delays.on_time_performance(delays_list)
    assert result == pytest.approx(0.5)


def test_on_time_performance_returns_one_when_all_flights_on_time() -> None:
    delays_list = [0, 5, 10, 14]
    result = delays.on_time_performance(delays_list)
    assert result == pytest.approx(1.0)


def test_on_time_performance_returns_zero_when_no_flight_on_time() -> None:
    delays_list = [15, 60, 200]
    result = delays.on_time_performance(delays_list)
    assert result == pytest.approx(0.0)


def test_on_time_performance_raises_for_empty_list() -> None:
    delays_list: list[int] = []
    with pytest.raises(ValueError, match="empty list"):
        delays.on_time_performance(delays_list)
