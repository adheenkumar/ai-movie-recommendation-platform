"""
Recommendation table component.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.recommendation.models import RecommendationResult


def render(
    recommendations: list[RecommendationResult],
) -> None:
    """
    Render a recommendation table.
    """

    if not recommendations:
        st.info("No recommendations available.")
        return

    rows = []

    for result in recommendations:

        movie = result.recommendation

        rows.append(
            {
                "Title": movie.title,
                "Year": movie.release_year,
                "Genres": movie.genres.replace("|", ", "),
                "Average Rating": round(movie.average_rating, 2),
                "Ratings": movie.rating_count,
                "Source": result.source,
                "Recommendation Score": round(result.score, 3),
            }
        )

    dataframe = pd.DataFrame(rows)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )
