@echo off
title Luenen Terminplaner - Installation
echo =========================================
echo    Luenen Terminplaner - Installation
echo =========================================
echo.

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\LuenenTerminplaner"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying files to %INSTALL_DIR%...
xcopy /E /I /Y "." "%INSTALL_DIR%" >nul

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Luenen Terminplaner.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\LuenenTerminplaner.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Luenen Terminplaner - Ratsinformationen automatisiert'; $Shortcut.Save()"

echo.
echo =========================================
echo Installation completed successfully!
echo =========================================
echo.
echo The program has been installed to:
echo %INSTALL_DIR%
echo.
echo Desktop shortcut has been created.
echo.
echo To start: Double-click the desktop shortcut
echo          or run LuenenTerminplaner.bat
echo.
pause
