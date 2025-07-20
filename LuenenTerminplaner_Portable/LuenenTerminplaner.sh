#!/bin/bash

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
