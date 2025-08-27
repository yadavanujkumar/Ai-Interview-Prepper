"""
Flask extensions initialization
"""
from utils.document_processor import DocumentProcessor
from utils.ai_analyzer import AIAnalyzer
from utils.interview_generator import InterviewGenerator
from services.study_resources_service import StudyResourcesService


# Initialize core services
doc_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()
interview_gen = InterviewGenerator()
study_service = StudyResourcesService()


def init_extensions(app):
    """Initialize Flask extensions and services"""
    
    # Store services in app context for easy access
    app.doc_processor = doc_processor
    app.ai_analyzer = ai_analyzer
    app.interview_gen = interview_gen
    app.study_service = study_service
    
    # Initialize any other extensions here
    # e.g., database, cache, etc.
    
    return app