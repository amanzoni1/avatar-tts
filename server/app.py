from flask import Flask
from flask_cors import CORS
from routes import register_routes
from config import Config
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register routes
    register_routes(app)
    return app

app = create_app()
socketio = SocketIO(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
