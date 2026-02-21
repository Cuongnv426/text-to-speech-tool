"""
Configuration settings for TTS Tool
"""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# Output folder
OUTPUT_FOLDER = PROJECT_ROOT / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Web server settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = False

# TTS Engine settings
TTS_ENGINE = "pyttsx3"  # Options: pyttsx3, espeak, freetts
TTS_RATE = 150  # Words per minute (normal: 150-160)
TTS_VOLUME = 1.0  # 0.0 to 1.0

# Voice assignments
# Available voices depend on system (see list_voices function)
VOICE_PRESETS = {
    "male": [0, 2, 4],      # Male voice indices
    "female": [1, 3, 5],    # Female voice indices
    "default": 0
}

# Speaker voice mapping (can be customized per dialogue)
SPEAKER_VOICES = {}

# Audio format settings
AUDIO_FORMAT = {
    "sample_rate": 44100,   # Hz
    "channels": 1,          # Mono
    "bitrate": "192k",      # MP3 bitrate
}

# Pause between speakers (milliseconds)
SPEAKER_PAUSE = 500  # 0.5 second pause

# Maximum file size for upload (bytes)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# Logging
DEBUG = False
LOG_LEVEL = "INFO"
