"""
Ratings dataset ingestion entry point.
"""

from src.ingestion.ingest_dataset import ingest_dataset


RATINGS_REQUIRED_COLUMNS = [
    "userId",
    "movieId",
    "rating",
    "timestamp",
]


def ingest_ratings() -> None:
    """Ingest the MovieLens ratings dataset."""

    ingest_dataset(
        dataset_name="ratings",
        required_columns=RATINGS_REQUIRED_COLUMNS,
    )


if __name__ == "__main__":
    ingest_ratings()