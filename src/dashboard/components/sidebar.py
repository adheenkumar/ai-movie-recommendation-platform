"""
Sidebar component for dashboard navigation.
"""

from __future__ import annotations

import streamlit as st


PAGES = {
    "🏠 Home": "home",
    "🎯 Recommendations": "recommendations",
    "📊 Analytics": "analytics",
}


def render() -> str:
    """
    Render the dashboard sidebar.

    Returns
    -------
    str
        Selected page identifier.
    """

    with st.sidebar:
        st.title("🎬 Movie AI")

        st.caption(
            "AI Movie Recommendation Platform"
        )

        st.divider()

        page = st.radio(
            "Navigation",
            options=list(PAGES.keys()),
        )

        st.divider()

        st.caption("Version 1.0")

    return PAGES[page]
