# Web Version Usage Guide

Complete guide to using the FastAPI web interface.

## Starting the Server

```bash
python tts-web.py
```

You'll see:
```
============================================================
TTS Tool - Web Version
============================================================
Starting server on http://0.0.0.0:5000
Open in browser: http://localhost:5000
Output folder: /root/clawd/text-to-speech/output
============================================================
```

Open **http://localhost:5000** in your web browser.

## Main Interface

The web interface has three sections:

### 1. Input Panel (Left Side)

**📝 Paste Your Dialogue**

- **Text Area** - Paste your dialogue with [SPEAKER_NAME] format
- **Detect Speakers** button - Scan text for unique speakers
- **Load File** button - Upload a .txt file
- **File Input** - Select file to process

Example format:
```
[JOHN] Hello, how are you?
[SARAH] Hi John! I'm doing great.
[JOHN] That's wonderful!
```

### 2. Configuration Panel (Right Side)

**👥 Detected Speakers**

After clicking "Detect Speakers", you'll see a list:
```
1. JOHN
2. SARAH
```

**🎙️ Voice Assignment**

For each speaker, select which voice to use:
```
JOHN:  Voice 0: en-US male (David)
SARAH: Voice 1: en-US female (Nancy)
```

Click dropdown to change voices.

### 3. Generation Section

**🎵 Generate MP3**
- Click to create the audio file
- Progress bar shows generation status
- Takes 2-5 seconds depending on dialogue length

**✅ Success! (After generation)**
- Shows filename, duration, speakers
- Audio player preview
- Download MP3 button

### 4. History Section (Bottom)

**📋 Recent Files**

Shows your last generated files. Click any file to:
- Preview audio
- Download again

## Step-by-Step Workflow

### 1. Paste Dialogue

```
[ALICE] Good morning! Did you sleep well?
[BOB] Yes, I did. How about you?
[ALICE] Pretty well, thanks!
```

### 2. Detect Speakers

Click **🔍 Detect Speakers**

The tool will:
- Find all unique speaker names
- Display them in "👥 Detected Speakers"
- Auto-assign voices (male/female alternating)

### 3. Review Voice Assignment

In "🎙️ Voice Assignment":
- ALICE gets a female voice
- BOB gets a male voice
- (Optional) Change by selecting different voices

### 4. Generate MP3

Click **🎵 Generate MP3**

You'll see:
- Progress bar animating
- Status message "Generating audio..."
- Takes ~2-5 seconds

### 5. Download

Once generated, you'll see:
- ✅ Success message
- File details (name, duration, speakers)
- Audio preview player
- **⬇️ Download MP3** button

Click to download.

## Features Explained

### Auto-Detect Speakers

The tool looks for this pattern:
```
[SPEAKER_NAME] text
```

- Names must be in [UPPERCASE_BRACKETS]
- Names can have letters, numbers, underscores
- Text can span multiple paragraphs if next line starts with [SPEAKER]

### Voice Assignment

Voices available depend on your system:
- **Male voices** (usually indices 0, 2, 4)
- **Female voices** (usually indices 1, 3, 5)

Assign manually by selecting from dropdown.

### Progress Indicator

Shows real-time status:
- 10% - Starting engine
- 30% - Parsing dialogue
- 50% - Mixing audio
- 80% - Saving file
- 100% - Complete!

### Audio Preview

The embedded player lets you:
- Play the generated audio
- Pause/resume
- Volume control
- Seek through timeline

Perfect for checking quality before download.

### Recent Files

Keep track of generated files:
- Shows filename and timestamp
- Click to download again
- Prevents re-generation of same dialogue

## File Upload

### Upload .txt File

1. Click **📤 Load File**
2. Select a .txt file with your dialogue
3. Text automatically loads into textarea
4. Optionally click "Detect Speakers"
5. Generate as normal

### Supported Formats

Must be:
- Plain text (.txt)
- UTF-8 encoded
- Under 10 MB

### Example File

`sample_dialogue.txt`:
```
[JOHN] Hello, how are you today?
[SARAH] Hi John! I'm doing great, thanks for asking.
[JOHN] That's wonderful! What did you do this morning?
[SARAH] I went to the market and bought some fresh fruits.
```

