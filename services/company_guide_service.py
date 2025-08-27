"""
Company-Specific Preparation Guides Service
"""
import json
import os
from typing import Dict, List, Optional, Any

class CompanyGuideService:
    """Service for providing company-specific interview preparation guides"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.companies_file = os.path.join(data_dir, 'companies.json')
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize company data
        self._initialize_company_data()
        
        # Load company data
        self.companies = self._load_company_data()
    
    def get_company_guide(self, company_name: str) -> Dict[str, Any]:
        """Get comprehensive interview guide for a specific company"""
        company_key = self._normalize_company_name(company_name)
        company_data = self.companies.get(company_key, {})
        
        if not company_data:
            return self._generate_generic_guide(company_name)
        
        return {
            'company_name': company_data.get('name', company_name),
            'overview': company_data.get('overview', {}),
            'interview_process': company_data.get('interview_process', {}),
            'common_questions': company_data.get('common_questions', []),
            'technical_focus': company_data.get('technical_focus', []),
            'company_culture': company_data.get('culture', {}),
            'preparation_tips': company_data.get('preparation_tips', []),
            'salary_info': company_data.get('salary_info', {}),
            'resources': company_data.get('resources', []),
            'insider_tips': company_data.get('insider_tips', [])
        }
    
    def search_companies(self, query: str) -> List[Dict[str, Any]]:
        """Search for companies by name or industry"""
        query_lower = query.lower()
        results = []
        
        for company_key, company_data in self.companies.items():
            company_name = company_data.get('name', '').lower()
            industry = company_data.get('overview', {}).get('industry', '').lower()
            
            if (query_lower in company_name or 
                query_lower in industry or
                any(query_lower in tag.lower() for tag in company_data.get('tags', []))):
                
                results.append({
                    'name': company_data.get('name'),
                    'industry': company_data.get('overview', {}).get('industry'),
                    'size': company_data.get('overview', {}).get('size'),
                    'locations': company_data.get('overview', {}).get('locations', []),
                    'key': company_key
                })
        
        return results
    
    def get_industry_companies(self, industry: str) -> List[Dict[str, Any]]:
        """Get companies in a specific industry"""
        industry_lower = industry.lower()
        results = []
        
        for company_key, company_data in self.companies.items():
            company_industry = company_data.get('overview', {}).get('industry', '').lower()
            
            if industry_lower in company_industry:
                results.append({
                    'name': company_data.get('name'),
                    'industry': company_data.get('overview', {}).get('industry'),
                    'size': company_data.get('overview', {}).get('size'),
                    'key': company_key
                })
        
        return results
    
    def get_supported_companies(self) -> List[str]:
        """Get list of all supported companies"""
        return [company_data.get('name') for company_data in self.companies.values()]
    
    def get_company_questions(self, company_name: str, question_type: str = 'all') -> List[str]:
        """Get specific types of questions for a company"""
        company_key = self._normalize_company_name(company_name)
        company_data = self.companies.get(company_key, {})
        
        all_questions = company_data.get('common_questions', [])
        
        if question_type == 'all':
            return all_questions
        elif question_type == 'technical':
            return [q for q in all_questions if self._is_technical_question(q)]
        elif question_type == 'behavioral':
            return [q for q in all_questions if self._is_behavioral_question(q)]
        else:
            return all_questions
    
    def get_interview_timeline(self, company_name: str) -> Dict[str, Any]:
        """Get typical interview timeline for a company"""
        company_key = self._normalize_company_name(company_name)
        company_data = self.companies.get(company_key, {})
        
        return company_data.get('interview_process', {}).get('timeline', {})
    
    def get_salary_insights(self, company_name: str, role: str = '') -> Dict[str, Any]:
        """Get salary insights for a company and role"""
        company_key = self._normalize_company_name(company_name)
        company_data = self.companies.get(company_key, {})
        
        salary_info = company_data.get('salary_info', {})
        
        if role:
            role_key = self._normalize_company_name(role)
            role_specific = salary_info.get('roles', {}).get(role_key, {})
            if role_specific:
                return role_specific
        
        return salary_info.get('general', {})
    
    def _normalize_company_name(self, name: str) -> str:
        """Normalize company name for lookup"""
        return name.lower().replace(' ', '_').replace('.', '').replace(',', '')
    
    def _load_company_data(self) -> Dict[str, Any]:
        """Load company data from file"""
        try:
            with open(self.companies_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_company_data(self, data: Dict[str, Any]):
        """Save company data to file"""
        with open(self.companies_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _initialize_company_data(self):
        """Initialize default company data"""
        if os.path.exists(self.companies_file):
            return
        
        default_companies = {
            'google': {
                'name': 'Google',
                'overview': {
                    'industry': 'Technology',
                    'size': 'Large (100,000+ employees)',
                    'locations': ['Mountain View, CA', 'New York, NY', 'Seattle, WA', 'Global'],
                    'founded': 1998,
                    'description': 'Multinational technology company specializing in internet services and products'
                },
                'interview_process': {
                    'stages': [
                        'Phone/Video Screening',
                        'Technical Phone Interview',
                        'On-site Interviews (4-5 rounds)',
                        'Team Matching'
                    ],
                    'timeline': {
                        'total_duration': '4-6 weeks',
                        'phone_screen': '30-45 minutes',
                        'technical_phone': '45-60 minutes',
                        'onsite': '4-5 hours'
                    },
                    'focus_areas': ['Coding', 'System Design', 'Behavioral', 'Googleyness']
                },
                'common_questions': [
                    'Why do you want to work at Google?',
                    'Tell me about a time you had to deal with ambiguity.',
                    'Design a system like Google Search.',
                    'Implement a function to reverse a linked list.',
                    'How would you improve Google Maps?',
                    'Describe a time when you had to work with someone difficult.',
                    'What\'s your favorite Google product and how would you improve it?'
                ],
                'technical_focus': [
                    'Data Structures and Algorithms',
                    'System Design',
                    'Coding Proficiency',
                    'Problem Solving',
                    'Scalability'
                ],
                'culture': {
                    'values': ['Focus on the user', 'Think big', 'Innovation', 'Collaboration'],
                    'work_environment': 'Fast-paced, collaborative, innovation-focused',
                    'perks': ['Free meals', 'On-site gym', 'Flexible work arrangements', '20% time for personal projects']
                },
                'preparation_tips': [
                    'Practice coding problems on LeetCode (focus on medium/hard)',
                    'Study system design fundamentals',
                    'Learn about Google\'s products and services',
                    'Practice behavioral questions using STAR method',
                    'Review Google\'s engineering blog and research papers',
                    'Understand distributed systems concepts'
                ],
                'salary_info': {
                    'general': {
                        'compensation_philosophy': 'Competitive base + equity + bonuses',
                        'negotiation_tips': ['Research market rates', 'Highlight unique value', 'Be prepared to discuss total compensation']
                    },
                    'roles': {
                        'software_engineer': {
                            'base_range': '$130k - $200k+',
                            'total_comp': '$200k - $400k+',
                            'equity': 'Significant RSU component'
                        }
                    }
                },
                'resources': [
                    'https://careers.google.com',
                    'Google Engineering Blog',
                    'Cracking the Coding Interview book',
                    'System Design Interview book'
                ],
                'insider_tips': [
                    'Google values candidates who can think at scale',
                    'Show genuine interest in Google\'s mission and products',
                    'Be prepared to code on a whiteboard or Google Docs',
                    'Ask clarifying questions before diving into solutions',
                    'Demonstrate leadership and collaboration skills'
                ],
                'tags': ['tech', 'faang', 'software', 'engineering', 'ai', 'search']
            },
            'amazon': {
                'name': 'Amazon',
                'overview': {
                    'industry': 'E-commerce / Cloud Computing',
                    'size': 'Large (1,000,000+ employees)',
                    'locations': ['Seattle, WA', 'Global'],
                    'founded': 1994,
                    'description': 'Multinational technology company focusing on e-commerce, cloud computing, and AI'
                },
                'interview_process': {
                    'stages': [
                        'Online Assessment',
                        'Phone Screen',
                        'On-site/Virtual Loop (5-6 rounds)'
                    ],
                    'timeline': {
                        'total_duration': '3-5 weeks',
                        'online_assessment': '90 minutes',
                        'phone_screen': '45-60 minutes',
                        'onsite': '5-6 hours'
                    },
                    'focus_areas': ['Leadership Principles', 'Technical Skills', 'Problem Solving']
                },
                'common_questions': [
                    'Tell me about a time you had to deal with a difficult customer.',
                    'Describe a situation where you had to work backwards from a goal.',
                    'How do you handle working under pressure?',
                    'Design a recommendation system.',
                    'Implement a LRU cache.',
                    'Tell me about a time you failed.',
                    'Why Amazon?'
                ],
                'technical_focus': [
                    'Data Structures and Algorithms',
                    'System Design',
                    'Object-Oriented Design',
                    'Distributed Systems',
                    'AWS Knowledge (for some roles)'
                ],
                'culture': {
                    'values': ['Customer Obsession', 'Ownership', 'Invent and Simplify', 'Learn and Be Curious'],
                    'work_environment': 'High-performance, customer-focused, data-driven',
                    'leadership_principles': 16
                },
                'preparation_tips': [
                    'Study Amazon\'s 16 Leadership Principles thoroughly',
                    'Prepare STAR method stories for each principle',
                    'Practice system design questions',
                    'Understand AWS services (if applicable)',
                    'Focus on customer-centric thinking',
                    'Practice coding under time pressure'
                ],
                'salary_info': {
                    'general': {
                        'compensation_philosophy': 'Competitive total compensation with significant equity',
                        'negotiation_tips': ['Understand the total package', 'Consider growth potential', 'Negotiate sign-on bonus']
                    }
                },
                'resources': [
                    'https://amazon.jobs',
                    'Amazon Leadership Principles',
                    'AWS Documentation',
                    'The Everything Store book'
                ],
                'insider_tips': [
                    'Every answer should demonstrate leadership principles',
                    'Be specific with metrics and results in your stories',
                    'Show customer obsession in your examples',
                    'Demonstrate bias for action',
                    'Prepare for bar raiser interview'
                ],
                'tags': ['tech', 'faang', 'ecommerce', 'aws', 'cloud', 'leadership']
            },
            'microsoft': {
                'name': 'Microsoft',
                'overview': {
                    'industry': 'Technology / Software',
                    'size': 'Large (200,000+ employees)',
                    'locations': ['Redmond, WA', 'Global'],
                    'founded': 1975,
                    'description': 'Multinational technology corporation developing software, services, and solutions'
                },
                'interview_process': {
                    'stages': [
                        'Phone/Video Screen',
                        'Technical Interview',
                        'Final Round (As Appropriate)'
                    ],
                    'timeline': {
                        'total_duration': '2-4 weeks',
                        'phone_screen': '30-45 minutes',
                        'technical': '45-60 minutes',
                        'final_round': '3-4 hours'
                    },
                    'focus_areas': ['Technical Skills', 'Collaboration', 'Growth Mindset']
                },
                'common_questions': [
                    'Why Microsoft?',
                    'Tell me about a time you had to learn something quickly.',
                    'How would you test this feature?',
                    'Design a chat application.',
                    'Reverse a binary tree.',
                    'Describe a time you disagreed with a team member.',
                    'What motivates you?'
                ],
                'technical_focus': [
                    'Data Structures and Algorithms',
                    'System Design',
                    'Software Engineering Practices',
                    '.NET/Azure knowledge (for some roles)',
                    'Problem Solving'
                ],
                'culture': {
                    'values': ['Respect', 'Integrity', 'Accountability', 'Inclusive'],
                    'work_environment': 'Collaborative, growth-focused, inclusive',
                    'mission': 'Empower every person and organization to achieve more'
                },
                'preparation_tips': [
                    'Understand Microsoft\'s mission and values',
                    'Prepare examples showing growth mindset',
                    'Study common algorithms and data structures',
                    'Learn about Microsoft\'s products and services',
                    'Practice coding in your preferred language',
                    'Demonstrate collaboration skills'
                ],
                'salary_info': {
                    'general': {
                        'compensation_philosophy': 'Competitive compensation with strong benefits',
                        'negotiation_tips': ['Consider total package including benefits', 'Highlight relevant experience']
                    }
                },
                'resources': [
                    'https://careers.microsoft.com',
                    'Microsoft Engineering Blog',
                    'Azure Documentation',
                    'Hit Refresh book by Satya Nadella'
                ],
                'insider_tips': [
                    'Show genuine passion for technology',
                    'Demonstrate inclusive leadership',
                    'Be open to feedback and learning',
                    'Ask thoughtful questions about the role',
                    'Show how you can contribute to Microsoft\'s mission'
                ],
                'tags': ['tech', 'software', 'azure', 'cloud', 'enterprise', 'inclusive']
            }
        }
        
        self._save_company_data(default_companies)
    
    def _generate_generic_guide(self, company_name: str) -> Dict[str, Any]:
        """Generate a generic guide for companies not in our database"""
        return {
            'company_name': company_name,
            'overview': {
                'note': 'This is a generic guide. Company-specific data not available.'
            },
            'interview_process': {
                'common_stages': [
                    'Initial Screening',
                    'Technical/Behavioral Interview',
                    'Final Interview with Manager/Team'
                ],
                'preparation_areas': ['Technical Skills', 'Behavioral Questions', 'Company Research']
            },
            'common_questions': [
                'Tell me about yourself.',
                'Why do you want to work here?',
                'What are your strengths and weaknesses?',
                'Describe a challenging project you worked on.',
                'Where do you see yourself in 5 years?',
                'Do you have any questions for us?'
            ],
            'preparation_tips': [
                'Research the company thoroughly',
                'Practice common interview questions',
                'Prepare specific examples using STAR method',
                'Review the job description carefully',
                'Prepare thoughtful questions to ask',
                'Practice technical skills relevant to the role'
            ],
            'resources': [
                'Company website and career pages',
                'LinkedIn company page',
                'Glassdoor reviews',
                'Industry news and reports'
            ],
            'note': 'For more specific guidance, consider adding this company to our database or researching company-specific interview experiences online.'
        }
    
    def _is_technical_question(self, question: str) -> bool:
        """Determine if a question is technical"""
        technical_keywords = [
            'implement', 'design', 'algorithm', 'data structure', 'code', 'programming',
            'system', 'database', 'api', 'architecture', 'performance', 'scale'
        ]
        return any(keyword in question.lower() for keyword in technical_keywords)
    
    def _is_behavioral_question(self, question: str) -> bool:
        """Determine if a question is behavioral"""
        behavioral_keywords = [
            'tell me about a time', 'describe a situation', 'how do you handle',
            'what would you do', 'give me an example', 'experience with'
        ]
        return any(keyword in question.lower() for keyword in behavioral_keywords)