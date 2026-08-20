"""
Content-based recommendation engine.
"""

from __future__ import annotations

from typing import List

import pandas as pd
from pyspark.sql import SparkSession
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.recommendation.config import (
    CONTENT_STOP_WORDS,
    DEFAULT_TOP_N,
    MINIMUM_VOTES,
)
from src.recommendation.models import (
    MovieRecommendation,
    RecommendationResult,
)
from src.utils.logger import get_logger
from src.utils.paths import GOLD_DATA_DIR


logger = get_logger(__name__)

RECOMMENDATION_FEATURES_PATH = (
    GOLD_DATA_DIR / "recommendation_features.parquet"
)


class ContentBasedRecommender:
    """
    TF-IDF based movie recommender.
    """

    def __init__(
        self,
        spark: SparkSession,
        minimum_votes: int = MINIMUM_VOTES,
    ) -> None:

        self.spark = spark
        self.minimum_votes = minimum_votes

        self.movies = self._load_movies()

        self._prepare_movies()

        self.vectorizer = self._build_vectorizer()

        self.similarity_matrix = (
            self._build_similarity_matrix()
        )

        logger.info(
            "Content recommender initialized with %d movies.",
            len(self.movies),
        )

    # --------------------------------------------------
    # Data Loading
    # --------------------------------------------------

    def _load_movies(self) -> pd.DataFrame:
        """
        Load recommendation features.
        """

        logger.info(
            "Loading recommendation features."
        )

        return (
            self.spark
            .read
            .parquet(
                str(RECOMMENDATION_FEATURES_PATH)
            )
            .toPandas()
        )

    # --------------------------------------------------
    # Data Preparation
    # --------------------------------------------------

    def _prepare_movies(self) -> None:
        """
        Filter movies and create lookup columns.
        """

        self.movies = self.movies[
            self.movies["ratingCount"]
            >= self.minimum_votes
        ].reset_index(drop=True)

        self.movies["normalizedTitle"] = (
            self.movies["title"]
            .str.lower()
            .str.strip()
        )

        logger.info(
            "Retained %d movies after vote filtering.",
            len(self.movies),
        )

    # --------------------------------------------------
    # Available Movie Titles
    # --------------------------------------------------

    def get_available_titles(
        self,
    ) -> list[str]:
        """
        Return titles available to the recommendation
        engine.

        Returns
        -------
        list[str]
            Movie titles that passed the recommendation
            engine's minimum vote filter.
        """

        return self.movies["title"].tolist()

    # --------------------------------------------------
    # TF-IDF
    # --------------------------------------------------

    def _build_vectorizer(
        self,
    ) -> TfidfVectorizer:
        """
        Build TF-IDF vectorizer.
        """

        logger.info(
            "Building TF-IDF matrix."
        )

        vectorizer = TfidfVectorizer(
            stop_words=CONTENT_STOP_WORDS,
        )

        self.tfidf_matrix = (
            vectorizer.fit_transform(
                self.movies["contentText"]
            )
        )

        return vectorizer

    # --------------------------------------------------
    # Similarity Matrix
    # --------------------------------------------------

    def _build_similarity_matrix(self):
        """
        Compute cosine similarity matrix.
        """

        logger.info(
            "Computing cosine similarity matrix."
        )

        return cosine_similarity(
            self.tfidf_matrix,
            self.tfidf_matrix,
        )

    # --------------------------------------------------
    # Movie Lookup
    # --------------------------------------------------

    def _find_movie_index(
        self,
        movie_title: str,
    ) -> int:
        """
        Locate a movie by title.
        """

        normalized = (
            movie_title
            .lower()
            .strip()
        )

        matches = self.movies[
            self.movies[
                "normalizedTitle"
            ].str.contains(
                normalized,
                regex=False,
            )
        ]

        if matches.empty:

            raise ValueError(
                f"No movie matching "
                f"'{movie_title}' was found."
            )

        return int(
            matches.index[0]
        )

    # --------------------------------------------------
    # Recommendation Builder
    # --------------------------------------------------

    def _build_recommendation(
        self,
        row: pd.Series,
        score: float,
    ) -> RecommendationResult:
        """
        Convert dataframe row into
        RecommendationResult.
        """

        return RecommendationResult(
            recommendation=MovieRecommendation(
                movie_id=int(
                    row.movieId
                ),
                title=row.title,
                release_year=int(
                    row.releaseYear
                ),
                genres=row.genres,
                rating_count=int(
                    row.ratingCount
                ),
                average_rating=float(
                    row.averageRating
                ),
                weighted_rating=float(
                    row.weightedRating
                ),
                popularity_score=float(
                    row.popularityScore
                ),
            ),
            score=float(score),
            source="content",
        )

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    def recommend(
        self,
        movie_title: str,
        top_n: int = DEFAULT_TOP_N,
    ) -> List[RecommendationResult]:
        """
        Recommend similar movies.
        """

        movie_index = (
            self._find_movie_index(
                movie_title
            )
        )

        scores = list(
            enumerate(
                self.similarity_matrix[
                    movie_index
                ]
            )
        )

        scores.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        recommendations: List[
            RecommendationResult
        ] = []

        for index, similarity in scores:

            if index == movie_index:
                continue

            row = self.movies.iloc[index]

            recommendations.append(
                self._build_recommendation(
                    row,
                    similarity,
                )
            )

            if (
                len(recommendations)
                >= top_n
            ):
                break

        logger.info(
            "Generated %d content-based "
            "recommendations for '%s'.",
            len(recommendations),
            movie_title,
        )

        return recommendations
