"""
Tags dataset ingestion entry point.
"""

from src.ingestion.ingest_dataset import ingest_dataset


TAGS_REQUIRED_COLUMNS = [
    "userId",
    "movieId",
    "tag",
    "timestamp",
]


def ingest_tags() -> None:
    """Ingest the MovieLens tags dataset."""

    ingest_dataset(
        dataset_name="tags",
        required_columns=TAGS_REQUIRED_COLUMNS,
    )


if __name__ == "__main__":
    ingest_tags()