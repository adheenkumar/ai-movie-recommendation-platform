import numpy as np

from src.vector_store.faiss_index import build_faiss_index


def test_build_faiss_index():
    embeddings = np.random.rand(10, 384).astype("float32")

    index = build_faiss_index(embeddings)

    assert index.ntotal == 10