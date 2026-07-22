"""
Links dataset ingestion entry point.
"""

from src.ingestion.ingest_dataset import ingest_dataset

LINKS_REQUIRED_COLUMNS = [
    "movieId",
    "imdbId",
    "tmdbId",
]


def ingest_links() -> None:
    """Ingest the MovieLens links dataset."""

    ingest_dataset(
        dataset_name="links",
        required_columns=LINKS_REQUIRED_COLUMNS,
    )


if __name__ == "__main__":
    ingest_links()
