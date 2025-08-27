"""
Localization API Routes
"""
from flask import request, jsonify, session
from api import api_v1
from services.localization_service import LocalizationService

# Initialize localization service
localization_service = LocalizationService()

@api_v1.route('/localization/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        languages = localization_service.get_supported_languages()
        return jsonify(languages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/set-language', methods=['POST'])
def set_language():
    """Set the current language for the session"""
    try:
        data = request.get_json()
        language_code = data.get('language', 'en')
        
        success = localization_service.set_language(language_code)
        
        if success:
            session['language'] = language_code
            return jsonify({
                'success': True,
                'language': language_code,
                'message': 'Language set successfully'
            }), 200
        else:
            return jsonify({'error': 'Unsupported language'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/text/<key>', methods=['GET'])
def get_localized_text(key):
    """Get localized text for a specific key"""
    try:
        language = session.get('language', 'en')
        text = localization_service.get_text(key, language)
        
        return jsonify({
            'key': key,
            'language': language,
            'text': text
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/content/<content_type>', methods=['GET'])
def get_localized_content(content_type):
    """Get localized content for specific content types"""
    try:
        language = request.args.get('language') or session.get('language', 'en')
        content = localization_service.get_localized_content(content_type, language)
        
        return jsonify({
            'content_type': content_type,
            'language': language,
            'content': content
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/translate-questions', methods=['POST'])
def translate_interview_questions():
    """Translate interview questions to target language"""
    try:
        data = request.get_json()
        
        questions = data.get('questions', [])
        target_language = data.get('target_language', 'en')
        
        if not questions:
            return jsonify({'error': 'Questions are required'}), 400
        
        translated_questions = localization_service.translate_interview_questions(
            questions, target_language
        )
        
        return jsonify({
            'original_questions': questions,
            'translated_questions': translated_questions,
            'target_language': target_language
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/domains', methods=['GET'])
def get_localized_domains():
    """Get domain names in specific language"""
    try:
        language = request.args.get('language') or session.get('language', 'en')
        domains = localization_service.get_language_specific_domains(language)
        
        return jsonify({
            'language': language,
            'domains': domains
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/localization/current-language', methods=['GET'])
def get_current_language():
    """Get the current language setting"""
    try:
        current_language = session.get('language', 'en')
        return jsonify({
            'current_language': current_language,
            'available_languages': localization_service.get_supported_languages()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500