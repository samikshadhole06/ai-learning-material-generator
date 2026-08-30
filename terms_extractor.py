from gemini_service import generate_response
import json


def extract_key_terms(context, keywords, number_of_terms=15):
    """
    Extract key terms and their definitions from the study material.
    """

    prompt = f"""You are extracting key terms and definitions from study material.

Extract the {number_of_terms} MOST IMPORTANT terms/concepts with their definitions.

IMPORTANT KEYWORDS (prioritize these):
{", ".join(keywords[:20])}

EXTRACTION GUIDELINES:
- Focus on technical terms, concepts, theories, and important ideas
- Provide clear, concise definitions (1-3 sentences)
- Include both simple and complex terms
- Prioritize terms that appear multiple times or are emphasized
- Order by importance (most important first)

OUTPUT FORMAT:
You MUST respond with a valid JSON array:

[
  {{
    "term": "Term Name",
    "definition": "Clear, concise definition",
    "importance": "high/medium/low"
  }}
]

STUDY MATERIAL:
{context}

Extract {number_of_terms} key terms in JSON format. Respond ONLY with the JSON array."""

    response = generate_response(prompt, temperature=0.4, max_tokens=4000)
    
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
        
        terms = json.loads(cleaned_response)
        return terms
    except:
        # If JSON parsing fails, return empty list
        return []
