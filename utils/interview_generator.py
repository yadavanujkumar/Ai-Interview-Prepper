import random
from typing import List, Dict, Any

class InterviewGenerator:
    """Generates mock interview questions based on job description and CV"""
    
    def __init__(self):
        self.question_templates = {
            'technical': {
                'software_engineering': [
                    "Explain the difference between {concept1} and {concept2}",
                    "How would you implement {feature} in {technology}?",
                    "What are the pros and cons of using {technology}?",
                    "Walk me through how you would design a {system_type}",
                    "How do you handle {technical_challenge} in your code?"
                ],
                'data_science': [
                    "Explain how {algorithm} works and when you would use it",
                    "How would you approach a {data_problem} problem?",
                    "What metrics would you use to evaluate {model_type}?",
                    "How do you handle {data_issue} in your datasets?",
                    "Walk me through your process for {data_task}"
                ],
                'general': [
                    "How would you approach {problem_type}?",
                    "What tools would you use for {task}?",
                    "Explain your experience with {skill}",
                    "How do you stay updated with {field} trends?",
                    "What's your process for {work_activity}?"
                ]
            },
            'behavioral': [
                "Tell me about a time when you faced a significant challenge at work",
                "Describe a situation where you had to work with a difficult team member",
                "Give me an example of when you had to learn something new quickly",
                "Tell me about a project you're particularly proud of",
                "Describe a time when you had to meet a tight deadline",
                "How do you handle constructive criticism?",
                "Tell me about a time when you made a mistake and how you handled it",
                "Describe a situation where you had to take initiative",
                "Give me an example of when you had to persuade someone to see your point of view",
                "Tell me about a time when you had to adapt to a significant change"
            ],
            'situational': {
                'software_engineering': [
                    "Your application is experiencing performance issues. How would you diagnose and fix them?",
                    "A critical bug is found in production. Walk me through your response process",
                    "You need to integrate with a third-party API that has poor documentation. How do you proceed?",
                    "Your team is split on a technical decision. How do you reach consensus?",
                    "You're behind schedule on a project. How do you handle this situation?"
                ],
                'data_science': [
                    "Your model's accuracy suddenly drops in production. How do you investigate?",
                    "Stakeholders want results from incomplete data. How do you respond?",
                    "You find significant bias in your training data. What's your approach?",
                    "Multiple models give conflicting predictions. How do you proceed?",
                    "You need to explain complex results to non-technical stakeholders. How do you approach this?"
                ],
                'healthcare': [
                    "A patient presents with symptoms that could indicate multiple conditions. How do you proceed?",
                    "You disagree with a colleague's treatment recommendation. How do you handle this?",
                    "A patient is non-compliant with their treatment plan. What's your approach?",
                    "You make an error in patient care. How do you handle the situation?",
                    "Multiple emergencies arrive simultaneously. How do you prioritize?"
                ],
                'education': [
                    "A student is consistently disruptive in class. How do you address this?",
                    "Parents disagree with your teaching methods. How do you respond?",
                    "You have students with vastly different learning abilities. How do you adapt?",
                    "Budget cuts affect your classroom resources. How do you adapt?",
                    "A student reports bullying. What's your response process?"
                ],
                'general': [
                    "You're assigned a project outside your expertise. How do you approach it?",
                    "You receive conflicting priorities from different managers. How do you handle this?",
                    "A client is unsatisfied with your work. How do you address their concerns?",
                    "You notice a colleague consistently missing deadlines. What do you do?",
                    "You're asked to present to senior leadership with short notice. How do you prepare?"
                ]
            }
        }
    
    def generate_questions(self, jd_text: str, cv_text: str, difficulty: int = 2) -> Dict[str, List[str]]:
        """Generate interview questions based on difficulty level (1-3)"""
        
        domain = self._extract_domain(jd_text)
        skills = self._extract_skills(jd_text, cv_text)
        
        questions = {
            'technical': self._generate_technical_questions(domain, skills, difficulty),
            'behavioral': self._generate_behavioral_questions(difficulty),
            'situational': self._generate_situational_questions(domain, difficulty)
        }
        
        return questions
    
    def _generate_technical_questions(self, domain: str, skills: List[str], difficulty: int) -> List[str]:
        """Generate technical questions based on domain and skills"""
        
        templates = self.question_templates['technical'].get(domain, self.question_templates['technical']['general'])
        questions = []
        
        # Domain-specific question parameters
        params = self._get_domain_params(domain, skills)
        
        # Generate questions based on difficulty
        num_questions = 3 + difficulty  # 4-6 questions
        
        for i in range(num_questions):
            template = random.choice(templates)
            question = self._fill_template(template, params)
            questions.append(question)
        
        return questions
    
    def _generate_behavioral_questions(self, difficulty: int) -> List[str]:
        """Generate behavioral questions"""
        
        num_questions = 2 + difficulty  # 3-5 questions
        return random.sample(self.question_templates['behavioral'], min(num_questions, len(self.question_templates['behavioral'])))
    
    def _generate_situational_questions(self, domain: str, difficulty: int) -> List[str]:
        """Generate situational questions"""
        
        questions = self.question_templates['situational'].get(domain, self.question_templates['situational']['general'])
        num_questions = 2 + difficulty  # 3-5 questions
        
        return random.sample(questions, min(num_questions, len(questions)))
    
    def _extract_domain(self, jd_text: str) -> str:
        """Extract domain from job description"""
        jd_lower = jd_text.lower()
        
        if any(term in jd_lower for term in ['software', 'developer', 'engineer', 'programming']):
            return 'software_engineering'
        elif any(term in jd_lower for term in ['data scientist', 'machine learning', 'analytics']):
            return 'data_science'
        elif any(term in jd_lower for term in ['doctor', 'physician', 'medical', 'healthcare']):
            return 'healthcare'
        elif any(term in jd_lower for term in ['teacher', 'educator', 'professor', 'instructor']):
            return 'education'
        else:
            return 'general'
    
    def _extract_skills(self, jd_text: str, cv_text: str) -> List[str]:
        """Extract relevant skills from job description and CV"""
        
        combined_text = (jd_text + " " + cv_text).lower()
        
        skills = []
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science', 'angular', 'vue',
            'html', 'css', 'git', 'linux', 'mongodb', 'postgresql', 'redis',
            'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'
        ]
        
        for skill in skill_keywords:
            if skill in combined_text:
                skills.append(skill)
        
        return skills
    
    def _get_domain_params(self, domain: str, skills: List[str]) -> Dict[str, List[str]]:
        """Get domain-specific parameters for question templates"""
        
        base_params = {
            'technology': skills if skills else ['your preferred technology'],
            'skill': skills if skills else ['relevant skills'],
            'field': [domain.replace('_', ' ')],
            'problem_type': ['complex problem', 'technical challenge', 'difficult situation'],
            'task': ['project planning', 'implementation', 'optimization'],
            'work_activity': ['problem solving', 'decision making', 'collaboration']
        }
        
        if domain == 'software_engineering':
            base_params.update({
                'concept1': ['REST', 'OOP', 'SQL', 'NoSQL', 'synchronous'],
                'concept2': ['GraphQL', 'functional programming', 'NoSQL', 'SQL', 'asynchronous'],
                'feature': ['authentication system', 'payment gateway', 'search functionality', 'real-time notifications'],
                'system_type': ['distributed system', 'microservices architecture', 'database schema', 'API'],
                'technical_challenge': ['performance optimization', 'memory management', 'concurrency', 'error handling']
            })
        elif domain == 'data_science':
            base_params.update({
                'algorithm': ['linear regression', 'random forest', 'neural networks', 'clustering'],
                'data_problem': ['classification', 'regression', 'clustering', 'recommendation'],
                'model_type': ['classification model', 'regression model', 'clustering algorithm'],
                'data_issue': ['missing values', 'outliers', 'class imbalance', 'data leakage'],
                'data_task': ['feature engineering', 'model selection', 'data preprocessing', 'model validation']
            })
        
        return base_params
    
    def _fill_template(self, template: str, params: Dict[str, List[str]]) -> str:
        """Fill template with random parameters"""
        
        import re
        
        # Find all placeholders in the template
        placeholders = re.findall(r'\{(\w+)\}', template)
        
        filled_template = template
        for placeholder in placeholders:
            if placeholder in params:
                replacement = random.choice(params[placeholder])
                filled_template = filled_template.replace(f'{{{placeholder}}}', replacement)
        
        return filled_template