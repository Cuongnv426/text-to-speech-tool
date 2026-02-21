#!/bin/bash

echo "Installing dependencies..."
pip install -q pyttsx3

echo ""
echo "Starting TTS Tool with Multiple Voices..."
python3 tts-simple.py
