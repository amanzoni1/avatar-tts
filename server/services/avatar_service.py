import requests
import json
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
        # We only support the audio script type.
        auth_header = f"Basic {self.did_api_key}"  # "username:password" format

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header
            # Removed "x-api-key-external" since we are only using external audio.
        }

        payload = {
            "source_url": self.source_url,
            "script": {
                "type": "audio",
                "audio_url": audio_url
            },
            "config": {
                "fluent": False,
                "pad_audio": 0,
                "stitch": True
            },
            "webhook": current_app.config["DID_WEBHOOK_URL"]
        }

        logger.info("Sending request to D-ID API...")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            logger.info(f"Response Code: {response.status_code}")
            try:
                response_json = response.json()
                logger.info(f"Response Body: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.error(f"Response Body: {response.text}")
            response.raise_for_status()
            result = response.json()
            return {
                "talk_id": result.get("id"),
                "status": result.get("status"),
                "result_url": result.get("result_url")
            }
        except requests.exceptions.RequestException as e:
            err_msg = f"Failed to generate avatar video: {e}"
            logger.error(err_msg)
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_detail = e.response.json().get("message", err_msg)
                    logger.error(f"Detail: {error_detail}")
                    err_msg = error_detail
                except Exception:
                    pass
            raise Exception(err_msg)
