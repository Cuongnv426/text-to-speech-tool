# Troubleshooting Guide

Solutions to common issues with the TTS Tool.

## Installation Issues

### "ModuleNotFoundError: No module named 'pyttsx3'"

**Problem:** Python packages not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

If still failing:
```bash
pip install pyttsx3==2.90 --force-reinstall
```

---

### "No module named 'PyQt5'"

**Problem:** PyQt5 not installed (for desktop version).

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyqt5
```

**macOS:**
```bash
brew install pyqt@5
```

**Windows:**
```bash
pip install PyQt5==5.15.9 --force-reinstall
```

---

### "FFmpeg not found"

**Problem:** Audio processing library missing.

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add to PATH (Environment Variables)
4. Verify: `ffmpeg -version`

---

### "pip command not found"

**Problem:** pip not installed or not in PATH.

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pip
```

**macOS:**
```bash
sudo easy_install pip
# or
brew install python3
```

**Windows:**
- Reinstall Python 3.8+
- Check "Add Python to PATH" during installation

---

## Startup Issues

### Web Version - "Address already in use"

**Problem:** Port 5000 already in use.

**Solution 1 - Use different port:**
Edit `config.py`:
```python
WEB_PORT = 5001  # or any free port
```

**Solution 2 - Find what's using port 5000:**

```bash
# Linux/macOS
lsof -i :5000
# Kill process:
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
# taskkill /PID <PID> /F
```

---

### Web Version - "Cannot GET /"

**Problem:** Browser can't reach server.

**Check:**
1. Is server running? (`python tts-web.py`)
2. Wait 2-3 seconds after starting
3. Try `http://127.0.0.1:5000` instead of localhost
4. Check firewall isn't blocking port 5000
5. Try different port in config.py

---

### Desktop Version - "QXcbConnection: Could not connect to display"

**Problem:** No graphical display (running on server/SSH).

**Solution:**

```bash
export QT_QPA_PLATFORM=offscreen
python tts-gui.py
```

Or use web version instead:
```bash
python tts-web.py
```

---

### Desktop Version - Window won't appear

**Problem:** Application started but window hidden.

**Solution:**

**Windows:**
```bash
python tts-gui.py
```
Check taskbar or try Alt+Tab.

**Linux:**
```bash
python tts-gui.py &
wmctrl -a "TTS Tool"
```

**macOS:**
```bash
python tts-gui.py
# Then click the app in Dock
```

---

## Dialogue Format Issues

### "No speakers detected"

**Problem:** Dialogue not recognized.

**Check format:**

❌ Wrong:
```
john: Hello
[john] Hello
JOHN hello
[JOHN]Hello
```

✓ Correct:
```
[JOHN] Hello
[SARAH] Hi
```

**Solution:**
- Use [UPPERCASE_NAMES]
- Space after closing bracket
- Text on same line

---

### Some speakers not detected

**Problem:** Inconsistent naming.

**Check for:**
- Case inconsistency: `[JOHN]` vs `[john]`
- Typos: `[JAHN]` vs `[JOHN]`
- Extra spaces: `[JOHN ]` vs `[JOHN]`

**Solution:**
Use exactly the same name every time:
```
[JOHN] Hello  ✓
[JOHN] Hi     ✓
[john] Hello  ✗ Different!
```

---

### Spaces in speaker names

**Problem:** `[JOHN SMITH]` not recognized properly.

**Solution:**
Use underscores instead:
```
[JOHN_SMITH] Hello  ✓
[John_Smith] Hello  ✓
[JOHN SMITH] Hello  ✗ Might fail
```

---

### Special characters in names

**Problem:** `[DR. JOHN]` or `[JOHN-DOE]`

**Solution:**
Remove special characters:
```
[DR_JOHN] Hello     ✓
[DRJOHN] Hello      ✓
[JOHNSMITH] Hello   ✓
[DR. JOHN] Hello    ✗ Avoid periods
[JOHN-DOE] Hello    ✗ Avoid hyphens
```

