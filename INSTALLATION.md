# Installation Guide

Complete step-by-step setup for the TTS Tool.

## Prerequisites

- **Python 3.8 or higher**
- **FFmpeg** - Required for audio processing
- **pip** - Python package manager
- **Git** (optional, for cloning)

## Step 1: Install FFmpeg

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

### Windows

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH:
   - Search "Environment Variables" in Windows
   - Add `C:\ffmpeg\bin` to the PATH variable
4. Verify installation:
   ```cmd
   ffmpeg -version
   ```

### Verify Installation

```bash
ffmpeg -version
```

Should show version information.

## Step 2: Clone or Download the Project

### Option A: Using Git

```bash
cd /root/clawd
git clone <repository-url> text-to-speech
cd text-to-speech
```

### Option B: Manual Download

```bash
cd /root/clawd
mkdir text-to-speech
cd text-to-speech
# Download files to this directory
```

## Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pyttsx3` - Text-to-speech
- `PyQt5` - Desktop GUI
- `pydub` - Audio mixing

**Installation may take 2-3 minutes.**

### Troubleshooting Installation

If you encounter issues with specific packages:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install individually
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pyttsx3==2.90
pip install PyQt5==5.15.9
pip install pydub==0.25.1
```

## Step 5: Test Installation

### Test TTS Engine

```python
python3 << EOF
from tts_engine import get_tts_engine

engine = get_tts_engine()
voices = engine.list_voices()
print(f"✓ TTS Engine working! Found {len(voices)} voices")
print("Available voices:")
for voice in voices[:5]:
    print(f"  - {voice}")
EOF
```

### Test Web Version

```bash
python tts-web.py
```

You should see:
```
============================================================
TTS Tool - Web Version
============================================================
Starting server on http://0.0.0.0:5000
Open in browser: http://localhost:5000
Output folder: /root/clawd/text-to-speech/output
============================================================
```

Press `Ctrl+C` to stop.

### Test Desktop Version

```bash
python tts-gui.py
```

Should open a GUI window.

## Step 6: Verify All Files

Check that these files exist:

```
/root/clawd/text-to-speech/
├── ✓ tts-web.py
├── ✓ tts-gui.py
├── ✓ tts_engine.py
├── ✓ config.py
├── ✓ requirements.txt
├── ✓ templates/index.html
├── ✓ static/style.css
├── ✓ static/script.js
├── ✓ output/ (directory)
├── ✓ examples/ (directory with sample files)
└── ✓ README.md
```

## Troubleshooting

### "Module not found" errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### PyQt5 installation fails

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyqt5
```

**macOS:**
```bash
brew install pyqt@5
```

### pyttsx3 engine issues

```bash
# Try espeak backend instead
sudo apt-get install espeak espeak-ng
pip install pyttsx3
```

### FFmpeg not found

```bash
# Verify path
which ffmpeg  # Linux/macOS
where ffmpeg  # Windows

# If not found, add to PATH or reinstall
```

### Port 5000 already in use

Edit `config.py`:
```python
WEB_PORT = 5001  # Use different port
```

Then run:
```bash
python tts-web.py --port 5001
```

## Next Steps

1. **Read** the [README.md](README.md) for features and usage
2. **Try examples** in the `examples/` folder
3. **Test** the web version at http://localhost:5000
4. **Explore** the GUI app with `python tts-gui.py`
5. **Configure** settings in `config.py` as needed

## Performance Notes

- **First run** may be slow as TTS engine initializes
- **Audio generation** takes ~1-2 seconds per 10 seconds of dialogue
- **Subsequent runs** are faster due to caching
- **Large dialogues** (100+ lines) may take 5-10 minutes

## Support for Different TTS Engines

The tool currently uses `pyttsx3`, which supports:

- **Linux**: eSpeak (ESPEAK_DATA_PATH)
- **macOS**: NSSpeechSynthesizer
- **Windows**: SAPI5

To list voices available on your system:

```python
from tts_engine import get_tts_engine
engine = get_tts_engine()
for voice in engine.list_voices():
    print(voice)
```

## Next: Running the Application

### Web Version

```bash
python tts-web.py
# Open http://localhost:5000 in browser
```

### Desktop Version

```bash
python tts-gui.py
```

See [README.md](README.md) for detailed usage instructions.

---

**Installation complete! You're ready to generate MP3 dialogues. 🎉**
