from src.vector_store.search import SemanticSearch


def test_semantic_search_returns_results():
    search = SemanticSearch()

    results = search.search(
        "animated toy movie",
        top_k=5,
    )

    assert len(results) == 5

    assert results[0].title
