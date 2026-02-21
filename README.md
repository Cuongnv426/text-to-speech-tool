# 🎙️ Text-to-Speech Tool for English Learning

Convert English dialogues with multiple speakers into professional MP3 files for YouTube learning content. Two versions included: **Web UI** (FastAPI) and **Desktop GUI** (PyQt5).

## Features

✅ **Auto-detect speakers** from dialogue text ([SPEAKER_NAME] format)  
✅ **Automatically assign voices** to speakers (alternating male/female)  
✅ **Multiple voices** available (5+ different voices)  
✅ **Seamless audio mixing** with natural pauses between speakers  
✅ **Web version** - Paste text, download MP3  
✅ **Desktop version** - File browser, drag-drop support, offline  
✅ **Clean, professional UI** on both platforms  
✅ **Batch processing** support  
✅ **Recent files history** for quick access  
✅ **MP3 export** with customizable bitrate  

## Quick Start

### 1. Install Dependencies

```bash
cd /root/clawd/text-to-speech
pip install -r requirements.txt
```

### 2. Run Web Version

```bash
python tts-web.py
```

Then open `http://localhost:5000` in your browser.

### 3. Run Desktop Version

```bash
python tts-gui.py
```

## System Requirements

- **Python 3.8+**
- **FFmpeg** (for audio processing)
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org

## File Structure

```
/root/clawd/text-to-speech/
├── tts-web.py                  # Web server (FastAPI)
├── tts-gui.py                  # Desktop app (PyQt5)
├── tts_engine.py              # Core TTS engine
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web UI
├── static/
│   ├── style.css            # Web styling
│   └── script.js            # Web client script
├── output/                   # Generated MP3 files
├── examples/                 # Sample dialogues
│   ├── sample_dialogue.txt
│   ├── restaurant_dialogue.txt
│   ├── job_interview.txt
│   ├── daily_conversation.txt
│   └── shopping_dialogue.txt
└── README.md                 # This file
```

## Dialogue Format

The tool expects dialogues in this format:

```
[SPEAKER_NAME] Text for the speaker
[ANOTHER_SPEAKER] Their response
[SPEAKER_NAME] More dialogue
```

### Example

```
[JOHN] Hello, how are you today?
[SARAH] Hi John! I'm doing great, thanks for asking.
[JOHN] That's wonderful! What did you do this morning?
[SARAH] I went to the market and bought some fresh fruits.
```

### Rules

- Speaker names must be in **[UPPERCASE_BRACKETS]**
- One speaker per line (or paragraph)
- Names can contain letters, numbers, and underscores
- Text can span multiple lines if you want, just start the next line with [SPEAKER]

## Web Version Usage

1. **Open** `http://localhost:5000`
2. **Paste** your dialogue text in the text area
3. **Click** "🔍 Detect Speakers" to identify all speakers
4. **(Optional)** Adjust voice assignments for each speaker
5. **Click** "🎵 Generate MP3" to create the audio
6. **Download** the MP3 file or preview it

### Features

- **Text Input Area** - Paste multi-speaker dialogues
- **Speaker Detection** - Automatically identifies unique speakers
- **Voice Assignment** - Assign different voices to different speakers
- **Progress Bar** - Visual feedback during generation
- **Audio Preview** - Listen before downloading
- **Recent Files** - Quick access to recently generated files
- **File Upload** - Load dialogue from .txt files
- **Responsive Design** - Works on desktop and mobile

## Desktop Version Usage

1. **Run** `python tts-gui.py`
2. **Load** a dialogue file or paste text
3. **Click** "🔍 Detect Speakers" to identify speakers
4. **Assign voices** using the dropdown menus
5. **Click** "🎵 Generate MP3" to create the audio
6. **Preview** or **Download** the result

### Features

- **File Browser** - Open and edit .txt files
- **Drag-Drop** - Drop files directly into the window
- **Text Editor** - Edit dialogues directly
- **Speaker Configuration** - Assign voices to each speaker
- **Progress Bar** - Real-time generation progress
- **Audio Preview** - Play generated MP3 directly
- **Output Folder** - Quick access to generated files
- **Recent Files** - History of generated dialogues

## Configuration

Edit `config.py` to customize:

```python
# Web server
WEB_PORT = 5000              # Change port if needed

# Audio format
AUDIO_FORMAT = {
    "sample_rate": 44100,    # Hz
    "channels": 1,           # Mono
    "bitrate": "192k",       # MP3 bitrate
}

# Voices
SPEAKER_PAUSE = 500          # Pause between speakers (ms)
TTS_RATE = 150              # Speaking rate (words per minute)
TTS_VOLUME = 1.0            # Volume (0.0 to 1.0)
```

