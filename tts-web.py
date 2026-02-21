"""
Web version of TTS Tool using FastAPI
Run: python tts-web.py
Access: http://localhost:5000
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import Optional
import logging
from datetime import datetime
from pydantic import BaseModel

from tts_engine import get_tts_engine
from config import OUTPUT_FOLDER, WEB_HOST, WEB_PORT

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TTS Tool", description="Text-to-Speech for English Learning")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
PROJECT_ROOT = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")

# History file
HISTORY_FILE = PROJECT_ROOT / "generation_history.json"


class GenerateRequest(BaseModel):
    """Request model for generation"""
    dialogue_text: str
    filename: Optional[str] = None


def load_history() -> list:
    """Load generation history"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_history(history: list):
    """Save generation history"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def add_to_history(filename: str, speakers: list, duration: int):
    """Add entry to history"""
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "filename": filename,
        "speakers": speakers,
        "duration": duration
    })
    # Keep only last 50 entries
    history = history[-50:]
    save_history(history)


@app.get("/")
async def read_root():
    """Serve index.html"""
    index_path = PROJECT_ROOT / "templates" / "index.html"
    return FileResponse(index_path)


@app.post("/api/generate")
async def generate_audio(request: GenerateRequest):
    """
    Generate MP3 from dialogue text
    
    Request body:
    {
        "dialogue_text": "[JOHN] Hello...",
        "filename": "dialogue.mp3"  # optional
    }
    """
    try:
        if not request.dialogue_text or not request.dialogue_text.strip():
            raise HTTPException(status_code=400, detail="No dialogue provided")
        
        engine = get_tts_engine()
        
        # Generate MP3
        output_path, audio = engine.generate_dialogue_mp3(
            request.dialogue_text,
            request.filename
        )
        
        # Get metadata
        speakers = engine.detect_speakers(request.dialogue_text)
        duration = int(len(audio) / 1000)  # Convert ms to seconds
        filename = Path(output_path).name
        
        # Add to history
        add_to_history(filename, speakers, duration)
        
        return JSONResponse({
            "success": True,
            "filename": filename,
            "filepath": output_path,
            "speakers": speakers,
            "duration": duration,
            "message": "MP3 generated successfully"
        })
    
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voices")
async def get_voices():
    """Get list of available voices"""
    try:
        engine = get_tts_engine()
        voices = engine.list_voices()
        return JSONResponse({
            "success": True,
            "voices": voices
        })
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/detect-speakers")
async def detect_speakers(request: GenerateRequest):
    """Detect speakers in dialogue"""
    try:
        engine = get_tts_engine()
        speakers = engine.detect_speakers(request.dialogue_text)
        
        return JSONResponse({
            "success": True,
            "speakers": speakers,
            "count": len(speakers)
        })
    except Exception as e:
        logger.error(f"Error detecting speakers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history():
    """Get generation history"""
    try:
        history = load_history()
        return JSONResponse({
            "success": True,
            "history": history
        })
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download generated MP3"""
    try:
        filepath = OUTPUT_FOLDER / filename
        
        if not filepath.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a dialogue text file
    """
    try:
        contents = await file.read()
        dialogue_text = contents.decode('utf-8')
        
        if not dialogue_text.strip():
            raise HTTPException(status_code=400, detail="File is empty")
        
        return JSONResponse({
            "success": True,
            "dialogue_text": dialogue_text,
            "filename": file.filename
        })
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*60}")
    print("TTS Tool - Web Version")
    print(f"{'='*60}")
    print(f"Starting server on http://{WEB_HOST}:{WEB_PORT}")
    print(f"Open in browser: http://localhost:{WEB_PORT}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        app,
        host=WEB_HOST,
        port=WEB_PORT,
        log_level="info"
    )
