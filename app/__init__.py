from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # ✅ Load Google Maps API Key from environment into app config
    app.config['GOOGLE_MAPS_API_KEY'] = os.getenv("GOOGLE_MAPS_API_KEY")

    # Register Blueprints
    from .home.routes import home_bp
    from .results.routes import results_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(results_bp)

    return app
