# API Reference

Complete API documentation for developers integrating with the TTS Tool.

## Core TTS Engine (`tts_engine.py`)

The core engine handles all text-to-speech operations.

### TTSEngine Class

Main class for TTS operations.

#### Initialization

```python
from tts_engine import get_tts_engine

engine = get_tts_engine()
```

#### Methods

##### `detect_speakers(dialogue_text: str) -> List[str]`

Extract unique speaker names from dialogue text.

**Parameters:**
- `dialogue_text` (str): Text with [SPEAKER_NAME] markers

**Returns:**
- `List[str]`: List of unique speaker names in order of appearance

**Example:**
```python
text = "[JOHN] Hello\n[SARAH] Hi there"
speakers = engine.detect_speakers(text)
# Returns: ['JOHN', 'SARAH']
```

---

##### `parse_dialogue(dialogue_text: str) -> List[Tuple[str, str]]`

Parse dialogue into (speaker, text) tuples.

**Parameters:**
- `dialogue_text` (str): Text with [SPEAKER_NAME] markers

**Returns:**
- `List[Tuple[str, str]]`: List of (speaker_name, text) tuples

**Example:**
```python
text = "[JOHN] Hello\n[SARAH] Hi"
lines = engine.parse_dialogue(text)
# Returns: [('JOHN', 'Hello'), ('SARAH', 'Hi')]
```

---

##### `list_voices() -> List[str]`

Get list of available voices on the system.

**Returns:**
- `List[str]`: Voice descriptions with index (e.g., "0: David", "1: Nancy")

**Example:**
```python
voices = engine.list_voices()
for voice in voices:
    print(voice)
# Output:
# 0: David
# 1: Nancy
# 2: Will
```

---

##### `auto_assign_voices(speakers: List[str], male_voice_ids: List[int] = None, female_voice_ids: List[int] = None) -> Dict[str, int]`

Automatically assign voices to speakers (alternating male/female).

**Parameters:**
- `speakers` (List[str]): List of speaker names
- `male_voice_ids` (List[int], optional): List of male voice indices
- `female_voice_ids` (List[int], optional): List of female voice indices

**Returns:**
- `Dict[str, int]`: Mapping of speaker names to voice IDs

**Example:**
```python
speakers = ['JOHN', 'SARAH', 'BOB']
voices = engine.auto_assign_voices(speakers)
# Returns: {'JOHN': 0, 'SARAH': 1, 'BOB': 0}

# Custom voice selection
voices = engine.auto_assign_voices(
    speakers,
    male_voice_ids=[0, 2],
    female_voice_ids=[1, 3, 5]
)
```

---

##### `preview_speaker(text: str, voice_id: int) -> AudioSegment`

Generate audio preview for a single speaker.

**Parameters:**
- `text` (str): Text to convert to speech
- `voice_id` (int): Voice index

**Returns:**
- `AudioSegment`: pydub AudioSegment object

**Example:**
```python
audio = engine.preview_speaker("Hello world", 0)
audio.export("preview.wav", format="wav")
```

---

##### `mix_dialogue(dialogue_lines: List[Tuple[str, str]], speaker_voices: Dict[str, int], pause_duration: int = 500) -> AudioSegment`

Mix multiple audio segments into a single dialogue.

**Parameters:**
- `dialogue_lines` (List[Tuple[str, str]]): List of (speaker, text) tuples
- `speaker_voices` (Dict[str, int]): Mapping of speakers to voice IDs
- `pause_duration` (int, optional): Pause between speakers in milliseconds

**Returns:**
- `AudioSegment`: Mixed audio

**Example:**
```python
lines = [('JOHN', 'Hello'), ('SARAH', 'Hi there')]
voices = {'JOHN': 0, 'SARAH': 1}
audio = engine.mix_dialogue(lines, voices, pause_duration=500)
```

---

##### `generate_dialogue_mp3(dialogue_text: str, output_filename: str = None, speaker_voices: Dict[str, int] = None) -> Tuple[str, AudioSegment]`

Complete workflow: Parse dialogue, mix audio, and save to MP3.

