import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DEBUG = False

    # CORS settings
    CORS_ORIGINS = ['https://avatar-tts.vercel.app']
    # CORS_ORIGINS = ['http://localhost:3003']

    # Server settings
    # NGROK_URL = "https://f9ee-94-205-217-109.ngrok-free.app"
    # SERVER_URL = 'http://localhost:5003'
    SERVER_URL = 'https://avatar-tts.onrender.com'

    # BASE_DIR: set to the server folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Audio settings
    AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # ElevenLabs settings
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = "XrExE9yKIg1WjnnlVkGX"
    ELEVENLABS_MAX_CHARS = 350  # Maximum characters per request (approximately 30 seconds of audio)

    # D-ID settings
    DID_API_KEY = os.environ.get("DID_API_KEY")
    DID_API_URL = "https://api.d-id.com/talks"
    DID_SOURCE_URL = "https://res.cloudinary.com/drvwan14l/image/upload/v1743239627/magen_igp4ts.png"
    DID_WEBHOOK_URL = f"{SERVER_URL}/api/webhook"
