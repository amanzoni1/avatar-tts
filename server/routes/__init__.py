from routes.api import api_bp
from routes.health import health_bp

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api/health")
