/**
 * TTS Tool - Web UI JavaScript
 */

const API_BASE = '/api';
let currentFilename = null;
let currentSpeakers = [];
let voiceAssignment = {};

// DOM Elements
const dialogueText = document.getElementById('dialogue-text');
const detectBtn = document.getElementById('detect-btn');
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');
const generateBtn = document.getElementById('generate-btn');
const downloadBtn = document.getElementById('download-btn');
const speakersList = document.getElementById('speakers-list');
const voiceAssignment_el = document.getElementById('voice-assignment');
const progressContainer = document.getElementById('progress-container');
const resultSection = document.getElementById('result-section');
const errorSection = document.getElementById('error-section');
const historyList = document.getElementById('history-list');

// Event Listeners
detectBtn.addEventListener('click', detectSpeakers);
uploadBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', uploadFile);
generateBtn.addEventListener('click', generateAudio);
downloadBtn.addEventListener('click', downloadAudio);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
});

/**
 * Detect speakers in dialogue
 */
async function detectSpeakers() {
    const text = dialogueText.value.trim();
    
    if (!text) {
        showError('Please paste a dialogue first');
        return;
    }

    try {
        showProgress(true, 'Detecting speakers...');
        
        const response = await fetch(`${API_BASE}/detect-speakers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dialogue_text: text })
        });

        if (!response.ok) throw new Error('Failed to detect speakers');
        
        const data = await response.json();
        currentSpeakers = data.speakers;

        displaySpeakers(data.speakers);
        generateVoiceAssignment(data.speakers);
        
        showProgress(false);
    } catch (error) {
        showError('Error detecting speakers: ' + error.message);
        showProgress(false);
    }
}

/**
 * Display detected speakers
 */
function displaySpeakers(speakers) {
    if (speakers.length === 0) {
        speakersList.innerHTML = '<p class="placeholder">No speakers detected. Check your text format: [SPEAKER_NAME] text</p>';
        return;
    }

    let html = '';
    speakers.forEach((speaker, idx) => {
        html += `
            <div class="speaker-item">
                <span class="speaker-name">${idx + 1}. ${speaker}</span>
                <span>👤</span>
            </div>
        `;
    });

    speakersList.innerHTML = html;
}

/**
 * Generate voice assignment dropdowns
 */
async function generateVoiceAssignment(speakers) {
    try {
        const response = await fetch(`${API_BASE}/voices`);
        const data = await response.json();
        const voices = data.voices;

        let html = '';
        speakers.forEach((speaker, idx) => {
            const voiceId = idx % voices.length;
            voiceAssignment[speaker] = voiceId;

            html += `
                <div class="voice-item">
                    <label for="voice-${speaker}" style="margin-bottom: 0; flex: 1;">
                        <strong>${speaker}</strong>
                    </label>
                    <select id="voice-${speaker}" class="voice-select" onchange="updateVoice('${speaker}', this.value)">
            `;

            voices.forEach((voice, idx) => {
                const selected = voiceId === idx ? 'selected' : '';
                html += `<option value="${idx}" ${selected}>${voice}</option>`;
            });

            html += `
                    </select>
                </div>
            `;
        });

        voiceAssignment_el.innerHTML = html;
    } catch (error) {
        console.error('Error loading voices:', error);
    }
}

/**
 * Update voice assignment
 */
function updateVoice(speaker, voiceId) {
    voiceAssignment[speaker] = parseInt(voiceId);
}

/**
 * Upload file
 */
async function uploadFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    try {
        showProgress(true, 'Uploading file...');

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Failed to upload file');

        const data = await response.json();
        dialogueText.value = data.dialogue_text;
        
        // Auto-detect speakers
        await detectSpeakers();
        
        showProgress(false);
    } catch (error) {
        showError('Error uploading file: ' + error.message);
        showProgress(false);
    }
}

/**
 * Generate audio
 */
async function generateAudio() {
    const text = dialogueText.value.trim();

    if (!text) {
        showError('Please paste a dialogue first');
        return;
    }

    if (currentSpeakers.length === 0) {
        showError('Please detect speakers first');
        return;
    }

    try {
        generateBtn.disabled = true;
        showProgress(true, 'Generating MP3...');
        hideError();
        hideResult();

        // Generate filename with timestamp
        const timestamp = new Date().getTime();
        const filename = `dialogue_${timestamp}.mp3`;

        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                dialogue_text: text,
                filename: filename,
                speaker_voices: voiceAssignment
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate audio');
        }

        const data = await response.json();
        currentFilename = data.filename;

        // Show result
        displayResult(data);
        
        // Reload history
        loadHistory();

        showProgress(false);
    } catch (error) {
        showError('Error generating audio: ' + error.message);
        showProgress(false);
    } finally {
        generateBtn.disabled = false;
    }
}

/**
 * Display generation result
 */
function displayResult(data) {
    document.getElementById('result-filename').textContent = data.filename;
    document.getElementById('result-duration').textContent = `${data.duration} seconds`;
    document.getElementById('result-speakers').textContent = data.speakers.join(', ');

    // Set audio preview
    const audioUrl = `/api/download/${data.filename}`;
    document.getElementById('preview-audio').src = audioUrl;

    resultSection.style.display = 'block';
}

/**
 * Download audio
 */
function downloadAudio() {
    if (!currentFilename) return;

    const link = document.createElement('a');
    link.href = `/api/download/${currentFilename}`;
    link.download = currentFilename;
    link.click();
}

/**
 * Load and display history
 */
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history`);
        const data = await response.json();
        
        const history = data.history.reverse();

        if (history.length === 0) {
            historyList.innerHTML = '<p class="placeholder">No recent files</p>';
            return;
        }

        let html = '';
        history.forEach(item => {
            const date = new Date(item.timestamp);
            const dateStr = date.toLocaleString();

            html += `
                <div class="history-item" onclick="loadFromHistory('${item.filename}')">
                    <div class="history-filename">📁 ${item.filename}</div>
                    <div class="history-meta">
                        <span>👥 ${item.speakers.join(', ')}</span>
                        <span class="history-timestamp">⏱️ ${dateStr}</span>
                    </div>
                </div>
            `;
        });

        historyList.innerHTML = html;
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

/**
 * Load file from history
 */
function loadFromHistory(filename) {
    const link = document.createElement('a');
    link.href = `/api/download/${filename}`;
    link.download = filename;
    link.click();
}

/**
 * Show/hide progress indicator
 */
function showProgress(show, message = '') {
    if (show) {
        progressContainer.style.display = 'block';
        if (message) {
            document.getElementById('progress-text').textContent = message;
        }
    } else {
        progressContainer.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('error-message').textContent = message;
    errorSection.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Hide result section
 */
function hideResult() {
    resultSection.style.display = 'none';
}
