"""
PyQt5 Desktop GUI for TTS Tool
Run: python tts-gui.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QComboBox, QListWidget, QListWidgetItem,
    QFileDialog, QProgressBar, QMessageBox, QSplitter, QGroupBox,
    QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QDragEnterEvent, QDropEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

from tts_engine import get_tts_engine
from config import OUTPUT_FOLDER


class TTSWorkerThread(QThread):
    """Worker thread for TTS generation to avoid blocking UI"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, dialogue_text: str, speaker_voices: Dict):
        super().__init__()
        self.dialogue_text = dialogue_text
        self.speaker_voices = speaker_voices

    def run(self):
        try:
            self.progress.emit(10)
            engine = get_tts_engine()

            self.progress.emit(30)
            dialogue_lines = engine.parse_dialogue(self.dialogue_text)

            self.progress.emit(50)
            mixed_audio = engine.mix_dialogue(dialogue_lines, self.speaker_voices)

            self.progress.emit(80)
            speakers = engine.detect_speakers(self.dialogue_text)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            speakers_str = "_".join(speakers[:2])
            filename = f"dialogue_{speakers_str}_{timestamp}.mp3"

            output_path = OUTPUT_FOLDER / filename
            mixed_audio.export(str(output_path), format="mp3", bitrate="192k")

            self.progress.emit(100)

            self.finished.emit({
                "success": True,
                "filename": filename,
                "filepath": str(output_path),
                "speakers": speakers,
                "duration": int(len(mixed_audio) / 1000),
                "message": "MP3 generated successfully!"
            })
        except Exception as e:
            self.error.emit(str(e))


