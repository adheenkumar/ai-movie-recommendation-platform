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
from src.dashboard.components.movie_card import (
    render as render_movie_card,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


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

        # ----------------------------------------------
        # Session State
        # ----------------------------------------------

        if "movie_suggestions" not in st.session_state:
            st.session_state.movie_suggestions = []

        if "movie_results" not in st.session_state:
            st.session_state.movie_results = None

        movie_title = st.text_input(
            "Movie Title",
            placeholder="Example: Toy Story",
        )

        if st.button(
                "🎯 Recommend Movies",
                use_container_width=True,
        ):

            if not movie_title.strip():

                st.warning(
                    "Please enter a movie title."
                )

            else:

                try:

                    with st.spinner(
                            "Searching movie..."
                    ):

                        recommendations, suggestions = (
                            service.recommend_by_movie(
                                movie_title=movie_title,
                            )
                        )

                    # Clear previous results
                    st.session_state.movie_results = None
                    st.session_state.movie_suggestions = []

                    if recommendations:

                        st.session_state.movie_results = recommendations

                    elif suggestions:

                        st.session_state.movie_suggestions = suggestions

                    else:

                        st.info(
                            "No matching movies were found."
                        )

                except Exception as exc:
                    logger.exception(
                        "Failed to generate recommendations: %s",
                        exc,
                    )

                    st.error(
                        "Failed to generate recommendations."
                    )

        # ----------------------------------------------
        # Show Suggestions
        # ----------------------------------------------

        if st.session_state.movie_suggestions:

            st.warning(
                "No exact match found."
            )

            selected_movie = st.selectbox(
                "Did you mean...",
                st.session_state.movie_suggestions,
                key="movie_selector",
            )

            if st.button(
                    "🎬 Recommend Selected Movie",
                    use_container_width=True,
            ):
                try:
                    recommendations, _ = service.recommend_by_movie(
                        selected_movie,
                        top_n=10,
                    )

                    if recommendations:
                        st.success(
                            f"Showing {len(recommendations)} recommendations "
                            f"based on **{selected_movie}**."
                        )

                        render_recommendation_table(
                            recommendations,
                        )

                    else:
                        st.info(
                            f"No recommendations were found for "
                            f"**{selected_movie}**."
                        )

                except ValueError as exc:
                    st.warning(str(exc))

                except Exception as exc:
                    logger.exception(
                        "Something went wrong while generating recommendations: %s",
                        exc,
                    )

                    st.error(
                        "Something went wrong while generating recommendations."
                    )

        # ----------------------------------------------
        # Show Recommendations
        # ----------------------------------------------

        if st.session_state.movie_results:

            recommendations = st.session_state.movie_results

            st.success(
                f"Found {len(recommendations)} recommendations."
            )

            st.subheader(
                "🎬 Top Recommendations"
            )

            # Show top 4 recommendations as cards
            for index in range(
                    0,
                    min(4, len(recommendations)),
                    2,
            ):

                col1, col2 = st.columns(2)

                with col1:

                    render_movie_card(
                        recommendations[index],
                        rank=index + 1,
                    )

                if index + 1 < min(
                        4,
                        len(recommendations),
                ):
                    with col2:
                        render_movie_card(
                            recommendations[index + 1],
                            rank=index + 2,
                        )

            # Detailed results
            with st.expander(
                    "📋 View All Recommendation Details",
                    expanded=False,
            ):

                render_recommendation_table(
                    recommendations,
                )

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

                    st.markdown(explanation)

                    st.divider()

                    st.subheader(
                        "Recommended Movies"
                    )

                    render_recommendation_table(
                        recommendations,
                    )

                except Exception as exc:
                    logger.exception(
                        "Failed to generate AI recommendations.: %s",
                        exc,
                    )

                    st.error(
                        "Failed to generate AI recommendations."
                    )
