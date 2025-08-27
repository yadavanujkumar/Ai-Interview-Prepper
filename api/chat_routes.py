"""
Chat API Routes for Real-time Interview Practice
"""
from flask import request, jsonify, session
from api import api_v1
from services.chat_service import ChatService
import uuid

# Initialize chat service
chat_service = ChatService()

@api_v1.route('/chat/start', methods=['POST'])
def start_chat():
    """Start a new interview chat session"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_description', 'cv_text']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: job_description, cv_text'}), 400
        
        # Generate user ID if not provided
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        # Start chat session
        result = chat_service.start_interview_chat(
            user_id=user_id,
            job_description=data['job_description'],
            cv_text=data['cv_text'],
            difficulty=data.get('difficulty', 'medium'),
            domain=data.get('domain', 'general')
        )
        
        # Store session in Flask session for web interface
        session['chat_session_id'] = result['session_id']
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/chat/message', methods=['POST'])
def send_message():
    """Send a message to the AI interviewer"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get session ID from request or Flask session
        session_id = data.get('session_id') or session.get('chat_session_id')
        if not session_id:
            return jsonify({'error': 'No active chat session'}), 400
        
        # Send message and get response
        result = chat_service.send_message(session_id, data['message'])
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get conversation history for a session"""
    try:
        history = chat_service.get_conversation_history(session_id)
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/chat/end', methods=['POST'])
def end_chat():
    """End the current chat session and get feedback"""
    try:
        data = request.get_json() or {}
        
        # Get session ID from request or Flask session
        session_id = data.get('session_id') or session.get('chat_session_id')
        if not session_id:
            return jsonify({'error': 'No active chat session'}), 400
        
        # End chat session
        result = chat_service.end_interview_chat(session_id)
        
        # Clear session
        session.pop('chat_session_id', None)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/chat/status/<session_id>', methods=['GET'])
def get_chat_status(session_id):
    """Get current status of a chat session"""
    try:
        if session_id not in chat_service.interview_context:
            return jsonify({'error': 'Session not found'}), 404
        
        context = chat_service.interview_context[session_id]
        history_length = len(chat_service.conversation_history.get(session_id, []))
        
        return jsonify({
            'session_id': session_id,
            'context': context,
            'message_count': history_length,
            'status': 'active'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500