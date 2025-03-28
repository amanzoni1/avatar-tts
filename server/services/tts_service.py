from gtts import gTTS
import time
import os
from flask import current_app
import requests
from typing import Optional, Dict, Any
import base64
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.provider = current_app.config['TTS_PROVIDER']
        if self.provider == 'elevenlabs':
            self.api_key = current_app.config['ELEVENLABS_API_KEY']
            self.voice_id = current_app.config['ELEVENLABS_VOICE_ID']
            if not self.api_key:
                logger.error("ElevenLabs API key is missing")
                raise ValueError("ELEVENLABS_API_KEY is required when using ElevenLabs provider")
            logger.info(f"Initialized ElevenLabs TTS service with voice ID: {self.voice_id}")

    def generate_speech(self, text: str) -> Dict[str, Any]:
        """
        Generate speech from text and save it to a file.

        Args:
            text (str): The text to convert to speech

        Returns:
            Dict[str, Any]: Dictionary containing filename and timing information
        """
        # Generate unique filename
        filename = f'output_{int(time.time())}.mp3'
        audio_path = os.path.join(current_app.config['AUDIO_DIR'], filename)

        try:
            if self.provider == 'gtts':
                self._generate_with_gtts(text, audio_path)
                return {'filename': filename, 'timing': None}
            elif self.provider == 'elevenlabs':
                return self._generate_with_elevenlabs(text, audio_path)
            else:
                logger.error(f"Unsupported TTS provider: {self.provider}")
                raise ValueError(f"Unsupported TTS provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to generate speech: {str(e)}")
            raise

    def _generate_with_gtts(self, text: str, output_path: str) -> None:
        """Generate speech using gTTS"""
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            logger.info(f"Successfully generated speech using gTTS: {output_path}")
        except Exception as e:
            logger.error(f"gTTS generation failed: {str(e)}")
            raise

    def _generate_with_elevenlabs(self, text: str, output_path: str) -> Dict[str, Any]:
        """Generate speech using ElevenLabs API with word timing"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/with-timestamps"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.8,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
                "speed": 1.0
            },
            "optimize_streaming_latency": 4,
            "output_format": "mp3_44100_128",
            "apply_text_normalization": "on"
        }

        try:
            response = requests.post(url, json=data, headers=headers)

            if response.status_code != 200:
                error_msg = f"ElevenLabs API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

            response_data = response.json()

            # Save the audio file (decode base64)
            audio_data = base64.b64decode(response_data['audio_base64'])
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            logger.info(f"Successfully generated and saved speech using ElevenLabs: {output_path}")

            # Return both alignment and normalized alignment for better timing control
            return {
                'filename': os.path.basename(output_path),
                'timing': {
                    'alignment': response_data.get('alignment', {}),
                    'normalized_alignment': response_data.get('normalized_alignment', {})
                }
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error while calling ElevenLabs API: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error generating speech: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
