from flask import Blueprint, request, jsonify, send_file, current_app
from services.tts_service import TTSService
import os

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Initialize service inside the route where we have app context
        tts_service = TTSService()
        result = tts_service.generate_speech(text)

        # Construct the full URL for the audio file
        audio_url = f"{current_app.config['SERVER_URL']}/api/audio/{result['filename']}"

        return jsonify({
            'success': True,
            'audio_url': audio_url,
            'timing': result['timing']  # Include timing information in response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tts_bp.route('/audio/<filename>')
def serve_audio(filename):
    audio_path = os.path.join(current_app.config['AUDIO_DIR'], filename)

    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mpeg')
    else:
        return jsonify({'error': 'Audio file not found'}), 404
