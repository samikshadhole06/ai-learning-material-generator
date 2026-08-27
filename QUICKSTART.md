# Quick Start Guide

Get your AI Learning Material Generator up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for downloading models and API access)

## Setup Instructions

### Option 1: Automated Setup (Recommended)

#### Windows
```bash
# Run the setup script
setup.bat
```

#### macOS/Linux
```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

#### 4. Configure Gemini API

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Open the `.env` file
3. Replace `your_gemini_api_key_here` with your actual API key:

```
GEMINI_API_KEY=AIzaSyXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
```

## Verify Installation

Run the verification script:
```bash
python verify_setup.py
```

If all checks pass ✅, you're ready to go!

## Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Test the Components

Test individual components:
```bash
# Test Gemini API
python test_gemini.py

# Test all components
python test_all.py
```

## Usage

1. **Upload PDF**: Click "Browse files" and select your study material
2. **Wait**: The app processes the PDF (extracts text, creates embeddings)
3. **Customize**: Set your learning level and study mode in the sidebar
4. **Use Features**:
   - 📝 **Smart Notes**: Generate summarized notes
   - 🧠 **Quiz**: Create practice questions with answers
   - 💬 **Ask AI**: Get answers to your questions

## Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify you've replaced the placeholder with your actual API key
- API key should start with `AIza`

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### "ImportError" or missing packages
```bash
pip install -r requirements.txt
```

### FAISS installation issues
```bash
pip uninstall faiss-cpu
pip install faiss-cpu --no-cache-dir
```

### PDF not processing
- Ensure the PDF contains readable text (not just images)
- Try a different PDF
- Check file size (very large PDFs may take longer)

## Tips

- Use clear, well-formatted PDFs for best results
- Smaller PDFs (< 50 pages) process faster
- The AI only uses information from your uploaded PDF
- You can download generated notes and quizzes
- Adjust learning preferences for personalized content

## Need Help?

- Check the full README.md for detailed documentation
- Verify all components with `python test_all.py`
- Check `python verify_setup.py` output for missing dependencies

## Next Steps

Once everything works:
1. Try different learning levels and study modes
2. Experiment with quiz difficulties
3. Ask various questions to test the RAG system
4. Download and save your generated materials

Happy learning! 🎓
