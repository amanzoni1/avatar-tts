import os
import time
import logging
import requests
from flask import current_app
from typing import Dict, Any

# Minimal logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_folder(folder_path: str, max_files: int = 3) -> None:
    """
    Keeps only the most recent max_files in the folder,
    deleting older ones.
    """
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    if len(files) > max_files:
        # Sort files by modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(x))
        # Delete the oldest files
        files_to_delete = files[:len(files) - max_files]
        for file in files_to_delete:
            os.remove(file)
            logger.info(f"Deleted old audio file: {file}")

class TTSService:
    def __init__(self):
        self.api_key = current_app.config['ELEVENLABS_API_KEY']
        self.voice_id = current_app.config['ELEVENLABS_VOICE_ID']
        self.max_chars = current_app.config['ELEVENLABS_MAX_CHARS']
        if not self.api_key:
            logger.error("ElevenLabs API key is missing")
            raise ValueError("ELEVENLABS_API_KEY is required when using ElevenLabs provider")
        logger.info(f"TTSService initialized using ElevenLabs with voice ID: {self.voice_id}")

    def _validate_text(self, text: str) -> str:
        """Truncate text if it exceeds the max character limit."""
        if len(text) > self.max_chars:
            logger.warning(f"Text length exceeds {self.max_chars} characters. Truncating...")
            return text[:self.max_chars]
        return text

    def generate_speech(self, text: str) -> Dict[str, Any]:
        """
        Generate TTS audio from text using ElevenLabs.
        The audio file is saved in AUDIO_DIR and only the latest three
        files are kept.
        """
        # Generate a filename; using a timestamp here ensures uniqueness.
        filename = f'output_{int(time.time())}.mp3'
        audio_path = os.path.join(current_app.config['AUDIO_DIR'], filename)
        try:
            validated_text = self._validate_text(text)
            result = self._generate_with_elevenlabs(validated_text, audio_path)
            # Clean up older files, keeping only the latest 3
            cleanup_folder(current_app.config['AUDIO_DIR'], max_files=3)
            return result
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise

    def _generate_with_elevenlabs(self, text: str, output_path: str) -> Dict[str, Any]:
        # Use the basic text-to-speech endpoint (without /with-timestamps)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.8,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
                "speed": 0.8
            },
            "output_format": "mp3_44100_128",
            "apply_text_normalization": "on"
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code != 200:
                err_msg = f"ElevenLabs error {response.status_code}: {response.text}"
                logger.error(err_msg)
                raise Exception(err_msg)
            audio_data = response.content
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            logger.info(f"ElevenLabs: Audio saved to {output_path}")
            return {'filename': os.path.basename(output_path)}
        except requests.exceptions.RequestException as e:
            err_msg = f"Network error: {e}"
            logger.error(err_msg)
            raise Exception(err_msg)
        except Exception as e:
            err_msg = f"Error generating ElevenLabs audio: {e}"
            logger.error(err_msg)
            raise Exception(err_msg)
