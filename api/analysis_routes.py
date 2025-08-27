"""
Analysis API Routes
"""

from flask import jsonify, request
from api import api_v1
from utils.ai_analyzer import AIAnalyzer
from services.study_resources_service import StudyResourcesService

# Initialize services
ai_analyzer = AIAnalyzer()
study_service = StudyResourcesService()

@api_v1.route('/analyze', methods=['POST'])
def analyze_job_cv_fit():
    """Enhanced API endpoint for analysis with study resources"""
    try:
        data = request.get_json()
        jd_text = data.get('job_description', '')
        cv_text = data.get('cv_text', '')
        
        if not jd_text or not cv_text:
            return jsonify({'error': 'Job description and CV text required'}), 400
        
        # Get basic analysis
        result = ai_analyzer.analyze_fit(jd_text, cv_text)
        
        # Enhance with study resources
        domain = result.get('job_analysis', {}).get('domain', 'general')
        missing_skills = result.get('recommendations', {}).get('skills_to_develop', [])
        
        # Add personalized study recommendations
        study_recommendations = study_service.get_personalized_recommendations(
            domain, missing_skills, 'intermediate'
        )
        
        # Add interview preparation guide
        interview_guide = study_service.get_interview_preparation_guide(domain)
        
        # Merge everything together
        result['study_resources'] = study_recommendations
        result['interview_guide'] = interview_guide
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

@api_v1.route('/domains')
def get_supported_domains():
    """Get list of supported domains"""
    domains = [
        'software_engineering', 'data_science', 'product_management', 
        'healthcare', 'education', 'general'
    ]
    return jsonify({'domains': domains})