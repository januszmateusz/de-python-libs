import flights.delays as delays
from helpers import assert_same_flight

def test_classify_delay():
    assert delays.classify_delay(5) == "on_time"
    assert delays.classify_delay(20) == "minor"
    assert delays.classify_delay(100) == "major"
    assert delays.classify_delay(200) == "severe"

# def test_first_failure():
#     assert "WAW" == "XXX"

# def test_second_failure():
#     assert {"airport":"WAW", "city":"Warsaw", "other":"aaa"} == {"airport":"WAW", "city":"Krakow", "other":"aaa"}

# def test_third_failure():
#     assert ["LOT", "1234", "WAW"] == ["LOT", "1234", "WAW"]

# def test_fourth_failure():
#     assert {"LOT", "WAW", "KRK"} == {"LOT", "WAW", "KRK", "GDN"}

def test_flight_via_helper() -> None:
    actual = {"airport": "WAW", "city": "Warsaw", "other": "aaa"}
    expected = {"airport": "WAW", "city": "Warsaw", "other": "aaa"}
    assert_same_flight(actual, expected)

# def test_classify_delay_minus_500():
#    assert delays.classify_delay(-500) == "on_time"