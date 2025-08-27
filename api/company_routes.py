"""
Company Guide API Routes
"""
from flask import request, jsonify
from api import api_v1
from services.company_guide_service import CompanyGuideService

# Initialize company guide service
company_service = CompanyGuideService()

@api_v1.route('/companies/guide/<company_name>', methods=['GET'])
def get_company_guide(company_name):
    """Get comprehensive interview guide for a company"""
    try:
        guide = company_service.get_company_guide(company_name)
        return jsonify(guide), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/search', methods=['GET'])
def search_companies():
    """Search for companies by name or industry"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        results = company_service.search_companies(query)
        return jsonify({'companies': results, 'count': len(results)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/industry/<industry>', methods=['GET'])
def get_industry_companies(industry):
    """Get companies in a specific industry"""
    try:
        companies = company_service.get_industry_companies(industry)
        return jsonify({'companies': companies, 'industry': industry}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/list', methods=['GET'])
def get_supported_companies():
    """Get list of all supported companies"""
    try:
        companies = company_service.get_supported_companies()
        return jsonify({'companies': companies, 'count': len(companies)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/<company_name>/questions', methods=['GET'])
def get_company_questions(company_name):
    """Get interview questions for a specific company"""
    try:
        question_type = request.args.get('type', 'all')
        questions = company_service.get_company_questions(company_name, question_type)
        return jsonify({
            'company': company_name,
            'question_type': question_type,
            'questions': questions,
            'count': len(questions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/<company_name>/timeline', methods=['GET'])
def get_interview_timeline(company_name):
    """Get interview timeline for a company"""
    try:
        timeline = company_service.get_interview_timeline(company_name)
        return jsonify({
            'company': company_name,
            'timeline': timeline
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/companies/<company_name>/salary', methods=['GET'])
def get_company_salary_insights(company_name):
    """Get salary insights for a company"""
    try:
        role = request.args.get('role', '')
        salary_info = company_service.get_salary_insights(company_name, role)
        return jsonify({
            'company': company_name,
            'role': role,
            'salary_insights': salary_info
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500