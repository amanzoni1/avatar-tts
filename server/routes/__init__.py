from routes.tts import tts_bp
from routes.health import health_bp

def register_routes(app):
    app.register_blueprint(tts_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
