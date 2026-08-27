from gemini_service import generate_response


def generate_quiz(
    context,
    difficulty,
    number_of_questions=5
):

    prompt = f"""
You are an academic question generator.

Generate {number_of_questions}
multiple-choice questions based ONLY
on the provided study material.

DIFFICULTY:
{difficulty}

RULES:

1. Every question must be answerable
   from the provided material.
2. Create exactly four options.
3. Only one option should be correct.
4. Provide the correct answer.
5. Provide a short explanation.
6. Do not use outside information.
7. Do not invent facts.

STUDY MATERIAL:

{context}

Format:

Question 1:
<question>

A. <option>
B. <option>
C. <option>
D. <option>

Correct Answer:
<letter>

Explanation:
<explanation>

Repeat this format for all questions.
"""

    return generate_response(prompt)