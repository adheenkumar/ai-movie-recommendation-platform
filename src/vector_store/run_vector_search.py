"""
CLI for semantic movie search.
"""

from __future__ import annotations

import argparse
import logging

from src.vector_store.search import SemanticSearch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Semantic movie search",
    )

    parser.add_argument(
        "--query",
        required=True,
        help="Search query",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    search = SemanticSearch()

    results = search.search(
        args.query,
        args.top_k,
    )

    print()

    for rank, movie in enumerate(results, start=1):
        genres = movie.genres.replace("|", ", ")

        print(
            f"{rank:2}. "
            f"{movie.title}\n"
            f"    Genres: {genres}\n"
            f"    Similarity: {movie.similarity_score:.3f}\n"
        )


if __name__ == "__main__":
    main()
