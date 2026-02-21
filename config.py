"""Configuration for TTS Tool"""
import os

# Output folder for generated MP3s
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output')

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Speaker voice mappings (using gTTS language variants for variety)
SPEAKER_VOICES = {
    'default': 'en',
    'male': 'en',
    'female': 'en-gb',
    'narrator': 'en-us',
    'speaker1': 'en-au',
    'speaker2': 'en-gb',
}

# Audio generation settings
TTS_SETTINGS = {
    'lang': 'en',
    'slow': False,  # Set to True for slower speech
}

# GUI Settings
GUI_SETTINGS = {
    'window_title': 'TTS Tool - Simple Text to Speech',
    'window_width': 900,
    'window_height': 700,
    'font_family': 'Helvetica',
    'font_size': 10,
}
