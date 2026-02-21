"""Configuration for TTS Tool"""
import os

# Output folder for generated MP3s
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output')

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Common female names (lowercase for matching)
FEMALE_NAMES = {
    'alice', 'sarah', 'jane', 'mary', 'emma', 'lisa', 'jessica', 'susan', 'karen',
    'nancy', 'betty', 'margaret', 'sandra', 'ashley', 'kimberly', 'donna', 'carol',
    'rachel', 'catherine', 'sophia', 'olivia', 'ava', 'mia', 'isabelle', 'charlotte',
    'diane', 'diana', 'patricia', 'barbara', 'ann', 'jennifer', 'linda', 'paula', 'anna',
    'ruth', 'victoria', 'lucy', 'alice', 'helen', 'deborah', 'stephanie',
}

# Common male names (lowercase for matching)
MALE_NAMES = {
    'bob', 'john', 'mike', 'david', 'tom', 'james', 'robert', 'william', 'richard',
    'joseph', 'thomas', 'charles', 'daniel', 'matthew', 'anthony', 'mark', 'donald',
    'steven', 'paul', 'andrew', 'joshua', 'kenneth', 'kevin', 'brian', 'george',
    'ryan', 'edward', 'edward', 'ronald', 'timothy', 'jason', 'jeffrey', 'frank',
    'scott', 'eric', 'stephen', 'larry', 'justin', 'christopher', 'terry', 'peter',
}

# Audio generation settings
TTS_SETTINGS = {
    'rate': 150,  # Speed of speech (words per minute)
    'volume': 1.0,  # Volume (0.0 to 1.0)
}

# GUI Settings
GUI_SETTINGS = {
    'window_title': 'TTS Tool - Multiple Voices (pyttsx3)',
    'window_width': 900,
    'window_height': 700,
    'font_family': 'Helvetica',
    'font_size': 10,
}


def detect_gender(speaker_name: str) -> str:
    """
    Detect gender based on speaker name.
    Returns 'female', 'male', or 'neutral' (for unknown/neutral names)
    """
    name_lower = speaker_name.lower().strip()
    
    if name_lower in FEMALE_NAMES:
        return 'female'
    elif name_lower in MALE_NAMES:
        return 'male'
    else:
        # Default: neutral (will alternate in the app)
        return 'neutral'
