from datetime import date
from typing import Any

import httpx
import pytest
import respx

from flights.api_client import (
    DEPARTURES_PATH,
    FlightApiError,
    fetch_departures,
    make_client,
)

HOST = "api.flights.example.com"
DAY = date(2026, 11, 14)

SAMPLE_DEPARTURES: list[dict[str, Any]] = [
    {"flight_number": "LO123", "destination": "KRK", "delay_minutes": 10},
    {"flight_number": "LO456", "destination": "GDN", "delay_minutes": 0},
]


def test_fetch_departures_returns_departures_from_response(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        return_value=httpx.Response(200, json={"departures": SAMPLE_DEPARTURES})
    )
    client = make_client(token="test-token")

    result = fetch_departures(client, "WAW", DAY)

    assert result == SAMPLE_DEPARTURES


def test_fetch_departures_sends_airport_date_and_token(
    respx_mock: respx.MockRouter,
) -> None:
    route = respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        return_value=httpx.Response(200, json={"departures": []})
    )
    client = make_client(token="test-token")

    fetch_departures(client, "WAW", DAY)

    assert route.call_count == 1
    request = route.calls.last.request

    assert request.url.params["airport"] == "WAW"
    assert request.url.params["date"] == "2026-11-14"
    assert request.headers["Authorization"] == "Bearer test-token"


def test_fetch_departures_retries_after_server_error(
    respx_mock: respx.MockRouter,
) -> None:
    route = respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(200, json={"departures": SAMPLE_DEPARTURES}),
        ]
    )
    client = make_client(token="test-token")
    sleeps: list[float] = []

    result = fetch_departures(client, "WAW", DAY, sleep=sleeps.append)

    assert result == SAMPLE_DEPARTURES
    assert route.call_count == 2
    assert sleeps == [1.0]


def test_fetch_departures_retries_after_timeout(
    respx_mock: respx.MockRouter,
) -> None:
    route = respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        side_effect=[
            httpx.ConnectTimeout("timed out"),
            httpx.Response(200, json={"departures": SAMPLE_DEPARTURES}),
        ]
    )
    client = make_client(token="test-token")
    sleeps: list[float] = []

    result = fetch_departures(client, "WAW", DAY, sleep=sleeps.append)

    assert result == SAMPLE_DEPARTURES
    assert route.call_count == 2
    assert sleeps == [1.0]


def test_fetch_departures_gives_up_after_max_attempts(
    respx_mock: respx.MockRouter,
) -> None:
    route = respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        return_value=httpx.Response(503)
    )
    client = make_client(token="test-token")
    sleeps: list[float] = []

    with pytest.raises(FlightApiError, match="HTTP 503"):
        fetch_departures(client, "WAW", DAY, max_attempts=3, sleep=sleeps.append)

    assert route.call_count == 3
    assert sleeps == [1.0, 2.0]


@pytest.mark.parametrize(
    "status_code",
    [
        pytest.param(404, id="not_found"),
        pytest.param(400, id="bad_request"),
        pytest.param(401, id="unauthorized"),
    ],
)
def test_fetch_departures_does_not_retry_client_errors(
    respx_mock: respx.MockRouter,
    status_code: int,
) -> None:
    route = respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        return_value=httpx.Response(status_code)
    )
    client = make_client(token="test-token")
    sleeps: list[float] = []

    with pytest.raises(FlightApiError, match=f"HTTP {status_code}"):
        fetch_departures(client, "WAW", DAY, sleep=sleeps.append)

    assert route.call_count == 1
    assert sleeps == []


def test_fetch_departures_keeps_timeout_as_cause_after_last_attempt(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        side_effect=httpx.ReadTimeout(
            "read timed out"
        )  # każde żądanie kończy się timeoutem
    )
    client = make_client(token="test-token")

    with pytest.raises(FlightApiError, match="Network error") as exc_info:
        fetch_departures(client, "WAW", DAY, max_attempts=2, sleep=lambda _: None)

    assert isinstance(exc_info.value.__cause__, httpx.ReadTimeout)


def test_fetch_departures_translates_connection_errors(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get(host=HOST, path=DEPARTURES_PATH).mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    client = make_client(token="test-token")

    with pytest.raises(FlightApiError) as exc_info:
        fetch_departures(client, "WAW", DAY, max_attempts=2, sleep=lambda _: None)

    assert isinstance(exc_info.value.__cause__, httpx.ConnectError)
