@echo off
echo ===============================================================================
echo                   PUSHING TO GITHUB
echo ===============================================================================
echo.

set /p USERNAME="Enter your GitHub username: "

if "%USERNAME%"=="" (
    echo Error: Username cannot be empty
    pause
    exit /b 1
)

echo.
echo Repository: https://github.com/%USERNAME%/egolife-video-annotation
echo.

echo Configuring remote...
git remote add origin https://github.com/%USERNAME%/egolife-video-annotation.git
if %errorlevel% neq 0 (
    echo Note: Remote might already exist, removing and re-adding...
    git remote remove origin
    git remote add origin https://github.com/%USERNAME%/egolife-video-annotation.git
)

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo                   SUCCESS!
    echo ===============================================================================
    echo.
    echo Your code is now on GitHub at:
    echo https://github.com/%USERNAME%/egolife-video-annotation
    echo.
    echo Next: Deploy to Streamlit Cloud
    echo Opening Streamlit Cloud...
    timeout /t 3 >nul
    start https://share.streamlit.io
    echo.
    echo In Streamlit Cloud:
    echo 1. Sign in with GitHub
    echo 2. Click "New app"
    echo 3. Repository: %USERNAME%/egolife-video-annotation
    echo 4. Branch: main
    echo 5. Main file: app.py
    echo 6. Click Deploy!
    echo.
) else (
    echo.
    echo Error pushing to GitHub!
    echo Please check:
    echo 1. Repository exists: https://github.com/%USERNAME%/egolife-video-annotation
    echo 2. Repository is public
    echo 3. You have push access
)

echo.
pause
