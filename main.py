
from models.sentence_embeddings import SentenceEmbeddings

if __name__ == '__main__':
    sentences = ["This is an example sentence", "Each sentence is converted"]

    model = SentenceEmbeddings()
    embeddings = model.encode(sentences)
    print(embeddings)
