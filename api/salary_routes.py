"""
Salary Negotiation API Routes
"""
from flask import request, jsonify
from api import api_v1
from services.salary_negotiation_service import SalaryNegotiationService

# Initialize salary service
salary_service = SalaryNegotiationService()

@api_v1.route('/salary/guidance', methods=['POST'])
def get_salary_guidance():
    """Get comprehensive salary negotiation guidance"""
    try:
        data = request.get_json()
        
        role = data.get('role', '')
        location = data.get('location', '')
        experience_years = data.get('experience_years', 0)
        company = data.get('company', '')
        industry = data.get('industry', '')
        
        if not role:
            return jsonify({'error': 'Role is required'}), 400
        
        guidance = salary_service.get_salary_guidance(
            role, location, experience_years, company, industry
        )
        
        return jsonify(guidance), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/market-data', methods=['POST'])
def get_market_data():
    """Get market salary data for a role"""
    try:
        data = request.get_json()
        
        role = data.get('role', '')
        location = data.get('location', '')
        experience_years = data.get('experience_years', 0)
        industry = data.get('industry', '')
        
        if not role:
            return jsonify({'error': 'Role is required'}), 400
        
        market_data = salary_service.get_market_data(
            role, location, experience_years, industry
        )
        
        return jsonify(market_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/strategies', methods=['POST'])
def get_negotiation_strategies():
    """Get negotiation strategies"""
    try:
        data = request.get_json()
        
        role = data.get('role', '')
        experience_years = data.get('experience_years', 0)
        company = data.get('company', '')
        
        if not role:
            return jsonify({'error': 'Role is required'}), 400
        
        strategies = salary_service.get_negotiation_strategies(
            role, experience_years, company
        )
        
        return jsonify({'strategies': strategies}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/preparation', methods=['GET'])
def get_negotiation_preparation():
    """Get negotiation preparation checklist"""
    try:
        preparation = salary_service.get_negotiation_preparation()
        return jsonify(preparation), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/mistakes', methods=['GET'])
def get_common_mistakes():
    """Get common negotiation mistakes to avoid"""
    try:
        mistakes = salary_service.get_common_mistakes()
        return jsonify({'mistakes': mistakes}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/timeline', methods=['GET'])
def get_negotiation_timeline():
    """Get negotiation timeline and best practices"""
    try:
        timeline = salary_service.get_negotiation_timeline()
        return jsonify(timeline), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/scripts', methods=['GET'])
def get_negotiation_scripts():
    """Get sample negotiation scripts and templates"""
    try:
        scripts = salary_service.get_negotiation_scripts()
        return jsonify(scripts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/benefits', methods=['GET'])
def get_benefits_breakdown():
    """Get comprehensive benefits breakdown"""
    try:
        benefits = salary_service.get_benefits_breakdown()
        return jsonify(benefits), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/resources', methods=['GET'])
def get_research_resources():
    """Get salary research resources"""
    try:
        resources = salary_service.get_research_resources()
        return jsonify(resources), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/salary/score-offer', methods=['POST'])
def score_job_offer():
    """Calculate and score a job offer"""
    try:
        data = request.get_json()
        
        offer_details = data.get('offer_details', {})
        preferences = data.get('preferences', {})
        
        if not offer_details:
            return jsonify({'error': 'Offer details are required'}), 400
        
        score_result = salary_service.calculate_offer_score(offer_details, preferences)
        
        return jsonify(score_result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500