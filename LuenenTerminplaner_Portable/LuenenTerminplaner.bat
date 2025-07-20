@echo off
title Luenen Terminplaner
cls
echo.
echo =========================================
echo    Luenen Terminplaner v1.0.3
echo =========================================
echo.
echo Starting application...
echo Browser will open automatically on http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo =========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
python -m pip install -r requirements_minimal.txt --user --quiet

REM Start the application
python main_standalone.py
pause
