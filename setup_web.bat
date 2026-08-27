@echo off

REM Setup script for React + FastAPI Web Application (Windows)

echo 🚀 Setting up AI Learning Material Generator Web App...
echo.

REM ============================================
REM BACKEND SETUP
REM ============================================
echo 📦 Setting up Backend...
echo.

cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Download spaCy model
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm

REM Copy Python modules from parent directory
echo Copying Python modules...
copy ..\config.py .
copy ..\pdf_processor.py .
copy ..\text_processor.py .
copy ..\embeddings.py .
copy ..\vector_store.py .
copy ..\notes_generator.py .
copy ..\quiz_generator.py .
copy ..\rag.py .
copy ..\gemini_service.py .

REM Check .env file
if not exist .env (
    echo ⚠️  .env file not found in backend/
    echo 📝 Please add your GEMINI_API_KEY to backend/.env
) else (
    echo ✅ .env file found
)

cd ..

echo.
echo ✅ Backend setup complete!
echo.

REM ============================================
REM FRONTEND SETUP
REM ============================================
echo 📦 Setting up Frontend...
echo.

cd frontend

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found!
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo npm version:
npm --version
echo.

REM Install npm dependencies
echo Installing npm dependencies...
call npm install

cd ..

echo.
echo ✅ Frontend setup complete!
echo.

REM ============================================
REM FINAL INSTRUCTIONS
REM ============================================
echo ════════════════════════════════════════════════════════
echo ✨ Setup Complete!
echo ════════════════════════════════════════════════════════
echo.
echo Next steps:
echo.
echo 1. Add your GEMINI_API_KEY to backend\.env
echo    Get key from: https://aistudio.google.com/app/apikey
echo.
echo 2. Start the backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. Start the frontend (Terminal 2):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open browser: http://localhost:3000
echo.
echo ════════════════════════════════════════════════════════
pause
