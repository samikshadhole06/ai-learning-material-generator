from gemini_service import generate_response
import json


def generate_flashcards(context, keywords, number_of_cards=10):
    """
    Generate flashcards for memorization with front/back format.
    """

    prompt = f"""You are creating study flashcards for memorization.

Generate EXACTLY {number_of_cards} flashcards from the provided study material.

IMPORTANT KEYWORDS TO FOCUS ON:
{", ".join(keywords[:20])}

FLASHCARD GUIDELINES:
- Front: A clear question, term, or concept
- Back: Concise answer or explanation (2-4 sentences max)
- Focus on important concepts, definitions, and key facts
- Make them specific and testable
- Use active recall principles

OUTPUT FORMAT:
You MUST respond with a valid JSON array. Each flashcard should be:

[
  {{
    "front": "What is X? or Define Y",
    "back": "Concise explanation or definition"
  }}
]

STUDY MATERIAL:
{context}

Generate {number_of_cards} flashcards in JSON format. Respond ONLY with the JSON array."""

    response = generate_response(prompt, temperature=0.5, max_tokens=4000)
    
    # Try to parse the JSON response
    try:
        # Clean up the response
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        flashcards = json.loads(cleaned_response)
        return flashcards
    except:
        # If JSON parsing fails, return empty list
        return []
