from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


model = SentenceTransformer(
    EMBEDDING_MODEL
)


def generate_embeddings(chunks):
    """
    Convert text chunks into numerical embeddings.
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings


def generate_query_embedding(query):
    """
    Convert a user question into an embedding.
    """

    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    return embedding[0]