## Supported Voices

The tool uses system TTS voices via pyttsx3. Available voices depend on your system:

### List Available Voices

```python
from tts_engine import get_tts_engine
engine = get_tts_engine()
print(engine.list_voices())
```

### Voice Assignment

Voices are automatically assigned by gender (male/female alternating). You can override this in the GUI by selecting specific voices for each speaker.

## Examples

### Simple Conversation

```
[ALICE] Hey Bob! How was your day?
[BOB] It was great! How about you?
[ALICE] Pretty good! Want to grab dinner?
[BOB] Sure! Let's go to that Italian place.
```

### Business Meeting

```
[MANAGER] Good morning, team. Let's start the meeting.
[DEVELOPER] Thanks for having me. I'm ready to discuss the project.
[MANAGER] Great. What's the current status?
[DEVELOPER] We've completed the API development. Testing starts next week.
[MANAGER] Excellent work! Keep up the progress.
```

### Multi-speaker Dialogue

```
[PERSON1] Have you seen the new movie?
[PERSON2] Not yet. What's it about?
[PERSON3] It's an action thriller. Highly recommended!
[PERSON1] Let's go watch it this weekend.
[PERSON2] Count me in!
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pyttsx3'"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### No speakers detected

**Problem:** Your dialogue format might be incorrect.  
**Solution:** Use the format `[SPEAKER_NAME] text`. Check:
- Speaker names are in [BRACKETS]
- Names contain only letters, numbers, underscores
- Text comes right after the closing bracket

### Audio quality is poor

**Solution:** Adjust in `config.py`:
```python
TTS_RATE = 150        # Lower = slower and clearer
TTS_VOLUME = 1.0      # Increase if too quiet
```

### Web page shows blank

**Problem:** Server might not have started.  
**Solution:**
1. Check console for errors
2. Verify port 5000 is not in use
3. Try port 5001: `python tts-web.py --port 5001`

### Desktop app won't start

**Problem:** PyQt5 not installed or display issues.  
**Solution:**
```bash
pip install PyQt5==5.15.9
```

On Linux with no display:
```bash
export QT_QPA_PLATFORM=offscreen
python tts-gui.py
```

## Performance Tips

1. **Keep dialogues under 20 speakers** for best performance
2. **Use short, clear sentences** for better pronunciation
3. **Test voices first** before generating long dialogues
4. **Save generated files** for repeated use (no re-generation needed)

## Advanced Usage

### Batch Processing

Process multiple files at once:

```bash
for file in examples/*.txt; do
    echo "Processing: $file"
    python -c "
from tts_engine import get_tts_engine
with open('$file') as f:
    engine = get_tts_engine()
    engine.generate_dialogue_mp3(f.read())
    "
done
```

### Custom Voice Mapping

```python
from tts_engine import get_tts_engine

dialogue = "[JOHN] Hello\n[SARAH] Hi there"
engine = get_tts_engine()

# Custom voice assignment
speaker_voices = {
    "JOHN": 0,    # First male voice
    "SARAH": 3    # Specific female voice
}

output_path, audio = engine.generate_dialogue_mp3(
    dialogue,
    speaker_voices=speaker_voices
)
```

### Programmatic Usage

```python
from tts_engine import get_tts_engine

engine = get_tts_engine()

# Detect speakers
speakers = engine.detect_speakers(dialogue_text)

# Parse dialogue
lines = engine.parse_dialogue(dialogue_text)

# Generate MP3
filepath, audio = engine.generate_dialogue_mp3(
    dialogue_text,
    output_filename="my_dialogue.mp3"
)
```

## API Reference

### TTSEngine Class

#### `detect_speakers(dialogue_text: str) -> List[str]`
Extract unique speaker names from dialogue.

#### `parse_dialogue(dialogue_text: str) -> List[Tuple[str, str]]`
Parse dialogue into (speaker, text) tuples.

#### `list_voices() -> List[str]`
Get available voice IDs and names.

#### `auto_assign_voices(speakers: List[str]) -> Dict[str, int]`
Automatically assign voices to speakers.

#### `generate_dialogue_mp3(dialogue_text, output_filename=None, speaker_voices=None) -> Tuple[str, AudioSegment]`
Generate MP3 from dialogue text. Returns (filepath, audio).

#### `preview_speaker(text: str, voice_id: int) -> AudioSegment`
Preview single speaker voice.

## License

Free and open source for educational use.

## Contributing

Feel free to submit improvements and bug reports!

## Contact

For questions or issues, reach out to the development team.

---

**Happy learning! 📚🎙️**
