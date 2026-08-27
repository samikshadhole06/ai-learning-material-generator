import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "GEMINI_API_KEY not found or not configured. "
        "Please add your actual API key to the .env file. "
        "Get your key from: https://aistudio.google.com/app/apikey"
    )

# Embedding model configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Text chunking configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# RAG configuration
TOP_K = 4

# Gemini model configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"