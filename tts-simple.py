#!/usr/bin/env python3
"""
TTS Tool - Simple Text to Speech Generator
No complex dependencies. Just gTTS + Tkinter.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import os
import re
import threading
from gtts import gTTS
from pathlib import Path
from config import OUTPUT_FOLDER, GUI_SETTINGS

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_SETTINGS['window_title'])
        self.root.geometry(f"{GUI_SETTINGS['window_width']}x{GUI_SETTINGS['window_height']}")
        self.root.resizable(True, True)
        
        self.temp_files = []
        self.is_generating = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the GUI layout"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text='🔊 TTS Tool - Simple Text to Speech',
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
            text='Format: [SPEAKER] Text here\nExample:\n[Alice] Hello, how are you?\n[Bob] I\'m doing great!',
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
            text='Ready',
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
    
    def get_voice_variant(self, speaker_index):
        """Alternate between voice variants for variety"""
        variants = ['en', 'en-us', 'en-gb', 'en-au', 'en-ie', 'en-za']
        return variants[speaker_index % len(variants)]
    
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
            
            for i, (speaker, content) in enumerate(lines):
                try:
                    # Get language variant for voice variety
                    lang = self.get_voice_variant(i)
                    
                    # Generate audio
                    tts = gTTS(text=content, lang=lang, slow=False)
                    
                    # Save temp file
                    temp_file = os.path.join(OUTPUT_FOLDER, f'temp_{i:03d}_{speaker}.mp3')
                    tts.save(temp_file)
                    audio_files.append(temp_file)
                    
                    self.update_status(f'Generated: [{speaker}] ({i+1}/{len(lines)})', '#3498db')
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
                messagebox.showinfo('Success', f'Audio generated successfully!\n\nFile: dialogue.mp3\nLocation: {OUTPUT_FOLDER}')
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
                os.system(f'open "{OUTPUT_FOLDER}"' if sys.platform == 'darwin' else f'xdg-open "{OUTPUT_FOLDER}"')
        except Exception as e:
            messagebox.showerror('Error', f'Could not open folder: {str(e)}')


def main():
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
