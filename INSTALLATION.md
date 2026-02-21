# Installation Guide - TTS Tool

## ✅ Zero Complexity

This tool requires:
1. **Python 3.6+** (you likely have this)
2. **pip** (comes with Python)
3. **One dependency: gTTS**

That's it. No Rust, no heavy frameworks, no build tools needed.

---

## 🚀 Quick Start

### Windows Users

**Step 1:** Double-click `run.bat`

That's it! The app opens automatically.

### macOS/Linux Users

**Step 1:** Open terminal in this folder

**Step 2:** Run:
```bash
chmod +x run.sh
./run.sh
```

Or manually:
```bash
pip install gtts==2.5.3
python3 tts-simple.py
```

---

## 🔧 Manual Installation

If the quick start doesn't work:

### 1. Install gTTS
```bash
pip install gtts==2.5.3
```

### 2. Run the app
```bash
python3 tts-simple.py
```

### Troubleshooting

**"Command not found: pip"**
Try:
```bash
python3 -m pip install gtts==2.5.3
```

**"No module named 'tkinter'" (Linux)**
```bash
sudo apt-get install python3-tk
```

**macOS Tkinter issues:**
Tkinter comes with Python. If missing:
```bash
brew install python-tk
```

---

## ✨ Features

- ✅ Multi-speaker support ([SPEAKER] format)
- ✅ Auto voice variation
- ✅ Beautiful Tkinter GUI
- ✅ Background processing
- ✅ MP3 generation
- ✅ Easy file management

---

## 📝 Usage Example

### Input
```
[Alice] Hello, how are you?
[Bob] I'm great, thanks!
[Alice] That's wonderful!
```

### Output
- `output/dialogue.mp3` (ready to use)

---

## 🆘 Support

**Installation stuck?** Check:

1. Python version:
   ```bash
   python3 --version
   ```
   (Should be 3.6 or higher)

2. pip available:
   ```bash
   python3 -m pip --version
   ```

3. gTTS installed:
   ```bash
   python3 -c "import gtts; print('OK')"
   ```

4. Tkinter available:
   ```bash
   python3 -c "import tkinter; print('OK')"
   ```

---

## 💡 Pro Tips

- Paste `example_dialogue.txt` into the app to test
- Voice rotates automatically for variety
- Generated files are in the `output/` folder
- Edit `config.py` to customize settings

---

**Ready? Double-click `run.bat` or run `./run.sh`!**
