"""
Verification script to check if all dependencies are installed correctly.
"""

import sys

def check_imports():
    """Check if all required packages can be imported."""
    
    print("🔍 Checking dependencies...\n")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'fitz': 'PyMuPDF',
        'sentence_transformers': 'Sentence Transformers',
        'faiss': 'FAISS',
        'spacy': 'spaCy',
        'google.genai': 'Google Gemini AI',
        'dotenv': 'python-dotenv',
        'numpy': 'NumPy'
    }
    
    failed = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            failed.append(name)
    
    print()
    
    # Check spaCy model
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model (en_core_web_sm)")
    except OSError:
        print("❌ spaCy model (en_core_web_sm) - NOT DOWNLOADED")
        print("   Run: python -m spacy download en_core_web_sm")
        failed.append("spaCy model")
    
    print()
    
    # Check .env file
    import os
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and gemini_key != "your_gemini_api_key_here":
            print("✅ GEMINI_API_KEY is set")
        else:
            print("⚠️  GEMINI_API_KEY not configured in .env")
            print("   Get your key from: https://aistudio.google.com/app/apikey")
    else:
        print("❌ .env file not found")
        failed.append(".env file")
    
    print()
    
    if failed:
        print(f"❌ Setup incomplete. Missing: {', '.join(failed)}")
        return False
    else:
        print("✅ All dependencies are installed correctly!")
        print("\n🚀 You can now run: streamlit run app.py")
        return True


if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
