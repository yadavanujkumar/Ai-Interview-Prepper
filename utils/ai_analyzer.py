import os
import json
import re
from typing import Dict, List, Any

class AIAnalyzer:
    """Handles AI analysis of job descriptions and CVs"""
    
    def __init__(self):
        # For now, we'll use rule-based analysis with AI-like scoring
        # In production, you would integrate with OpenAI API
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        
    def analyze_fit(self, jd_text: str, cv_text: str) -> Dict[str, Any]:
        """Analyze fit between job description and CV"""
        
        # Extract key information
        jd_analysis = self._analyze_job_description(jd_text)
        cv_analysis = self._analyze_cv(cv_text)
        
        # Calculate fit scores
        fit_scores = self._calculate_fit_scores(jd_analysis, cv_analysis)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(jd_analysis, cv_analysis, fit_scores)
        
        return {
            'job_analysis': jd_analysis,
            'cv_analysis': cv_analysis,
            'fit_scores': fit_scores,
            'recommendations': recommendations,
            'overall_score': fit_scores['overall'],
            'summary': self._generate_summary(fit_scores)
        }
    
    def _analyze_job_description(self, jd_text: str) -> Dict[str, Any]:
        """Extract key information from job description"""
        
        # Simple keyword extraction (in production, use NLP/AI)
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science', 'angular', 'vue',
            'html', 'css', 'git', 'linux', 'mongodb', 'postgresql', 'redis'
        ]
        
        soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'creative', 'adaptable', 'organized', 'detail-oriented', 'collaborative'
        ]
        
        experience_levels = ['entry level', 'junior', 'senior', 'lead', 'principal', 'manager']
        
        jd_lower = jd_text.lower()
        
        # Extract years of experience
        experience_match = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?experience', jd_lower)
        required_experience = int(experience_match.group(1)) if experience_match else 0
        
        # Extract domain/industry
        domain = self._extract_domain(jd_text)
        
        return {
            'domain': domain,
            'required_skills': [skill for skill in tech_keywords if skill in jd_lower],
            'soft_skills': [skill for skill in soft_skills if skill in jd_lower],
            'experience_required': required_experience,
            'seniority_level': next((level for level in experience_levels if level in jd_lower), 'not specified'),
            'key_responsibilities': self._extract_responsibilities(jd_text)
        }
    
    def _analyze_cv(self, cv_text: str) -> Dict[str, Any]:
        """Extract key information from CV"""
        
        cv_lower = cv_text.lower()
        
        # Extract experience (simple heuristic)
        experience_years = self._calculate_experience_years(cv_text)
        
        # Extract skills
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science', 'angular', 'vue',
            'html', 'css', 'git', 'linux', 'mongodb', 'postgresql', 'redis'
        ]
        
        # Extract education
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        education_level = 'not specified'
        if any(keyword in cv_lower for keyword in education_keywords):
            if 'master' in cv_lower or 'mba' in cv_lower:
                education_level = 'masters'
            elif 'phd' in cv_lower or 'doctorate' in cv_lower:
                education_level = 'doctorate'
            else:
                education_level = 'bachelors'
        
        return {
            'experience_years': experience_years,
            'skills': [skill for skill in tech_keywords if skill in cv_lower],
            'education_level': education_level,
            'domains': self._extract_cv_domains(cv_text),
            'certifications': self._extract_certifications(cv_text)
        }
    
    def _calculate_fit_scores(self, jd_analysis: Dict, cv_analysis: Dict) -> Dict[str, float]:
        """Calculate various fit scores"""
        
        # Skills match
        jd_skills = set(jd_analysis['required_skills'])
        cv_skills = set(cv_analysis['skills'])
        skills_match = len(jd_skills.intersection(cv_skills)) / max(len(jd_skills), 1) * 100
        
        # Experience match
        experience_ratio = cv_analysis['experience_years'] / max(jd_analysis['experience_required'], 1)
        experience_match = min(experience_ratio * 100, 100)
        
        # Education match (basic scoring)
        education_scores = {'not specified': 50, 'bachelors': 70, 'masters': 85, 'doctorate': 95}
        education_match = education_scores.get(cv_analysis['education_level'], 50)
        
        # Overall score (weighted average)
        overall = (skills_match * 0.4 + experience_match * 0.4 + education_match * 0.2)
        
        return {
            'skills': round(skills_match, 1),
            'experience': round(experience_match, 1),
            'education': round(education_match, 1),
            'overall': round(overall, 1)
        }
    
    def _generate_recommendations(self, jd_analysis: Dict, cv_analysis: Dict, fit_scores: Dict) -> Dict[str, List[str]]:
        """Generate personalized recommendations"""
        
        recommendations = {
            'skills_to_develop': [],
            'experience_gaps': [],
            'study_plan': [],
            'resume_improvements': []
        }
        
        # Skills recommendations
        missing_skills = set(jd_analysis['required_skills']) - set(cv_analysis['skills'])
        recommendations['skills_to_develop'] = list(missing_skills)
        
        # Experience recommendations
        if cv_analysis['experience_years'] < jd_analysis['experience_required']:
            gap = jd_analysis['experience_required'] - cv_analysis['experience_years']
            recommendations['experience_gaps'].append(f"Consider gaining {gap} more years of relevant experience")
        
        # Study plan based on domain
        domain = jd_analysis['domain']
        if domain == 'software_engineering':
            recommendations['study_plan'] = [
                "Practice coding problems on LeetCode/HackerRank",
                "Study system design principles",
                "Review data structures and algorithms",
                "Practice behavioral interview questions"
            ]
        elif domain == 'data_science':
            recommendations['study_plan'] = [
                "Review statistics and probability concepts",
                "Practice machine learning algorithms",
                "Study data visualization techniques",
                "Work on end-to-end data science projects"
            ]
        else:
            recommendations['study_plan'] = [
                "Research industry-specific best practices",
                "Study relevant tools and technologies",
                "Practice problem-solving scenarios",
                "Prepare for behavioral questions"
            ]
        
        # Resume improvements
        if fit_scores['skills'] < 70:
            recommendations['resume_improvements'].append("Highlight relevant technical skills more prominently")
        if fit_scores['experience'] < 70:
            recommendations['resume_improvements'].append("Emphasize relevant work experience and achievements")
        
        return recommendations
    
    def _extract_domain(self, jd_text: str) -> str:
        """Extract domain/industry from job description"""
        jd_lower = jd_text.lower()
        
        if any(term in jd_lower for term in ['software', 'developer', 'engineer', 'programming']):
            return 'software_engineering'
        elif any(term in jd_lower for term in ['data scientist', 'machine learning', 'analytics']):
            return 'data_science'
        elif any(term in jd_lower for term in ['doctor', 'physician', 'medical', 'healthcare']):
            return 'healthcare'
        elif any(term in jd_lower for term in ['teacher', 'educator', 'professor', 'instructor']):
            return 'education'
        elif any(term in jd_lower for term in ['designer', 'creative', 'graphic', 'ui/ux']):
            return 'design'
        elif any(term in jd_lower for term in ['marketing', 'sales', 'business development']):
            return 'marketing_sales'
        else:
            return 'general'
    
    def _extract_responsibilities(self, jd_text: str) -> List[str]:
        """Extract key responsibilities from job description"""
        # Simple extraction - in production, use NLP
        lines = jd_text.split('\n')
        responsibilities = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or 'responsible' in line.lower()):
                responsibilities.append(line)
        
        return responsibilities[:5]  # Return top 5
    
    def _calculate_experience_years(self, cv_text: str) -> int:
        """Calculate years of experience from CV"""
        # Simple heuristic - count date ranges
        import datetime
        current_year = datetime.datetime.now().year
        
        # Look for year patterns
        years = re.findall(r'\b(19|20)\d{2}\b', cv_text)
        if years:
            years = [int(year) for year in years]
            min_year = min(years)
            return max(0, current_year - min_year)
        
        return 0
    
    def _extract_cv_domains(self, cv_text: str) -> List[str]:
        """Extract domains from CV"""
        cv_lower = cv_text.lower()
        domains = []
        
        if any(term in cv_lower for term in ['software', 'developer', 'engineer', 'programming']):
            domains.append('software_engineering')
        if any(term in cv_lower for term in ['data', 'analytics', 'machine learning']):
            domains.append('data_science')
        if any(term in cv_lower for term in ['design', 'creative', 'ui', 'ux']):
            domains.append('design')
        
        return domains
    
    def _extract_certifications(self, cv_text: str) -> List[str]:
        """Extract certifications from CV"""
        # Simple pattern matching
        cert_patterns = [
            r'AWS\s+Certified',
            r'Google\s+Cloud',
            r'Microsoft\s+Azure',
            r'PMP',
            r'Scrum\s+Master',
            r'Certified\s+\w+'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, cv_text, re.IGNORECASE)
            certifications.extend(matches)
        
        return certifications
    
    def _generate_summary(self, fit_scores: Dict[str, float]) -> str:
        """Generate overall fit summary"""
        overall_score = fit_scores['overall']
        
        if overall_score >= 80:
            return "Excellent fit! You are well-qualified for this position."
        elif overall_score >= 60:
            return "Good fit with some areas for improvement."
        elif overall_score >= 40:
            return "Moderate fit. Consider developing key skills before applying."
        else:
            return "Limited fit. Significant preparation needed for this role."