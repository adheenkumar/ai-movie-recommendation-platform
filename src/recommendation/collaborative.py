"""
Item-based collaborative filtering recommendation engine.
"""

from __future__ import annotations

from typing import List

import pandas as pd
from pyspark.sql import SparkSession
from sklearn.metrics.pairwise import cosine_similarity

from src.recommendation.config import (
    COLLABORATIVE_FILL_VALUE,
    DEFAULT_TOP_N,
    MINIMUM_VOTES,
)
from src.recommendation.models import (
    MovieRecommendation,
    RecommendationResult,
)
from src.utils.logger import get_logger
from src.utils.paths import GOLD_DATA_DIR, SILVER_DATA_DIR

logger = get_logger(__name__)

RATINGS_PATH = SILVER_DATA_DIR / "ratings.parquet"
MOVIES_PATH = GOLD_DATA_DIR / "movie_metrics.parquet"


class CollaborativeRecommender:
    """
    Item-based collaborative filtering recommender.
    """

    def __init__(
        self,
        spark: SparkSession,
        minimum_votes: int = MINIMUM_VOTES,
    ) -> None:

        self.spark = spark
        self.minimum_votes = minimum_votes

        self.ratings = self._load_ratings()
        self.movies = self._load_movies()

        self._prepare_movies()
        self._prepare_lookup_tables()

        self.ratings_matrix = self._build_ratings_matrix()
        self.similarity_matrix = self._build_similarity_matrix()

        logger.info(
            "Collaborative recommender initialized with %d movies.",
            len(self.movie_ids),
        )

    def _load_ratings(self) -> pd.DataFrame:
        """
        Load ratings dataset.
        """

        logger.info("Loading ratings dataset.")

        ratings = self.spark.read.parquet(str(RATINGS_PATH)).toPandas()

        logger.info(
            "Loaded %d ratings.",
            len(ratings),
        )

        return ratings

    def _load_movies(self) -> pd.DataFrame:
        """
        Load movie metrics dataset.
        """

        logger.info("Loading movie metrics.")

        movies = self.spark.read.parquet(str(MOVIES_PATH)).toPandas()

        logger.info(
            "Loaded %d movies.",
            len(movies),
        )

        return movies

    def _prepare_movies(self) -> None:
        """
        Filter movies and create normalized titles.
        """

        self.movies = self.movies[
            self.movies["ratingCount"] >= self.minimum_votes
        ].reset_index(drop=True)

        self.movies["normalizedTitle"] = self.movies["title"].str.lower().str.strip()

        logger.info(
            "Retained %d movies after filtering.",
            len(self.movies),
        )

    def _prepare_lookup_tables(self) -> None:
        """
        Build lookup dictionaries.
        """

        self.movie_lookup = self.movies.set_index("movieId").to_dict("index")

        self.title_lookup = self.movies.set_index("normalizedTitle")[
            "movieId"
        ].to_dict()

    def _build_ratings_matrix(self) -> pd.DataFrame:
        """
        Build user-item matrix.
        """

        valid_movie_ids = set(self.movie_lookup.keys())

        ratings = self.ratings[self.ratings["movieId"].isin(valid_movie_ids)]

        logger.info("Building ratings matrix.")

        matrix = ratings.pivot_table(
            index="movieId",
            columns="userId",
            values="rating",
            fill_value=COLLABORATIVE_FILL_VALUE,
        )

        self.movie_ids = matrix.index.tolist()

        self.movie_id_to_index = {
            movie_id: index for index, movie_id in enumerate(self.movie_ids)
        }

        logger.info(
            "Ratings matrix shape: %s",
            matrix.shape,
        )

        return matrix

    def _build_similarity_matrix(self):
        """
        Compute cosine similarity matrix.
        """

        logger.info("Computing cosine similarity matrix.")

        return cosine_similarity(self.ratings_matrix)

    def _find_movie_id(
        self,
        movie_title: str,
    ) -> int:
        """
        Locate movie by title.
        """

        normalized = movie_title.lower().strip()

        movie_id = self.title_lookup.get(normalized)

        if movie_id is not None:
            return int(movie_id)

        matches = self.movies[
            self.movies["normalizedTitle"].str.contains(
                normalized,
                regex=False,
            )
        ]

        if matches.empty:
            raise ValueError(f"No movie matching '{movie_title}' was found.")

        return int(matches.iloc[0]["movieId"])

    def _build_recommendation(
        self,
        row: dict,
        score: float,
    ) -> RecommendationResult:
        """
        Convert lookup row into RecommendationResult.
        """

        return RecommendationResult(
            recommendation=MovieRecommendation(
                movie_id=int(row["movieId"]),
                title=row["title"],
                release_year=int(row["releaseYear"]),
                genres=row["genres"],
                rating_count=int(row["ratingCount"]),
                average_rating=float(row["averageRating"]),
                weighted_rating=float(row["weightedRating"]),
                popularity_score=float(row["popularityScore"]),
            ),
            score=float(score),
            source="collaborative",
        )

    def recommend(
        self,
        movie_title: str,
        top_n: int = DEFAULT_TOP_N,
    ) -> List[RecommendationResult]:
        """
        Recommend similar movies.
        """

        movie_id = self._find_movie_id(movie_title)

        movie_index = self.movie_id_to_index.get(movie_id)

        if movie_index is None:
            raise ValueError("Movie has insufficient ratings.")

        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))

        similarity_scores.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        recommendations: List[RecommendationResult] = []

        for index, similarity in similarity_scores:

            if index == movie_index:
                continue

            similar_movie_id = self.movie_ids[index]

            row = self.movie_lookup[similar_movie_id].copy()

            row["movieId"] = similar_movie_id

            recommendations.append(
                self._build_recommendation(
                    row,
                    similarity,
                )
            )

            if len(recommendations) >= top_n:
                break

        logger.info(
            "Generated %d collaborative recommendations for '%s'.",
            len(recommendations),
            movie_title,
        )

        return recommendations
