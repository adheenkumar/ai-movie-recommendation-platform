from src.embeddings.embedding_model import get_embedding_model


def test_embedding_model_loads():
    model = get_embedding_model()

    assert model is not None
    assert model.get_embedding_dimension() == 384