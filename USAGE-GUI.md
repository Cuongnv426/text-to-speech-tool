# Desktop GUI Version Usage Guide

Complete guide to the PyQt5 desktop application.

## Launching the Application

```bash
python tts-gui.py
```

A window titled "TTS Tool - English Learning" will open.

## Main Interface

The application has two main sections:

### Left Panel: Input & Configuration

- **Text Editor** - Type or paste dialogue
- **File Operations** - Open, clear, save
- **Speaker Detection** - Find speakers in text
- **Voice Assignment** - Choose voices for each speaker
- **Generate Button** - Create MP3
- **Progress Bar** - Shows generation status

### Right Panel: Output & History

- **Generation Result** - Details of generated audio
- **Audio Preview** - Play the generated MP3
- **Download/Save** - Export the file
- **Recent Files** - Quick access to previous outputs

## Getting Started

### 1. Load or Paste Dialogue

**Option A: Paste Text**
- Click in the text area on the left
- Paste your dialogue
- Example format:
```
[JOHN] Hello, how are you?
[SARAH] Hi! I'm doing great.
[JOHN] That's wonderful!
```

**Option B: Open File**
- Click **📂 Open File**
- Select a .txt file with your dialogue
- Text automatically loads

**Option C: Drag and Drop**
- Simply drag a .txt file into the window
- File content appears in text editor

### 2. Detect Speakers

Click **🔍 Detect Speakers**

The tool will:
- Scan for [SPEAKER_NAME] patterns
- List unique speakers (left panel)
- Create voice dropdown menus
- Auto-assign male/female voices

You'll see:
```
👥 Speakers
1. JOHN
2. SARAH
3. BOB

🎙️ Voice Assignment
JOHN:  [Dropdown] Voice 0: David (Male)
SARAH: [Dropdown] Voice 1: Nancy (Female)
BOB:   [Dropdown] Voice 0: David (Male)
```

### 3. Customize Voice Assignment (Optional)

Click any dropdown under "🎙️ Voice Assignment" to change:
- Voices for specific speakers
- Male to female or vice versa
- Example voices on your system

The tool shows:
```
0: David (Male)
1: Nancy (Female)
2: Will (Male)
3: Zira (Female)
...
```

### 4. Generate MP3

Click **🎵 Generate MP3** button

Progress:
- Progress bar fills from 0-100%
- Status shows: "Generating audio..."
- Time: 2-5 seconds for short dialogues

### 5. Preview & Download

After generation, the right panel shows:

**✅ Generation Result**
```
Filename: dialogue_JOHN_SARAH_20240115_103045.mp3
Duration: 42 seconds
Speakers: JOHN, SARAH
```

**Options:**
- **▶️ Preview Audio** - Play directly in application
- **⬇️ Download MP3** - Save to custom location
- **📁 Open Output Folder** - View generated files

## Menu & Button Guide

### File Operations

**📂 Open File**
- Opens file browser
- Select any .txt file
- Content loads into text editor
- Auto-detects dialogue format

**✏️ Clear**
- Empties the text editor
- Asks for confirmation
- Clears speaker list

**💾 Save Dialogue**
- Opens save dialog
- Save current text as .txt file
- Useful for saving edits before generation

### Speaker Detection

**🔍 Detect Speakers**
- Scans text for [SPEAKER_NAME] patterns
- Fills speakers list
- Creates voice dropdowns
- Must do this before generating

### Voice Assignment

Dropdown menus for each speaker:
- Select different voices
- See voice name and gender
- Changes apply immediately

### Generation

**🎵 Generate MP3**
- Creates audio file
- Shows progress bar
- Saves to output folder automatically
- Enables preview and download buttons

### Output Folder

**📁 Open Output Folder**
- Opens file manager showing generated files
- All MP3s saved here
- View, rename, delete files

### Recent Files

**History List** (bottom right)
- Shows last 20 generated files
- Shows filename, speakers, duration
- Click any file to:
  - Load it for preview
  - Download again
  - Delete from history

**🗑️ Clear History**
- Removes all files from recent list
- Does NOT delete actual MP3 files
- Asks for confirmation

## Step-by-Step Examples

### Example 1: Simple Conversation

1. **Paste Text:**
```
[ALICE] Good morning!
[BOB] Hi Alice! How are you?
[ALICE] I'm doing well. How about you?
[BOB] Great! Want to grab coffee?
[ALICE] Sure! Let's go to that cafe on Main Street.
```

2. **Click** "🔍 Detect Speakers"
   - ALICE detected as Female
   - BOB detected as Male

3. **Click** "🎵 Generate MP3"
   - Watch progress bar
   - Takes ~3 seconds

4. **Click** "▶️ Preview Audio"
   - Hear the dialogue
   - Check quality

5. **Click** "⬇️ Download MP3"
   - Choose save location
   - File saved

### Example 2: Restaurant Dialogue

1. **Click** "📂 Open File"
2. **Select** `examples/restaurant_dialogue.txt`
3. **Click** "🔍 Detect Speakers"
4. **Review voices** - Adjust if needed
5. **Click** "🎵 Generate MP3"
6. **Preview** then **Download**

### Example 3: Job Interview

