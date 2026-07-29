"""
Movie title search utilities.
"""

from __future__ import annotations

from difflib import get_close_matches

from pyspark.sql import SparkSession

class MovieSearch:

    def __init__(
        self,
        spark: SparkSession,
    ) -> None:

        self.spark = spark

        dataframe = (
            spark.read.parquet(
                "data/gold/movie_metrics.parquet"
            )
        )

        self.movies = (
            dataframe
            .select("title")
            .toPandas()["title"]
            .tolist()
        )

    def find_exact(
            self,
            title: str,
    ) -> str | None:

        title = title.lower()

        for movie in self.movies:

            if movie.lower() == title:
                return movie

        return None

    def find_partial(
            self,
            title: str,
    ) -> list[str]:

        title = title.lower()

        matches = []

        for movie in self.movies:

            if title in movie.lower():
                matches.append(movie)

        return matches[:10]

    def find_closest(
            self,
            title: str,
    ) -> list[str]:

        return get_close_matches(
            title,
            self.movies,
            n=5,
            cutoff=0.5,
        )

    def resolve_title(
            self,
            title: str,
    ) -> tuple[str | None, list[str]]: