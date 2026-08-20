"""
Ranking utilities for hybrid recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.recommendation.config import HYBRID_WEIGHTS
from src.recommendation.models import (
    MovieRecommendation,
    RecommendationResult,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Internal Model
# ---------------------------------------------------------------------


@dataclass(slots=True)
class ScoreRecord:
    """
    Internal container used while combining
    recommendation results from multiple algorithms.
    """

    recommendation: MovieRecommendation
    scores: dict[str, float] = field(default_factory=dict)
    hybrid_score: float = 0.0


# ---------------------------------------------------------------------
# Merge Results
# ---------------------------------------------------------------------


def merge_candidates(
    records: dict[int, ScoreRecord],
    results: list[RecommendationResult],
) -> None:
    """
    Merge recommendation results into a single score table.

    Parameters
    ----------
    records:
        Dictionary of accumulated recommendation scores.

    results:
        Recommendation results from one algorithm.
    """

    for result in results:

        movie = result.recommendation

        record = records.setdefault(
            movie.movie_id,
            ScoreRecord(recommendation=movie),
        )

        record.scores[result.source] = result.score


# ---------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------


def normalize_scores(
    records: dict[int, ScoreRecord],
) -> None:
    """
    Apply Min-Max normalization independently
    for each recommendation algorithm.

    Only candidates actually returned by an
    algorithm participate in that algorithm's
    normalization.
    """

    for algorithm in HYBRID_WEIGHTS:

        scored_records = [
            record
            for record in records.values()
            if algorithm in record.scores
        ]

        if not scored_records:
            continue

        values = [
            record.scores[algorithm]
            for record in scored_records
        ]

        minimum = min(values)
        maximum = max(values)

        if maximum == minimum:

            for record in scored_records:
                record.scores[algorithm] = 1.0

            continue

        denominator = maximum - minimum

        for record in scored_records:

            value = record.scores[algorithm]

            record.scores[algorithm] = (
                value - minimum
            ) / denominator

# ---------------------------------------------------------------------
# Hybrid Score Calculation
# ---------------------------------------------------------------------


def compute_hybrid_scores(
    records: dict[int, ScoreRecord],
) -> None:
    """
    Compute weighted hybrid scores.
    """

    for record in records.values():

        record.hybrid_score = sum(
            record.scores.get(algorithm, 0.0) * weight
            for algorithm, weight in HYBRID_WEIGHTS.items()
        )


# ---------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------


def rank_recommendations(
    content: list[RecommendationResult],
    collaborative: list[RecommendationResult],
    popularity: list[RecommendationResult],
    semantic: list[RecommendationResult],
) -> list[RecommendationResult]:
    """
    Combine multiple recommendation sources into
    a single ranked hybrid recommendation list.

    Parameters
    ----------
    content:
        Content-based recommendations.

    collaborative:
        Collaborative filtering recommendations.

    popularity:
        Popularity-based recommendations.

    semantic:
        Semantic search recommendations.

    Returns
    -------
    list[RecommendationResult]
        Hybrid ranked recommendations.
    """

    logger.info("Combining recommendation results.")

    records: dict[int, ScoreRecord] = {}

    merge_candidates(records, content)
    merge_candidates(records, collaborative)
    merge_candidates(records, popularity)
    merge_candidates(records, semantic)

    logger.info(
        "Merged %d unique candidate movies.",
        len(records),
    )

    if not records:
        logger.warning("No recommendation candidates were provided.")
        return []

    normalize_scores(records)

    compute_hybrid_scores(records)

    ranked = sorted(
        records.values(),
        key=lambda record: record.hybrid_score,
        reverse=True,
    )

    logger.info(
        "Generated %d hybrid recommendations.",
        len(ranked),
    )

    return [
        RecommendationResult(
            recommendation=record.recommendation,
            score=record.hybrid_score,
            source="hybrid",
        )
        for record in ranked
    ]