---

## Generation Issues

### Audio generation is very slow

**Normal times:**
- 10 sentences: 2-3 seconds
- 50 sentences: 10-15 seconds
- 100 sentences: 30-45 seconds

**If much slower:**

**Check:**
1. System CPU usage (might be slow machine)
2. Drive space available
3. Try shorter dialogue (10 lines)

**Speed up:**
```python
# In config.py, reduce pauses:
SPEAKER_PAUSE = 300  # From 500 ms
TTS_RATE = 180       # Faster speaking
```

---

### "ERROR: Could not generate audio"

**Problem:** Audio generation failed.

**Solutions:**

1. **Check text format:**
   ```
   [JOHN] Valid text here
   [SARAH] Valid response
   ```

2. **Check file size:**
   - Web: max 10 MB
   - Desktop: large files may fail

3. **Try shorter dialogue** (5-10 lines)

4. **Check FFmpeg installed:**
   ```bash
   ffmpeg -version
   ```

5. **Try web version** if GUI fails

6. **Check logs:**
   ```bash
   python tts-web.py 2>&1 | tail -20
   ```

---

### "File not found" error

**Problem:** Can't find generated MP3.

**Check:**
```bash
ls -la /root/clawd/text-to-speech/output/
```

**Solution:**
- Output folder might be missing
- Create it: `mkdir -p output/`
- Check folder permissions

---

### File too large

**Problem:** Generated MP3 is huge.

**Cause:** Long dialogue, high bitrate.

**Solution 1 - Reduce bitrate:**
Edit `config.py`:
```python
AUDIO_FORMAT = {
    "bitrate": "128k"  # From 192k
}
```

**Solution 2 - Split dialogue:**
Create multiple shorter files instead.

**Solution 3 - Compress after generation:**
```bash
ffmpeg -i original.mp3 -b:a 128k compressed.mp3
```

---

## Audio Quality Issues

### Audio sounds robotic/mechanical

**Expected behavior:** TTS always sounds somewhat synthetic.

**Improve quality:**

1. **Use clearer text:**
   ```
   [JOHN] Hello, how are you?  ✓ Clear
   [JOHN] H-e-l-l-o            ✗ Robotic
   ```

2. **Add punctuation:**
   ```
   [JOHN] Hello! How are you?  ✓
   [JOHN] Hello how are you     ✗
   ```

3. **Shorter sentences:**
   ```
   [JOHN] Hi there! How are you?          ✓
   [JOHN] Hi there how are you today ok   ✗
   ```

4. **Avoid acronyms:**
   ```
   [JOHN] This is very important     ✓
   [JOHN] This is VI                  ✗
   ```

---

### Audio cuts off or is incomplete

**Problem:** Last speaker doesn't finish.

**Solution:**
- Add a final line: `[SPEAKER] Thank you!`
- Try regenerating
- Check file isn't corrupted

---

### Audio is too quiet

**Solution:**
Increase volume in `config.py`:
```python
TTS_VOLUME = 1.2  # From 1.0 (might distort)
TTS_VOLUME = 1.0  # Or try external amplification
```

---

### Audio plays in browser but won't download

**Web version issue:**

**Solution:**
1. Try right-click → Save As
2. Check browser download settings
3. Disable ad blockers
4. Try different browser
5. Check disk space

---

## Browser/Web Version Issues

### Page shows blank/white screen

**Problem:** Web interface not loading.

**Check:**
1. Server running? (`python tts-web.py`)
2. Wait 3 seconds after starting
3. No JavaScript errors (F12 → Console)
4. Try hard refresh (Ctrl+Shift+R)

**Solution:**
```bash
# Restart server
python tts-web.py

# Check logs
tail -f server.log
```

---

### Upload button not working

**Problem:** Can't upload .txt file.

**Solutions:**
1. Check file size < 10 MB
2. Check file is plain text (.txt)
3. Try Web Version directly:
   ```bash
   curl -X POST -F "file=@myfile.txt" http://localhost:5000/api/upload
   ```

