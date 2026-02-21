@echo off
echo Installing dependencies...
pip install -q pyttsx3

echo.
echo Starting TTS Tool with Multiple Voices...
python tts-simple.py

pause
