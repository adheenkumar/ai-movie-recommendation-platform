"""
Movie title search utilities.
"""

from __future__ import annotations

from difflib import get_close_matches

from src.utils.logger import get_logger


logger = get_logger(__name__)


class MovieSearch:
    """
    Search and resolve movie titles supported by
    the recommendation engine.
    """

    def __init__(
        self,
        movie_titles: list[str],
    ) -> None:
        """
        Initialize movie search.

        Parameters
        ----------
        movie_titles:
            Titles available to the recommendation
            engine.
        """

        self.movies = movie_titles

        self.normalized_movies = {
            movie.lower().strip(): movie
            for movie in movie_titles
        }

        logger.info(
            "Movie search initialized with %d titles.",
            len(self.movies),
        )

    # --------------------------------------------------
    # Exact Search
    # --------------------------------------------------

    def find_exact(
        self,
        title: str,
    ) -> str | None:
        """
        Find an exact movie title match.
        """

        normalized = (
            title
            .lower()
            .strip()
        )

        return self.normalized_movies.get(
            normalized
        )

    # --------------------------------------------------
    # Partial Search
    # --------------------------------------------------

    def find_partial(
        self,
        title: str,
        limit: int = 10,
    ) -> list[str]:
        """
        Find partial movie title matches ranked
        by relevance.
        """

        normalized = (
            title
            .lower()
            .strip()
        )

        if not normalized:
            return []

        starts_with: list[str] = []
        word_matches: list[str] = []
        contains: list[str] = []

        for movie in self.movies:

            movie_lower = (
                movie
                .lower()
                .strip()
            )

            # Highest relevance:
            # title begins with search term
            if movie_lower.startswith(
                normalized
            ):
                starts_with.append(movie)

            # Medium relevance:
            # search term begins another word
            elif (
                f" {normalized}"
                in movie_lower
            ):
                word_matches.append(movie)

            # Lower relevance:
            # search appears elsewhere
            elif normalized in movie_lower:
                contains.append(movie)

        # Prefer shorter titles when relevance
        # category is identical.
        starts_with.sort(
            key=len
        )

        word_matches.sort(
            key=len
        )

        contains.sort(
            key=len
        )

        matches = (
            starts_with
            + word_matches
            + contains
        )

        return matches[:limit]

    # --------------------------------------------------
    # Fuzzy Search
    # --------------------------------------------------

    def find_fuzzy(
        self,
        title: str,
        limit: int = 10,
        cutoff: float = 0.5,
    ) -> list[str]:
        """
        Find similar movie titles using fuzzy
        string matching.
        """

        normalized = (
            title
            .lower()
            .strip()
        )

        if not normalized:
            return []

        normalized_titles = list(
            self.normalized_movies.keys()
        )

        matches = get_close_matches(
            normalized,
            normalized_titles,
            n=limit,
            cutoff=cutoff,
        )

        return [
            self.normalized_movies[
                match
            ]
            for match in matches
        ]

    # --------------------------------------------------
    # Title Resolution
    # --------------------------------------------------

    def resolve_title(
        self,
        title: str,
        limit: int = 10,
    ) -> tuple[
        str | None,
        list[str],
    ]:
        """
        Resolve user input to an available movie
        title.

        Search order:

        1. Exact match
        2. Partial matches
        3. Fuzzy matches

        Returns
        -------
        tuple[str | None, list[str]]

            Exact title and no suggestions:

                ("Toy Story (1995)", [])

            Or unresolved title with suggestions:

                (
                    None,
                    [
                        "Toy Story (1995)",
                        "Toy Story 2 (1999)",
                    ]
                )
        """

        if not title.strip():
            return None, []

        # ----------------------------------------------
        # Exact Match
        # ----------------------------------------------

        exact_match = self.find_exact(
            title
        )

        if exact_match:

            logger.info(
                "Resolved exact movie title '%s'.",
                exact_match,
            )

            return exact_match, []

        # ----------------------------------------------
        # Partial Match
        # ----------------------------------------------

        partial_matches = (
            self.find_partial(
                title,
                limit=limit,
            )
        )

        if partial_matches:

            logger.info(
                "Found %d partial matches for '%s'.",
                len(partial_matches),
                title,
            )

            return None, partial_matches

        # ----------------------------------------------
        # Fuzzy Match
        # ----------------------------------------------

        fuzzy_matches = (
            self.find_fuzzy(
                title,
                limit=limit,
            )
        )

        if fuzzy_matches:

            logger.info(
                "Found %d fuzzy matches for '%s'.",
                len(fuzzy_matches),
                title,
            )

            return None, fuzzy_matches

        logger.info(
            "No movie matches found for '%s'.",
            title,
        )

        return None, []
