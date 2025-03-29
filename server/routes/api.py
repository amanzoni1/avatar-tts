from flask import Blueprint, request, jsonify, send_file, current_app
import os
import time
import requests
from services.tts_service import TTSService
from services.avatar_service import AvatarService

api_bp = Blueprint('api', __name__)

@api_bp.route("/generate", methods=["POST"])
def generate():
    """
    Endpoint to generate TTS audio and then create an avatar video using D-ID.
    Expected JSON payload:
    {
        "text": "Text to be converted to speech",
        // Optionally, "audio_url": "https://yourdomain.com/path/to/audio.mp3"
    }
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"]

        # Generate TTS audio.
        tts_service = TTSService()
        tts_result = tts_service.generate_speech(text)
        audio_url = f"{current_app.config['NGROK_URL']}/api/audio/{tts_result['filename']}"

        time.sleep(3)

         # Verify audio file is accessible before proceeding
        audio_path = os.path.join(current_app.config["AUDIO_DIR"], tts_result['filename'])
        if not os.path.exists(audio_path):
            return jsonify({"error": "Generated audio file not found"}), 500

        # Generate Avatar Video using the audio.
        avatar_service = AvatarService()
        talk_result = avatar_service.generate_avatar_video(text, audio_url)

        return jsonify(talk_result), 200

    except Exception as e:
        current_app.logger.error("Error in /generate: %s", str(e))
        return jsonify({"error": str(e)}), 500


@api_bp.route("/audio/<filename>")
def serve_audio(filename):
    """
    Serve generated TTS audio files.
    """
    try:
        audio_path = os.path.join(current_app.config["AUDIO_DIR"], filename)
        if os.path.exists(audio_path):
            # Set CORS headers to allow D-ID to access the file
            response = send_file(audio_path, mimetype="audio/mpeg")
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            return jsonify({"error": "Audio file not found"}), 404
    except Exception as e:
        current_app.logger.error("Error serving audio: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint for D-ID to call once the video is ready.
    """
    try:
        data = request.get_json()
        current_app.logger.info("D-ID webhook received: %s", data)

        # Import socketio locally to avoid circular dependency
        from app import socketio
        socketio.emit("video_ready", data)

        return jsonify({"status": "received"}), 200
    except Exception as e:
        current_app.logger.error("Webhook error: %s", str(e))
        return jsonify({"error": "Webhook processing failed"}), 500


# @api_bp.route("/talk/<talk_id>", methods=["GET"])
# def get_talk_status(talk_id):
#     """
#     Proxy endpoint to fetch talk status from D-ID.
#     Calls D-ID's GET /talks/<talk_id> endpoint using Basic Auth.
#     """
#     try:
#         auth_header = f"Basic {current_app.config['DID_API_KEY']}"
#         headers = {
#             "accept": "application/json",
#             "Authorization": auth_header
#         }
#         url = f"{current_app.config['DID_API_URL']}/{talk_id}"
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         return jsonify(response.json()), 200
#     except requests.exceptions.RequestException as e:
#         error_message = f"Failed to fetch talk status: {str(e)}"
#         current_app.logger.error(error_message)
#         return jsonify({"error": error_message}), response.status_code if response else 500
