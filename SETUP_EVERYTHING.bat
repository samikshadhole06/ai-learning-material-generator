@echo off
SETLOCAL EnableDelayedExpansion

echo ================================================================
echo    AI LEARNING MATERIAL GENERATOR - COMPLETE SETUP
echo ================================================================
echo.

REM ============================================
REM Check Python
REM ============================================
echo [1/8] Checking Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM ============================================
REM Setup Backend
REM ============================================
echo [2/8] Setting up backend...
cd backend

REM Create venv
echo Creating virtual environment...
python -m venv venv

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install packages
echo Installing Python packages (this may take 2-3 minutes)...
pip install fastapi uvicorn[standard] python-multipart pymupdf sentence-transformers faiss-cpu spacy google-genai python-dotenv numpy --quiet

REM Download spaCy model
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm --quiet

REM Copy Python files
echo Copying Python modules...
copy ..\config.py . >nul 2>&1
copy ..\pdf_processor.py . >nul 2>&1
copy ..\text_processor.py . >nul 2>&1
copy ..\embeddings.py . >nul 2>&1
copy ..\vector_store.py . >nul 2>&1
copy ..\notes_generator.py . >nul 2>&1
copy ..\quiz_generator.py . >nul 2>&1
copy ..\rag.py . >nul 2>&1
copy ..\gemini_service.py . >nul 2>&1

echo ✓ Backend setup complete!
echo.

cd ..

REM ============================================
REM Check Node.js
REM ============================================
echo [3/8] Checking Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js not found!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo Download the LTS version and restart this script.
    pause
    exit /b 1
)
echo ✓ Node.js found
node --version
echo.

REM ============================================
REM Setup Frontend
REM ============================================
echo [4/8] Setting up frontend...
cd frontend

echo Installing npm packages (this may take 2-3 minutes)...
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm install failed!
    pause
    exit /b 1
)

echo ✓ Frontend setup complete!
echo.

cd ..

REM ============================================
REM Check API Key
REM ============================================
echo [5/8] Checking API key...
findstr /C:"your_gemini_api_key_here" backend\.env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo    WARNING: API KEY NOT CONFIGURED!
    echo ================================================================
    echo.
    echo You need to add your Gemini API key to backend\.env
    echo.
    echo Steps:
    echo 1. Go to: https://aistudio.google.com/app/apikey
    echo 2. Create/copy your API key
    echo 3. Open backend\.env in Notepad
    echo 4. Replace 'your_gemini_api_key_here' with your actual key
    echo 5. Save the file
    echo.
    echo Press any key to open the .env file now...
    pause >nul
    notepad backend\.env
    echo.
    echo Have you added your API key? (Press any key to continue)
    pause >nul
)
echo ✓ API key file exists
echo.

REM ============================================
REM Create Start Scripts
REM ============================================
echo [6/8] Creating start scripts...

REM Backend start script
echo @echo off > START_BACKEND.bat
echo cd backend >> START_BACKEND.bat
echo call venv\Scripts\activate >> START_BACKEND.bat
echo echo ================================================================ >> START_BACKEND.bat
echo echo    BACKEND SERVER STARTING >> START_BACKEND.bat
echo echo ================================================================ >> START_BACKEND.bat
echo echo. >> START_BACKEND.bat
echo python main.py >> START_BACKEND.bat
echo pause >> START_BACKEND.bat

REM Frontend start script
echo @echo off > START_FRONTEND.bat
echo cd frontend >> START_FRONTEND.bat
echo echo ================================================================ >> START_FRONTEND.bat
echo echo    FRONTEND SERVER STARTING >> START_FRONTEND.bat
echo echo ================================================================ >> START_FRONTEND.bat
echo echo. >> START_FRONTEND.bat
echo npm run dev >> START_FRONTEND.bat

echo ✓ Start scripts created
echo.

REM ============================================
REM Create Master Start Script
REM ============================================
echo [7/8] Creating master start script...

echo @echo off > START_APP.bat
echo echo ================================================================ >> START_APP.bat
echo echo    STARTING AI LEARNING MATERIAL GENERATOR >> START_APP.bat
echo echo ================================================================ >> START_APP.bat
echo echo. >> START_APP.bat
echo echo Starting backend server... >> START_APP.bat
echo start "Backend Server" cmd /k START_BACKEND.bat >> START_APP.bat
echo timeout /t 3 /nobreak ^>nul >> START_APP.bat
echo echo Starting frontend server... >> START_APP.bat
echo start "Frontend Server" cmd /k START_FRONTEND.bat >> START_APP.bat
echo timeout /t 5 /nobreak ^>nul >> START_APP.bat
echo echo. >> START_APP.bat
echo echo Opening browser... >> START_APP.bat
echo start http://localhost:3000 >> START_APP.bat
echo echo. >> START_APP.bat
echo echo ✓ App started! >> START_APP.bat
echo echo. >> START_APP.bat
echo echo Two windows opened: >> START_APP.bat
echo echo   1. Backend Server (keep open) >> START_APP.bat
echo echo   2. Frontend Server (keep open) >> START_APP.bat
echo echo. >> START_APP.bat
echo echo Browser should open automatically. >> START_APP.bat
echo echo If not, go to: http://localhost:3000 >> START_APP.bat
echo echo. >> START_APP.bat
echo pause >> START_APP.bat

echo ✓ Master start script created
echo.

REM ============================================
REM Final Instructions
REM ============================================
echo [8/8] Setup complete!
echo.
echo ================================================================
echo    ✓ SETUP COMPLETED SUCCESSFULLY!
echo ================================================================
echo.
echo Next steps:
echo.
echo 1. IMPORTANT: Add your Gemini API key to backend\.env
echo    (If you haven't done it yet, the file was just opened)
echo.
echo 2. To start the app, simply run:
echo    START_APP.bat
echo.
echo    This will:
echo    - Start backend server
echo    - Start frontend server  
echo    - Open browser automatically
echo.
echo 3. The app will open at: http://localhost:3000
echo.
echo ================================================================
echo.
echo Want to start the app now? (Y/N)
set /p START_NOW=
if /i "!START_NOW!"=="Y" (
    echo.
    echo Starting app...
    call START_APP.bat
) else (
    echo.
    echo Okay! Run START_APP.bat whenever you're ready.
)
echo.
pause
