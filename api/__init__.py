"""
API Blueprints for better organization
"""

from flask import Blueprint

# Create blueprints for different API sections
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
study_resources_bp = Blueprint('study_resources', __name__, url_prefix='/study-resources')
interview_bp = Blueprint('interview', __name__, url_prefix='/interview')