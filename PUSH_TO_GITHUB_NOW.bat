@echo off
echo ================================================================
echo    PUSHING TO GITHUB - samikshadhole06 account
echo ================================================================
echo.

echo Step 1: Clearing old credentials...
cmdkey /delete:git:https://github.com >nul 2>&1

echo Step 2: Configuring Git...
git config --global user.name "samikshadhole06"
git config --global user.email "samikshadhole06@users.noreply.github.com"

echo Step 3: Attempting to push...
echo.
echo A browser window will open for GitHub login.
echo Please login with your samikshadhole06 account!
echo.
pause

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo    SUCCESS! Your code is now on GitHub!
    echo ================================================================
    echo.
    echo View your repository at:
    echo https://github.com/samikshadhole06/ai-learning-material-generator
    echo.
) else (
    echo.
    echo ================================================================
    echo    Push failed. Try manual method:
    echo ================================================================
    echo.
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Generate new token (classic)
    echo 3. Select: repo (all permissions)
    echo 4. Copy the token
    echo 5. Run this command:
    echo.
    echo git remote set-url origin https://YOUR_TOKEN@github.com/samikshadhole06/ai-learning-material-generator.git
    echo git push -u origin main
    echo.
)

pause
