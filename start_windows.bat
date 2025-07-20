@echo off
title Luenen Terminplaner
echo ==========================================
echo    Luenen Terminplaner wird gestartet...
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo.
    echo Bitte installieren Sie Python von:
    echo https://www.python.org/downloads/
    echo.
    echo Waehlen Sie bei der Installation "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python gefunden, installiere Abhaengigkeiten...
python -m pip install -r requirements.txt --user --quiet

echo Starte Anwendung...
echo.
echo Die Anwendung startet auf: http://localhost:5000
echo Browser oeffnet sich automatisch...
echo.
echo Zum Beenden: Strg+C druecken oder dieses Fenster schliessen
echo.

python main.py
