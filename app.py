from flask import Flask
from flask_cors import CORS
import os
import logging

from src.api.routes import api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Ensure upload directory exists
    os.makedirs('uploads', exist_ok=True)
    
    return app

app = create_app()

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