1. **Load** `examples/job_interview.txt`
2. **Detect speakers** - INTERVIEWER, CANDIDATE
3. **Customize voices:**
   - INTERVIEWER → Professional male voice
   - CANDIDATE → Different male voice
4. **Generate** → Preview → Download

## Advanced Features

### Undo/Redo

Currently manual:
- Select all text (Ctrl+A)
- Paste new content
- Or use File → Open to reload

Coming in v1.1: Full undo/redo stack

### Speaker Preview

Preview before generating:
1. Type speaker's text
2. Select in dropdown
3. Right-click → "Preview Voice" (coming soon)

Currently: Generate full dialogue to preview.

### Drag & Drop

- Drag .txt file onto window
- Content automatically loads
- Detect speakers after drop

### Batch Processing (Manual)

1. **Load File 1** → **Detect** → **Generate** → **Download**
2. **Load File 2** → **Detect** → **Generate** → **Download**
3. Repeat for multiple files

Bulk batch processing coming in v1.1!

## Troubleshooting

### "No speakers detected"

**Check:**
- Text contains [SPEAKER_NAME] format
- Names are uppercase
- Names contain only letters, numbers, underscore
- Space after closing bracket

**Test:**
```
[JOHN] Hello  ✓ Works
[john] hello  ✗ Lowercase name
[John Doe] Hi ✗ Spaces in name
JOHN: Hello   ✗ Wrong format
```

### Application won't start

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyqt5
python tts-gui.py
```

**macOS:**
```bash
brew install pyqt@5
python tts-gui.py
```

**Windows:**
```bash
pip install --upgrade PyQt5
python tts-gui.py
```

### Audio generation is slow

**Normal times:**
- 10 sentences: 2-3 seconds
- 50 sentences: 10-15 seconds
- 100 sentences: 30-45 seconds

**To speed up:**
- Reduce dialogue length
- Split into multiple files
- Use shorter sentences

### Audio quality is poor

**Improve by:**
- Using shorter, simpler sentences
- Adding proper punctuation
- Avoiding special characters

**In config.py:**
```python
TTS_RATE = 120  # Slower = clearer
```

### Preview audio not playing

**Solutions:**
- Check system volume
- Verify file generated successfully
- Try downloading and playing externally
- Update audio drivers

### "Access Denied" on save

**Solution:**
- Choose different folder
- Check folder permissions
- Run as administrator (Windows)

### File too large after download

**Cause:** Long dialogue with many speakers

**Solutions:**
- Split dialogue into parts
- Reduce speaking rate (slower = smaller)
- Lower bitrate in config.py:
```python
AUDIO_FORMAT = {"bitrate": "128k"}  # From 192k
```

## Keyboard Shortcuts

Current shortcuts:
- **Ctrl+A** - Select all text
- **Ctrl+C** - Copy selected text
- **Ctrl+V** - Paste text
- **Ctrl+X** - Cut text

More shortcuts coming in v1.1!

## Configuration for Desktop App

Edit `config.py`:

```python
# Output folder
OUTPUT_FOLDER = Path.home() / "TTS_Output"

# Speaking rate
TTS_RATE = 150  # words per minute

# Voice volume
TTS_VOLUME = 1.0  # 0.0 to 1.0

# Pause between speakers
SPEAKER_PAUSE = 500  # milliseconds
```

Restart app to apply changes.

## Menu Structure

```
File
├── Open File (📂)
├── Save Dialogue (💾)
└── Clear (✏️)

Detect
├── Detect Speakers (🔍)

Generate
├── Generate MP3 (🎵)
└── [Progress bar]

Output
├── Preview Audio (▶️)
├── Download MP3 (⬇️)
├── Open Folder (📁)

History
├── Recent Files (list)
└── Clear History (🗑️)
```

## Tips for Best Results

### 1. Dialogue Format

Use clear format:
```
[CHARACTER_NAME] Their dialogue here.
[OTHER_CHARACTER] Response here.
```

### 2. Multiple Speakers

Works best with 2-4 speakers. More than 5 may sound cluttered.

### 3. Speaker Names

- Use clear, distinct names
- Avoid very similar names (Bob, Rob)
- CAN contain numbers/underscores: [PERSON_1], [JOHN_123]

### 4. Text Quality

- Use natural English
- Add punctuation (. ! ?)
- Short sentences work better than long ones
- Avoid abbreviations or acronyms

### 5. File Naming

When saving:
- Use descriptive names: `restaurant_scene_01.mp3`
- Include characters if relevant: `john_sarah_dialogue.mp3`
- Use date for organization: `dialogue_20240115.mp3`

## Keyboard Shortcuts (Coming Soon)

Planned for v1.1:
- **Ctrl+O** - Open file
- **Ctrl+S** - Save dialogue
- **Ctrl+D** - Detect speakers
- **Ctrl+G** - Generate MP3
- **Ctrl+P** - Preview audio
- **Ctrl+L** - Download
- **Ctrl+K** - Clear history

## Privacy & Storage

- **All files saved locally** on your computer
- **No uploads to servers** (desktop version)
- **Output folder:** `~/(user)/TTS_Output/`
- **History file:** `gui_history.json` in app directory
- **All data private** - nothing shared

---

**Start creating English learning dialogues today! 🎙️📚**
