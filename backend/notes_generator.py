from gemini_service import generate_response


def generate_notes(
    context,
    keywords,
    learning_level,
    study_mode
):

    prompt = f"""
You are an academic learning assistant.

Generate concise, exam-oriented study notes
from the provided study material.

STUDENT LEVEL:
{learning_level}

STUDY MODE:
{study_mode}

IMPORTANT KEYWORDS:
{", ".join(keywords)}

STRICT RULES:

1. Use ONLY the provided study material.
2. Do not introduce outside information.
3. Do not invent facts.
4. Keep important definitions.
5. Keep important concepts.
6. Keep important examples present in the material.
7. Remove unnecessary repetition.
8. Use headings and bullet points.
9. Make the content easy to revise.
10. Focus on exam-relevant information.

STUDY MATERIAL:

{context}

Generate the final study notes.
"""

    return generate_response(prompt)