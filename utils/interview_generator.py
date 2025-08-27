import random
from typing import List, Dict, Any

class InterviewGenerator:
    """Enhanced interview question generator with sophisticated AI-powered questions"""
    
    def __init__(self):
        self.question_templates = {
            'technical': {
                'software_engineering': [
                    # Core Programming Concepts
                    "Explain the difference between {concept1} and {concept2}",
                    "How would you implement {feature} in {technology}?",
                    "What are the pros and cons of using {technology}?",
                    "Walk me through how you would design a {system_type}",
                    "How do you handle {technical_challenge} in your code?",
                    # Advanced System Design
                    "How would you design a scalable {system_type} that handles millions of users?",
                    "Explain how you would implement caching for a {application_type}",
                    "How would you ensure data consistency in a distributed {system_type}?",
                    "Walk me through your approach to optimizing database queries for {use_case}",
                    "How would you implement real-time features in a {application_type}?",
                    # Code Quality & Best Practices
                    "How do you ensure code quality in a team environment?",
                    "Explain your approach to writing testable code",
                    "How would you refactor legacy code while maintaining functionality?",
                    "Describe your debugging process for complex issues",
                    "How do you handle code reviews and provide constructive feedback?"
                ],
                'data_science': [
                    # ML Fundamentals
                    "Explain how {algorithm} works and when you would use it",
                    "How would you approach a {data_problem} problem?",
                    "What metrics would you use to evaluate {model_type}?",
                    "How do you handle {data_issue} in your datasets?",
                    "Walk me through your process for {data_task}",
                    # Advanced ML Concepts
                    "How would you detect and handle overfitting in your model?",
                    "Explain the bias-variance tradeoff in machine learning",
                    "How would you design an A/B testing framework for ML models?",
                    "Walk me through feature engineering for {domain} data",
                    "How would you deploy and monitor ML models in production?",
                    # Data Engineering
                    "How would you design a data pipeline for real-time processing?",
                    "Explain your approach to handling missing data",
                    "How would you ensure data quality and integrity?",
                    "Describe your process for exploratory data analysis",
                    "How would you handle class imbalance in your dataset?"
                ],
                'product_management': [
                    "How would you prioritize features for a {product_type}?",
                    "Walk me through your process for conducting user research",
                    "How would you measure the success of a new feature?",
                    "Explain how you would handle conflicting stakeholder requirements",
                    "How do you approach competitive analysis?",
                    "Describe your process for creating a product roadmap",
                    "How would you handle a feature that's not performing well?",
                    "Walk me through your approach to market sizing",
                    "How do you balance technical debt with new feature development?",
                    "Explain your process for gathering and analyzing user feedback"
                ],
                'general': [
                    "How would you approach {problem_type}?",
                    "What tools would you use for {task}?",
                    "Explain your experience with {skill}",
                    "How do you stay updated with {field} trends?",
                    "What's your process for {work_activity}?",
                    "How do you prioritize tasks when everything seems urgent?",
                    "Describe your approach to learning new technologies",
                    "How do you handle working with tight deadlines?",
                    "Explain your process for making decisions with incomplete information",
                    "How do you ensure quality while maintaining efficiency?"
                ]
            },
            'behavioral': [
                # Leadership & Teamwork
                "Tell me about a time when you had to lead a team through a difficult situation",
                "Describe a situation where you had to work with a difficult team member",
                "Give me an example of when you had to motivate a demotivated team",
                "Tell me about a time when you had to give difficult feedback to a colleague",
                "Describe a situation where you had to collaborate with a cross-functional team",
                
                # Problem-Solving & Innovation
                "Tell me about a time when you faced a significant challenge at work",
                "Give me an example of when you had to think creatively to solve a problem",
                "Describe a time when you had to make a decision with limited information",
                "Tell me about a project where you had to overcome multiple obstacles",
                "Give me an example of when you improved an existing process",
                
                # Learning & Adaptation
                "Give me an example of when you had to learn something new quickly",
                "Tell me about a time when you had to adapt to a significant change",
                "Describe a situation where you made a mistake and how you handled it",
                "Tell me about a time when you received constructive criticism",
                "Give me an example of when you had to step outside your comfort zone",
                
                # Achievement & Impact
                "Tell me about a project you're particularly proud of",
                "Describe a time when you exceeded expectations",
                "Give me an example of when you had to persuade someone to see your point of view",
                "Tell me about a time when you had to meet a tight deadline",
                "Describe a situation where you took initiative without being asked",
                
                # Conflict Resolution & Communication
                "Tell me about a time when you had to resolve a conflict between team members",
                "Describe a situation where you had to communicate complex information to non-technical stakeholders",
                "Give me an example of when you had to deliver bad news",
                "Tell me about a time when you disagreed with your manager's decision",
                "Describe a situation where you had to build consensus among stakeholders"
            ],
            'situational': {
                'software_engineering': [
                    # Production & Performance Issues
                    "Your application is experiencing performance issues. How would you diagnose and fix them?",
                    "A critical bug is found in production. Walk me through your response process",
                    "The system goes down during peak hours. How do you handle the incident?",
                    "You discover a security vulnerability in your code. What's your immediate response?",
                    "Database queries are timing out frequently. How do you investigate and resolve this?",
                    
                    # Team & Technical Decisions
                    "You need to integrate with a third-party API that has poor documentation. How do you proceed?",
                    "Your team is split on a technical decision. How do you reach consensus?",
                    "A senior developer insists on using an outdated technology. How do you address this?",
                    "You're asked to estimate a complex project with many unknowns. How do you approach this?",
                    "The client wants to add major features close to the deadline. How do you respond?",
                    
                    # Code Quality & Process
                    "You inherit a legacy codebase with no documentation. How do you proceed?",
                    "A team member consistently writes code that breaks the build. How do you handle this?",
                    "You're behind schedule on a project. How do you handle this situation?",
                    "Code reviews are taking too long and blocking development. How do you optimize this process?",
                    "You find a critical flaw in code that's already been deployed. What's your approach?"
                ],
                'data_science': [
                    # Model & Data Issues
                    "Your model's accuracy suddenly drops in production. How do you investigate?",
                    "You find significant bias in your training data. What's your approach?",
                    "Multiple models give conflicting predictions. How do you proceed?",
                    "Your dataset has 70% missing values for a crucial feature. How do you handle this?",
                    "A model performs well in testing but poorly in production. What could be wrong?",
                    
                    # Stakeholder & Communication
                    "Stakeholders want results from incomplete data. How do you respond?",
                    "You need to explain complex results to non-technical stakeholders. How do you approach this?",
                    "Management wants to deploy a model you believe isn't ready. How do you handle this?",
                    "Business stakeholders disagree with your feature importance findings. How do you respond?",
                    "You're asked to build a model with unrealistic accuracy expectations. How do you manage this?",
                    
                    # Ethics & Compliance
                    "You discover your model may discriminate against certain groups. What's your response?",
                    "Data privacy regulations change mid-project. How do you adapt?",
                    "You're pressured to use data that may violate privacy policies. How do you respond?"
                ],
                'product_management': [
                    # Strategy & Prioritization
                    "Engineering says a critical feature will take 6 months, but sales promised it in 2. How do you handle this?",
                    "Two equally important stakeholders want conflicting features. How do you decide?",
                    "User research contradicts your product hypothesis. How do you proceed?",
                    "A competitor launches a feature you were planning. How do you respond?",
                    "Your product metrics are declining despite recent feature launches. What's your approach?",
                    
                    # Resource & Timeline Management
                    "The engineering team is consistently missing deadlines. How do you address this?",
                    "Budget cuts force you to reduce your team by 30%. How do you prioritize?",
                    "A key engineer quits mid-project. How do you adjust your roadmap?",
                    "Marketing wants to launch before the product is fully ready. How do you handle this?",
                    "You discover a major usability issue one week before launch. What do you do?"
                ],
                'general': [
                    # Project & Resource Management
                    "You're assigned a project outside your expertise. How do you approach it?",
                    "You receive conflicting priorities from different managers. How do you handle this?",
                    "Your team's budget is cut by 40% mid-project. How do you adapt?",
                    "A key team member is underperforming. How do you address this?",
                    "You're asked to deliver impossible results with limited resources. How do you respond?",
                    
                    # Client & Stakeholder Relations
                    "A client is unsatisfied with your work. How do you address their concerns?",
                    "You notice a colleague consistently missing deadlines. What do you do?",
                    "A stakeholder bypasses you to make direct requests to your team. How do you handle this?",
                    "You disagree with a decision made by senior leadership. How do you proceed?",
                    "You're asked to present to senior leadership with short notice. How do you prepare?",
                    
                    # Crisis & Change Management
                    "Your company is undergoing a major restructuring. How do you manage your team through this?",
                    "A major client threatens to leave unless you make immediate changes. What's your approach?",
                    "You discover unethical practices in your organization. How do you respond?",
                    "Remote work policies change suddenly. How do you adapt your team's workflow?",
                    "A natural disaster affects your ability to deliver. How do you manage the situation?"
                ]
            },
            
            # Enhanced parameter templates for better question generation
            'parameters': {
                'software_engineering': {
                    'concept1': ['synchronous', 'REST', 'SQL', 'object-oriented', 'functional', 'monolithic'],
                    'concept2': ['asynchronous', 'GraphQL', 'NoSQL', 'functional programming', 'reactive', 'microservices'],
                    'technology': ['React', 'Node.js', 'Python', 'Docker', 'Kubernetes', 'AWS', 'PostgreSQL', 'Redis'],
                    'feature': ['authentication system', 'real-time chat', 'payment processing', 'file upload', 'search functionality'],
                    'system_type': ['e-commerce platform', 'social media app', 'messaging system', 'content management system', 'API gateway'],
                    'technical_challenge': ['memory leaks', 'race conditions', 'deadlocks', 'performance bottlenecks', 'data consistency'],
                    'application_type': ['web application', 'mobile app', 'distributed system', 'API service', 'microservice'],
                    'use_case': ['high-traffic scenarios', 'real-time applications', 'data-intensive operations', 'multi-tenant systems']
                },
                'data_science': {
                    'algorithm': ['Random Forest', 'Linear Regression', 'K-means clustering', 'Neural Networks', 'SVM', 'Gradient Boosting'],
                    'data_problem': ['classification', 'regression', 'clustering', 'anomaly detection', 'time series forecasting'],
                    'model_type': ['classification model', 'regression model', 'recommendation system', 'deep learning model'],
                    'data_issue': ['missing values', 'outliers', 'class imbalance', 'data drift', 'multicollinearity'],
                    'data_task': ['feature engineering', 'model selection', 'hyperparameter tuning', 'model deployment', 'A/B testing'],
                    'domain': ['healthcare', 'finance', 'e-commerce', 'social media', 'transportation']
                },
                'product_management': {
                    'product_type': ['mobile app', 'SaaS platform', 'e-commerce site', 'social network', 'enterprise software'],
                    'metric_type': ['user engagement', 'conversion rate', 'retention', 'revenue', 'customer satisfaction'],
                    'feature_type': ['user onboarding', 'payment system', 'notification system', 'search functionality', 'recommendation engine']
                },
                'general': {
                    'problem_type': ['complex technical issue', 'team conflict', 'resource constraint', 'deadline pressure', 'quality issue'],
                    'task': ['project planning', 'team coordination', 'stakeholder communication', 'quality assurance', 'process improvement'],
                    'skill': ['communication', 'leadership', 'analytical thinking', 'project management', 'technical expertise'],
                    'field': ['technology', 'data science', 'product management', 'marketing', 'operations'],
                    'work_activity': ['code review', 'requirements gathering', 'testing', 'documentation', 'team meetings']
                }
            }
        }
    
    def generate_questions(self, jd_text: str, cv_text: str, difficulty: int = 2) -> Dict[str, List[str]]:
        """Generate interview questions based on difficulty level (1-3)"""
        
        domain = self._extract_domain(jd_text)
        skills = self._extract_skills(jd_text, cv_text)
        
        questions = {
            'technical': self._generate_technical_questions(domain, skills, difficulty),
            'behavioral': self._generate_behavioral_questions(difficulty),
            'situational': self._generate_situational_questions(domain, difficulty),
            'personalized': self._generate_personalized_questions(jd_text, cv_text, domain, difficulty)
        }
        
        return questions
    
    def _generate_technical_questions(self, domain: str, skills: List[str], difficulty: int) -> List[str]:
        """Generate technical questions based on domain and skills"""
        
        templates = self.question_templates['technical'].get(domain, self.question_templates['technical']['general'])
        questions = []
        
        # Get enhanced parameters
        params = self._get_enhanced_domain_params(domain, skills)
        
        # Generate questions based on difficulty (more questions for higher difficulty)
        base_questions = 3
        num_questions = base_questions + difficulty  # 4-6 questions
        
        # Ensure we have unique questions
        selected_templates = random.sample(templates, min(num_questions, len(templates)))
        
        for template in selected_templates:
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
        """Extract domain from job description with enhanced detection"""
        jd_lower = jd_text.lower()
        
        # Software Engineering keywords
        if any(term in jd_lower for term in [
            'software', 'developer', 'engineer', 'programming', 'frontend', 'backend', 
            'fullstack', 'devops', 'python', 'java', 'javascript', 'react', 'angular', 
            'node.js', 'api', 'microservices', 'database'
        ]):
            return 'software_engineering'
        
        # Data Science keywords  
        elif any(term in jd_lower for term in [
            'data scientist', 'machine learning', 'analytics', 'data engineer', 
            'ml engineer', 'ai', 'artificial intelligence', 'statistics', 'pandas', 
            'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'big data'
        ]):
            return 'data_science'
            
        # Product Management keywords
        elif any(term in jd_lower for term in [
            'product manager', 'product owner', 'product strategy', 'roadmap', 
            'user research', 'agile', 'scrum', 'stakeholder', 'market research',
            'product development', 'product marketing'
        ]):
            return 'product_management'
            
        # Healthcare keywords
        elif any(term in jd_lower for term in [
            'doctor', 'physician', 'medical', 'healthcare', 'nurse', 'clinical',
            'patient care', 'hospital', 'medical device', 'pharmaceutical'
        ]):
            return 'healthcare'
            
        # Education keywords
        elif any(term in jd_lower for term in [
            'teacher', 'educator', 'professor', 'instructor', 'curriculum',
            'academic', 'education', 'training', 'learning'
        ]):
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
    
    def _get_enhanced_domain_params(self, domain: str, skills: List[str]) -> Dict[str, List[str]]:
        """Get enhanced parameters using the new parameter templates"""
        domain_params = self.question_templates['parameters'].get(domain, {})
        general_params = self.question_templates['parameters']['general']
        
        # Merge domain-specific and general parameters
        combined_params = {**general_params, **domain_params}
        
        # Add user skills to relevant parameters
        if skills:
            combined_params['skill'] = skills + combined_params.get('skill', [])
            combined_params['technology'] = skills + combined_params.get('technology', [])
        
        return combined_params
    
    def _generate_personalized_questions(self, jd_text: str, cv_text: str, domain: str, difficulty: int) -> List[str]:
        """Generate personalized questions based on job description and CV content"""
        personalized_questions = []
        
        # Extract specific technologies/skills mentioned in both JD and CV
        common_skills = self._find_common_skills(jd_text, cv_text)
        jd_requirements = self._extract_key_requirements(jd_text)
        
        # Generate questions based on common skills
        for skill in common_skills[:2]:  # Limit to top 2 skills
            personalized_questions.append(f"Tell me about a specific project where you used {skill}. What challenges did you face?")
        
        # Generate questions based on JD requirements
        for requirement in jd_requirements[:2]:  # Limit to top 2 requirements
            personalized_questions.append(f"How would you approach {requirement} in this role?")
        
        # Add experience-based questions
        if difficulty >= 2:
            personalized_questions.append("Walk me through your most challenging project and how you overcame the obstacles.")
            
        if difficulty >= 3:
            personalized_questions.append("If you could redesign any system you've worked on, what would you change and why?")
        
        return personalized_questions[:difficulty + 1]  # Return 2-4 questions based on difficulty
    
    def _find_common_skills(self, jd_text: str, cv_text: str) -> List[str]:
        """Find skills mentioned in both job description and CV"""
        common_tech_skills = ['python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker', 
                             'kubernetes', 'machine learning', 'data science', 'angular', 'vue', 'tensorflow',
                             'pytorch', 'pandas', 'numpy', 'git', 'linux', 'mongodb', 'postgresql']
        
        jd_lower = jd_text.lower()
        cv_lower = cv_text.lower()
        
        common_skills = []
        for skill in common_tech_skills:
            if skill in jd_lower and skill in cv_lower:
                common_skills.append(skill.title())
        
        return common_skills
    
    def _extract_key_requirements(self, jd_text: str) -> List[str]:
        """Extract key requirements/responsibilities from job description"""
        jd_lower = jd_text.lower()
        
        requirements = []
        
        # Common requirement patterns
        requirement_patterns = [
            'develop', 'implement', 'design', 'build', 'create', 'maintain', 
            'optimize', 'integrate', 'test', 'deploy', 'analyze', 'research'
        ]
        
        for pattern in requirement_patterns:
            if pattern in jd_lower:
                requirements.append(f"implementing solutions for {pattern}ing requirements")
        
        return requirements[:5]  # Return top 5