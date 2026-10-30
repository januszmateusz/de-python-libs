from datetime import UTC, datetime
from pathlib import Path


def daily_partition_path(base: Path, now: datetime | None = None) -> Path:
    """Ścieżka partycji dziennej według daty UTC: <base>/date=YYYY-MM-DD."""
    current = now if now is not None else datetime.now(UTC)
    utc_date = current.astimezone(UTC).date()
    return base / f"date={utc_date.isoformat()}"
