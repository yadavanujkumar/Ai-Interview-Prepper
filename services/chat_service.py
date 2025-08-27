"""
Real-time AI Chat Service for Interview Practice
"""
import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime

class ChatService:
    """Service for handling real-time AI chat during interview practice"""
    
    def __init__(self):
        self.conversation_history = {}
        self.interview_context = {}
        
    def start_interview_chat(self, user_id: str, job_description: str, cv_text: str, 
                           difficulty: str = 'medium', domain: str = 'general') -> Dict[str, Any]:
        """Start a new interview chat session"""
        session_id = f"{user_id}_{int(datetime.now().timestamp())}"
        
        # Set up interview context
        self.interview_context[session_id] = {
            'job_description': job_description,
            'cv_text': cv_text,
            'difficulty': difficulty,
            'domain': domain,
            'started_at': datetime.now().isoformat(),
            'question_count': 0,
            'current_phase': 'introduction'
        }
        
        # Initialize conversation history
        self.conversation_history[session_id] = []
        
        # Generate opening message
        opening_message = self._generate_opening_message(domain, difficulty)
        
        return {
            'session_id': session_id,
            'message': opening_message,
            'status': 'started',
            'context': self.interview_context[session_id]
        }
    
    def send_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Process user message and generate AI response"""
        if session_id not in self.conversation_history:
            return {'error': 'Invalid session ID'}
        
        # Add user message to history
        self.conversation_history[session_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate AI response
        ai_response = self._generate_ai_response(session_id, user_message)
        
        # Add AI response to history
        self.conversation_history[session_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update context
        self._update_interview_context(session_id, user_message, ai_response)
        
        return {
            'message': ai_response,
            'context': self.interview_context[session_id],
            'conversation_length': len(self.conversation_history[session_id])
        }
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        return self.conversation_history.get(session_id, [])
    
    def end_interview_chat(self, session_id: str) -> Dict[str, Any]:
        """End interview chat session and provide feedback"""
        if session_id not in self.conversation_history:
            return {'error': 'Invalid session ID'}
        
        # Generate interview feedback
        feedback = self._generate_interview_feedback(session_id)
        
        # Mark session as ended
        self.interview_context[session_id]['ended_at'] = datetime.now().isoformat()
        self.interview_context[session_id]['status'] = 'completed'
        
        return {
            'feedback': feedback,
            'session_summary': self.interview_context[session_id],
            'total_messages': len(self.conversation_history[session_id])
        }
    
    def _generate_opening_message(self, domain: str, difficulty: str) -> str:
        """Generate opening message for interview"""
        domain_greetings = {
            'software_engineering': "Hello! I'm your AI interviewer for this software engineering position. I'll be asking you technical and behavioral questions based on the job description and your background.",
            'data_science': "Welcome! I'm here to conduct your data science interview. We'll cover technical concepts, problem-solving, and your experience with data analysis.",
            'general': "Hello! Welcome to your mock interview session. I'll be asking you questions relevant to the position and your background."
        }
        
        difficulty_note = {
            'easy': "We'll start with some foundational questions to warm up.",
            'medium': "I'll ask questions that match typical interview difficulty.",
            'hard': "Be prepared for challenging questions that test your expertise."
        }
        
        greeting = domain_greetings.get(domain, domain_greetings['general'])
        note = difficulty_note.get(difficulty, difficulty_note['medium'])
        
        return f"{greeting} {note} Let's begin with a simple question: Could you briefly introduce yourself and tell me what interests you most about this role?"
    
    def _generate_ai_response(self, session_id: str, user_message: str) -> str:
        """Generate AI response using context and conversation history"""
        context = self.interview_context[session_id]
        history = self.conversation_history[session_id]
        
        # Determine next question type based on conversation flow
        response_type = self._determine_response_type(context, len(history))
        
        if response_type == 'follow_up':
            return self._generate_follow_up_question(user_message, context)
        elif response_type == 'technical':
            return self._generate_technical_question(context)
        elif response_type == 'behavioral':
            return self._generate_behavioral_question(context)
        elif response_type == 'feedback':
            return self._generate_response_feedback(user_message, context)
        else:
            return self._generate_general_response(user_message, context)
    
    def _determine_response_type(self, context: Dict, message_count: int) -> str:
        """Determine what type of response to generate"""
        if message_count <= 2:
            return 'follow_up'
        elif message_count <= 6:
            return 'technical' if context['domain'] == 'software_engineering' else 'behavioral'
        elif message_count <= 10:
            return 'behavioral'
        else:
            return 'feedback'
    
    def _generate_technical_question(self, context: Dict) -> str:
        """Generate technical questions based on domain"""
        domain = context['domain']
        difficulty = context['difficulty']
        
        technical_questions = {
            'software_engineering': {
                'easy': [
                    "Can you explain the difference between a stack and a queue?",
                    "What is object-oriented programming and its main principles?",
                    "How would you explain recursion to someone new to programming?"
                ],
                'medium': [
                    "How would you design a URL shortener like bit.ly?",
                    "Explain the differences between SQL and NoSQL databases.",
                    "What are microservices and their advantages over monolithic architecture?"
                ],
                'hard': [
                    "Design a distributed caching system for a high-traffic application.",
                    "How would you handle race conditions in a multi-threaded environment?",
                    "Explain the CAP theorem and its implications for distributed systems."
                ]
            },
            'data_science': {
                'easy': [
                    "What's the difference between supervised and unsupervised learning?",
                    "Can you explain what overfitting is and how to prevent it?",
                    "What are the basic steps in a data science project?"
                ],
                'medium': [
                    "How would you handle missing data in a dataset?",
                    "Explain the bias-variance tradeoff in machine learning.",
                    "What evaluation metrics would you use for a classification problem?"
                ],
                'hard': [
                    "Design a recommendation system for a streaming platform.",
                    "How would you detect and handle concept drift in a production model?",
                    "Explain how you would approach A/B testing for a machine learning model."
                ]
            }
        }
        
        questions = technical_questions.get(domain, {}).get(difficulty, [
            "Can you walk me through a challenging project you've worked on?",
            "How do you approach learning new technologies?",
            "What technical skills do you want to develop further?"
        ])
        
        import random
        return random.choice(questions)
    
    def _generate_behavioral_question(self, context: Dict) -> str:
        """Generate behavioral questions"""
        behavioral_questions = [
            "Tell me about a time when you had to work with a difficult team member. How did you handle it?",
            "Describe a situation where you had to meet a tight deadline. What was your approach?",
            "Can you share an example of when you had to learn something completely new for a project?",
            "Tell me about a time when you disagreed with your manager or team lead. How did you handle it?",
            "Describe a project where you had to overcome significant obstacles.",
            "Can you give me an example of when you had to explain a complex technical concept to a non-technical person?"
        ]
        
        import random
        return random.choice(behavioral_questions)
    
    def _generate_follow_up_question(self, user_message: str, context: Dict) -> str:
        """Generate follow-up questions based on user response"""
        follow_ups = [
            "That's interesting! Can you elaborate on that a bit more?",
            "What challenges did you face in that situation?",
            "How did you measure the success of that approach?",
            "What would you do differently if you encountered a similar situation again?",
            "Can you walk me through your thought process there?"
        ]
        
        import random
        return random.choice(follow_ups)
    
    def _generate_response_feedback(self, user_message: str, context: Dict) -> str:
        """Generate feedback on user's response"""
        return "Thank you for sharing that. Let me ask you another question to explore a different aspect of your experience."
    
    def _generate_general_response(self, user_message: str, context: Dict) -> str:
        """Generate general response"""
        return "I appreciate your response. Let's move on to another area I'd like to explore with you."
    
    def _update_interview_context(self, session_id: str, user_message: str, ai_response: str):
        """Update interview context based on conversation"""
        context = self.interview_context[session_id]
        context['question_count'] += 1
        
        # Update phase based on question count
        if context['question_count'] <= 2:
            context['current_phase'] = 'introduction'
        elif context['question_count'] <= 6:
            context['current_phase'] = 'technical'
        elif context['question_count'] <= 10:
            context['current_phase'] = 'behavioral'
        else:
            context['current_phase'] = 'closing'
    
    def _generate_interview_feedback(self, session_id: str) -> Dict[str, Any]:
        """Generate comprehensive feedback for the interview"""
        context = self.interview_context[session_id]
        history = self.conversation_history[session_id]
        
        # Analyze conversation for feedback
        user_responses = [msg['content'] for msg in history if msg['role'] == 'user']
        
        feedback = {
            'overall_performance': 'Good',
            'strengths': [
                'Clear communication',
                'Relevant experience sharing',
                'Good engagement throughout the interview'
            ],
            'areas_for_improvement': [
                'Could provide more specific examples',
                'Consider using the STAR method for behavioral questions',
                'Practice explaining technical concepts more concisely'
            ],
            'recommendations': [
                'Practice more technical problems related to your field',
                'Prepare specific examples using the STAR method',
                'Research the company and role more thoroughly'
            ],
            'session_stats': {
                'duration_minutes': 15,  # Placeholder
                'questions_answered': len(user_responses),
                'phases_covered': ['introduction', 'technical', 'behavioral']
            }
        }
        
        return feedback