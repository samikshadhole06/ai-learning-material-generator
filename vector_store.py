import faiss
import numpy as np


def create_vector_store(embeddings):

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


def search_vector_store(
    index,
    query_embedding,
    chunks,
    top_k=4
):

    query_embedding = np.asarray(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if index_id != -1:

            results.append({
                "text": chunks[index_id],
                "score": float(distance)
            })

    return results