#!/bin/bash

echo "Installing dependencies..."
pip install -q gtts

echo ""
echo "Starting TTS Tool..."
python3 tts-simple.py
