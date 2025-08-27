"""
Feature routes (additional functionality)
"""
from flask import Blueprint, render_template, request, current_app

features_bp = Blueprint('features', __name__)


@features_bp.route('/chat')
def chat():
    """AI Interview Chat page"""
    return render_template('chat.html')


@features_bp.route('/analytics')
def analytics():
    """Analytics dashboard page"""
    return render_template('analytics.html')


@features_bp.route('/companies')
def companies():
    """Company guides page"""
    return render_template('companies.html')


@features_bp.route('/salary')
def salary():
    """Salary negotiation page"""
    return render_template('salary.html')


@features_bp.route('/study-resources')
def study_resources():
    """Study resources page"""
    domain = request.args.get('domain', 'general')
    resources = current_app.study_service.get_resources_by_domain(domain)
    learning_path = current_app.study_service.get_learning_path(domain)
    interview_guide = current_app.study_service.get_interview_preparation_guide(domain)
    
    return render_template('study_resources.html', 
                         domain=domain,
                         resources=resources,
                         learning_path=learning_path,
                         interview_guide=interview_guide)