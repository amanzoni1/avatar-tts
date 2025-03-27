from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from gtts import gTTS
import os
import time

app = Flask(__name__)
# Configure CORS with explicit headers
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Ensure the audio directory exists
os.makedirs('audio', exist_ok=True)

@app.route('/api/audio/<filename>')
def serve_audio(filename):
    return send_file(
        os.path.join('audio', filename),
        mimetype='audio/mpeg',
        as_attachment=False
    )

@app.route('/api/tts', methods=['POST', 'OPTIONS'])
def text_to_speech():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.json
        text = data.get('text')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Generate speech
        tts = gTTS(text=text, lang='en')
        audio_filename = f'output_{int(time.time())}.mp3'  # Unique filename
        audio_path = os.path.join('audio', audio_filename)
        tts.save(audio_path)

        response = jsonify({
            'success': True,
            'audio_url': f'http://localhost:5003/api/audio/{audio_filename}'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    response = jsonify({'status': 'healthy'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5003)
