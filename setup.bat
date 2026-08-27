@echo off

REM Setup script for AI Learning Material Generator (Windows)

echo 🚀 Setting up AI Learning Material Generator...
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Download spaCy model
echo 🧠 Downloading spaCy language model...
python -m spacy download en_core_web_sm

REM Create data directory
echo 📁 Creating data directory...
if not exist data mkdir data

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo 📝 Please create .env file and add your GEMINI_API_KEY
    echo    Get your key from: https://aistudio.google.com/app/apikey
) else (
    echo ✅ .env file found
)

echo.
echo ✨ Setup complete!
echo.
echo Next steps:
echo 1. Add your GEMINI_API_KEY to .env file
echo 2. Run: streamlit run app.py
echo.
pause
