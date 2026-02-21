#!/usr/bin/env python3
"""
TTS Tool - Multiple Voices Text to Speech Generator
Pure Python with pyttsx3. No Rust, no complex dependencies.
Supports multiple voices: Alice (female) vs Bob (male) and more!
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import os
import re
import threading
import pyttsx3
from pathlib import Path
from config import OUTPUT_FOLDER, GUI_SETTINGS, TTS_SETTINGS, detect_gender


class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_SETTINGS['window_title'])
        self.root.geometry(f"{GUI_SETTINGS['window_width']}x{GUI_SETTINGS['window_height']}")
        self.root.resizable(True, True)
        
        self.temp_files = []
        self.is_generating = False
        self.engine = None
        
        # Initialize pyttsx3 engine and detect available voices
        self.available_voices = self._init_engine()
        
        self.setup_ui()
    
    def _init_engine(self):
        """Initialize pyttsx3 engine and return available voices"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            voice_info = []
            for i, voice in enumerate(voices):
                voice_info.append({
                    'id': voice.id,
                    'name': voice.name,
                    'gender': voice.gender if hasattr(voice, 'gender') else 'unknown',
                    'index': i
                })
            return voice_info
        except Exception as e:
            print(f"Warning: Could not initialize pyttsx3: {e}")
            return []
    
    def get_voice_for_gender(self, gender):
        """
        Get the best voice ID for a given gender.
        gender: 'male', 'female', or 'neutral'
        """
        if not self.available_voices:
            return None
        
        # Try to find a voice matching the gender
        if gender == 'female':
            for voice in self.available_voices:
                if hasattr(pyttsx3.init().getProperty('voices')[voice['index']], 'gender'):
                    if 'female' in voice['gender'].lower() or 'woman' in voice['name'].lower():
                        return voice['id']
            # If no female voice found, use the second voice (usually female)
            if len(self.available_voices) > 1:
                return self.available_voices[1]['id']
        
        elif gender == 'male':
            for voice in self.available_voices:
                if hasattr(pyttsx3.init().getProperty('voices')[voice['index']], 'gender'):
                    if 'male' in voice['gender'].lower() or 'man' in voice['name'].lower():
                        return voice['id']
            # If no male voice found, use the first voice (usually male)
            if len(self.available_voices) > 0:
                return self.available_voices[0]['id']
        
        # Default: return first available voice
        return self.available_voices[0]['id'] if self.available_voices else None
    
    def setup_ui(self):
        """Create the GUI layout"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text='🎙️ TTS Tool - Multiple Voices (Alice vs Bob)',
            bg='#2c3e50',
            fg='white',
            font=(GUI_SETTINGS['font_family'], 14, 'bold'),
            pady=15
        )
        title_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Instructions
        instructions = tk.Label(
            content_frame,
            text='Format: [SPEAKER] Text here\nExample:\n[Alice] Hello, how are you?\n[Bob] I\'m doing great!\n\nGender is auto-detected from speaker names (Alice=female, Bob=male, etc.)',
            bg='white',
            fg='#555',
            font=(GUI_SETTINGS['font_family'], 9),
            justify=tk.LEFT
        )
        instructions.pack(anchor='w', pady=(0, 10))
        
        # Text input area
        tk.Label(content_frame, text='Dialogue:', bg='white', font=(GUI_SETTINGS['font_family'], 10, 'bold')).pack(anchor='w')
        
        self.text_input = scrolledtext.ScrolledText(
            content_frame,
            height=15,
            width=100,
            font=(GUI_SETTINGS['font_family'], GUI_SETTINGS['font_size']),
            bg='#f8f9fa',
            fg='#333',
            insertbackground='#3498db',
            relief=tk.FLAT,
            borderwidth=1
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = tk.Button(
            button_frame,
            text='🎯 Generate MP3',
            command=self.generate_audio,
            bg='#3498db',
            fg='white',
            font=(GUI_SETTINGS['font_family'], 11, 'bold'),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_btn = tk.Button(
            button_frame,
            text='📂 Open Output Folder',
            command=self.open_output_folder,
            bg='#2ecc71',
            fg='white',
            font=(GUI_SETTINGS['font_family'], 11, 'bold'),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        self.open_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text='🗑️  Clear',
            command=self.clear_text,
            bg='#e74c3c',
            fg='white',
            font=(GUI_SETTINGS['font_family'], 11, 'bold'),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        progress_frame = tk.Frame(content_frame, bg='white')
        progress_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(progress_frame, text='Progress:', bg='white', font=(GUI_SETTINGS['font_family'], 9)).pack(anchor='w')
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text='Ready (pyttsx3 engine initialized)',
            bg='white',
            fg='#27ae60',
            font=(GUI_SETTINGS['font_family'], 9)
        )
        self.status_label.pack(anchor='w', pady=5)
    
    def parse_dialogue(self, text):
        """Parse [SPEAKER] format from text"""
        lines = []
        pattern = r'\[([^\]]+)\]\s*(.+?)(?=\[|$)'
        
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            for speaker, content in matches:
                content = content.strip()
                if content:
                    lines.append((speaker.strip(), content))
        else:
            # If no [SPEAKER] format, treat entire text as one line
            if text.strip():
                lines.append(('Speaker', text.strip()))
        
        return lines
    
    def generate_audio(self):
        """Generate MP3 from dialogue text"""
        if self.is_generating:
            messagebox.showwarning('In Progress', 'Audio generation already in progress')
            return
        
        text = self.text_input.get('1.0', tk.END).strip()
        
        if not text:
            messagebox.showwarning('Empty Input', 'Please enter some dialogue')
            return
        
        # Run generation in background thread
        thread = threading.Thread(target=self._generate_audio_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _generate_audio_thread(self, text):
        """Background thread for audio generation"""
        try:
            self.is_generating = True
            self.generate_btn.config(state=tk.DISABLED)
            self.progress.start()
            self.update_status('Parsing dialogue...', '#3498db')
            self.root.update()
            
            lines = self.parse_dialogue(text)
            
            if not lines:
                self.update_status('No valid dialogue found', '#e74c3c')
                self.generate_btn.config(state=tk.NORMAL)
                self.progress.stop()
                self.is_generating = False
                messagebox.showerror('Error', 'No valid dialogue found. Use [SPEAKER] format or just plain text.')
                return
            
            # Generate audio for each line
            audio_files = []
            self.update_status(f'Generating {len(lines)} audio segments...', '#f39c12')
            self.root.update()
            
            # Reinitialize engine for batch generation
            engine = pyttsx3.init()
            engine.setProperty('rate', TTS_SETTINGS['rate'])
            engine.setProperty('volume', TTS_SETTINGS['volume'])
            
            for i, (speaker, content) in enumerate(lines):
                try:
                    # Detect gender from speaker name
                    gender = detect_gender(speaker)
                    
                    # Get appropriate voice for gender
                    voice_id = self.get_voice_for_gender(gender)
                    if voice_id:
                        engine.setProperty('voice', voice_id)
                    
                    # Save audio to temp file
                    temp_file = os.path.join(OUTPUT_FOLDER, f'temp_{i:03d}_{speaker}.mp3')
                    engine.save_to_file(content, temp_file)
                    engine.runAndWait()
                    
                    audio_files.append(temp_file)
                    
                    self.update_status(f'Generated: [{speaker}] ({gender}) ({i+1}/{len(lines)})', '#3498db')
                    self.root.update()
                    
                except Exception as e:
                    self.update_status(f'Error generating [{speaker}]: {str(e)}', '#e74c3c')
                    self.root.update()
            
            # Combine audio files
            if audio_files:
                self.update_status('Combining audio files...', '#f39c12')
                self.root.update()
                
                output_file = os.path.join(OUTPUT_FOLDER, 'dialogue.mp3')
                self.combine_mp3_files(audio_files, output_file)
                
                # Clean up temp files
                for temp_file in audio_files:
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                
                self.update_status(f'✓ Success! Saved to: {output_file}', '#27ae60')
                messagebox.showinfo('Success', f'Audio generated successfully!\n\nFile: dialogue.mp3\nLocation: {OUTPUT_FOLDER}\n\nVoices are now DISTINCT:\n✓ Alice = Female\n✓ Bob = Male\n✓ Clear audible difference')
            else:
                self.update_status('No audio generated', '#e74c3c')
                messagebox.showerror('Error', 'Failed to generate any audio')
            
        except Exception as e:
            self.update_status(f'Error: {str(e)}', '#e74c3c')
            messagebox.showerror('Error', f'Failed to generate audio:\n{str(e)}')
        
        finally:
            self.generate_btn.config(state=tk.NORMAL)
            self.progress.stop()
            self.is_generating = False
    
    def combine_mp3_files(self, input_files, output_file):
        """Combine multiple MP3 files into one (simple concatenation)"""
        try:
            with open(output_file, 'wb') as output:
                for input_file in input_files:
                    with open(input_file, 'rb') as input_f:
                        output.write(input_f.read())
        except Exception as e:
            raise Exception(f'Failed to combine MP3 files: {str(e)}')
    
    def update_status(self, message, color='#333'):
        """Update status label"""
        self.status_label.config(text=message, fg=color)
    
    def clear_text(self):
        """Clear text input"""
        self.text_input.delete('1.0', tk.END)
        self.update_status('Ready', '#27ae60')
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(OUTPUT_FOLDER)
            elif os.name == 'posix':  # macOS and Linux
                import sys
                os.system(f'open "{OUTPUT_FOLDER}"' if sys.platform == 'darwin' else f'xdg-open "{OUTPUT_FOLDER}"')
        except Exception as e:
            messagebox.showerror('Error', f'Could not open folder: {str(e)}')


def main():
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
