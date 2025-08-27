"""
Job Board Integration API Routes
"""
from flask import request, jsonify
from api import api_v1
from services.job_board_service import JobBoardService

# Initialize job board service
job_board_service = JobBoardService()

@api_v1.route('/jobboards/extract', methods=['POST'])
def extract_job_from_url():
    """Extract job description from a job board URL"""
    try:
        data = request.get_json()
        
        if 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        # Validate URL first
        validation = job_board_service.validate_job_url(url)
        if not validation['valid']:
            return jsonify(validation), 400
        
        # Extract job information
        result = job_board_service.extract_job_from_url(url)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/jobboards/validate', methods=['POST'])
def validate_job_url():
    """Validate if a URL is from a supported job board"""
    try:
        data = request.get_json()
        
        if 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        result = job_board_service.validate_job_url(data['url'])
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/jobboards/supported', methods=['GET'])
def get_supported_job_boards():
    """Get list of supported job board domains"""
    try:
        domains = job_board_service.get_supported_domains()
        
        return jsonify({
            'supported_domains': domains,
            'count': len(domains),
            'examples': [
                'https://www.linkedin.com/jobs/view/123456789',
                'https://www.indeed.com/viewjob?jk=abcd1234',
                'https://www.glassdoor.com/job-listing/example'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/jobboards/search', methods=['POST'])
def search_jobs():
    """Search for jobs on specified job board"""
    try:
        data = request.get_json()
        
        required_fields = ['query']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        location = data.get('location', '')
        job_board = data.get('job_board', 'indeed')
        
        result = job_board_service.search_jobs(query, location, job_board)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500