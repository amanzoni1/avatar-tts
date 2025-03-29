import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DEBUG = True

    # CORS settings
    CORS_ORIGINS = ['http://localhost:3003']

    # Server settings
    NGROK_URL = "https://09db-94-205-217-109.ngrok-free.app"
    # SERVER_URL = NGROK_URL
    SERVER_URL = 'http://localhost:5003'

    # BASE_DIR: set to the server folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Audio settings
    AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # TTS Provider settings
    TTS_PROVIDER = os.environ.get('TTS_PROVIDER', 'elevenlabs')  # 'gtts' or 'elevenlabs'

    # ElevenLabs settings
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID")
    ELEVENLABS_MAX_CHARS = 350  # Maximum characters per request (approximately 30 seconds of audio)

    # D-ID settings
    DID_API_KEY = os.environ.get("DID_API_KEY")
    DID_API_URL = "https://api.d-id.com/talks"
    DID_SOURCE_URL = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
    DID_WEBHOOK_URL = os.environ.get("DID_WEBHOOK_URL", f"{NGROK_URL}/api/webhook")
