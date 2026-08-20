"""
AI-powered recommendation chat.
"""

from __future__ import annotations

from pyspark.sql import SparkSession

from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.recommendation.hybrid import HybridRecommender
from src.recommendation.models import RecommendationResult
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationChat:
    """
    AI-powered movie recommendation assistant.
    """

    def __init__(
        self,
        spark: SparkSession,
    ) -> None:
        """
        Initialize the recommendation chat.
        """

        self.recommender = HybridRecommender(spark)
        self.llm = OllamaClient()

        logger.info(
            "Recommendation chat initialized."
        )

    def chat(
            self,
            query: str,
            top_n: int = 10,
    ) -> str:
        """
        Convenience method.

        Generates recommendations and then explains them.
        """

        logger.info(
            "Processing user query: %s",
            query,
        )

        try:
            recommendations = self.recommender.recommend(
                semantic_query=query,
                top_n=top_n,
            )

            if not recommendations:
                logger.warning(
                    "No recommendations found for query: %s",
                    query,
                )
                return (
                    "I couldn't find any movies matching your request."
                )

            return self.explain(
                query=query,
                recommendations=recommendations,
            )

        except Exception:
            logger.exception(
                "Failed to generate AI recommendations."
            )

            return (
                "Sorry, something went wrong while generating recommendations."
            )

        finally:
            logger.info(
                "Recommendation chat completed."
            )

    def explain(
            self,
            query: str,
            recommendations: list[RecommendationResult],
    ) -> str:
        """
        Generate an AI explanation from existing recommendations.
        """

        logger.info(
            "Generating AI explanation."
        )

        try:
            prompt = PromptBuilder.build(
                user_query=query,
                recommendations=recommendations,
            )

            return self.llm.generate(prompt)


        except Exception as exc:

            logger.exception(

                "Failed to generate AI explanation."

            )

            return (

                f"AI explanation failed: "

                f"{type(exc).__name__}: {exc}"

            )

        finally:
            logger.info(
                "AI explanation completed."
            )
