"""
Recommendations page for the AI Movie Recommendation Platform.
"""

from __future__ import annotations

import streamlit as st

from src.dashboard.services.recommendation_service import (
    RecommendationService,
)
from src.dashboard.components.recommendation_table import (
    render as render_recommendation_table,
)


def render(
    service: RecommendationService,
) -> None:
    """
    Render the recommendations page.
    """

    st.title("🎯 Movie Recommendations")

    st.markdown(
        """
        Generate recommendations using either a movie title
        or a natural language query.
        """
    )

    tab_movie, tab_ai = st.tabs(
        [
            "🎬 Movie Title",
            "🤖 AI Search",
        ]
    )

    # --------------------------------------------------
    # Movie Recommendation
    # --------------------------------------------------

    with tab_movie:

        movie_title = st.text_input(
            "Movie Title",
            placeholder="Example: Toy Story",
        )

        if st.button(
            "Recommend Movies",
            key="movie_button",
        ):

            if not movie_title.strip():
                st.warning(
                    "Please enter a movie title."
                )
            else:

                try:

                    recommendations = (
                        service.recommend_by_movie(
                            movie_title=movie_title,
                        )
                    )

                    if recommendations:
                        st.success(
                            f"Found {len(recommendations)} recommendations."
                        )

                        render_recommendation_table(
                            recommendations,
                        )

                    else:
                        st.info(
                            "No recommendations found."
                        )

                except Exception as exc:
                    st.error(str(exc))

    # --------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------

    with tab_ai:

        query = st.text_area(
            "Describe what you want",
            placeholder=(
                "Funny animated movies with toys"
            ),
        )

        if st.button(
            "Ask AI",
            key="ai_button",
        ):

            if not query.strip():
                st.warning(
                    "Please enter a search query."
                )

            else:

                try:

                    explanation, recommendations = (
                        service.recommend_by_query(
                            query=query,
                        )
                    )

                    st.subheader(
                        "🤖 AI Explanation"
                    )

                    st.write(explanation)

                    st.divider()

                    st.subheader(
                        "Recommended Movies"
                    )

                    render_recommendation_table(
                        recommendations,
                    )

                except Exception as exc:
                    st.error(str(exc))