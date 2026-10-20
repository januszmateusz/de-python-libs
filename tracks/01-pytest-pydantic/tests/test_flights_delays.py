import pytest

import flights.delays as delays


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
        