"""
Tests for dataset quality profiling.
"""

import pandas as pd

from src.ingestion.quality_report import generate_quality_report


def test_generate_quality_report() -> None:
    """Verify quality metrics are calculated correctly."""

    dataframe = pd.DataFrame(
        {
            "movieId": [1, 2, 2, 3],
            "title": [
                "Movie A",
                "Movie B",
                "Movie B",
                None,
            ],
        }
    )

    report = generate_quality_report(
        dataset_name="test_movies",
        dataframe=dataframe,
    )

    assert report["dataset"] == "test_movies"
    assert report["row_count"] == 4
    assert report["column_count"] == 2
    assert report["duplicate_rows"] == 1
    assert report["total_null_values"] == 1
    assert report["null_counts"]["movieId"] == 0
    assert report["null_counts"]["title"] == 1
    assert report["data_types"]["movieId"] == "int64"
    assert report["data_types"]["title"] in {"object", "str", "string"}