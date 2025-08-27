"""
Analytics API Routes for Progress Tracking
"""
from flask import request, jsonify, session
from api import api_v1
from services.analytics_service import AnalyticsService
import uuid

# Initialize analytics service
analytics_service = AnalyticsService()

@api_v1.route('/analytics/track-session', methods=['POST'])
def track_session():
    """Track a user session for analytics"""
    try:
        data = request.get_json()
        
        # Get or generate user ID
        user_id = data.get('user_id') or session.get('user_id') or str(uuid.uuid4())
        session['user_id'] = user_id
        
        # Validate session data
        if 'session_data' not in data:
            return jsonify({'error': 'Session data is required'}), 400
        
        # Track the session
        success = analytics_service.track_user_session(user_id, data['session_data'])
        
        if success:
            return jsonify({
                'success': True,
                'user_id': user_id,
                'message': 'Session tracked successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to track session'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/analytics/progress/<user_id>', methods=['GET'])
@api_v1.route('/analytics/progress', methods=['GET'])
def get_user_progress(user_id=None):
    """Get user progress data"""
    try:
        # Use provided user_id or get from session
        if not user_id:
            user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        progress_data = analytics_service.get_user_progress(user_id)
        
        return jsonify(progress_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/analytics/dashboard/<user_id>', methods=['GET'])
@api_v1.route('/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard(user_id=None):
    """Get analytics dashboard data"""
    try:
        # Use provided user_id or get from session
        if not user_id:
            user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Get time range from query parameters
        time_range = request.args.get('time_range', '30d')
        
        dashboard_data = analytics_service.get_analytics_dashboard(user_id, time_range)
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/analytics/track-interview', methods=['POST'])
def track_interview_performance():
    """Track interview performance specifically"""
    try:
        data = request.get_json()
        
        # Get or generate user ID
        user_id = data.get('user_id') or session.get('user_id') or str(uuid.uuid4())
        session['user_id'] = user_id
        
        # Validate interview data
        if 'interview_data' not in data:
            return jsonify({'error': 'Interview data is required'}), 400
        
        # Track the interview
        success = analytics_service.track_interview_performance(user_id, data['interview_data'])
        
        if success:
            return jsonify({
                'success': True,
                'user_id': user_id,
                'message': 'Interview performance tracked successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to track interview performance'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/analytics/insights/<user_id>', methods=['GET'])
@api_v1.route('/analytics/insights', methods=['GET'])
def get_performance_insights(user_id=None):
    """Get AI-generated performance insights"""
    try:
        # Use provided user_id or get from session
        if not user_id:
            user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        insights = analytics_service.get_performance_insights(user_id)
        
        return jsonify(insights), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/analytics/user-id', methods=['GET', 'POST'])
def manage_user_id():
    """Get or set user ID for session"""
    try:
        if request.method == 'GET':
            # Get current user ID
            user_id = session.get('user_id')
            if not user_id:
                user_id = str(uuid.uuid4())
                session['user_id'] = user_id
            
            return jsonify({'user_id': user_id}), 200
        
        elif request.method == 'POST':
            # Set user ID
            data = request.get_json()
            user_id = data.get('user_id')
            
            if user_id:
                session['user_id'] = user_id
                return jsonify({'user_id': user_id, 'message': 'User ID set successfully'}), 200
            else:
                return jsonify({'error': 'User ID is required'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500