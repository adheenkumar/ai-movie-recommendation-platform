"""
Movie dataset ingestion entry point.
"""

from src.ingestion.ingest_dataset import ingest_dataset


MOVIES_REQUIRED_COLUMNS = [
    "movieId",
    "title",
    "genres",
]


def ingest_movies() -> None:
    """Ingest the MovieLens movies dataset."""

    ingest_dataset(
        dataset_name="movies",
        required_columns=MOVIES_REQUIRED_COLUMNS,
    )


if __name__ == "__main__":
    ingest_movies()