**Parameters:**
- `dialogue_text` (str): Text with [SPEAKER_NAME] markers
- `output_filename` (str, optional): Output filename (auto-generated if None)
- `speaker_voices` (Dict[str, int], optional): Voice assignment (auto-assigned if None)

**Returns:**
- `Tuple[str, AudioSegment]`: (filepath, audio) tuple

**Raises:**
- `ValueError`: If no valid dialogue found

**Example:**
```python
dialogue = "[JOHN] Hello\n[SARAH] Hi"
filepath, audio = engine.generate_dialogue_mp3(
    dialogue,
    output_filename="greeting.mp3"
)
print(f"Saved to: {filepath}")
print(f"Duration: {len(audio)/1000:.1f} seconds")
```

---

##### `save_audio(audio: AudioSegment, filename: str, format: str = "mp3") -> str`

Save audio to file.

**Parameters:**
- `audio` (AudioSegment): Audio to save
- `filename` (str): Output filename
- `format` (str, optional): Audio format (mp3, wav, ogg, etc.)

**Returns:**
- `str`: Path to saved file

**Example:**
```python
audio = engine.generate_speech("Hello", 0)
filepath = engine.save_audio(audio, "hello.mp3", format="mp3")
```

---

## Web API (FastAPI)

REST endpoints for the web version.

### Generate MP3

**Endpoint:** `POST /api/generate`

**Request:**
```json
{
  "dialogue_text": "[JOHN] Hello\n[SARAH] Hi",
  "filename": "dialogue.mp3"  // optional
}
```

**Response (Success):**
```json
{
  "success": true,
  "filename": "dialogue_JOHN_SARAH_20240115.mp3",
  "filepath": "/path/to/output/dialogue.mp3",
  "speakers": ["JOHN", "SARAH"],
  "duration": 10,
  "message": "MP3 generated successfully"
}
```

**Response (Error):**
```json
{
  "detail": "No dialogue provided"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"dialogue_text": "[JOHN] Hello\n[SARAH] Hi"}'
```

---

### Detect Speakers

**Endpoint:** `POST /api/detect-speakers`

**Request:**
```json
{
  "dialogue_text": "[JOHN] Hello\n[SARAH] Hi"
}
```

**Response:**
```json
{
  "success": true,
  "speakers": ["JOHN", "SARAH"],
  "count": 2
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/detect-speakers \
  -H "Content-Type: application/json" \
  -d '{"dialogue_text": "[JOHN] Hello\n[SARAH] Hi"}'
```

---

### Get Available Voices

**Endpoint:** `GET /api/voices`

**Response:**
```json
{
  "success": true,
  "voices": [
    "0: David",
    "1: Nancy",
    "2: Will",
    "3: Zira"
  ]
}
```

**Example (curl):**
```bash
curl http://localhost:5000/api/voices
```

---

### Download File

**Endpoint:** `GET /api/download/{filename}`

**Parameters:**
- `filename` (str): Name of the MP3 file

**Response:** Binary MP3 file

**Example (curl):**
```bash
curl -o output.mp3 http://localhost:5000/api/download/dialogue.mp3
```

---

### Get Generation History

**Endpoint:** `GET /api/history`

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "filename": "dialogue_JOHN_SARAH_20240115.mp3",
      "speakers": ["JOHN", "SARAH"],
      "duration": 10
    },
    ...
  ]
}
```

**Example (curl):**
```bash
curl http://localhost:5000/api/history
```

---

### Upload File

**Endpoint:** `POST /api/upload`

**Request:** Multipart form with file

**Response:**
```json
{
  "success": true,
  "dialogue_text": "...",
  "filename": "sample.txt"
}
```

**Example (curl):**
```bash
curl -F "file=@dialogue.txt" http://localhost:5000/api/upload
```

---

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Configuration (`config.py`)

Configuration options for customization.

### Web Server Settings

```python
WEB_HOST = "0.0.0.0"      # Listening address
WEB_PORT = 5000           # Port number
WEB_DEBUG = False         # Debug mode
```

### TTS Engine Settings

```python
TTS_ENGINE = "pyttsx3"    # Engine choice
TTS_RATE = 150            # Speaking rate (words/min)
TTS_VOLUME = 1.0          # Volume (0.0-1.0)
```

### Voice Configuration

```python
VOICE_PRESETS = {
    "male": [0, 2, 4],      # Male voice indices
    "female": [1, 3, 5],    # Female voice indices
    "default": 0
}
```

### Audio Format

```python
AUDIO_FORMAT = {
    "sample_rate": 44100,   # Hz
    "channels": 1,          # Mono
    "bitrate": "192k",      # MP3 bitrate
}
```

### Other Settings

```python
SPEAKER_PAUSE = 500       # Pause between speakers (ms)
MAX_UPLOAD_SIZE = 10485760  # 10 MB
OUTPUT_FOLDER = Path(__file__).parent / "output"
```

---

## Python Examples

### Simple Script

```python
from tts_engine import get_tts_engine

