@echo off
title Luenen Terminplaner - Installation
echo ==========================================
echo    Luenen Terminplaner - Installation
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNUNG: Python ist nicht installiert!
    echo.
    echo Fuer die beste Erfahrung installieren Sie Python von:
    echo https://www.python.org/downloads/
    echo.
    echo Waehlen Sie bei der Installation "Add Python to PATH"
    echo.
)

echo Erstelle Programmordner...
set "INSTALL_DIR=%USERPROFILE%\LuenenTerminplaner"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Kopiere Dateien...
xcopy /E /I /Y "." "%INSTALL_DIR%" >nul

echo Erstelle Desktop-Verknuepfung...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Luenen Terminplaner.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\start_windows.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Luenen Terminplaner - Ratsinformationen automatisiert'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation erfolgreich abgeschlossen!
echo ========================================
echo.
echo Das Programm wurde installiert in:
echo %INSTALL_DIR%
echo.
echo Zum Starten:
echo 1. Desktop-Verknuepfung verwenden, ODER
echo 2. start_windows.bat doppelklicken
echo.
echo Bei erstem Start werden automatisch die
echo Python-Pakete installiert.
echo.
pause
