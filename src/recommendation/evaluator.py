"""
Evaluation metrics for recommendation engines.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class EvaluationResult:
    """
    Evaluation metrics.
    """

    precision: float
    recall: float
    f1_score: float
    hit_rate: float


class RecommendationEvaluator:
    """
    Offline recommendation evaluator.
    """

    @staticmethod
    def precision_at_k(
        recommended: list[int],
        relevant: set[int],
    ) -> float:
        """
        Compute Precision@K.
        """

        if not recommended:
            return 0.0

        hits = sum(movie in relevant for movie in recommended)

        return hits / len(recommended)

    @staticmethod
    def recall_at_k(
        recommended: list[int],
        relevant: set[int],
    ) -> float:
        """
        Compute Recall@K.
        """

        if not relevant:
            return 0.0

        hits = sum(movie in relevant for movie in recommended)

        return hits / len(relevant)

    @staticmethod
    def f1_score(
        precision: float,
        recall: float,
    ) -> float:
        """
        Compute F1 score.
        """

        if precision + recall == 0:
            return 0.0

        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def hit_rate(
        recommended: list[int],
        relevant: set[int],
    ) -> float:
        """
        Compute Hit Rate.
        """

        return float(any(movie in relevant for movie in recommended))

    def evaluate(
        self,
        recommended: list[int],
        relevant: set[int],
    ) -> EvaluationResult:
        """
        Evaluate recommendations.
        """

        logger.info("Evaluating recommendation quality.")

        precision = self.precision_at_k(
            recommended,
            relevant,
        )

        recall = self.recall_at_k(
            recommended,
            relevant,
        )

        f1 = self.f1_score(
            precision,
            recall,
        )

        hit = self.hit_rate(
            recommended,
            relevant,
        )

        logger.info(
            "Precision=%.3f Recall=%.3f F1=%.3f HitRate=%.3f",
            precision,
            recall,
            f1,
            hit,
        )

        return EvaluationResult(
            precision=precision,
            recall=recall,
            f1_score=f1,
            hit_rate=hit,
        )