---

### Voice dropdown showing wrong voices

**Problem:** Voice list not loading.

**Solution:**
1. Refresh page (F5)
2. Check browser console (F12)
3. Restart server: `python tts-web.py`

---

### History not saving

**Problem:** Recent files disappear.

**Check:**
```bash
ls -la /root/clawd/text-to-speech/generation_history.json
```

**Solution:**
- Check folder permissions
- Manually create file:
  ```bash
  echo "[]" > generation_history.json
  chmod 666 generation_history.json
  ```

---

## Desktop Version Issues

### Window appears but buttons don't work

**Problem:** UI not responsive.

**Solution:**
1. Wait a moment (TTS engine initializing)
2. Restart app: `python tts-gui.py`
3. Check Python version: `python --version` (needs 3.8+)

---

### Drag-drop not working

**Problem:** Can't drag .txt file into window.

**Solution:**
1. Use "📂 Open File" button instead
2. Drag file to specific area (main window)
3. Try different file manager

---

### Recent files history empty

**Check file:**
```bash
cat gui_history.json
```

**Clear and reset:**
```bash
echo "[]" > gui_history.json
```

---

### Preview audio won't play

**Problem:** Player doesn't work.

**Solution:**
1. Check system volume
2. Try downloading and playing externally
3. Check audio drivers installed
4. Try: `speaker-test -t sine -f 1000 -l 1` (Linux)

---

## Permission Issues

### "Permission denied" on output folder

**Problem:** Can't write to output folder.

**Solution:**
```bash
# Fix permissions
chmod 755 /root/clawd/text-to-speech/output
chmod 755 /root/clawd/text-to-speech

# Or change output folder in config.py:
OUTPUT_FOLDER = Path.home() / "TTS_Output"
```

---

### "Access denied" saving file

**Windows issue:**

**Solution:**
1. Run as Administrator
2. Choose different save location
3. Check antivirus isn't blocking

---

## Performance Issues

### Slow generation on first run

**Expected:** First run initializes TTS engine (10-30 seconds).

**Subsequent runs are faster.**

---

### CPU usage very high

**Normal:** CPU peaks during generation.

**If sustained high:**
1. Close other apps
2. Try shorter dialogues first
3. Update OS and drivers

---

### Memory issues / Out of RAM

**Problem:** App crashes with "MemoryError".

**Solution:**
1. Reduce dialogue length
2. Close other applications
3. Increase swap space (Linux)
4. Restart computer

---

## Getting Help

### Report Bugs

Include:
1. Error message (exact text)
2. What you were doing
3. Dialogue text (if safe to share)
4. System info: `python --version`, `ffmpeg -version`
5. Operating system

### Enable Debug Logging

```bash
# Web version
DEBUG=1 python tts-web.py 2>&1 | tee debug.log

# Desktop version
# Check console output for errors
```

### Check System

```bash
# Python version
python --version

# FFmpeg
ffmpeg -version

# Available voices
python -c "from tts_engine import get_tts_engine; engine = get_tts_engine(); print(engine.list_voices())"

# Disk space
df -h /root/clawd/text-to-speech

# RAM available
free -h  # Linux
vm_stat  # macOS
```

---

## Common Workflows

### "Everything is broken"

1. Verify installation:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

2. Test TTS engine:
   ```bash
   python -c "from tts_engine import get_tts_engine; print('OK')"
   ```

3. Start fresh:
   ```bash
   rm -rf output/ gui_history.json generation_history.json
   mkdir output/
   ```

4. Try again with simple dialogue:
   ```
   [TEST] Hello world
   [TEST2] Hi there
   ```

### Using Web Version Instead of GUI

If GUI has issues:
```bash
python tts-web.py
# Open http://localhost:5000
```

Web version is more stable.

---

**Still having issues? Check the detailed docs or create an issue on GitHub! 🐛→✅**
