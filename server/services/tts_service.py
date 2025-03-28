from gtts import gTTS
import time
import os
from flask import current_app
import requests
from typing import Dict, Any
import base64
import logging

# Minimal logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.provider = current_app.config['TTS_PROVIDER']
        if self.provider == 'elevenlabs':
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
        """Generate TTS audio from text and return the filename."""
        filename = f'output_{int(time.time())}.mp3'
        audio_path = os.path.join(current_app.config['AUDIO_DIR'], filename)
        try:
            if self.provider == 'gtts':
                self._generate_with_gtts(text, audio_path)
                return {'filename': filename}
            elif self.provider == 'elevenlabs':
                validated_text = self._validate_text(text)
                return self._generate_with_elevenlabs(validated_text, audio_path)
            else:
                logger.error(f"Unsupported TTS provider: {self.provider}")
                raise ValueError(f"Unsupported TTS provider: {self.provider}")
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise

    def _generate_with_gtts(self, text: str, output_path: str) -> None:
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            logger.info(f"gTTS: Audio saved to {output_path}")
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            raise

    def _generate_with_elevenlabs(self, text: str, output_path: str) -> Dict[str, Any]:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/with-timestamps"
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
            response_data = response.json()
            audio_data = base64.b64decode(response_data['audio_base64'])
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