## Tips & Tricks

### 1. Format Dialogue Correctly

✅ Correct:
```
[ALICE] Hello
[BOB] Hi there
```

❌ Wrong:
```
[alice] Hello  # lowercase
[Bob Smith] Hi there  # spaces in name
Alice: Hello  # no brackets
```

### 2. Improve Audio Quality

In browser console (F12), you can check:
- Generation time
- File size
- Audio duration

Longer dialogues = larger files.

### 3. Multiple Speakers

Use unique names for each character:
```
[DOCTOR] How are you feeling?
[PATIENT] I'm better now.
[NURSE] Time for your medication.
[DOCTOR] Let's check your vitals.
```

### 4. Batch Processing

Generate multiple dialogues:
1. Paste first dialogue
2. Generate and download
3. Clear textarea (button coming soon)
4. Paste next dialogue
5. Repeat

### 5. Speaker Preview

Can't preview individual speakers yet, but you can:
- Click "Detect Speakers" multiple times
- Dialogues auto-save to history
- Download again from history

## Troubleshooting

### "No speakers detected"

**Problem:** Dialogue format issue

**Solutions:**
- Use [UPPERCASE_NAMES]
- Remove special characters (except _ and numbers)
- Ensure [NAME] is followed by space and text

**Test:**
```
[JOHN] This works fine
[SARAH_JONES] Names with underscore work
[BOB123] Numbers too
```

### Audio sounds robotic

**Cause:** TTS engine limitation (expected)

**Improve:**
- Use shorter sentences
- Add natural punctuation
- Avoid complex words

### Download button not working

**Solution:**
- Try right-click → Save As
- Check browser download settings
- Verify output folder has permissions

### File too large

**Cause:** Long dialogue with many speakers

**Solution:**
- Split into multiple files
- Use shorter sentences
- Reduce bitrate in config.py

### Browser shows "Cannot reach server"

**Solution:**
- Verify server is running (`python tts-web.py`)
- Check port 5000 is not blocked
- Try `http://127.0.0.1:5000` instead of localhost

## REST API (For Developers)

The web version exposes REST APIs:

### Generate Audio
```
POST /api/generate
Content-Type: application/json

{
  "dialogue_text": "[JOHN] Hello\n[SARAH] Hi",
  "filename": "my_dialogue.mp3"  // optional
}

Response:
{
  "success": true,
  "filename": "dialogue_JOHN_SARAH_20240115.mp3",
  "speakers": ["JOHN", "SARAH"],
  "duration": 5,
  "filepath": "/path/to/file.mp3"
}
```

### Detect Speakers
```
POST /api/detect-speakers
Content-Type: application/json

{
  "dialogue_text": "[JOHN] Hello\n[SARAH] Hi"
}

Response:
{
  "success": true,
  "speakers": ["JOHN", "SARAH"],
  "count": 2
}
```

### Get Voices
```
GET /api/voices

Response:
{
  "success": true,
  "voices": [
    "0: David",
    "1: Nancy",
    "2: Will",
    "3: Zira",
    ...
  ]
}
```

### Download File
```
GET /api/download/{filename}

Returns: Audio file (MP3)
```

### Get History
```
GET /api/history

Response:
{
  "success": true,
  "history": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "filename": "dialogue_JOHN_SARAH_20240115_103000.mp3",
      "speakers": ["JOHN", "SARAH"],
      "duration": 5
    },
    ...
  ]
}
```

### Upload File
```
POST /api/upload
Content-Type: multipart/form-data

Body: file (binary)

Response:
{
  "success": true,
  "dialogue_text": "...",
  "filename": "sample.txt"
}
```

## Customization

### Change Port

Edit `config.py`:
```python
WEB_PORT = 5001  # Use port 5001 instead
```

Then start with:
```bash
python tts-web.py
```

### Adjust Speaking Rate

Edit `config.py`:
```python
TTS_RATE = 120  # Slower (words per minute)
TTS_RATE = 180  # Faster
```

### Change Voice Assignment Logic

Edit `tts_engine.py`, method `auto_assign_voices()`.

## Keyboard Shortcuts

Coming soon in v1.1!

---

**Enjoy generating English learning dialogues! 🎙️📚**
