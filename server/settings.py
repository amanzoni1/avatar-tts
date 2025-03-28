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
    SERVER_URL = 'http://localhost:5003'

    # Audio settings
    AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio')

    # TTS Provider settings
    TTS_PROVIDER = os.environ.get('TTS_PROVIDER', 'gtts')  # 'gtts' or 'elevenlabs'

    # ElevenLabs settings
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.environ.get('ELEVENLABS_VOICE_ID', 'default')  # You can set a default voice ID

    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # Ensure audio directory exists
    os.makedirs(AUDIO_DIR, exist_ok=True)
