"""
Prompt builder for movie recommendations.
"""

from __future__ import annotations

from src.recommendation.models import RecommendationResult


class PromptBuilder:
    """
    Builds prompts for the LLM using recommendation results.
    """

    @staticmethod
    def build(
        user_query: str,
        recommendations: list[RecommendationResult],
    ) -> str:
        """
        Build a prompt for the LLM.

        Parameters
        ----------
        user_query:
            Natural language query from the user.

        recommendations:
            Ranked recommendations from the hybrid recommender.

        Returns
        -------
        str
            Prompt sent to the LLM.
        """

        movie_lines: list[str] = []

        for index, result in enumerate(recommendations, start=1):
            movie = result.recommendation

            movie_lines.append(
                (
                    f"{index}. {movie.title} ({movie.release_year})\n"
                    f"Genres: {movie.genres.replace('|', ', ')}\n"
                    f"Average Rating: {movie.average_rating:.2f}\n"
                    f"Hybrid Score: {result.score:.3f}\n"
                    f"Recommendation Source: {result.source}\n"
                )
            )

        movies_text = "\n".join(movie_lines)

        return f"""
You are an AI movie recommendation assistant.

The user asked:

"{user_query}"

The recommendation engine returned these movies:

{movies_text}

You must answer using ONLY the movies listed above.

Rules:

- Do NOT recommend any movie that is not listed.
- Do NOT invent titles.
- Do NOT replace any movie with another movie.
- Explain why each movie matches using ONLY the information provided below.
- Do not describe plots, characters, or scenes unless they are explicitly included in the movie information.
- If there is insufficient information, simply say that the movie was selected because its genres and hybrid recommendation score closely matched the user's request.
- If fewer than 3 movies are listed, only discuss those movies.

For EACH movie listed:

- Use the movie title as a heading.
- Write 2–3 sentences explaining why it matches.
- Treat each movie independently.
- Do not combine multiple movies into a single explanation.
"""
