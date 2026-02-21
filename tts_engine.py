"""
Core Text-to-Speech Engine
Handles speech generation, speaker detection, and audio mixing
"""
import re
import io
import pyttsx3
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import wave
from pydub import AudioSegment
from config import (
    OUTPUT_FOLDER, TTS_RATE, TTS_VOLUME, 
    SPEAKER_PAUSE, VOICE_PRESETS, TTS_ENGINE
)


class TTSEngine:
    """Main TTS Engine for dialogue processing"""
    
    def __init__(self):
        """Initialize the TTS engine"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', TTS_RATE)
        self.engine.setProperty('volume', TTS_VOLUME)
        self._available_voices = self._get_voices()
        
    def _get_voices(self) -> List[Dict]:
        """Get available voices on the system"""
        voices = self.engine.getProperty('voices')
        return voices
    
    def list_voices(self) -> List[str]:
        """Return list of available voice IDs and names"""
        voices = self.engine.getProperty('voices')
        voice_list = []
        for idx, voice in enumerate(voices):
            voice_list.append(f"{idx}: {voice.name}")
        return voice_list
    
    def detect_speakers(self, dialogue_text: str) -> List[str]:
        """
        Detect speakers from dialogue text in format [SPEAKER_NAME]
        
        Args:
            dialogue_text: Text with [SPEAKER_NAME] markers
            
        Returns:
            List of unique speaker names in order of appearance
        """
        # Pattern to match [SPEAKER_NAME]
        pattern = r'\[([A-Z][A-Za-z0-9_]*)\]'
        speakers = []
        seen = set()
        
        for match in re.finditer(pattern, dialogue_text):
            speaker = match.group(1)
            if speaker not in seen:
                speakers.append(speaker)
                seen.add(speaker)
        
        return speakers
    
    def parse_dialogue(self, dialogue_text: str) -> List[Tuple[str, str]]:
        """
        Parse dialogue into (speaker, text) tuples
        
        Args:
            dialogue_text: Text with [SPEAKER_NAME] markers
            
        Returns:
            List of (speaker_name, text) tuples
        """
        pattern = r'\[([A-Z][A-Za-z0-9_]*)\]\s*(.*?)(?=\[|$)'
        dialogue_lines = []
        
        for match in re.finditer(pattern, dialogue_text, re.DOTALL):
            speaker = match.group(1)
            text = match.group(2).strip()
            if text:  # Only add non-empty text
                dialogue_lines.append((speaker, text))
        
        return dialogue_lines
    
    def _generate_audio_segment(self, text: str, voice_id: int) -> AudioSegment:
        """
        Generate audio for text using specified voice
        
        Args:
            text: Text to convert to speech
            voice_id: Voice index to use
            
        Returns:
            AudioSegment object
        """
        try:
            # Set voice
            voices = self.engine.getProperty('voices')
            if 0 <= voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
            
            # Generate audio to bytes
            audio_buffer = io.BytesIO()
            self.engine.save_to_file(text, str(audio_buffer))
            self.engine.runAndWait()
            
            # Since pyttsx3 save_to_file saves to a file, we need a workaround
            # Generate to a temporary file and read it
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp_path = tmp.name
            
            self.engine.save_to_file(text, tmp_path)
            self.engine.runAndWait()
            
            audio = AudioSegment.from_wav(tmp_path)
            Path(tmp_path).unlink()  # Clean up temp file
            
            return audio
        
        except Exception as e:
            print(f"Error generating audio: {e}")
            return AudioSegment.silent(duration=500)
    
    def mix_dialogue(
        self, 
        dialogue_lines: List[Tuple[str, str]], 
        speaker_voices: Dict[str, int],
        pause_duration: int = SPEAKER_PAUSE
    ) -> AudioSegment:
        """
        Mix multiple audio segments into a single dialogue
        
        Args:
            dialogue_lines: List of (speaker, text) tuples
            speaker_voices: Dict mapping speaker names to voice IDs
            pause_duration: Pause between speakers (milliseconds)
            
        Returns:
            Mixed AudioSegment
        """
        mixed_audio = AudioSegment.silent(duration=0)
        
        for speaker, text in dialogue_lines:
            # Get voice for this speaker
            voice_id = speaker_voices.get(speaker, 0)
            
            # Generate audio
            speaker_audio = self._generate_audio_segment(text, voice_id)
            
            # Add pause after this speaker (except for last line)
            if (speaker, text) != dialogue_lines[-1]:
                pause = AudioSegment.silent(duration=pause_duration)
                mixed_audio += speaker_audio + pause
            else:
                mixed_audio += speaker_audio
        
        return mixed_audio
    
    def auto_assign_voices(
        self, 
        speakers: List[str], 
        male_voice_ids: Optional[List[int]] = None,
        female_voice_ids: Optional[List[int]] = None
    ) -> Dict[str, int]:
        """
        Automatically assign voices to speakers (alternating male/female)
        
        Args:
            speakers: List of speaker names
            male_voice_ids: List of male voice IDs
            female_voice_ids: List of female voice IDs
            
        Returns:
            Dict mapping speaker names to voice IDs
        """
        if male_voice_ids is None:
            male_voice_ids = VOICE_PRESETS.get("male", [0, 2, 4])
        if female_voice_ids is None:
            female_voice_ids = VOICE_PRESETS.get("female", [1, 3, 5])
        
        speaker_voices = {}
        available_voices = self.engine.getProperty('voices')
        
        # Clamp voice IDs to available voices
        male_voice_ids = [v for v in male_voice_ids if v < len(available_voices)]
        female_voice_ids = [v for v in female_voice_ids if v < len(available_voices)]
        
        # If no specific voices available, use what we have
        if not male_voice_ids and not female_voice_ids:
            male_voice_ids = [0]
            female_voice_ids = [1] if len(available_voices) > 1 else [0]
        
        for idx, speaker in enumerate(speakers):
            # Alternate between male and female
            if idx % 2 == 0:
                voice_list = male_voice_ids
            else:
                voice_list = female_voice_ids
            
            # Cycle through voices in the list
            voice_id = voice_list[idx % len(voice_list)]
            speaker_voices[speaker] = voice_id
        
        return speaker_voices
    
    def generate_dialogue_mp3(
        self,
        dialogue_text: str,
        output_filename: Optional[str] = None,
        speaker_voices: Optional[Dict[str, int]] = None
    ) -> Tuple[str, AudioSegment]:
        """
        Generate MP3 from dialogue text
        
        Args:
            dialogue_text: Text with [SPEAKER_NAME] markers
            output_filename: Output filename (auto-generated if None)
            speaker_voices: Voice assignment dict (auto-assigned if None)
            
        Returns:
            Tuple of (filepath, AudioSegment)
        """
        # Parse dialogue
        dialogue_lines = self.parse_dialogue(dialogue_text)
        if not dialogue_lines:
            raise ValueError("No valid dialogue found. Use format: [SPEAKER] Text")
        
        # Detect speakers
        speakers = self.detect_speakers(dialogue_text)
        
        # Auto-assign voices if not provided
        if speaker_voices is None:
            speaker_voices = self.auto_assign_voices(speakers)
        
        # Mix audio
        mixed_audio = self.mix_dialogue(dialogue_lines, speaker_voices)
        
        # Generate filename if not provided
        if output_filename is None:
            speakers_str = "_".join(speakers[:3])  # Use first 3 speakers
            output_filename = f"dialogue_{speakers_str}.mp3"
        
        # Save to file
        output_path = OUTPUT_FOLDER / output_filename
        mixed_audio.export(str(output_path), format="mp3", bitrate="192k")
        
        return str(output_path), mixed_audio
    
    def preview_speaker(self, text: str, voice_id: int) -> AudioSegment:
        """
        Generate preview audio for a single speaker
        
        Args:
            text: Text to speak
            voice_id: Voice ID
            
        Returns:
            AudioSegment
        """
        return self._generate_audio_segment(text, voice_id)
    
    def save_audio(
        self, 
        audio: AudioSegment, 
        filename: str, 
        format: str = "mp3"
    ) -> str:
        """
        Save audio to file
        
        Args:
            audio: AudioSegment to save
            filename: Output filename
            format: Audio format (mp3, wav, ogg, etc)
            
        Returns:
            Path to saved file
        """
        output_path = OUTPUT_FOLDER / filename
        audio.export(str(output_path), format=format)
        return str(output_path)


def get_tts_engine() -> TTSEngine:
    """Factory function to get TTS engine instance"""
    return TTSEngine()
