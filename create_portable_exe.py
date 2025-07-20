#!/usr/bin/env python3
"""
Create a portable Windows-like executable package
Since we can't use PyInstaller on this system, we create a self-contained package
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_launcher_bat():
    """Create Windows batch launcher"""
    launcher_content = '''@echo off
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
'''
    
    with open('LuenenTerminplaner.bat', 'w', encoding='cp1252') as f:
        f.write(launcher_content)
    print("✅ LuenenTerminplaner.bat created")

def create_linux_launcher():
    """Create Linux shell launcher"""
    launcher_content = '''#!/bin/bash

echo "========================================="
echo "   Lünen Terminplaner v1.0.3"
echo "========================================="
echo
echo "Starting application..."
echo "Browser will open automatically on http://localhost:5000"
echo
echo "Press Ctrl+C to stop the application"
echo "========================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed!"
    echo
    echo "Please install Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora:        sudo dnf install python3 python3-pip"
    echo "  Arch:          sudo pacman -S python python-pip"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
python3 -m pip install -r requirements_minimal.txt --user --quiet

# Start the application
python3 main_standalone.py
'''
    
    with open('LuenenTerminplaner.sh', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Make executable
    os.chmod('LuenenTerminplaner.sh', 0o755)
    print("✅ LuenenTerminplaner.sh created")

def create_installer():
    """Create installation script"""
    installer_content = '''@echo off
title Luenen Terminplaner - Installation
echo =========================================
echo    Luenen Terminplaner - Installation
echo =========================================
echo.

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\\LuenenTerminplaner"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying files to %INSTALL_DIR%...
xcopy /E /I /Y "." "%INSTALL_DIR%" >nul

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Luenen Terminplaner.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\LuenenTerminplaner.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Luenen Terminplaner - Ratsinformationen automatisiert'; $Shortcut.Save()"

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
'''
    
    with open('install.bat', 'w', encoding='cp1252') as f:
        f.write(installer_content)
    print("✅ install.bat created")

def create_readme():
    """Create comprehensive README"""
    readme_content = '''# Lünen Terminplaner - Portable Version

## 🚀 Quick Start

### Windows:
1. Double-click `LuenenTerminplaner.bat`
2. Browser opens automatically on http://localhost:5000

### Linux:
1. Run `./LuenenTerminplaner.sh` in terminal
2. Browser opens automatically on http://localhost:5000

## 📦 Installation (Optional)

### Windows Auto-Installation:
1. Double-click `install.bat`
2. Follow the instructions
3. Desktop shortcut will be created

### Manual Installation:
1. Extract all files to a folder
2. Run the launcher from that folder

## 🔧 Requirements

- **Python 3.8+** (Download from https://python.org)
- **Internet connection** (for downloading meeting data)
- **100 MB free space**

## 📋 Features

- ✅ **Meeting Scraper**: Automatically downloads Lünen council meetings
- ✅ **PDF Processing**: Extracts and summarizes meeting documents
- ✅ **Smart Filtering**: Filter by committees and date ranges
- ✅ **Multiple Exports**: Markdown, HTML, PDF, JSON formats
- ✅ **Detail Views**: Comprehensive meeting summaries
- ✅ **Responsive Design**: Works on all screen sizes

## 🎯 Usage

1. **Start the application** (see Quick Start above)
2. **Select date range** for meetings to search
3. **Choose committees** you're interested in
4. **Click "Termine laden"** to search for meetings
5. **Browse results** and view detailed summaries
6. **Export data** in your preferred format

## 🛠️ Troubleshooting

### "Python is not installed"
- Download Python from https://python.org/downloads/
- ⚠️ **Important**: Check "Add Python to PATH" during installation
- Restart computer after installation

### "Dependencies failed to install"
- Run as Administrator (Windows) or with sudo (Linux)
- Check internet connection
- Temporarily disable antivirus/firewall

### "Browser doesn't open automatically"
- Manually open http://localhost:5000 in your browser
- Keep the console window open

### "Port already in use"
- Close other applications using port 5000
- Or edit `main_standalone.py` and change the port number

### "No meetings found"
- Check internet connection
- Try different date ranges
- Select more committees

## 📁 File Structure

```
LuenenTerminplaner/
├── LuenenTerminplaner.bat    # Windows launcher
├── LuenenTerminplaner.sh     # Linux launcher
├── main_standalone.py        # Main application
├── app.py                    # Flask web app
├── scraper.py               # Web scraping logic
├── pdf_processor.py         # PDF processing
├── export_manager.py        # Export functionality
├── requirements_minimal.txt  # Python dependencies
├── templates/               # Web interface
├── downloads/              # PDF cache
└── exports/               # Exported files
```

## 🌐 Web Interface

Once started, the application runs a local web server accessible at:
**http://localhost:5000**

The interface includes:
- Date range selector
- Committee filter checkboxes
- Real-time search progress
- Meeting cards with summaries
- Export buttons for different formats
- Detailed meeting view pages

## 📄 Data Sources

This application extracts data from:
- **Lünen Council Information System** (official public data)
- **Meeting PDFs** for detailed summaries
- **Committee listings** for filtering options

## 🔒 Privacy

- All data processing happens **locally** on your computer
- No data is sent to external servers (except for downloading public meeting data)
- PDF files are cached locally for faster access
- No personal information is collected or stored

## 📞 Support

For technical issues:
1. Check this README for common solutions
2. Verify Python installation: `python --version`
3. Check console output for error messages
4. Ensure internet connectivity for data downloads

## 📈 Version Information

**Version**: 1.0.3  
**Build**: Portable Python Distribution  
**Compatibility**: Windows 10+, Linux (Ubuntu 18.04+)  
**Python**: 3.8+ required  

---

🎉 **Thank you for using Lünen Terminplaner!**

This tool helps make local government more transparent and accessible.
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README.md created")

def create_portable_package():
    """Create complete portable package"""
    
    print("📦 Creating Portable Lünen Terminplaner Package")
    print("=" * 50)
    
    # Check required files
    required_files = [
        'main_standalone.py', 'app.py', 'scraper.py', 
        'pdf_processor.py', 'export_manager.py',
        'requirements_minimal.txt', 'spezifikation.md'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    # Create launchers and installers
    create_launcher_bat()
    create_linux_launcher()
    create_installer()
    create_readme()
    
    # Create package directory
    package_dir = 'LuenenTerminplaner_Portable'
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Files to include
    files_to_copy = [
        'main_standalone.py', 'app.py', 'scraper.py', 
        'pdf_processor.py', 'export_manager.py',
        'requirements_minimal.txt', 'spezifikation.md',
        'LuenenTerminplaner.bat', 'LuenenTerminplaner.sh',
        'install.bat', 'README.md'
    ]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"📄 Copied: {file}")
    
    # Copy directories
    dirs_to_copy = ['templates']
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(package_dir, dir_name))
            print(f"📁 Copied: {dir_name}/")
    
    # Create empty working directories
    os.makedirs(os.path.join(package_dir, 'downloads'), exist_ok=True)
    os.makedirs(os.path.join(package_dir, 'exports'), exist_ok=True)
    
    # Create ZIP package
    zip_filename = 'LuenenTerminplaner_Portable.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    # Calculate size
    zip_size = os.path.getsize(zip_filename) / (1024*1024)
    
    print(f"\n🎉 Portable Package Created Successfully!")
    print(f"📦 Package: {zip_filename} ({zip_size:.1f} MB)")
    print(f"📁 Directory: {package_dir}/")
    
    print(f"\n📋 For Users:")
    print("1. Download and extract the ZIP file")
    print("2. Windows: Double-click LuenenTerminplaner.bat")
    print("3. Linux: Run ./LuenenTerminplaner.sh")
    print("4. Browser opens automatically on http://localhost:5000")
    
    return True

if __name__ == '__main__':
    create_portable_package()