import json
import requests
import logging
from typing import Dict, Any
from flask import current_app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FastGenService:
    def __init__(self):
        self.did_api_key = current_app.config["DID_API_KEY"]
        self.api_url = current_app.config["DID_API_URL"]
        self.source_url = current_app.config["DID_SOURCE_URL"]
        self.max_chars = current_app.config.get("ELEVENLABS_MAX_CHARS", 350)

        if not self.did_api_key:
            logger.error("DID_API_KEY not set")
            raise ValueError("DID_API_KEY environment variable is not set")

        logger.info(f"FastGenService initialized with source URL: {self.source_url}")

    def _validate_text(self, text: str) -> str:
        """Truncate text if it exceeds the max character limit."""
        if len(text) > self.max_chars:
            logger.warning(f"Text length exceeds {self.max_chars} characters. Truncating...")
            return text[:self.max_chars]
        return text

    def generate_avatar_video_text(self, text: str) -> Dict[str, Any]:
        """
        Fast generation: sends text directly to D-ID using a text script payload.
        This payload includes provider details for ElevenLabs so that D-ID
        internally calls ElevenLabs TTS.
        """
        validated_text = self._validate_text(text)
        auth_header = f"Basic {self.did_api_key}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header
        }

        # Construct the payload with a text script and ElevenLabs provider details.
        payload = {
            "source_url": self.source_url,
            "script": {
                "type": "text",
                "input": validated_text,
                "provider": {
                    "type": "elevenlabs",
                    "voice_id": current_app.config["ELEVENLABS_VOICE_ID"],
                    "voice_config": {
                        "model_id": "eleven_multilingual_v2",
                        "stability": 0.8,
                        "similarity_boost": 0.75,
                        "style": 0.0,
                        "use_speaker_boost": True,
                        "speed": 0.8
                    }
                }
            },
            "config": {
                "stitch": True,
                "fluent": True
            },
            "webhook": current_app.config["DID_WEBHOOK_URL"]
        }

        logger.info("Sending request to D-ID API with text script (fast generation)...")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return {
                "talk_id": result.get("id"),
                "status": result.get("status")
            }
        except requests.exceptions.RequestException as e:
            error_json = {}
            try:
                error_json = e.response.json()
            except Exception:
                logger.error("Failed to parse error JSON from text request.")
            logger.error(f"Text request failed: {json.dumps(error_json, indent=2)}")
            raise Exception(f"Failed to generate avatar video (fast): {e}")
