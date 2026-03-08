@echo off
echo ===============================================================
echo   VIDEO ANNOTATION SYSTEM - ONE-CLICK DEPLOYMENT
echo ===============================================================
echo.

:: Check if app is running
echo [1/5] Checking if Streamlit app is running...
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% == 0 (
    echo   ^>> App is already running at http://localhost:8501
    echo   ^>> Opening in browser...
    start http://localhost:8501
) else (
    echo   ^>> Starting Streamlit app...
    start /B python -m streamlit run app.py --server.headless=true
    timeout /t 5 >nul
    echo   ^>> App started at http://localhost:8501
    start http://localhost:8501
)
echo.

:: Open Graph Explorer for token
echo [2/5] Opening Graph Explorer for OneDrive setup...
echo   ^>> Complete these steps in the browser:
echo   1. Sign in with your UNC email
echo   2. Click 'Modify permissions'
echo   3. Enable: Files.Read.All and Files.ReadWrite.All
echo   4. Click 'Consent' and 'Accept'
echo   5. Click 'Access token' tab and copy the token
echo.
start https://developer.microsoft.com/en-us/graph/graph-explorer
timeout /t 3 >nul

:: Run setup script
echo [3/5] Run video setup when ready...
echo   ^>> Press any key when you have the access token ready...
pause >nul
python tools/quick_setup.py
echo.

:: Open GitHub
echo [4/5] Setting up GitHub repository...
echo   ^>> Opening GitHub in browser...
echo   ^>> Create a new repository named: video-annotation-system
echo   ^>> Make it Public
echo   ^>> Don't initialize with README
echo.
start https://github.com/new
timeout /t 3 >nul
echo   ^>> Press any key after creating the repository...
pause >nul

:: Git commands
echo.
echo [5/5] Git commands ready!
echo.
echo   Run these commands (replace YOUR-USERNAME):
echo.
echo   git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git
echo   git branch -M main
echo   git push -u origin main
echo.
echo ===============================================================
echo   NEXT: Deploy to Streamlit Cloud
echo ===============================================================
echo   1. Go to: https://share.streamlit.io
echo   2. Sign in with GitHub
echo   3. Click 'New app'
echo   4. Select your repository
echo   5. Main file: app.py
echo   6. Click 'Deploy'
echo.
echo Opening Streamlit Cloud...
start https://share.streamlit.io
echo.
echo ===============================================================
echo   DEPLOYMENT GUIDE COMPLETE!
echo ===============================================================
pause
