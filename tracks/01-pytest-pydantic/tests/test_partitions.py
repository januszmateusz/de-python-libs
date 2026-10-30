from datetime import UTC, datetime, tzinfo
from pathlib import Path
from typing import Self

import pytest

from flights import partitions

# 23:30 UTC — w Warszawie jest już 00:30 następnego dnia
FIXED_NOW = datetime(2026, 10, 30, 23, 30, tzinfo=UTC)
BASE = Path("data") / "flights"


class FakeDatetime(datetime):
    """datetime z zamrożonym now(), do podmiany w module partitions."""

    @classmethod
    def now(cls, tz: tzinfo | None = None) -> Self:
        return cls(2026, 10, 30, 23, 30, tzinfo=UTC)


def test_daily_partition_path_uses_utc_date_with_patched_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(partitions, "datetime", FakeDatetime)

    result = partitions.daily_partition_path(BASE)

    assert result == BASE / "date=2026-10-30"


def test_daily_partition_path_uses_injected_now() -> None:
    result = partitions.daily_partition_path(BASE, now=FIXED_NOW)

    assert result == BASE / "date=2026-10-30"


def test_experiment_patch_datetime_now(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        datetime,
        "now",
        lambda tz=None: FIXED_NOW,
    )