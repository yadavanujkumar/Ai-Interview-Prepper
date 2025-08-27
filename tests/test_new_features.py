"""
Tests for the new enhanced features
"""
import unittest
import tempfile
import os
import json
from services.chat_service import ChatService
from services.job_board_service import JobBoardService
from services.analytics_service import AnalyticsService
from services.localization_service import LocalizationService
from services.company_guide_service import CompanyGuideService
from services.salary_negotiation_service import SalaryNegotiationService

class TestNewFeatures(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures for new features"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Initialize services
        self.chat_service = ChatService()
        self.job_board_service = JobBoardService()
        self.analytics_service = AnalyticsService(data_dir=self.temp_dir)
        self.localization_service = LocalizationService(languages_dir=os.path.join(self.temp_dir, 'languages'))
        self.company_service = CompanyGuideService(data_dir=self.temp_dir)
        self.salary_service = SalaryNegotiationService(data_dir=self.temp_dir)
    
    def test_chat_service_start_session(self):
        """Test starting a chat session"""
        result = self.chat_service.start_interview_chat(
            user_id='test_user',
            job_description='Software Engineer at Tech Company',
            cv_text='Experienced developer with Python skills',
            difficulty='medium',
            domain='software_engineering'
        )
        
        self.assertIn('session_id', result)
        self.assertIn('message', result)
        self.assertEqual(result['status'], 'started')
        
        # Test session is tracked
        session_id = result['session_id']
        self.assertIn(session_id, self.chat_service.interview_context)
    
    def test_chat_service_send_message(self):
        """Test sending a message in chat"""
        # Start session first
        result = self.chat_service.start_interview_chat(
            user_id='test_user',
            job_description='Software Engineer position',
            cv_text='Python developer',
            difficulty='medium'
        )
        session_id = result['session_id']
        
        # Send a message
        response = self.chat_service.send_message(session_id, 'I have 3 years of Python experience')
        
        self.assertIn('message', response)
        self.assertIn('context', response)
        self.assertGreater(response['conversation_length'], 1)
    
    def test_chat_service_end_session(self):
        """Test ending a chat session"""
        # Start and use session
        result = self.chat_service.start_interview_chat(
            user_id='test_user',
            job_description='Test job',
            cv_text='Test CV'
        )
        session_id = result['session_id']
        
        self.chat_service.send_message(session_id, 'Test message')
        
        # End session
        end_result = self.chat_service.end_interview_chat(session_id)
        
        self.assertIn('feedback', end_result)
        self.assertIn('session_summary', end_result)
        self.assertIn('total_messages', end_result)
    
    def test_job_board_service_validate_url(self):
        """Test job board URL validation"""
        # Test valid URLs
        valid_urls = [
            'https://www.linkedin.com/jobs/view/123456',
            'https://indeed.com/viewjob?jk=test123',
            'https://www.glassdoor.com/job-listing/test'
        ]
        
        for url in valid_urls:
            result = self.job_board_service.validate_job_url(url)
            self.assertTrue(result['valid'])
            self.assertTrue(result['supported'])
        
        # Test invalid URL
        invalid_result = self.job_board_service.validate_job_url('https://example.com/job')
        self.assertFalse(invalid_result['supported'])
    
    def test_job_board_service_supported_domains(self):
        """Test getting supported domains"""
        domains = self.job_board_service.get_supported_domains()
        
        self.assertIsInstance(domains, list)
        self.assertIn('linkedin.com', domains)
        self.assertIn('indeed.com', domains)
        self.assertGreater(len(domains), 0)
    
    def test_analytics_service_track_session(self):
        """Test tracking user sessions"""
        session_data = {
            'session_id': 'test_session_123',
            'activity_type': 'interview_practice',
            'duration_minutes': 15,
            'questions_answered': 5,
            'domain': 'software_engineering',
            'difficulty': 'medium',
            'completion_status': 'completed',
            'scores': {'overall_rating': 7}
        }
        
        success = self.analytics_service.track_user_session('test_user', session_data)
        self.assertTrue(success)
        
        # Check if session was tracked
        progress = self.analytics_service.get_user_progress('test_user')
        self.assertIn('statistics', progress)
        self.assertEqual(progress['statistics']['total_sessions'], 1)
    
    def test_analytics_service_get_dashboard(self):
        """Test getting analytics dashboard"""
        # Track a few sessions first
        for i in range(3):
            session_data = {
                'session_id': f'test_session_{i}',
                'activity_type': 'interview_practice',
                'duration_minutes': 10 + i,
                'questions_answered': 3 + i,
                'domain': 'software_engineering',
                'completion_status': 'completed'
            }
            self.analytics_service.track_user_session('test_user', session_data)
        
        dashboard = self.analytics_service.get_analytics_dashboard('test_user', '30d')
        
        self.assertIn('session_count', dashboard)
        self.assertIn('total_time_minutes', dashboard)
        self.assertIn('domain_distribution', dashboard)
        self.assertEqual(dashboard['session_count'], 3)
    
    def test_analytics_service_performance_insights(self):
        """Test getting performance insights"""
        # Track some sessions with scores
        session_data = {
            'session_id': 'test_session',
            'activity_type': 'interview_practice',
            'duration_minutes': 20,
            'questions_answered': 8,
            'domain': 'software_engineering',
            'completion_status': 'completed',
            'scores': {'overall_rating': 8}
        }
        self.analytics_service.track_user_session('test_user', session_data)
        
        insights = self.analytics_service.get_performance_insights('test_user')
        
        self.assertIn('strengths', insights)
        self.assertIn('improvement_areas', insights)
        self.assertIn('learning_patterns', insights)
        self.assertIn('next_steps', insights)
    
    def test_localization_service_supported_languages(self):
        """Test getting supported languages"""
        languages = self.localization_service.get_supported_languages()
        
        self.assertIsInstance(languages, dict)
        self.assertIn('en', languages)
        self.assertIn('es', languages)
        self.assertIn('fr', languages)
        self.assertEqual(languages['en'], 'English')
    
    def test_localization_service_set_language(self):
        """Test setting language"""
        # Test valid language
        success = self.localization_service.set_language('es')
        self.assertTrue(success)
        self.assertEqual(self.localization_service.current_language, 'es')
        
        # Test invalid language
        success = self.localization_service.set_language('invalid')
        self.assertFalse(success)
    
    def test_localization_service_get_text(self):
        """Test getting localized text"""
        # Test English (default)
        text = self.localization_service.get_text('app.title')
        self.assertIn('AI Interview Prepper', text)
        
        # Test Spanish
        self.localization_service.set_language('es')
        text = self.localization_service.get_text('app.title')
        self.assertIn('Preparador de Entrevistas IA', text)
        
        # Test missing key
        text = self.localization_service.get_text('nonexistent.key')
        self.assertIn('[Missing:', text)
    
    def test_localization_service_domain_translations(self):
        """Test domain name translations"""
        # Test English domains
        domains_en = self.localization_service.get_language_specific_domains('en')
        self.assertIn('software_engineering', domains_en)
        self.assertEqual(domains_en['software_engineering'], 'Software Engineering')
        
        # Test Spanish domains
        domains_es = self.localization_service.get_language_specific_domains('es')
        self.assertIn('software_engineering', domains_es)
        self.assertEqual(domains_es['software_engineering'], 'Ingeniería de Software')
    
    def test_company_service_get_guide(self):
        """Test getting company interview guide"""
        # Test known company
        guide = self.company_service.get_company_guide('Google')
        
        self.assertIn('company_name', guide)
        self.assertIn('overview', guide)
        self.assertIn('interview_process', guide)
        self.assertIn('common_questions', guide)
        self.assertIn('preparation_tips', guide)
        
        # Test unknown company
        unknown_guide = self.company_service.get_company_guide('Unknown Company')
        self.assertIn('note', unknown_guide['overview'])
    
    def test_company_service_search(self):
        """Test searching companies"""
        results = self.company_service.search_companies('Google')
        
        self.assertIsInstance(results, list)
        if results:  # If Google is in the database
            self.assertTrue(any('Google' in company['name'] for company in results))
    
    def test_company_service_get_questions(self):
        """Test getting company-specific questions"""
        questions = self.company_service.get_company_questions('Google', 'all')
        
        self.assertIsInstance(questions, list)
        
        # Test question type filtering
        tech_questions = self.company_service.get_company_questions('Google', 'technical')
        behavioral_questions = self.company_service.get_company_questions('Google', 'behavioral')
        
        self.assertIsInstance(tech_questions, list)
        self.assertIsInstance(behavioral_questions, list)
    
    def test_salary_service_get_market_data(self):
        """Test getting salary market data"""
        market_data = self.salary_service.get_market_data(
            role='Software Engineer',
            location='San Francisco',
            experience_years=3,
            industry='Technology'
        )
        
        self.assertIn('salary_range', market_data)
        self.assertIn('market_percentiles', market_data)
        self.assertIn('total_compensation', market_data)
        self.assertIn('confidence_level', market_data)
        
        # Check salary range structure
        salary_range = market_data['salary_range']
        self.assertIn('min', salary_range)
        self.assertIn('median', salary_range)
        self.assertIn('max', salary_range)
    
    def test_salary_service_get_negotiation_strategies(self):
        """Test getting negotiation strategies"""
        strategies = self.salary_service.get_negotiation_strategies(
            role='Software Engineer',
            experience_years=5,
            company='Google'
        )
        
        self.assertIsInstance(strategies, list)
        self.assertGreater(len(strategies), 0)
        
        # Check strategy structure
        if strategies:
            strategy = strategies[0]
            self.assertIn('strategy', strategy)
            self.assertIn('description', strategy)
            self.assertIn('talking_points', strategy)
    
    def test_salary_service_preparation_checklist(self):
        """Test getting negotiation preparation checklist"""
        preparation = self.salary_service.get_negotiation_preparation()
        
        self.assertIn('research_phase', preparation)
        self.assertIn('documentation', preparation)
        self.assertIn('strategy_development', preparation)
        self.assertIn('practice_and_rehearsal', preparation)
        
        # Check each phase has items
        for phase in preparation.values():
            self.assertIsInstance(phase, list)
            self.assertGreater(len(phase), 0)
    
    def test_salary_service_common_mistakes(self):
        """Test getting common negotiation mistakes"""
        mistakes = self.salary_service.get_common_mistakes()
        
        self.assertIsInstance(mistakes, list)
        self.assertGreater(len(mistakes), 0)
        
        # Check mistake structure
        if mistakes:
            mistake = mistakes[0]
            self.assertIn('mistake', mistake)
            self.assertIn('why_problematic', mistake)
            self.assertIn('how_to_avoid', mistake)
    
    def test_salary_service_offer_scoring(self):
        """Test job offer scoring"""
        offer_details = {
            'base_salary': 120000,
            'bonus': 15000,
            'equity': 30000,
            'benefits': ['health_insurance', '401k_match', 'unlimited_pto'],
            'wlb_features': ['flexible_hours', 'remote_work'],
            'growth_features': ['mentorship', 'training_budget']
        }
        
        preferences = {
            'base_salary': 40,
            'work_life_balance': 30,
            'growth_opportunities': 20,
            'benefits': 10
        }
        
        score_result = self.salary_service.calculate_offer_score(offer_details, preferences)
        
        self.assertIn('overall_score', score_result)
        self.assertIn('component_scores', score_result)
        self.assertIn('weights_used', score_result)
        self.assertIn('recommendations', score_result)
        
        # Check score is within valid range
        self.assertGreaterEqual(score_result['overall_score'], 0)
        self.assertLessEqual(score_result['overall_score'], 10)

if __name__ == '__main__':
    unittest.main()