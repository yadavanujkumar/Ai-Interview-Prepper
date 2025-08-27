"""
AI Interview Prepper Application Package
Modern Flask application with factory pattern
"""
from flask import Flask
from app.core.config import Config
from app.core.extensions import init_extensions
from app.routes import register_blueprints
import os


def create_app(config_class=Config):
    """Application factory pattern for creating Flask app instances"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app