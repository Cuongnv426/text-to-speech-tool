# ⚡ Quick Start Guide - 5 Minutes

Get up and running in **5 minutes**!

---

## Step 1: Install (2 minutes)

### Prerequisites
- Python 3.8+
- FFmpeg

### Install

```bash
# Navigate to project
cd /root/clawd/text-to-speech

# Install dependencies
pip install -r requirements.txt
```

**That's it!** ✅

---

## Step 2: Choose Your Version

### 🌐 Web Version (Easy)
```bash
python tts-web.py
```
Then open: **http://localhost:5000**

### 🖥️ Desktop Version (Offline)
```bash
python tts-gui.py
```

---

## Step 3: Generate Your First MP3 (3 minutes)

### Copy This Example

```
[JOHN] Hello, how are you today?
[SARAH] Hi John! I'm doing great, thanks for asking.
[JOHN] That's wonderful! What did you do this morning?
[SARAH] I went to the market and bought some fresh fruits.
[JOHN] Nice! Which fruits did you get?
[SARAH] I got apples, bananas, and oranges.
```

### Web Version
1. **Paste** text in left panel
2. **Click** "🔍 Detect Speakers"
3. **Click** "🎵 Generate MP3"
4. **Click** "⬇️ Download MP3"

### Desktop Version
1. **Paste** text in left panel
2. **Click** "🔍 Detect Speakers"
3. **Click** "🎵 Generate MP3"
4. **Click** "⬇️ Download MP3"

---

## Done! 🎉

Your first MP3 is generated and ready to use!

---

## Format Rules (Important!)

Use this exact format:

```
[SPEAKER_NAME] Their dialogue text here
[OTHER_SPEAKER] Their response
```

### ✅ Correct
```
[JOHN] Hello world
[SARAH] Hi there
[JOHN] How are you?
```

### ❌ Wrong
```
john: Hello world      (no brackets)
[john] Hi there        (lowercase)
[JOHN SMITH] Hi        (spaces - use underscore)
JOHN: Hello            (wrong format)
```

---

## Common Tasks

### Try the Examples

Files are ready in `examples/`:
- `sample_dialogue.txt` - Simple greeting
- `restaurant_dialogue.txt` - Restaurant scene
- `job_interview.txt` - Job interview
- `daily_conversation.txt` - Casual chat
- `shopping_dialogue.txt` - Shopping

### Create Your Own

Any dialogue works! Just follow the format:
```
[CHARACTER_NAME] What they say
[OTHER_CHARACTER] Their reply
```

### Find Generated Files

**Web Version:** Click "📁 Open Output Folder"  
**Desktop Version:** Click "📁 Open Output Folder"  
**Or:** Check `/root/clawd/text-to-speech/output/`

---

## Troubleshooting (Quick Fixes)

| Problem | Solution |
|---------|----------|
| "No speakers detected" | Check format: [UPPERCASE] Text |
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| Port 5000 in use | Edit `config.py`, change WEB_PORT |
| Audio too slow/fast | Edit `config.py`, change TTS_RATE |
| Can't find FFmpeg | Install: `sudo apt install ffmpeg` (Linux) |

See **TROUBLESHOOTING.md** for more solutions.

---

## Next Steps

1. **Generate 5 MP3s** from different dialogues
2. **Listen** to the audio quality
3. **Adjust voices** if needed (dropdown in web version)
4. **Share** MP3s on YouTube or with learners
5. **Create more** dialogues for your course

---

## Key Features

- ✅ Auto-detect speakers
- ✅ Multiple voices (male/female)
- ✅ Clear pronunciation
- ✅ Fast generation
- ✅ Professional MP3 quality
- ✅ Easy web interface
- ✅ Desktop app with drag-drop
- ✅ Completely offline (no cloud)

---

## Documentation

- **README.md** - Full overview
- **INSTALLATION.md** - Detailed setup
- **USAGE-WEB.md** - Web interface guide
- **USAGE-GUI.md** - Desktop app guide
- **DIALOGUE-FORMAT.md** - Text formatting
- **EXAMPLES.md** - 12 ready-to-use dialogues
- **TROUBLESHOOTING.md** - Common issues
- **API-REFERENCE.md** - For developers

---

## API Quick Reference (For Developers)

```python
from tts_engine import get_tts_engine

engine = get_tts_engine()

# Simple usage
dialogue = "[JOHN] Hello\n[SARAH] Hi"
filepath, audio = engine.generate_dialogue_mp3(dialogue)

# With options
speaker_voices = {"JOHN": 0, "SARAH": 1}
filepath, audio = engine.generate_dialogue_mp3(
    dialogue,
    output_filename="custom.mp3",
    speaker_voices=speaker_voices
)
```

---

## Keyboard Shortcuts

### Web Version
- (Coming in v1.1)

### Desktop Version
- Ctrl+O - Open file
- Ctrl+S - Save dialogue
- Ctrl+G - Generate MP3

---

## Settings (Optional)

Edit `config.py` to customize:

```python
TTS_RATE = 150              # Speaking speed (words/min)
TTS_VOLUME = 1.0            # Volume (0.0-1.0)
SPEAKER_PAUSE = 500         # Pause between speakers (ms)
WEB_PORT = 5000             # Web server port
```

Restart application for changes to take effect.

---

## Example Workflow

```
1. Copy example from EXAMPLES.md
   ↓
2. Paste into TTS Tool
   ↓
3. Click "Detect Speakers"
   ↓
4. Click "Generate MP3"
   ↓
5. Preview audio
   ↓
6. Download MP3
   ↓
7. Use in video/presentation
```

---

## Quality Tips

### For Best Results
- ✅ Use short sentences
- ✅ Add proper punctuation
- ✅ Use simple, clear English
- ✅ Avoid abbreviations
- ✅ Test with a small dialogue first

### Avoid
- ❌ Very long dialogues (split into parts)
- ❌ Unclear pronunciation
- ❌ Complex words (use simple ones)
- ❌ Empty lines between speakers

---

## File Locations

```
Generated MP3s: /root/clawd/text-to-speech/output/
Examples:       /root/clawd/text-to-speech/examples/
Web UI:         http://localhost:5000
Config:         /root/clawd/text-to-speech/config.py
```

---

## Real-World Uses

- 📚 English learning videos
- 🎓 Educational content
- 📖 Audiobook narration
- 🎬 Video subtitles/voiceover
- 💼 Business presentations
- 🎙️ Podcasts
- 🎮 Game dialogue

---

## Questions?

1. **Read** the relevant guide (USAGE-WEB.md or USAGE-GUI.md)
2. **Check** TROUBLESHOOTING.md for common issues
3. **Review** EXAMPLES.md for usage patterns
4. **See** API-REFERENCE.md for code details

---

**You're all set! Start creating now! 🚀**

Questions? Check the full documentation in the project folder.

---

## One-Liner Commands

```bash
# Generate MP3 from command line
python -c "from tts_engine import get_tts_engine; engine = get_tts_engine(); engine.generate_dialogue_mp3('[JOHN] Hello\n[SARAH] Hi')"

# List available voices
python -c "from tts_engine import get_tts_engine; engine = get_tts_engine(); print('\n'.join(engine.list_voices()))"

# Process all examples
for f in examples/*.txt; do python -c "from tts_engine import get_tts_engine; engine = get_tts_engine(); engine.generate_dialogue_mp3(open('$f').read())"; done
```

---

**Happy Learning! 📚🎙️✨**
