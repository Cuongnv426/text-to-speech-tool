#!/bin/bash
# Text-to-Speech Tool - Run Script (Linux/Mac)
# Just run: chmod +x run.sh && ./run.sh

clear
echo "============================================"
echo "   Text-to-Speech Tool Launcher"
echo "============================================"
echo ""

# Check Python installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not installed"
    echo "Please install Python 3"
    exit 1
fi

# Install requirements if needed
echo "Checking dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Choose version to run:"
echo "[1] Desktop GUI (recommended - easy to use)"
echo "[2] Web Version (open browser)"
echo ""

read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Starting Desktop Application..."
        echo ""
        python3 tts-gui.py
        ;;
    2)
        echo ""
        echo "Starting Web Server..."
        echo "Open your browser and go to: http://localhost:5000"
        echo ""
        python3 tts-web.py
        ;;
    *)
        echo "Invalid choice. Starting Desktop GUI..."
        echo ""
        python3 tts-gui.py
        ;;
esac
