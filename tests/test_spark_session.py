"""
Tests for centralized Spark session configuration.
"""

from src.spark_jobs.spark_session import create_spark_session


def test_create_spark_session() -> None:
    """Verify Spark session configuration."""

    spark = create_spark_session("Spark Session Test")

    try:
        assert spark.version.startswith("3.5")
        assert spark.conf.get("spark.sql.session.timeZone") == "UTC"
        assert spark.conf.get("spark.sql.parquet.compression.codec") == "snappy"
        assert spark.conf.get("spark.sql.shuffle.partitions") == "4"
    finally:
        spark.stop()
