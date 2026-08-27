@echo off
echo ================================================================
echo    SIMPLE STREAMLIT APP SETUP
echo ================================================================
echo.

echo Installing packages...
pip install streamlit pymupdf sentence-transformers faiss-cpu spacy google-genai python-dotenv numpy

echo.
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo ================================================================
echo Setup complete!
echo ================================================================
echo.
echo IMPORTANT: Add your Gemini API key to .env file
echo.
echo Opening .env file now...
timeout /t 2 /nobreak >nul
notepad .env

echo.
echo After adding your API key, run:
echo    streamlit run app.py
echo.
pause
