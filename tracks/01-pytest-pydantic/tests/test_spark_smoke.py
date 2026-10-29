from __future__ import annotations

import os
from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyspark.sql import SparkSession

pytestmark = [pytest.mark.integration, pytest.mark.slow]


@pytest.fixture(scope="session")
def spark() -> Iterator[SparkSession]:
    """Lokalna sesja Spark na cały przebieg; pomija zależne testy, gdy PySpark nie jest zainstalowany."""
    require_spark = os.getenv("REQUIRE_SPARK") == "1"

    try:
        import pyspark.sql as pyspark_sql
    except ImportError:
        if require_spark:
            pytest.fail(
                "REQUIRE_SPARK=1, ale PySpark nie jest zainstalowany.",
                pytrace=False,
            )
        pytest.skip("PySpark nie jest zainstalowany.")

    session = (
        pyspark_sql.SparkSession.builder.master("local[1]")
        .appName("pytest-flights")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_spark_creates_dataframe_with_three_rows(spark: SparkSession) -> None:
    df = spark.createDataFrame(
        [("LO123", 10), ("LO456", 0), ("FR789", 45)],
        ["flight_number", "delay_minutes"],
    )

    assert df.count() == 3
