import pytest

from models.sentence_embeddings import SentenceEmbeddings


@pytest.fixture(scope="session")
def embedding_model(
):
    return SentenceEmbeddings()


def test_encode(embedding_model):
    sentences = ["Hello, how are you?", "I am doing well, thank you!"]
    embeddings = embedding_model.encode(sentences)
    assert embeddings.shape == (2, 384)
    assert embeddings[0].shape == (384,)
    assert embeddings[1].shape == (384,)
    assert embeddings[0].tolist() != embeddings[1].tolist()
    assert embeddings[0].tolist() == embeddings[0].tolist()
    assert embeddings[1].tolist() == embeddings[1].tolist()
    assert embeddings[0].tolist() != embeddings[1].tolist()
