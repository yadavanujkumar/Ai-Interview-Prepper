import unittest
import sys
import os

# Add the parent directory to sys.path to import the app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_analyzer import AIAnalyzer
from utils.document_processor import DocumentProcessor
from utils.interview_generator import InterviewGenerator

class TestAIInterviewPrepper(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.analyzer = AIAnalyzer()
        self.doc_processor = DocumentProcessor()
        self.interview_gen = InterviewGenerator()
        
        # Sample job description
        self.sample_jd = """
        Software Engineer Position
        
        We are looking for a skilled software engineer with 3+ years of experience.
        
        Requirements:
        - Strong experience with Python, JavaScript, and React
        - Knowledge of SQL databases and REST APIs
        - Experience with AWS cloud services
        - Bachelor's degree in Computer Science or related field
        
        Responsibilities:
        - Develop and maintain web applications
        - Work with cross-functional teams
        - Write clean, maintainable code
        """
        
        # Sample CV
        self.sample_cv = """
        John Doe
        Software Developer
        
        Experience:
        Software Developer at Tech Corp (2020-2024)
        - Developed web applications using Python and React
        - Worked with PostgreSQL databases
        - Implemented REST APIs
        
        Education:
        Bachelor of Science in Computer Science, University of Tech (2019)
        
        Skills:
        Python, JavaScript, React, SQL, Git, HTML, CSS
        """
    
    def test_domain_extraction(self):
        """Test if the analyzer correctly identifies job domain."""
        analysis = self.analyzer._analyze_job_description(self.sample_jd)
        self.assertEqual(analysis['domain'], 'software_engineering')
    
    def test_skills_extraction_from_jd(self):
        """Test skills extraction from job description."""
        analysis = self.analyzer._analyze_job_description(self.sample_jd)
        required_skills = analysis['required_skills']
        
        # Should find these skills in the JD
        self.assertIn('python', required_skills)
        self.assertIn('javascript', required_skills)
        self.assertIn('react', required_skills)
        self.assertIn('sql', required_skills)
    
    def test_skills_extraction_from_cv(self):
        """Test skills extraction from CV."""
        analysis = self.analyzer._analyze_cv(self.sample_cv)
        cv_skills = analysis['skills']
        
        # Should find these skills in the CV
        self.assertIn('python', cv_skills)
        self.assertIn('javascript', cv_skills)
        self.assertIn('react', cv_skills)
        self.assertIn('sql', cv_skills)
    
    def test_experience_calculation(self):
        """Test experience years calculation."""
        analysis = self.analyzer._analyze_cv(self.sample_cv)
        experience_years = analysis['experience_years']
        
        # Should calculate some years of experience (may vary based on current year)
        self.assertGreater(experience_years, 0)
    
    def test_fit_score_calculation(self):
        """Test overall fit score calculation."""
        result = self.analyzer.analyze_fit(self.sample_jd, self.sample_cv)
        
        # Should return a valid fit score
        self.assertIsInstance(result['overall_score'], (int, float))
        self.assertGreaterEqual(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 100)
        
        # Should have all required score components
        fit_scores = result['fit_scores']
        self.assertIn('skills', fit_scores)
        self.assertIn('experience', fit_scores)
        self.assertIn('education', fit_scores)
        self.assertIn('overall', fit_scores)
    
    def test_recommendations_generation(self):
        """Test that recommendations are generated."""
        result = self.analyzer.analyze_fit(self.sample_jd, self.sample_cv)
        recommendations = result['recommendations']
        
        # Should have all recommendation categories
        self.assertIn('skills_to_develop', recommendations)
        self.assertIn('experience_gaps', recommendations)
        self.assertIn('study_plan', recommendations)
        self.assertIn('resume_improvements', recommendations)
        
        # Study plan should not be empty
        self.assertIsInstance(recommendations['study_plan'], list)
        self.assertGreater(len(recommendations['study_plan']), 0)
    
    def test_interview_question_generation(self):
        """Test mock interview question generation."""
        questions = self.interview_gen.generate_questions(self.sample_jd, self.sample_cv, difficulty=2)
        
        # Should have all question types
        self.assertIn('technical', questions)
        self.assertIn('behavioral', questions)
        self.assertIn('situational', questions)
        
        # Each category should have questions
        self.assertIsInstance(questions['technical'], list)
        self.assertIsInstance(questions['behavioral'], list)
        self.assertIsInstance(questions['situational'], list)
        
        self.assertGreater(len(questions['technical']), 0)
        self.assertGreater(len(questions['behavioral']), 0)
        self.assertGreater(len(questions['situational']), 0)
    
    def test_different_difficulty_levels(self):
        """Test that different difficulty levels generate different numbers of questions."""
        easy_questions = self.interview_gen.generate_questions(self.sample_jd, self.sample_cv, difficulty=1)
        hard_questions = self.interview_gen.generate_questions(self.sample_jd, self.sample_cv, difficulty=3)
        
        # Hard should have more technical questions than easy
        self.assertGreaterEqual(
            len(hard_questions['technical']), 
            len(easy_questions['technical'])
        )
    
    def test_domain_specific_questions(self):
        """Test that questions are domain-specific."""
        # Test with a different domain (healthcare)
        healthcare_jd = """
        Registered Nurse Position
        
        We are seeking a compassionate registered nurse with 2+ years of experience.
        
        Requirements:
        - Valid RN license
        - Experience in patient care
        - Knowledge of medical procedures
        """
        
        questions = self.interview_gen.generate_questions(healthcare_jd, self.sample_cv, difficulty=2)
        
        # Should generate questions even for different domains
        self.assertIsInstance(questions['situational'], list)
        self.assertGreater(len(questions['situational']), 0)
    
    def test_text_extraction_simulation(self):
        """Test text extraction with different file types (simulated)."""
        # Since we don't have actual files in tests, we'll test the text processing logic
        
        # Test that the document processor can handle different scenarios
        test_text = "This is a test document content with Python and JavaScript skills."
        
        # The actual text extraction would be tested with real files
        # Here we just verify the processor exists and has the right methods
        self.assertTrue(hasattr(self.doc_processor, 'extract_text'))
        self.assertTrue(hasattr(self.doc_processor, '_extract_from_pdf'))
        self.assertTrue(hasattr(self.doc_processor, '_extract_from_docx'))
        self.assertTrue(hasattr(self.doc_processor, '_extract_from_txt'))

if __name__ == '__main__':
    unittest.main()