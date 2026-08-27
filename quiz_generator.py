from gemini_service import generate_response
import json


def generate_quiz(context, difficulty, number_of_questions=5):
    """
    Generate quiz questions in JSON format for flashcard display.
    """

    prompt = f"""You are an expert question generator creating interactive quiz questions.

Generate EXACTLY {number_of_questions} multiple-choice questions based on the provided study material.

DIFFICULTY: {difficulty}

DIFFICULTY GUIDELINES:
- Easy: Basic recall, definitions, simple concepts
- Medium: Application, understanding, connecting ideas
- Hard: Analysis, evaluation, complex scenarios

REQUIREMENTS:
1. Every question MUST be answerable from the provided material
2. Create EXACTLY 4 options (A, B, C, D)
3. Only ONE option is correct
4. Make distractors (wrong answers) plausible but clearly incorrect
5. Provide a detailed explanation for the correct answer
6. Include why wrong answers are incorrect (if space permits)

OUTPUT FORMAT:
You MUST respond with a valid JSON array. Each question should be an object with this exact structure:

[
  {{
    "question": "Clear, specific question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation of why this answer is correct and what concept it tests."
  }}
]

STUDY MATERIAL:
{context}

Generate {number_of_questions} questions in JSON format. Respond ONLY with the JSON array, no other text."""

    response = generate_response(prompt, temperature=0.6)
    
    # Try to parse the JSON response
    try:
        # Clean up the response - remove markdown code blocks if present
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        questions = json.loads(cleaned_response)
        return questions
    except:
        # If JSON parsing fails, return empty list
        return []