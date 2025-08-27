import unittest
import sys
import os

# Add the parent directory to sys.path to import the app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.study_resources_service import StudyResourcesService
from utils.interview_generator import InterviewGenerator

class TestEnhancedFeatures(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures for enhanced features."""
        self.study_service = StudyResourcesService()
        self.interview_gen = InterviewGenerator()
        
        # Sample data
        self.sample_jd = """
        Senior Software Engineer Position
        
        We are looking for a skilled senior software engineer with 5+ years of experience.
        
        Requirements:
        - Strong experience with Python, JavaScript, React, Node.js
        - Knowledge of AWS, Docker, Kubernetes
        - Experience with microservices and system design
        - Bachelor's degree in Computer Science or related field
        
        Responsibilities:
        - Design and develop scalable web applications
        - Lead technical discussions and mentor junior developers
        - Implement CI/CD pipelines and DevOps practices
        """
        
        self.sample_cv = """
        Jane Doe
        Senior Software Developer
        
        Experience:
        Senior Software Developer at TechCorp (2019-2024)
        - Developed web applications using Python, React, and Node.js
        - Worked with AWS services and Docker containers
        - Led a team of 3 junior developers
        - Implemented microservices architecture
        
        Software Developer at StartupXYZ (2017-2019)
        - Built REST APIs using Python and Flask
        - Worked with PostgreSQL and Redis
        
        Education:
        Master of Science in Computer Science, Tech University (2017)
        
        Skills:
        Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL, Redis, Git
        """
    
    def test_study_resources_service(self):
        """Test the study resources service functionality."""
        # Test getting resources by domain
        resources = self.study_service.get_resources_by_domain('software_engineering')
        
        self.assertIn('learning_paths', resources)
        self.assertIn('books', resources)
        self.assertIn('online_platforms', resources)
        self.assertIn('practice_projects', resources)
        
        # Test learning paths
        learning_paths = resources['learning_paths']
        self.assertGreater(len(learning_paths), 0)
        self.assertIn('title', learning_paths[0])
        self.assertIn('duration', learning_paths[0])
        self.assertIn('topics', learning_paths[0])
    
    def test_personalized_recommendations(self):
        """Test personalized study recommendations."""
        missing_skills = ['kubernetes', 'system design', 'machine learning']
        recommendations = self.study_service.get_personalized_recommendations(
            'software_engineering', missing_skills, 'intermediate'
        )
        
        self.assertIn('priority_skills', recommendations)
        self.assertIn('recommended_books', recommendations)
        self.assertIn('online_courses', recommendations)
        self.assertIn('practice_projects', recommendations)
        self.assertIn('learning_path', recommendations)
        self.assertIn('study_schedule', recommendations)
        
        # Check that priority skills match missing skills
        self.assertEqual(recommendations['priority_skills'], missing_skills[:5])
    
    def test_interview_preparation_guide(self):
        """Test interview preparation guide generation."""
        guide = self.study_service.get_interview_preparation_guide('software_engineering')
        
        self.assertIn('technical_preparation', guide)
        self.assertIn('behavioral_preparation', guide)
        self.assertIn('domain_specific_tips', guide)
        self.assertIn('common_mistakes', guide)
        self.assertIn('day_before_checklist', guide)
        
        # Check that lists are not empty
        self.assertGreater(len(guide['technical_preparation']), 0)
        self.assertGreater(len(guide['behavioral_preparation']), 0)
        self.assertGreater(len(guide['domain_specific_tips']), 0)
    
    def test_enhanced_question_generation(self):
        """Test enhanced interview question generation with personalized questions."""
        questions = self.interview_gen.generate_questions(self.sample_jd, self.sample_cv, difficulty=2)
        
        # Should have all question types including personalized
        self.assertIn('technical', questions)
        self.assertIn('behavioral', questions)
        self.assertIn('situational', questions)
        self.assertIn('personalized', questions)
        
        # Check personalized questions are generated
        self.assertGreater(len(questions['personalized']), 0)
        
        # Check that technical questions use enhanced templates
        self.assertGreater(len(questions['technical']), 3)  # Should have more questions for medium difficulty
        
        # Verify behavioral questions have enhanced variety
        self.assertGreater(len(questions['behavioral']), 3)
    
    def test_enhanced_domain_detection(self):
        """Test enhanced domain detection with more keywords."""
        # Test software engineering detection
        self.assertEqual(
            self.interview_gen._extract_domain("Full stack developer with React and Node.js"), 
            'software_engineering'
        )
        
        # Test data science detection
        self.assertEqual(
            self.interview_gen._extract_domain("Data scientist with machine learning and TensorFlow"), 
            'data_science'
        )
        
        # Test product management detection
        self.assertEqual(
            self.interview_gen._extract_domain("Product manager for SaaS platform"), 
            'product_management'
        )
    
    def test_personalized_question_content(self):
        """Test that personalized questions contain relevant content."""
        questions = self.interview_gen.generate_questions(self.sample_jd, self.sample_cv, difficulty=3)
        personalized_questions = questions['personalized']
        
        # Should have questions for high difficulty
        self.assertGreaterEqual(len(personalized_questions), 3)
        
        # Check that questions reference relevant technologies/skills
        question_text = ' '.join(personalized_questions).lower()
        
        # Should mention skills present in both JD and CV
        common_skills = ['python', 'react', 'node.js', 'aws', 'docker']
        skill_mentioned = any(skill in question_text for skill in common_skills)
        self.assertTrue(skill_mentioned, "Personalized questions should reference common skills")
    
    def test_study_schedule_generation(self):
        """Test study schedule generation."""
        missing_skills = ['kubernetes', 'system design']
        schedule = self.study_service._generate_study_schedule('software_engineering', missing_skills)
        
        # Should have weekly breakdown
        self.assertIn('week_1_2', schedule)
        self.assertIn('week_3_4', schedule)
        self.assertIn('week_5_6', schedule)
        self.assertIn('week_7_8', schedule)
        
        # Should have daily focus for missing skills
        self.assertIn('daily_focus', schedule)
        self.assertGreater(len(schedule['daily_focus']), 0)
    
    def test_different_domains_resources(self):
        """Test that different domains return different resources."""
        sw_resources = self.study_service.get_resources_by_domain('software_engineering')
        ds_resources = self.study_service.get_resources_by_domain('data_science')
        pm_resources = self.study_service.get_resources_by_domain('product_management')
        
        # Should have different books for different domains
        sw_books = [book['title'] for book in sw_resources['books']]
        ds_books = [book['title'] for book in ds_resources['books']]
        pm_books = [book['title'] for book in pm_resources['books']]
        
        # Books should be different across domains
        self.assertNotEqual(sw_books, ds_books)
        self.assertNotEqual(sw_books, pm_books)
        self.assertNotEqual(ds_books, pm_books)
    
    def test_enhanced_parameters_usage(self):
        """Test that enhanced parameters are used in question generation."""
        # Get parameters for software engineering
        params = self.interview_gen._get_enhanced_domain_params('software_engineering', ['python', 'react'])
        
        # Should have enhanced parameter categories
        self.assertIn('concept1', params)
        self.assertIn('concept2', params)
        self.assertIn('technology', params)
        self.assertIn('feature', params)
        self.assertIn('system_type', params)
        
        # Should include user skills in technology parameters
        self.assertIn('python', [tech.lower() for tech in params.get('technology', [])])
        self.assertIn('react', [tech.lower() for tech in params.get('technology', [])])

if __name__ == '__main__':
    unittest.main()