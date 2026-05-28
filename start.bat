@echo off
title Coaching Audit Agent
setlocal

echo.
echo  ============================================
echo   Coaching Institute Audit Agent
echo  ============================================
echo.

:: Check if .venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at .venv\
    echo.
    echo To set up, run these commands once:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    echo   .venv\Scripts\playwright install chromium
    echo.
    pause
    exit /b 1
)

:: Activate venv
call .venv\Scripts\activate.bat

echo [*] Starting server on http://localhost:8000 ...
echo     (this window keeps the server alive - don't close it)
echo.

:: Open browser after a 4-second delay (server should be up by then)
start /b cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:8000"

:: Run server in foreground (keeps window alive = server stays up)
python run.py
