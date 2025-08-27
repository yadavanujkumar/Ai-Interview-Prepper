"""
Feature routes (additional API functionality)
"""
from flask import Blueprint, request, jsonify, current_app

features_bp = Blueprint('features', __name__)


@features_bp.route('/api/chat', methods=['GET', 'POST'])
def chat():
    """AI Interview Chat API"""
    if request.method == 'GET':
        return jsonify({
            'message': 'Chat endpoint ready',
            'endpoints': [
                '/api/chat - POST with {"message": "your question"}',
            ]
        })
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Simple chat response (can be enhanced with actual AI)
        response = {
            'response': f"Thanks for your question: '{message}'. This is a placeholder response. The chat feature can be enhanced with actual AI integration.",
            'timestamp': str(request.date),
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@features_bp.route('/api/analytics')
def analytics():
    """Analytics API endpoint"""
    return jsonify({
        'message': 'Analytics dashboard data',
        'features': [
            'CV analysis trends',
            'Interview performance metrics', 
            'Skill gap analysis',
            'Market demand insights'
        ],
        'status': 'placeholder'
    })


@features_bp.route('/api/companies')
def companies():
    """Company guides API"""
    companies_data = {
        'tech_giants': [
            {'name': 'Google', 'focus': 'Technical excellence, cultural fit'},
            {'name': 'Microsoft', 'focus': 'Growth mindset, collaboration'},
            {'name': 'Amazon', 'focus': 'Leadership principles, customer obsession'},
            {'name': 'Apple', 'focus': 'Innovation, attention to detail'}
        ],
        'startups': [
            {'name': 'Early Stage', 'focus': 'Adaptability, multi-tasking'},
            {'name': 'Growth Stage', 'focus': 'Scaling experience, systems thinking'}
        ],
        'consulting': [
            {'name': 'McKinsey', 'focus': 'Problem-solving, structured thinking'},
            {'name': 'BCG', 'focus': 'Creative solutions, client impact'}
        ]
    }
    
    return jsonify(companies_data)


@features_bp.route('/api/salary')
def salary():
    """Salary negotiation guidance API"""
    salary_data = {
        'negotiation_tips': [
            'Research market rates for your role and location',
            'Prepare your value proposition with specific examples',
            'Consider the total compensation package',
            'Practice your negotiation conversation',
            'Be prepared to walk away if needed'
        ],
        'factors_to_consider': [
            'Base salary',
            'Bonuses and equity',
            'Benefits and perks',
            'Growth opportunities',
            'Work-life balance'
        ],
        'common_mistakes': [
            'Not researching market rates',
            'Accepting the first offer',
            'Focusing only on salary',
            'Being too aggressive or passive',
            'Not getting offers in writing'
        ]
    }
    
    return jsonify(salary_data)


@features_bp.route('/api/study-resources')
def study_resources():
    """Study resources API"""
    domain = request.args.get('domain', 'general')
    
    try:
        resources = current_app.study_service.get_resources_by_domain(domain)
        learning_path = current_app.study_service.get_learning_path(domain)
        interview_guide = current_app.study_service.get_interview_preparation_guide(domain)
        
        return jsonify({
            'domain': domain,
            'resources': resources,
            'learning_path': learning_path, 
            'interview_guide': interview_guide
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500