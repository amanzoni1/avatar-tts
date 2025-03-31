import os
import sys
import time
import json
import requests
import logging

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
DID_API_KEY = os.environ.get("DID_API_KEY")
TALK_API_URL = "https://api.d-id.com/talks"
DID_SOURCE_URL = "https://res.cloudinary.com/drvwan14l/image/upload/v1743403431/Joaquin_xmhhqp.jpg"
ELEVENLABS_VOICE_CLIP_ID = "CwhRBWXzGAHq8TQ4Fs17"
POLL_INTERVAL = 5
TIMEOUT = 300

def create_talk(text: str) -> dict:
    """
    Sends a request to D-ID's talks endpoint using a text script payload.
    """

    payload = {
        "source_url": DID_SOURCE_URL,
        "script": {
            "type": "text",
            "input": text,
            "provider": {
                "type": "elevenlabs",
                "voice_id": ELEVENLABS_VOICE_CLIP_ID,
                "voice_config": {
                    "model_id": "eleven_multilingual_v2",
                    "stability": 0.85,
                    "similarity_boost": 1,
                    "style": 0.0,
                    "use_speaker_boost": True,
                    "speed": 0.75
                }
            }
        },
        "config": {
            "stitch": True,
            "fluent": True
        }
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {DID_API_KEY}",
    }

    logger.info("Creating talk with payload:")
    logger.info(json.dumps(payload, indent=2))

    try:
        response = requests.post(TALK_API_URL, headers=headers, json=payload)
        if response.status_code not in (200, 201):
            raise Exception(f"Talk creation failed with status {response.status_code}: {response.text}")
        result = response.json()
        logger.info(f"Talk created: {result}")
        return {
            "talk_id": result.get("id"),
            "status": result.get("status")
        }
    except requests.exceptions.RequestException as e:
        try:
            error_json = e.response.json()
        except Exception:
            error_json = {}
        logger.error(f"Request failed with status {e.response.status_code if e.response else 'N/A'}")
        logger.error(f"Error details: {json.dumps(error_json, indent=2)}")
        raise Exception(f"Failed to generate talk: {e}")


def poll_talk_status(talk_id: str) -> dict:
    """
    Polls the talk status endpoint until the talk status is 'done'
    or a timeout occurs.
    """
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {DID_API_KEY}"
    }
    talk_url = f"{TALK_API_URL}/{talk_id}"
    logger.info(f"Polling talk status at: {talk_url}")
    start_time = time.time()
    while True:
        response = requests.get(talk_url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Error polling talk status: {response.status_code} {response.text}")
            sys.exit(1)
        result = response.json()
        status = result.get("status")
        logger.info(f"Talk status: {status}")
        if status == "done":
            return result
        if time.time() - start_time > TIMEOUT:
            logger.error("Polling timed out.")
            sys.exit(1)
        time.sleep(POLL_INTERVAL)

def download_video(video_url: str, save_dir: str = "talks") -> str:
    """
    Downloads the video from the given URL and saves it locally.
    Returns the local file path.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = f"talk_{int(time.time())}.mp4"
    save_path = os.path.join(save_dir, filename)
    logger.info(f"Downloading video from {video_url}...")
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logger.info(f"Video saved to {save_path}")
        return save_path
    else:
        logger.error(f"Failed to download video. Status: {response.status_code}")
        sys.exit(1)

def main():
    text = """Hello there! I'm Joaquin, your AI avatar host for today. Welcome to the Avatar Text-to-Speech project demonstration.

        What you're witnessing right now is exactly what this project is all about – a synthetic voice synchronized with facial animations to create a natural-looking digital presenter. Pretty cool, right?

        This system works by taking text input, converting it to speech using ElevenLabs' advanced TTS technology, and then synchronizing that audio with facial animations through D-ID's animation API. The result is what you see now – an avatar that can deliver messages with realistic expressions and lip movements.

        If you'd like to try this out yourself, you can visit the live demo at the link provided above. There, you can type any text you want into the input field, click "Generate Avatar's Speech," and watch as Magen brings your words to life with appropriate facial movements and expressions.

        Additionally, all the code, documentation, and methodology behind this project are available on GitHub – you'll find the link above as well. There, you can explore the full implementation, including the server architecture, API integrations, and frontend components.

        Thank you for taking the time to review my work, and I look forward to discussing how this system can drive innovative solutions in communication and beyond. Enjoy the demo and feel free to reach out with any questions!

        Until next time, this is Joaquin signing off. I hope to speak your words soon!"""

    talk_metadata = create_talk(text)
    talk_id = talk_metadata["talk_id"]
    logger.info(f"Talk ID: {talk_id}")
    final_result = poll_talk_status(talk_id)
    video_url = final_result.get("result_url")
    if video_url:
        download_video(video_url)
    else:
        logger.error("Video URL not found in final talk result.")
        sys.exit(1)

if __name__ == "__main__":
    main()