class TTSToolGUI(QMainWindow):
    """Main GUI Application"""

    def __init__(self):
        super().__init__()
        self.engine = get_tts_engine()
        self.current_audio_file = None
        self.speaker_voices: Dict[str, int] = {}
        self.dialogue_text = ""
        self.recent_files: List[dict] = []

        self.initUI()
        self.loadRecentFiles()
        self.setAcceptDrops(True)

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("TTS Tool - English Learning")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(self.getStyleSheet())

        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left Panel - Input & Configuration
        left_panel = self.createLeftPanel()

        # Right Panel - Output & History
        right_panel = self.createRightPanel()

        # Splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def createLeftPanel(self) -> QWidget:
        """Create left panel (input and configuration)"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("📝 Dialogue Input")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "[JOHN] Hello, how are you?\n"
            "[SARAH] Hi John! I'm doing great.\n"
            "[JOHN] That's wonderful!"
        )
        self.text_edit.setMinimumHeight(250)
        layout.addWidget(self.text_edit)

        # File buttons
        file_buttons = QHBoxLayout()

        open_btn = QPushButton("📂 Open File")
        open_btn.clicked.connect(self.openFile)
        file_buttons.addWidget(open_btn)

        new_btn = QPushButton("✏️ Clear")
        new_btn.clicked.connect(self.clearText)
        file_buttons.addWidget(new_btn)

        save_btn = QPushButton("💾 Save Dialogue")
        save_btn.clicked.connect(self.saveDialogue)
        file_buttons.addWidget(save_btn)

        layout.addLayout(file_buttons)

        # Speaker Detection
        speaker_group = QGroupBox("👥 Speakers")
        speaker_layout = QVBoxLayout()

        detect_btn = QPushButton("🔍 Detect Speakers")
        detect_btn.clicked.connect(self.detectSpeakers)
        speaker_layout.addWidget(detect_btn)

        self.speakers_list = QListWidget()
        self.speakers_list.setMaximumHeight(120)
        speaker_layout.addWidget(self.speakers_list)

        speaker_group.setLayout(speaker_layout)
        layout.addWidget(speaker_group)

        # Voice Assignment
        voice_group = QGroupBox("🎙️ Voice Assignment")
        voice_layout = QVBoxLayout()

        self.voice_widgets = {}
        self.voice_assignment_layout = QVBoxLayout()
        voice_layout.addLayout(self.voice_assignment_layout)

        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)

        # Generate Button
        generate_btn = QPushButton("🎵 Generate MP3")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        generate_btn.setMinimumHeight(40)
        generate_btn.clicked.connect(self.generateAudio)
        layout.addWidget(generate_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def createRightPanel(self) -> QWidget:
        """Create right panel (output and history)"""
        panel = QWidget()
        layout = QVBoxLayout()

        # Result section
        result_group = QGroupBox("✅ Generation Result")
        result_layout = QVBoxLayout()

        self.result_label = QLabel("No audio generated yet")
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)

        # Audio preview
        self.audio_player = QMediaPlayer()
        self.play_btn = QPushButton("▶️ Preview Audio")
        self.play_btn.clicked.connect(self.previewAudio)
        self.play_btn.setEnabled(False)
        result_layout.addWidget(self.play_btn)

        # Download button
        self.download_btn = QPushButton("⬇️ Download MP3")
        self.download_btn.clicked.connect(self.downloadAudio)
        self.download_btn.setEnabled(False)
        result_layout.addWidget(self.download_btn)

        # Open folder button
        open_folder_btn = QPushButton("📁 Open Output Folder")
        open_folder_btn.clicked.connect(self.openOutputFolder)
        result_layout.addWidget(open_folder_btn)

        result_group.setLayout(result_layout)
        layout.addWidget(result_group)

        # Recent files
        history_group = QGroupBox("📋 Recent Files")
        history_layout = QVBoxLayout()

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.onHistoryItemClicked)
        history_layout.addWidget(self.history_list)

        clear_history_btn = QPushButton("🗑️ Clear History")
        clear_history_btn.clicked.connect(self.clearHistory)
        history_layout.addWidget(clear_history_btn)

        history_group.setLayout(history_layout)
        layout.addWidget(history_group)

        panel.setLayout(layout)
        return panel

    def detectSpeakers(self):
        """Detect speakers from dialogue"""
        text = self.text_edit.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Error", "Please paste dialogue text first")
            return

        speakers = self.engine.detect_speakers(text)

        if not speakers:
            QMessageBox.warning(self, "Error", "No speakers detected. Use format: [SPEAKER_NAME] text")
            return

        # Display speakers
        self.speakers_list.clear()
        for speaker in speakers:
            self.speakers_list.addItem(speaker)

        # Generate voice assignment
        self.speaker_voices = self.engine.auto_assign_voices(speakers)

        # Update voice selectors
        self.updateVoiceSelectors(speakers)

    def updateVoiceSelectors(self, speakers: List[str]):
        """Update voice selector dropdowns"""
        # Clear existing widgets
        while self.voice_assignment_layout.count():
            self.voice_assignment_layout.takeAt(0).widget().deleteLater()

        self.voice_widgets = {}
        voices = self.engine.list_voices()

        for speaker in speakers:
            h_layout = QHBoxLayout()

            label = QLabel(speaker)
            label.setMinimumWidth(100)
            h_layout.addWidget(label)

            combo = QComboBox()
            combo.addItems(voices)

            current_voice = self.speaker_voices.get(speaker, 0)
            combo.setCurrentIndex(current_voice)
            combo.currentIndexChanged.connect(
                lambda idx, s=speaker: self.updateVoiceMapping(s, idx)
            )

            self.voice_widgets[speaker] = combo
            h_layout.addWidget(combo)
            h_layout.addStretch()

            self.voice_assignment_layout.addLayout(h_layout)

    def updateVoiceMapping(self, speaker: str, voice_id: int):
        """Update voice mapping when dropdown changes"""
        self.speaker_voices[speaker] = voice_id

    def generateAudio(self):
        """Generate MP3 from dialogue"""
        text = self.text_edit.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Error", "Please paste dialogue text first")
            return

        if not self.speaker_voices:
            QMessageBox.warning(self, "Error", "Please detect speakers and assign voices first")
            return

        # Start worker thread
        self.worker = TTSWorkerThread(text, self.speaker_voices)
        self.worker.progress.connect(self.updateProgress)
        self.worker.finished.connect(self.onGenerationFinished)
        self.worker.error.connect(self.onGenerationError)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.worker.start()

    def updateProgress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def onGenerationFinished(self, result: dict):
        """Handle generation completion"""
        self.progress_bar.setVisible(False)

        self.current_audio_file = result['filepath']
        self.play_btn.setEnabled(True)
        self.download_btn.setEnabled(True)

        # Display result
        result_text = (
            f"✅ Successfully Generated!\n\n"
            f"Filename: {result['filename']}\n"
            f"Duration: {result['duration']} seconds\n"
            f"Speakers: {', '.join(result['speakers'])}\n"
            f"Path: {result['filepath']}"
        )
        self.result_label.setText(result_text)

        # Add to recent files
        self.addToRecentFiles(result)

        # Show success message
        QMessageBox.information(self, "Success", result['message'])

    def onGenerationError(self, error: str):
        """Handle generation error"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Error", f"Failed to generate audio:\n{error}")

    def previewAudio(self):
        """Play audio preview"""
        if self.current_audio_file:
            self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_audio_file)))
            self.audio_player.play()

    def downloadAudio(self):
        """Save audio file to user-selected location"""
        if not self.current_audio_file:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save MP3", "", "MP3 Files (*.mp3)"
        )

        if file_path:
            import shutil
            shutil.copy(self.current_audio_file, file_path)
            QMessageBox.information(self, "Success", f"File saved to:\n{file_path}")

    def openOutputFolder(self):
        """Open output folder in file explorer"""
        import subprocess
        subprocess.Popen(f'explorer "{OUTPUT_FOLDER}"' if sys.platform == 'win32' else f'open "{OUTPUT_FOLDER}"')

    def openFile(self):
        """Open dialogue file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Dialogue File", "", "Text Files (*.txt)")

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")

    def saveDialogue(self):
        """Save dialogue to file"""
        text = self.text_edit.toPlainText()

        if not text.strip():
            QMessageBox.warning(self, "Error", "No dialogue to save")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Dialogue", "", "Text Files (*.txt)")

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Success", "Dialogue saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def clearText(self):
        """Clear text editor"""
        reply = QMessageBox.question(
            self, "Confirm", "Clear dialogue text?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.text_edit.clear()
            self.speakers_list.clear()
            self.voice_widgets.clear()

    def addToRecentFiles(self, result: dict):
        """Add file to recent files list"""
        self.recent_files.insert(0, {
            "timestamp": datetime.now().isoformat(),
            "filename": result['filename'],
            "filepath": result['filepath'],
            "speakers": result['speakers'],
            "duration": result['duration']
        })

        # Keep only 20 recent files
        self.recent_files = self.recent_files[:20]

        self.saveRecentFiles()
        self.loadRecentFiles()

    def onHistoryItemClicked(self, item: QListWidgetItem):
        """Handle history item click"""
        try:
            filename = item.text().split('\n')[0]
            # Find file in recent files
            for file_info in self.recent_files:
                if filename in file_info['filename']:
                    self.current_audio_file = file_info['filepath']
                    self.play_btn.setEnabled(True)
                    self.download_btn.setEnabled(True)
                    
                    # Update result label
                    result_text = (
                        f"Filename: {file_info['filename']}\n"
                        f"Duration: {file_info['duration']} seconds\n"
                        f"Speakers: {', '.join(file_info['speakers'])}"
                    )
                    self.result_label.setText(result_text)
                    break
        except Exception as e:
            print(f"Error loading history file: {e}")

    def loadRecentFiles(self):
        """Load and display recent files"""
        history_file = Path(__file__).parent / "gui_history.json"

        if history_file.exists():
            with open(history_file, 'r') as f:
                self.recent_files = json.load(f)
        else:
            self.recent_files = []

        self.history_list.clear()
        for file_info in self.recent_files:
            item_text = (
                f"{file_info['filename']}\n"
                f"👥 {', '.join(file_info['speakers'])} | ⏱️ {file_info['duration']}s"
            )
            self.history_list.addItem(item_text)

    def saveRecentFiles(self):
        """Save recent files to JSON"""
        history_file = Path(__file__).parent / "gui_history.json"

        with open(history_file, 'w') as f:
            json.dump(self.recent_files, f, indent=2)

    def clearHistory(self):
        """Clear recent files"""
        reply = QMessageBox.question(
            self, "Confirm", "Clear recent files?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.recent_files = []
            self.history_list.clear()
            self.saveRecentFiles()

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle file drop"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files and files[0].endswith('.txt'):
            try:
                with open(files[0], 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")

    def getStyleSheet(self) -> str:
        """Return application stylesheet"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
            }
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """


def main():
    app = QApplication(sys.argv)
    window = TTSToolGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
