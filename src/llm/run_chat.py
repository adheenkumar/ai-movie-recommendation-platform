"""
Interactive AI movie recommendation chat.
"""

from __future__ import annotations

from src.llm.recommendation_chat import RecommendationChat
from src.spark_jobs.spark_session import create_spark_session


def main() -> None:
    """
    Launch the AI recommendation chat.
    """

    spark = create_spark_session(
        app_name="AI Recommendation Chat",
    )

    assistant = RecommendationChat(spark)

    print("=" * 60)
    print("🤖 AI Movie Recommendation Assistant")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        print("\nAssistant:\n")

        response = assistant.chat(
            query=query,
            top_n=10,
        )

        print(response)
        print()

    spark.stop()


if __name__ == "__main__":
    main()