@echo off
echo Installing dependencies...
pip install -q gtts

echo.
echo Starting TTS Tool...
python tts-simple.py

pause
