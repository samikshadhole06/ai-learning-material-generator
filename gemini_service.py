import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def generate_response(prompt, temperature=0.7):
    """
    Send a prompt to Gemini and return the response.
    
    Args:
        prompt (str): The prompt to send to Gemini
        temperature (float): Controls randomness (0.0-1.0)
        
    Returns:
        str: Generated response text
    """
    try:
        # Create model instance
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': temperature,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        return response.text
        
    except Exception as e:
        error_msg = f"Gemini API Error: {str(e)}"
        print(error_msg)
        return f"Error generating response: {str(e)}"