# Initialize engine
engine = get_tts_engine()

# Dialogue text
dialogue = """
[ALICE] Good morning! How are you?
[BOB] Hi Alice! I'm doing well, thanks for asking.
[ALICE] That's great! Want to get coffee?
[BOB] Sure! Let's go to our favorite cafe.
"""

# Generate MP3
filepath, audio = engine.generate_dialogue_mp3(dialogue)
print(f"Generated: {filepath}")
print(f"Duration: {len(audio)/1000:.1f} seconds")
```

### Batch Processing

```python
from pathlib import Path
from tts_engine import get_tts_engine

engine = get_tts_engine()

# Process all .txt files in examples/
for txt_file in Path("examples").glob("*.txt"):
    print(f"Processing: {txt_file.name}")
    
    with open(txt_file) as f:
        dialogue = f.read()
    
    # Generate MP3
    filepath, audio = engine.generate_dialogue_mp3(dialogue)
    print(f"  → {filepath}")
```

### Custom Voice Assignment

```python
from tts_engine import get_tts_engine

engine = get_tts_engine()

dialogue = "[JOHN] Hello\n[SARAH] Hi"

# Custom voices
speaker_voices = {
    "JOHN": 0,      # First available voice
    "SARAH": 1      # Second available voice
}

filepath, audio = engine.generate_dialogue_mp3(
    dialogue,
    output_filename="custom_voices.mp3",
    speaker_voices=speaker_voices
)
```

### Web Client Example

```python
import requests

API_URL = "http://localhost:5000"

# Generate MP3
response = requests.post(
    f"{API_URL}/api/generate",
    json={
        "dialogue_text": "[JOHN] Hello\n[SARAH] Hi",
        "filename": "test.mp3"
    }
)

result = response.json()
print(f"Generated: {result['filename']}")

# Download file
download_response = requests.get(
    f"{API_URL}/api/download/{result['filename']}"
)

with open("output.mp3", "wb") as f:
    f.write(download_response.content)
```

---

## Error Handling

### Python API

```python
from tts_engine import get_tts_engine

engine = get_tts_engine()

try:
    filepath, audio = engine.generate_dialogue_mp3(dialogue_text)
except ValueError as e:
    print(f"Format error: {e}")
except Exception as e:
    print(f"Generation error: {e}")
```

### Web API

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (invalid input)
- `404` - File not found
- `500` - Server error

**Error Response:**
```json
{
  "detail": "Error message"
}
```

---

## Performance Tips

### For Large Dialogues

```python
# Increase pause for clarity
audio = engine.mix_dialogue(
    lines,
    voices,
    pause_duration=1000  # 1 second pause
)
```

### For Faster Processing

```python
# Reduce speaking rate (takes less time)
engine.engine.setProperty('rate', 200)
```

### Batch with Threading

```python
from concurrent.futures import ThreadPoolExecutor

def process_file(filepath):
    with open(filepath) as f:
        return engine.generate_dialogue_mp3(f.read())

files = list(Path("examples").glob("*.txt"))

with ThreadPoolExecutor(max_workers=2) as executor:
    results = executor.map(process_file, files)
```

---

## Dependencies

Core dependencies:

- **pyttsx3** - Text-to-speech library
- **pydub** - Audio processing
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **PyQt5** - Desktop GUI (optional)

---

## Version Information

- **Version:** 1.0
- **Python:** 3.8+
- **Last Updated:** January 2024

---

**For more information, see README.md and other documentation files.**
