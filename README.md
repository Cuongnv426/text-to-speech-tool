# TTS Tool - Simple Text to Speech

## Overview

A **zero-dependency** text-to-speech application built with:
- ✅ **gTTS** - Simple Google Text-to-Speech
- ✅ **Tkinter** - Built-in Python GUI (no external dependencies)
- ✅ **No complex build tools** - Just Python + 1 pip install

## Features

- 🎯 **Multi-speaker support** - Parse dialogue with `[SPEAKER]` format
- 🎵 **Auto voice variation** - Automatically assigns different voice variants
- 📦 **MP3 generation** - Creates combined single MP3 file from dialogue
- 🎨 **Beautiful GUI** - Clean, intuitive Tkinter interface
- 📂 **Easy output management** - Generated files saved to `./output/`
- 🚀 **Instant startup** - No complex initialization, just works

## Installation

### Requirements
- Python 3.6+
- No other system dependencies needed

### Setup

#### Option 1: Automated (Recommended)

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

#### Option 2: Manual

```bash
pip install gtts==2.5.3
python tts-simple.py
```

That's it!

## Usage

### 1. Launch the app
```bash
python tts-simple.py
```

### 2. Enter dialogue with speaker format
```
[Alice] Hello, how are you today?
[Bob] I'm doing great, thanks for asking!
[Alice] That's wonderful to hear!
```

### 3. Click "🎯 Generate MP3"
- App parses dialogue
- Generates audio for each line
- Combines into single MP3
- Saves to `output/dialogue.mp3`

### 4. Optional: Open output folder
- Click "📂 Open Output Folder" to see generated files

## Format

### With Speaker Tags (Recommended)
```
[SPEAKER_NAME] Text here...
[ANOTHER_SPEAKER] More text here...
```

### Plain Text (Fallback)
If no speaker tags found, entire text is spoken as one segment.

## Features

- **Auto voice assignment**: Each speaker gets a different voice variant (en, en-us, en-gb, en-au, en-ie, en-za)
- **Variety**: Voice rotates automatically for natural dialogue
- **MP3 combining**: All segments combined into single file
- **Progress feedback**: Real-time status updates during generation
- **Background threading**: UI stays responsive during generation

## File Structure

```
text-to-speech/
├── tts-simple.py          # Main application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies (just gTTS)
├── run.bat               # Windows launcher
├── run.sh                # Unix/Linux/macOS launcher
├── README.md             # This file
├── output/               # Generated MP3 files (auto-created)
└── .git/                 # Version control
```

## Configuration

Edit `config.py` to customize:

```python
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output')
TTS_SETTINGS = {
    'lang': 'en',
    'slow': False,  # Set to True for slower speech
}
```

## Troubleshooting

### "No module named 'gtts'"
```bash
pip install gtts==2.5.3
```

### "No module named 'tkinter'" (Linux only)
```bash
sudo apt-get install python3-tk
```

### Audio quality issues
- Edit `config.py` and set `'slow': True` for clearer audio
- Try different speaker names to get different voice variants

### Large output files
- This is normal for MP3 speech
- Each line of dialogue is ~5-20KB depending on length

## Why This Works

- **gTTS**: Lightweight, no build dependencies, works everywhere
- **Tkinter**: Built-in with Python, no external GUI framework needed
- **Pure Python**: No C extensions, Rust, or compilation required
- **Simple MP3 combining**: Just concatenate MP3 frames (standard approach)

## Performance

- Typical 10-line dialogue: < 5 seconds
- No lag in UI (background threading)
- Output MP3s can be edited in any audio editor

## Limitations

- Supports English and several English variants (en, en-us, en-gb, en-au, en-ie, en-za)
- Speech quality depends on internet connection (gTTS requires network)
- MP3 combining is simple concatenation (no cross-fade)

## Future Enhancements

Possible additions without adding dependencies:
- [ ] Speed control slider
- [ ] Volume adjustment
- [ ] Pause/resume preview
- [ ] Custom speaker names → language mapping
- [ ] Batch processing

## License

MIT - Use freely

## Support

For issues or questions:
1. Check requirements are installed: `pip install -r requirements.txt`
2. Ensure Python 3.6+ is installed
3. Check internet connection (gTTS needs network)

## Example Dialog

Save this to a file and copy-paste into the app:

```
[Narrator] Welcome to the TTS Tool demonstration.
[Alice] Hello everyone, I'm Alice.
[Bob] And I'm Bob. Nice to meet you all!
[Alice] Let's test the text-to-speech system.
[Bob] This is a simple, zero-dependency TTS application.
[Narrator] It works on Windows, macOS, and Linux.
[Alice] No complex dependencies, just Python and gTTS.
[Bob] Ready to generate some awesome audio?
[All] Let's go!
```

---

**Happy speaking! 🎵**
