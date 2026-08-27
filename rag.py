from embeddings import (
    generate_query_embedding
)

from vector_store import (
    search_vector_store
)

from gemini_service import (
    generate_response
)


def ask_question(
    question,
    index,
    chunks,
    top_k=4
):

    # Convert question into embedding
    query_embedding = (
        generate_query_embedding(
            question
        )
    )

    # Search FAISS
    results = search_vector_store(
        index,
        query_embedding,
        chunks,
        top_k
    )

    # If nothing relevant was retrieved
    if not results:

        return (
            "I could not find this information "
            "in the uploaded material.",
            []
        )

    # Combine retrieved chunks
    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY
the study material provided below.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer cannot be found in the
   material, say:

"I could not find this information in the
uploaded material."

4. Keep the answer clear and concise.
5. Explain using information from the material.

STUDY MATERIAL:

{context}

STUDENT QUESTION:

{question}

ANSWER:
"""

    answer = generate_response(
        prompt
    )

    return answer, results