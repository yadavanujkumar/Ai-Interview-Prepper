"""
Study Resources Service
Provides comprehensive study materials and learning paths for different domains
"""

from typing import Dict, List, Any
import json

class StudyResourcesService:
    """Service for managing and providing study resources"""
    
    def __init__(self):
        self.resources = self._initialize_resources()
    
    def _initialize_resources(self) -> Dict[str, Any]:
        """Initialize comprehensive study resources for different domains"""
        return {
            'software_engineering': {
                'learning_paths': [
                    {
                        'title': 'Full Stack Development Path',
                        'duration': '3-6 months',
                        'difficulty': 'Intermediate',
                        'topics': [
                            'Frontend Development (HTML, CSS, JavaScript)',
                            'Backend Development (Python/Node.js)',
                            'Database Design (SQL/NoSQL)',
                            'API Development (REST/GraphQL)',
                            'Cloud Services (AWS/Azure)',
                            'DevOps Basics (CI/CD, Docker)'
                        ]
                    },
                    {
                        'title': 'Data Structures & Algorithms Mastery',
                        'duration': '2-4 months',
                        'difficulty': 'Intermediate to Advanced',
                        'topics': [
                            'Arrays and Strings',
                            'Linked Lists and Trees',
                            'Graphs and Dynamic Programming',
                            'Sorting and Searching Algorithms',
                            'System Design Basics'
                        ]
                    }
                ],
                'books': [
                    {
                        'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                        'author': 'Robert C. Martin',
                        'difficulty': 'Intermediate',
                        'focus': 'Code Quality & Best Practices'
                    },
                    {
                        'title': 'Cracking the Coding Interview',
                        'author': 'Gayle Laakmann McDowell',
                        'difficulty': 'Intermediate to Advanced',
                        'focus': 'Technical Interview Preparation'
                    },
                    {
                        'title': 'System Design Interview',
                        'author': 'Alex Xu',
                        'difficulty': 'Advanced',
                        'focus': 'System Architecture & Scalability'
                    }
                ],
                'online_platforms': [
                    {
                        'name': 'LeetCode',
                        'url': 'https://leetcode.com',
                        'type': 'Coding Practice',
                        'focus': 'Algorithms & Data Structures',
                        'cost': 'Free/Premium'
                    },
                    {
                        'name': 'HackerRank',
                        'url': 'https://hackerrank.com',
                        'type': 'Coding Practice',
                        'focus': 'Programming Skills',
                        'cost': 'Free'
                    },
                    {
                        'name': 'Coursera',
                        'url': 'https://coursera.org',
                        'type': 'Online Courses',
                        'focus': 'Comprehensive Learning',
                        'cost': 'Free/Paid'
                    },
                    {
                        'name': 'Pluralsight',
                        'url': 'https://pluralsight.com',
                        'type': 'Video Courses',
                        'focus': 'Technology Skills',
                        'cost': 'Subscription'
                    }
                ],
                'practice_projects': [
                    {
                        'title': 'Personal Portfolio Website',
                        'difficulty': 'Beginner',
                        'technologies': ['HTML', 'CSS', 'JavaScript'],
                        'description': 'Build a responsive portfolio showcasing your projects'
                    },
                    {
                        'title': 'Task Management API',
                        'difficulty': 'Intermediate',
                        'technologies': ['Python/Node.js', 'Database', 'REST API'],
                        'description': 'Create a full-featured task management system'
                    },
                    {
                        'title': 'Real-time Chat Application',
                        'difficulty': 'Advanced',
                        'technologies': ['WebSockets', 'React/Vue', 'Database'],
                        'description': 'Build a scalable real-time messaging system'
                    }
                ]
            },
            'data_science': {
                'learning_paths': [
                    {
                        'title': 'Data Science Fundamentals',
                        'duration': '4-6 months',
                        'difficulty': 'Beginner to Intermediate',
                        'topics': [
                            'Statistics and Probability',
                            'Python for Data Science',
                            'Data Manipulation (Pandas, NumPy)',
                            'Data Visualization (Matplotlib, Seaborn)',
                            'Machine Learning Basics',
                            'SQL for Data Analysis'
                        ]
                    },
                    {
                        'title': 'Machine Learning Specialization',
                        'duration': '3-5 months',
                        'difficulty': 'Intermediate to Advanced',
                        'topics': [
                            'Supervised Learning Algorithms',
                            'Unsupervised Learning',
                            'Deep Learning Fundamentals',
                            'Model Evaluation and Selection',
                            'Feature Engineering',
                            'MLOps and Deployment'
                        ]
                    }
                ],
                'books': [
                    {
                        'title': 'Python for Data Analysis',
                        'author': 'Wes McKinney',
                        'difficulty': 'Beginner to Intermediate',
                        'focus': 'Data Manipulation & Analysis'
                    },
                    {
                        'title': 'Hands-On Machine Learning',
                        'author': 'Aurélien Géron',
                        'difficulty': 'Intermediate',
                        'focus': 'Practical ML Implementation'
                    },
                    {
                        'title': 'The Elements of Statistical Learning',
                        'author': 'Hastie, Tibshirani, Friedman',
                        'difficulty': 'Advanced',
                        'focus': 'Statistical Learning Theory'
                    }
                ],
                'online_platforms': [
                    {
                        'name': 'Kaggle',
                        'url': 'https://kaggle.com',
                        'type': 'Competitions & Datasets',
                        'focus': 'Practical Data Science',
                        'cost': 'Free'
                    },
                    {
                        'name': 'Coursera ML Course',
                        'url': 'https://coursera.org/learn/machine-learning',
                        'type': 'Online Course',
                        'focus': 'Machine Learning Theory',
                        'cost': 'Free/Certificate Fee'
                    },
                    {
                        'name': 'DataCamp',
                        'url': 'https://datacamp.com',
                        'type': 'Interactive Learning',
                        'focus': 'Data Science Skills',
                        'cost': 'Subscription'
                    }
                ],
                'practice_projects': [
                    {
                        'title': 'Exploratory Data Analysis',
                        'difficulty': 'Beginner',
                        'technologies': ['Python', 'Pandas', 'Matplotlib'],
                        'description': 'Analyze a dataset and create visualizations'
                    },
                    {
                        'title': 'Predictive Modeling Project',
                        'difficulty': 'Intermediate',
                        'technologies': ['Scikit-learn', 'Feature Engineering'],
                        'description': 'Build and evaluate a machine learning model'
                    },
                    {
                        'title': 'End-to-End ML Pipeline',
                        'difficulty': 'Advanced',
                        'technologies': ['MLOps', 'Docker', 'Cloud Deployment'],
                        'description': 'Create a complete ML system from data to deployment'
                    }
                ]
            },
            'product_management': {
                'learning_paths': [
                    {
                        'title': 'Product Management Fundamentals',
                        'duration': '2-3 months',
                        'difficulty': 'Beginner',
                        'topics': [
                            'Product Strategy & Vision',
                            'Market Research & Analysis',
                            'User Experience Design',
                            'Agile & Scrum Methodologies',
                            'Data-Driven Decision Making',
                            'Stakeholder Management'
                        ]
                    }
                ],
                'books': [
                    {
                        'title': 'Inspired: How to Create Tech Products Customers Love',
                        'author': 'Marty Cagan',
                        'difficulty': 'Intermediate',
                        'focus': 'Product Strategy & Development'
                    },
                    {
                        'title': 'The Lean Startup',
                        'author': 'Eric Ries',
                        'difficulty': 'Beginner',
                        'focus': 'Product Innovation & Validation'
                    }
                ],
                'online_platforms': [
                    {
                        'name': 'Product School',
                        'url': 'https://productschool.com',
                        'type': 'Specialized Training',
                        'focus': 'Product Management',
                        'cost': 'Paid'
                    },
                    {
                        'name': 'Coursera Product Management',
                        'url': 'https://coursera.org',
                        'type': 'Online Courses',
                        'focus': 'PM Skills & Strategy',
                        'cost': 'Free/Paid'
                    }
                ],
                'practice_projects': [
                    {
                        'title': 'Product Requirements Document',
                        'difficulty': 'Beginner',
                        'technologies': ['Documentation', 'User Research'],
                        'description': 'Create a comprehensive PRD for a new feature'
                    },
                    {
                        'title': 'Product Launch Plan',
                        'difficulty': 'Intermediate',
                        'technologies': ['Strategy', 'Analytics', 'Marketing'],
                        'description': 'Develop a complete go-to-market strategy'
                    }
                ]
            },
            'general': {
                'learning_paths': [
                    {
                        'title': 'Professional Development',
                        'duration': '1-2 months',
                        'difficulty': 'All Levels',
                        'topics': [
                            'Communication Skills',
                            'Leadership & Management',
                            'Problem Solving',
                            'Time Management',
                            'Emotional Intelligence',
                            'Networking & Relationship Building'
                        ]
                    }
                ],
                'books': [
                    {
                        'title': 'How to Win Friends and Influence People',
                        'author': 'Dale Carnegie',
                        'difficulty': 'Beginner',
                        'focus': 'Communication & Relationships'
                    },
                    {
                        'title': 'The 7 Habits of Highly Effective People',
                        'author': 'Stephen Covey',
                        'difficulty': 'Beginner',
                        'focus': 'Personal Effectiveness'
                    }
                ],
                'online_platforms': [
                    {
                        'name': 'LinkedIn Learning',
                        'url': 'https://linkedin.com/learning',
                        'type': 'Professional Development',
                        'focus': 'Soft Skills & Business',
                        'cost': 'Subscription'
                    },
                    {
                        'name': 'Udemy',
                        'url': 'https://udemy.com',
                        'type': 'Online Courses',
                        'focus': 'Diverse Skills',
                        'cost': 'Per Course'
                    }
                ],
                'practice_projects': [
                    {
                        'title': 'Personal Brand Development',
                        'difficulty': 'Beginner',
                        'technologies': ['Social Media', 'Content Creation'],
                        'description': 'Build and maintain your professional online presence'
                    }
                ]
            }
        }
    
    def get_resources_by_domain(self, domain: str) -> Dict[str, Any]:
        """Get study resources for a specific domain"""
        return self.resources.get(domain, self.resources['general'])
    
    def get_learning_path(self, domain: str, skill_level: str = 'beginner') -> Dict[str, Any]:
        """Get recommended learning path based on domain and skill level"""
        domain_resources = self.get_resources_by_domain(domain)
        learning_paths = domain_resources.get('learning_paths', [])
        
        # Filter by skill level or return the first appropriate path
        for path in learning_paths:
            if skill_level.lower() in path.get('difficulty', '').lower():
                return path
        
        return learning_paths[0] if learning_paths else {}
    
    def get_personalized_recommendations(self, domain: str, missing_skills: List[str], 
                                       experience_level: str = 'intermediate') -> Dict[str, Any]:
        """Generate personalized study recommendations"""
        domain_resources = self.get_resources_by_domain(domain)
        
        recommendations = {
            'priority_skills': missing_skills[:5],  # Top 5 missing skills
            'recommended_books': domain_resources.get('books', [])[:3],
            'online_courses': domain_resources.get('online_platforms', [])[:4],
            'practice_projects': domain_resources.get('practice_projects', []),
            'learning_path': self.get_learning_path(domain, experience_level),
            'study_schedule': self._generate_study_schedule(domain, missing_skills)
        }
        
        return recommendations
    
    def _generate_study_schedule(self, domain: str, missing_skills: List[str]) -> Dict[str, List[str]]:
        """Generate a weekly study schedule"""
        schedule = {
            'week_1_2': [
                'Focus on fundamental concepts and theory',
                'Read recommended books and articles',
                'Complete basic online tutorials'
            ],
            'week_3_4': [
                'Start hands-on practice with coding/projects',
                'Join online communities and forums',
                'Practice problem-solving exercises'
            ],
            'week_5_6': [
                'Work on practical projects',
                'Participate in online challenges',
                'Seek feedback from peers and mentors'
            ],
            'week_7_8': [
                'Build portfolio projects',
                'Practice mock interviews',
                'Refine and improve your work'
            ]
        }
        
        # Customize based on missing skills
        if missing_skills:
            schedule['daily_focus'] = [
                f"Spend 30 minutes daily on {skill}" for skill in missing_skills[:3]
            ]
        
        return schedule
    
    def get_interview_preparation_guide(self, domain: str) -> Dict[str, Any]:
        """Get comprehensive interview preparation guide"""
        return {
            'technical_preparation': [
                'Review core concepts and fundamentals',
                'Practice coding problems daily',
                'Understand system design principles',
                'Prepare real-world examples from your experience'
            ],
            'behavioral_preparation': [
                'Practice STAR method for behavioral questions',
                'Prepare specific examples for common scenarios',
                'Research the company culture and values',
                'Practice storytelling and clear communication'
            ],
            'domain_specific_tips': self._get_domain_interview_tips(domain),
            'common_mistakes': [
                'Not asking clarifying questions',
                'Jumping to solutions without planning',
                'Not explaining thought process clearly',
                'Not preparing questions for the interviewer'
            ],
            'day_before_checklist': [
                'Review your resume and be ready to discuss any point',
                'Research the company and role thoroughly',
                'Prepare thoughtful questions about the role',
                'Get a good night\'s sleep and eat well',
                'Plan your route and arrive early'
            ]
        }
    
    def _get_domain_interview_tips(self, domain: str) -> List[str]:
        """Get domain-specific interview tips"""
        tips = {
            'software_engineering': [
                'Practice whiteboard coding regularly',
                'Understand time and space complexity',
                'Be ready to discuss your code architecture choices',
                'Know multiple approaches to solve problems'
            ],
            'data_science': [
                'Be ready to explain ML algorithms in simple terms',
                'Practice interpreting data and drawing insights',
                'Understand statistical concepts and their applications',
                'Prepare to discuss your data science project lifecycle'
            ],
            'product_management': [
                'Practice product case studies and frameworks',
                'Be ready to discuss metrics and KPIs',
                'Understand user research and market analysis',
                'Prepare examples of cross-functional collaboration'
            ]
        }
        
        return tips.get(domain, [
            'Focus on demonstrating problem-solving approach',
            'Show enthusiasm and genuine interest in the role',
            'Demonstrate continuous learning mindset',
            'Provide specific examples from your experience'
        ])