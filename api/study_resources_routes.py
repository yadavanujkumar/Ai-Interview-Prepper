"""
Study Resources API Routes
"""

from flask import jsonify, request
from api import study_resources_bp
from services.study_resources_service import StudyResourcesService

# Initialize service
study_service = StudyResourcesService()

@study_resources_bp.route('/domains/<domain>')
def get_domain_resources(domain):
    """Get all resources for a specific domain"""
    try:
        resources = study_service.get_resources_by_domain(domain)
        return jsonify(resources)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_resources_bp.route('/learning-path/<domain>')
def get_learning_path(domain):
    """Get learning path for a domain"""
    try:
        skill_level = request.args.get('level', 'beginner')
        learning_path = study_service.get_learning_path(domain, skill_level)
        return jsonify(learning_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_resources_bp.route('/recommendations', methods=['POST'])
def get_personalized_recommendations():
    """Get personalized study recommendations"""
    try:
        data = request.get_json()
        domain = data.get('domain', 'general')
        missing_skills = data.get('missing_skills', [])
        experience_level = data.get('experience_level', 'intermediate')
        
        recommendations = study_service.get_personalized_recommendations(
            domain, missing_skills, experience_level
        )
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_resources_bp.route('/interview-guide/<domain>')
def get_interview_guide(domain):
    """Get comprehensive interview preparation guide"""
    try:
        guide = study_service.get_interview_preparation_guide(domain)
        return jsonify(guide)
    except Exception as e:
        return jsonify({'error': str(e)}), 500