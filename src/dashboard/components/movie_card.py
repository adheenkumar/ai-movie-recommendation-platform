"""
Reusable movie card component for recommendation results.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render(
    result: Any,
    rank: int | None = None,
) -> None:
    """
    Render a recommendation result as a movie card.

    Parameters
    ----------
    result:
        RecommendationResult containing the recommended movie,
        recommendation score, and recommendation source.

    rank:
        Optional ranking position.
    """

    movie = result.recommendation

    score = getattr(
        result,
        "score",
        None,
    )

    source = getattr(
        result,
        "source",
        "Unknown",
    )

    title = getattr(
        movie,
        "title",
        "Unknown Movie",
    )

    release_year = getattr(
        movie,
        "release_year",
        None,
    )

    genres = getattr(
        movie,
        "genres",
        "Unknown",
    )

    average_rating = getattr(
        movie,
        "average_rating",
        None,
    )

    rating_count = getattr(
        movie,
        "rating_count",
        None,
    )

    # Format title
    if release_year and f"({release_year})" not in title:
        display_title = f"{title} ({release_year})"
    else:
        display_title = title

    # Format genres
    genres_display = str(genres).replace(
        "|",
        ", ",
    )

    # Format recommendation source
    source_display = (
        str(source).title()
        if source
        else "Unknown"
    )

    # Render card
    with st.container(border=True):

        if rank is not None:
            st.markdown(
                f"### #{rank} 🎬 {display_title}"
            )
        else:
            st.markdown(
                f"### 🎬 {display_title}"
            )

        st.caption(
            f"🎭 {genres_display}"
        )

        col1, col2, col3 = st.columns(3)

        # Rating
        if average_rating is not None:
            col1.metric(
                "⭐ Rating",
                f"{float(average_rating):.2f}",
            )
        else:
            col1.metric(
                "⭐ Rating",
                "N/A",
            )

        # Rating count
        if rating_count is not None:
            col2.metric(
                "👥 Ratings",
                f"{int(rating_count):,}",
            )
        else:
            col2.metric(
                "👥 Ratings",
                "N/A",
            )

        # Recommendation score
        if score is not None:
            col3.metric(
                "🎯 Match Score",
                f"{float(score):.3f}",
            )
        else:
            col3.metric(
                "🎯 Match Score",
                "N/A",
            )

        st.caption(
            f"Recommendation source: {source_display}"
        )
