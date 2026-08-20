"""
Configuration for recommendation engines.
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Recommendation Defaults
# ---------------------------------------------------------------------

DEFAULT_TOP_N: int = 10

MINIMUM_VOTES: int = 10

# ---------------------------------------------------------------------
# Hybrid Weights
# ---------------------------------------------------------------------

CONTENT_WEIGHT: float = 0.40

COLLABORATIVE_WEIGHT: float = 0.40

POPULARITY_WEIGHT: float = 0.20

SEMANTIC_WEIGHT: float = 0.80

HYBRID_WEIGHTS: dict[str, float] = {
    "content": CONTENT_WEIGHT,
    "collaborative": COLLABORATIVE_WEIGHT,
    "popularity": POPULARITY_WEIGHT,
    "semantic": SEMANTIC_WEIGHT,
}

# ---------------------------------------------------------------------
# Content-Based Recommendation
# ---------------------------------------------------------------------

CONTENT_STOP_WORDS: str = "english"

# ---------------------------------------------------------------------
# Collaborative Filtering
# ---------------------------------------------------------------------

COLLABORATIVE_FILL_VALUE: float = 0.0
