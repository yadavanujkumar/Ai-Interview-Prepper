"""
Interview API Routes  
"""

from flask import jsonify, request
from api import interview_bp
from utils.interview_generator import InterviewGenerator

# Initialize service
interview_gen = InterviewGenerator()

@interview_bp.route('/generate', methods=['POST'])
def generate_interview_questions():
    """Generate interview questions via API"""
    try:
        data = request.get_json()
        jd_text = data.get('job_description', '')
        cv_text = data.get('cv_text', '')
        difficulty = data.get('difficulty', 2)
        
        if not jd_text or not cv_text:
            return jsonify({'error': 'Job description and CV text required'}), 400
        
        questions = interview_gen.generate_questions(jd_text, cv_text, difficulty)
        
        # Add metadata
        response = {
            'questions': questions,
            'metadata': {
                'difficulty': difficulty,
                'total_questions': sum(len(q) for q in questions.values()),
                'categories': list(questions.keys())
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/question-tips/<category>')
def get_question_tips(category):
    """Get tips for answering specific question categories"""
    tips = {
        'technical': {
            'approach': 'Think out loud and explain your reasoning',
            'tips': [
                'Break down complex problems into smaller parts',
                'Consider multiple solutions and trade-offs',
                'Discuss time and space complexity',
                'Ask clarifying questions',
                'Test your solution with examples'
            ]
        },
        'behavioral': {
            'approach': 'Use the STAR method (Situation, Task, Action, Result)',
            'tips': [
                'Be specific with examples',
                'Focus on your role and actions',
                'Quantify results when possible',
                'Show learning and growth',
                'Keep answers concise but complete'
            ]
        },
        'situational': {
            'approach': 'Use a structured problem-solving framework',
            'tips': [
                'Understand the problem completely',
                'Consider stakeholder perspectives',
                'Propose multiple solutions',
                'Explain your decision-making process',
                'Discuss implementation and follow-up'
            ]
        },
        'personalized': {
            'approach': 'Draw from your actual experience and be authentic',
            'tips': [
                'Prepare specific examples from your background',
                'Connect your experience to the role requirements',
                'Show progression and learning over time',
                'Demonstrate impact and results',
                'Be honest about challenges and how you overcame them'
            ]
        }
    }
    
    return jsonify(tips.get(category, {'error': 'Category not found'}))