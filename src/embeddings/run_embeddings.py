"""
CLI entry point for generating movie embeddings and FAISS index.
"""

from __future__ import annotations

import logging

from src.embeddings.build_embeddings import build_movie_embeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main() -> None:
    build_movie_embeddings()


if __name__ == "__main__":
    main()