import time
from collections.abc import Callable
from datetime import date
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://api.flights.example.com"
DEPARTURES_PATH = "/v1/departures"
RETRYABLE_STATUS_CODES = frozenset({500, 502, 503, 504})
BACKOFF_SECONDS = 1.0


class FlightApiError(Exception):
    """Nie udało się pobrać danych z API lotów (błąd domenowy, niezależny od biblioteki HTTP)."""


def make_client(token: str, base_url: str = DEFAULT_BASE_URL) -> httpx.Client:
    """Klient HTTP z adresem bazowym, tokenem i timeoutem."""
    return httpx.Client(
        base_url=base_url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )


def fetch_departures(
    client: httpx.Client,
    airport: str,
    day: date,
    *,
    max_attempts: int = 3,
    sleep: Callable[[float], None] = time.sleep,
) -> list[dict[str, Any]]:
    """Pobiera odloty z lotniska w danym dniu. Ponawia przy błędach 5xx i timeoutach."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    params = {"airport": airport, "date": day.isoformat()}
    response = _get_with_retries(
        client, DEPARTURES_PATH, params, max_attempts=max_attempts, sleep=sleep
    )
    if response.is_error:
        raise FlightApiError(
            f"API rejected departures request for {airport} on {day}: "
            f"HTTP {response.status_code}"
        )
    payload = response.json()
    return list(payload["departures"])


def _get_with_retries(
    client: httpx.Client,
    path: str,
    params: dict[str, str],
    *,
    max_attempts: int,
    sleep: Callable[[float], None],
) -> httpx.Response:
    for attempt in range(1, max_attempts + 1):
        is_last_attempt = attempt == max_attempts
        try:
            response = client.get(path, params=params)
        except httpx.TransportError as exc:
            if is_last_attempt:
                raise FlightApiError(
                    f"Network error calling {path} after {max_attempts} attempts"
                ) from exc
        else:
            if response.status_code not in RETRYABLE_STATUS_CODES or is_last_attempt:
                return response
        sleep(BACKOFF_SECONDS * 2 ** (attempt - 1))

    raise AssertionError("unreachable: loop always returns or raises")
