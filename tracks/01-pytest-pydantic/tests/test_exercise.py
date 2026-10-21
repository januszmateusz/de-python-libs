import pytest

from flights.delays import average_delay, classify_delay


def test_classify_delay_5_min_on_time() -> None:
    assert classify_delay(5) == "on_time"


def test_classify_delay_200_min_severe() -> None:
    assert classify_delay(200) == "severe"


def test_classify_delay_raises_for_delay_below_minus_120() -> None:
    with pytest.raises(ValueError, match="below allowed minimum"):
        classify_delay(-200)


def test_average_delay_returns_mean_for_whole_number_result() -> None:
    delays_list = [10, 20, 30]
    result = average_delay(delays_list)
    assert result == pytest.approx(20.0)
