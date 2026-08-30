import requests
import json
import time
from config import GEMINI_API_KEY, GEMINI_MODEL


def generate_response(prompt, temperature=0.7, max_tokens=8000, retries=3):
    """
    Send a prompt to Gemini and return the response using REST API.
    Works with new AQ. format API keys (authorization keys).
    Includes retry logic for 503 errors.
    
    Args:
        prompt (str): The prompt to send to Gemini
        temperature (float): Controls randomness (0.0-1.0)
        max_tokens (int): Maximum output tokens (default 8000 for longer responses)
        retries (int): Number of retry attempts for failed requests
        
    Returns:
        str: Generated response text
    """
    
    for attempt in range(retries):
        try:
            # Use the REST API endpoint - try gemini-1.5-flash as fallback
            models_to_try = [GEMINI_MODEL, "gemini-1.5-flash", "gemini-pro"]
            
            for model in models_to_try:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                    
                    # For new AQ. format keys, pass API key in header
                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": GEMINI_API_KEY
                    }
                    
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
                            "maxOutputTokens": max_tokens,
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=payload, timeout=60)
                    
                    # If successful, return the result
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Extract text from response
                        if 'candidates' in result and len(result['candidates']) > 0:
                            return result['candidates'][0]['content']['parts'][0]['text']
                        else:
                            continue  # Try next model
                    
                    # If 503 or 429, retry with exponential backoff
                    elif response.status_code in [503, 429]:
                        if attempt < retries - 1:
                            wait_time = (2 ** attempt) + 1  # Exponential backoff: 2, 5, 9 seconds
                            time.sleep(wait_time)
                            break  # Break inner loop to retry
                        else:
                            continue  # Try next model
                    else:
                        continue  # Try next model
                        
                except requests.exceptions.Timeout:
                    if attempt < retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        return f"Error: Request timed out after {retries} attempts"
                except requests.exceptions.RequestException as e:
                    continue  # Try next model
            
            # If we get here and it's not the last attempt, retry
            if attempt < retries - 1:
                time.sleep(2)
                continue
            else:
                return "Error: Unable to generate response. The AI service is currently experiencing high demand. Please try again in a few moments."
                
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            else:
                error_msg = f"Gemini API Error: {str(e)}"
                print(error_msg)
                return f"Error generating response: {str(e)}"
    
    return "Error: Unable to generate response after multiple attempts. Please try again later."