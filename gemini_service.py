import requests
import json
from config import GEMINI_API_KEY, GEMINI_MODEL


def generate_response(prompt, temperature=0.7):
    """
    Send a prompt to Gemini and return the response using REST API.
    
    Args:
        prompt (str): The prompt to send to Gemini
        temperature (float): Controls randomness (0.0-1.0)
        
    Returns:
        str: Generated response text
    """
    try:
        # Use the REST API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        # Add API key to URL as query parameter
        url_with_key = f"{url}?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 2048,
            }
        }
        
        response = requests.post(url_with_key, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract text from response
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Error: No response generated"
        
    except Exception as e:
        error_msg = f"Gemini API Error: {str(e)}"
        print(error_msg)
        return f"Error generating response: {str(e)}"