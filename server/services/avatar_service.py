import json
import requests
import logging
from typing import Dict, Any
from flask import current_app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AvatarService:
    def __init__(self):
        self.did_api_key = current_app.config["DID_API_KEY"]
        self.api_url = current_app.config["DID_API_URL"]
        self.source_url = current_app.config["DID_SOURCE_URL"]

        if not self.did_api_key:
            logger.error("DID_API_KEY not set")
            raise ValueError("DID_API_KEY environment variable is not set")

        logger.info(f"AvatarService initialized with source URL: {self.source_url}")

    def generate_avatar_video(self, text: str, audio_url: str) -> Dict[str, Any]:
        auth_header = f"Basic {self.did_api_key}"

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header
        }

        # Primary payload using the audio file.
        payload = {
            "source_url": self.source_url,
            "script": {
                "type": "audio",
                "audio_url": audio_url
            },
            "config": {
                "fluent": False,
                "stitch": True
            },
            "webhook": current_app.config["DID_WEBHOOK_URL"]
        }

        logger.info("Sending request to D-ID API with audio script...")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return {
                "talk_id": result.get("id"),
                "status": result.get("status"),
            }
        except requests.exceptions.RequestException as e:
            error_json = {}
            try:
                error_json = e.response.json()
            except Exception:
                logger.error("Failed to parse error JSON from audio request.")

            description = error_json.get("description", "").lower()
            logger.error(f"Audio request failed: {json.dumps(error_json, indent=2)}")

            # If error indicates audio validation failed, fallback to text script.
            if "cannot validate" in description and "audio" in description:
                logger.info("Audio validation failed; falling back to text script.")
                fallback_payload = {
                    "source_url": self.source_url,
                    "script": {
                        "type": "text",
                        "input": text
                    },
                    "config": {
                        "stitch": True
                    },
                    "webhook": current_app.config["DID_WEBHOOK_URL"]
                }
                logger.info("Sending request to D-ID API with text script fallback...")
                logger.info(f"Fallback Payload: {json.dumps(fallback_payload, indent=2)}")
                try:
                    response = requests.post(self.api_url, headers=headers, json=fallback_payload)
                    response.raise_for_status()
                    result = response.json()
                    return {
                        "talk_id": result.get("id"),
                        "status": result.get("status"),
                    }
                except requests.exceptions.RequestException as fallback_exception:
                    logger.error(f"Fallback request error: {fallback_exception}")
            raise Exception(f"Failed to generate avatar video: {e}")
