@echo off
REM Text-to-Speech Tool - Run Script (Windows)
REM Just click this file to start

setlocal enabledelayexpansion

echo ============================================
echo   Text-to-Speech Tool Launcher
echo ============================================
echo.

REM Check Python installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Install requirements if needed
echo Checking dependencies...
pip install -q -r requirements.txt 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Choose version to run:
echo [1] Desktop GUI (recommended - easy to use)
echo [2] Web Version (open browser)
echo.

set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting Desktop Application...
    echo.
    python tts-gui.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Web Server...
    echo Open your browser and go to: http://localhost:5000
    echo.
    python tts-web.py
) else (
    echo Invalid choice. Starting Desktop GUI...
    echo.
    python tts-gui.py
)

pause
