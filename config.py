import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# For Streamlit Cloud, check Streamlit secrets
try:
    import streamlit as st
    if not GEMINI_API_KEY and hasattr(st, 'secrets'):
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)
except:
    pass

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "⚠️ GEMINI_API_KEY not found!\n\n"
        "Please add your API key in Streamlit Cloud:\n"
        "1. Go to your app settings\n"
        "2. Click 'Secrets'\n"
        "3. Add: GEMINI_API_KEY = 'your_actual_key'\n\n"
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
GEMINI_MODEL = "gemini-3.6-flash"