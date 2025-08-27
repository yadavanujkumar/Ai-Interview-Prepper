"""
Salary Negotiation Guidance Service
"""
import json
import os
from typing import Dict, List, Optional, Any
import statistics

class SalaryNegotiationService:
    """Service for providing salary negotiation guidance and insights"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.salary_data_file = os.path.join(data_dir, 'salary_data.json')
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize salary data
        self._initialize_salary_data()
        
        # Load salary data
        self.salary_data = self._load_salary_data()
    
    def get_salary_guidance(self, role: str, location: str = '', experience_years: int = 0, 
                          company: str = '', industry: str = '') -> Dict[str, Any]:
        """Get comprehensive salary negotiation guidance"""
        
        # Get market data
        market_data = self.get_market_data(role, location, experience_years, industry)
        
        # Get negotiation strategies
        strategies = self.get_negotiation_strategies(role, experience_years, company)
        
        # Get preparation checklist
        preparation = self.get_negotiation_preparation()
        
        # Get common mistakes to avoid
        mistakes = self.get_common_mistakes()
        
        return {
            'market_data': market_data,
            'negotiation_strategies': strategies,
            'preparation_checklist': preparation,
            'common_mistakes': mistakes,
            'negotiation_timeline': self.get_negotiation_timeline(),
            'scripts_and_templates': self.get_negotiation_scripts(),
            'benefits_to_consider': self.get_benefits_breakdown(),
            'research_resources': self.get_research_resources()
        }
    
    def get_market_data(self, role: str, location: str = '', experience_years: int = 0, 
                       industry: str = '') -> Dict[str, Any]:
        """Get market salary data for the role"""
        role_key = self._normalize_key(role)
        location_key = self._normalize_key(location)
        industry_key = self._normalize_key(industry)
        
        # Get base role data
        role_data = self.salary_data.get('roles', {}).get(role_key, {})
        
        # Calculate experience multiplier
        experience_multiplier = self._get_experience_multiplier(experience_years)
        
        # Get location adjustment
        location_multiplier = self._get_location_multiplier(location_key)
        
        # Get industry adjustment
        industry_multiplier = self._get_industry_multiplier(industry_key)
        
        # Calculate adjusted salary ranges
        base_salary = role_data.get('base_salary', {})
        if base_salary:
            adjusted_salary = self._apply_multipliers(
                base_salary, 
                experience_multiplier, 
                location_multiplier, 
                industry_multiplier
            )
        else:
            adjusted_salary = self._get_generic_salary_range(experience_years)
        
        return {
            'role': role,
            'location': location,
            'experience_years': experience_years,
            'industry': industry,
            'salary_range': adjusted_salary,
            'market_percentiles': self._calculate_percentiles(adjusted_salary),
            'total_compensation': self._estimate_total_compensation(adjusted_salary),
            'data_sources': ['Industry reports', 'Glassdoor', 'PayScale', 'Levels.fyi'],
            'last_updated': '2024',
            'confidence_level': self._calculate_confidence_level(role_data)
        }
    
    def get_negotiation_strategies(self, role: str, experience_years: int, company: str = '') -> List[Dict[str, Any]]:
        """Get role and experience-specific negotiation strategies"""
        strategies = []
        
        # Experience-based strategies
        if experience_years < 2:
            strategies.extend([
                {
                    'strategy': 'Focus on Growth Potential',
                    'description': 'Emphasize your eagerness to learn and grow within the role',
                    'talking_points': [
                        'Long-term commitment to the company',
                        'Specific skills you want to develop',
                        'How you plan to add value quickly'
                    ]
                },
                {
                    'strategy': 'Highlight Relevant Projects',
                    'description': 'Showcase projects or achievements that demonstrate your potential',
                    'talking_points': [
                        'Academic projects with real-world applications',
                        'Internship achievements',
                        'Personal projects or certifications'
                    ]
                }
            ])
        elif experience_years < 5:
            strategies.extend([
                {
                    'strategy': 'Market Rate Research',
                    'description': 'Come prepared with solid market research',
                    'talking_points': [
                        'Specific salary data for your role and location',
                        'Industry trends and growth',
                        'Your unique combination of skills'
                    ]
                },
                {
                    'strategy': 'Value Demonstration',
                    'description': 'Quantify your contributions and achievements',
                    'talking_points': [
                        'Specific metrics from previous roles',
                        'Process improvements you\'ve implemented',
                        'Revenue impact or cost savings'
                    ]
                }
            ])
        else:
            strategies.extend([
                {
                    'strategy': 'Senior-Level Positioning',
                    'description': 'Negotiate as a strategic hire with proven track record',
                    'talking_points': [
                        'Leadership experience and team building',
                        'Strategic initiatives you\'ve led',
                        'Industry expertise and network'
                    ]
                },
                {
                    'strategy': 'Total Package Negotiation',
                    'description': 'Look beyond base salary to total compensation',
                    'talking_points': [
                        'Equity and stock options',
                        'Bonus structure and targets',
                        'Executive benefits and perks'
                    ]
                }
            ])
        
        # Role-specific strategies
        role_strategies = self._get_role_specific_strategies(role)
        strategies.extend(role_strategies)
        
        # Company-specific strategies
        if company:
            company_strategies = self._get_company_specific_strategies(company)
            strategies.extend(company_strategies)
        
        return strategies
    
    def get_negotiation_preparation(self) -> Dict[str, List[str]]:
        """Get negotiation preparation checklist"""
        return {
            'research_phase': [
                'Research market rates for your role and location',
                'Understand the company\'s financial health and compensation philosophy',
                'Know your own value proposition and unique strengths',
                'Research the hiring manager and team structure',
                'Understand industry trends and growth projections'
            ],
            'documentation': [
                'Gather salary data from multiple sources',
                'Document your achievements with specific metrics',
                'Prepare a list of your unique skills and certifications',
                'Collect reference letters or performance reviews',
                'Create a portfolio showcasing your best work'
            ],
            'strategy_development': [
                'Define your minimum acceptable offer',
                'Identify your ideal compensation package',
                'Determine non-negotiable items vs. nice-to-haves',
                'Plan your negotiation timeline',
                'Prepare alternative proposals and counteroffers'
            ],
            'practice_and_rehearsal': [
                'Practice your pitch with friends or mentors',
                'Rehearse responses to common objections',
                'Practice active listening and asking questions',
                'Role-play different negotiation scenarios',
                'Prepare answers for salary history questions'
            ]
        }
    
    def get_common_mistakes(self) -> List[Dict[str, str]]:
        """Get common salary negotiation mistakes to avoid"""
        return [
            {
                'mistake': 'Accepting the First Offer',
                'why_problematic': 'Most first offers have room for improvement',
                'how_to_avoid': 'Always ask for time to consider and research market rates'
            },
            {
                'mistake': 'Focusing Only on Base Salary',
                'why_problematic': 'Total compensation includes many valuable components',
                'how_to_avoid': 'Consider benefits, equity, bonuses, and growth opportunities'
            },
            {
                'mistake': 'Not Doing Market Research',
                'why_problematic': 'You can\'t negotiate effectively without data',
                'how_to_avoid': 'Research multiple sources and understand the full market range'
            },
            {
                'mistake': 'Revealing Your Current Salary Too Early',
                'why_problematic': 'It can anchor the negotiation to your current pay',
                'how_to_avoid': 'Focus on the value you bring and market rates instead'
            },
            {
                'mistake': 'Making Demands Instead of Requests',
                'why_problematic': 'Aggressive approach can damage relationships',
                'how_to_avoid': 'Frame negotiations as collaborative problem-solving'
            },
            {
                'mistake': 'Not Having Alternatives',
                'why_problematic': 'Weak position if you have no other options',
                'how_to_avoid': 'Continue interviewing and build multiple options'
            },
            {
                'mistake': 'Negotiating Too Early',
                'why_problematic': 'Salary discussions should happen after mutual interest',
                'how_to_avoid': 'Wait until you have an offer or strong interest is expressed'
            },
            {
                'mistake': 'Not Getting Everything in Writing',
                'why_problematic': 'Verbal agreements can be forgotten or misunderstood',
                'how_to_avoid': 'Request written confirmation of all agreed terms'
            }
        ]
    
    def get_negotiation_timeline(self) -> Dict[str, Any]:
        """Get typical negotiation timeline and best practices"""
        return {
            'phases': [
                {
                    'phase': 'Pre-Interview',
                    'duration': 'Ongoing',
                    'activities': [
                        'Research company and role',
                        'Understand market rates',
                        'Prepare your value proposition'
                    ]
                },
                {
                    'phase': 'During Interviews',
                    'duration': 'Interview process',
                    'activities': [
                        'Focus on demonstrating value',
                        'Avoid detailed salary discussions',
                        'Ask about compensation philosophy if appropriate'
                    ]
                },
                {
                    'phase': 'Initial Offer',
                    'duration': '1-3 days',
                    'activities': [
                        'Thank them for the offer',
                        'Ask for time to review (24-48 hours)',
                        'Request details on full compensation package'
                    ]
                },
                {
                    'phase': 'Negotiation',
                    'duration': '3-7 days',
                    'activities': [
                        'Present your counteroffer',
                        'Justify with market research',
                        'Be open to alternative solutions'
                    ]
                },
                {
                    'phase': 'Final Decision',
                    'duration': '1-2 days',
                    'activities': [
                        'Review final offer thoroughly',
                        'Get all terms in writing',
                        'Make your decision promptly'
                    ]
                }
            ],
            'timing_tips': [
                'End of quarter/fiscal year may offer more flexibility',
                'Avoid negotiating during company budget freezes',
                'Friday afternoon offers often have more room for improvement',
                'Consider industry hiring cycles and peak seasons'
            ]
        }
    
    def get_negotiation_scripts(self) -> Dict[str, List[str]]:
        """Get sample scripts and templates for negotiations"""
        return {
            'initial_response': [
                'Thank you for the offer. I\'m excited about the opportunity to join [Company]. Could I have a day or two to review the details?',
                'I appreciate the offer and I\'m very interested in the role. Before I accept, I\'d like to discuss the compensation package.',
                'Thank you for extending this offer. Based on my research and experience, I was hoping we could discuss the salary component.'
            ],
            'presenting_counteroffer': [
                'Based on my research of market rates for this role in [location], I was expecting a salary in the range of $X to $Y.',
                'Given my [specific experience/skills], I believe a salary of $X would be more appropriate for this role.',
                'I\'ve researched similar positions at comparable companies, and the market rate appears to be around $X.'
            ],
            'negotiating_benefits': [
                'While I understand the base salary may be fixed, are there other components we could adjust, such as the bonus structure or start date?',
                'Would it be possible to discuss additional vacation days or professional development opportunities?',
                'Could we explore options like a signing bonus or earlier review cycle?'
            ],
            'accepting_offer': [
                'I\'m happy to accept the offer at $X. Could you please send me the written offer letter with all the details we discussed?',
                'Thank you for working with me on this. I accept the position and look forward to starting on [date].',
                'I\'m excited to accept this offer and join the team. When can I expect the formal offer letter?'
            ],
            'declining_offer': [
                'After careful consideration, I don\'t think this opportunity is the right fit for me at this time. Thank you for your time and consideration.',
                'While I\'m impressed with the company and role, I\'ve decided to pursue a different opportunity. I appreciate the offer.',
                'Thank you for the offer. Unfortunately, I won\'t be able to accept, but I hope we can work together in the future.'
            ]
        }
    
    def get_benefits_breakdown(self) -> Dict[str, Any]:
        """Get comprehensive breakdown of benefits to consider"""
        return {
            'financial_benefits': {
                'base_salary': 'Your regular paycheck amount',
                'bonus': 'Performance-based additional compensation',
                'equity': 'Stock options, RSUs, or company ownership',
                'signing_bonus': 'One-time payment upon joining',
                'retention_bonus': 'Bonus for staying with company',
                'commission': 'Sales-based compensation'
            },
            'time_off_benefits': {
                'vacation_days': 'Paid time off for personal use',
                'sick_leave': 'Paid time off for illness',
                'personal_days': 'Flexible paid time off',
                'sabbatical': 'Extended leave options',
                'parental_leave': 'Time off for new parents',
                'holidays': 'Company-observed paid holidays'
            },
            'health_benefits': {
                'health_insurance': 'Medical coverage and company contribution',
                'dental_insurance': 'Dental care coverage',
                'vision_insurance': 'Eye care coverage',
                'mental_health': 'Counseling and therapy coverage',
                'wellness_programs': 'Gym memberships, health coaching',
                'health_savings_account': 'Tax-advantaged health savings'
            },
            'professional_development': {
                'training_budget': 'Annual allowance for courses and conferences',
                'certification_support': 'Company-paid professional certifications',
                'conference_attendance': 'Paid attendance at industry events',
                'tuition_assistance': 'Support for continued education',
                'mentorship_programs': 'Access to senior mentors',
                'career_coaching': 'Professional development support'
            },
            'work_life_balance': {
                'flexible_hours': 'Flexible start and end times',
                'remote_work': 'Work from home options',
                'compressed_workweek': '4-day work weeks or flexible schedules',
                'commuter_benefits': 'Transportation assistance',
                'childcare_support': 'On-site or subsidized childcare',
                'eldercare_support': 'Support for caring for aging parents'
            },
            'additional_perks': {
                'equipment': 'Laptop, phone, home office setup',
                'meals': 'Free or subsidized food at work',
                'parking': 'Free parking or transportation subsidies',
                'employee_discounts': 'Discounts on company products',
                'social_events': 'Company parties and team building',
                'volunteer_time': 'Paid time off for volunteering'
            }
        }
    
    def get_research_resources(self) -> Dict[str, List[str]]:
        """Get resources for salary research"""
        return {
            'salary_data_sites': [
                'Glassdoor.com - Employee-reported salaries',
                'PayScale.com - Comprehensive salary data',
                'Salary.com - Professional salary reports',
                'Levels.fyi - Tech industry compensation',
                'Indeed.com - Salary insights and trends',
                'LinkedIn Salary Insights - Professional network data'
            ],
            'industry_reports': [
                'Robert Half Salary Guide',
                'Hays Salary Guide',
                'Stack Overflow Developer Survey',
                'Dice Tech Salary Report',
                'Bureau of Labor Statistics',
                'McKinsey Global Institute reports'
            ],
            'negotiation_resources': [
                'Harvard Business Review negotiation articles',
                'Never Eat Alone by Keith Ferrazzi',
                'Getting to Yes by Roger Fisher',
                'Lean In by Sheryl Sandberg',
                'Salary Negotiation workshop videos',
                'Professional career coaching services'
            ],
            'company_research': [
                'Company annual reports and SEC filings',
                'Crunchbase for funding and valuation data',
                'Company career pages and benefits information',
                'Employee reviews on Glassdoor',
                'Recent news and company announcements',
                'LinkedIn for employee backgrounds and connections'
            ]
        }
    
    def calculate_offer_score(self, offer_details: Dict[str, Any], preferences: Dict[str, int]) -> Dict[str, Any]:
        """Calculate and score a job offer based on user preferences"""
        # Default weights if not provided
        default_weights = {
            'base_salary': 30,
            'bonus': 15,
            'equity': 20,
            'benefits': 15,
            'work_life_balance': 10,
            'growth_opportunities': 10
        }
        
        weights = {**default_weights, **preferences}
        
        # Normalize weights to sum to 100
        total_weight = sum(weights.values())
        normalized_weights = {k: (v / total_weight) * 100 for k, v in weights.items()}
        
        # Score each component (0-10 scale)
        scores = {}
        scores['base_salary'] = self._score_salary(offer_details.get('base_salary', 0))
        scores['bonus'] = self._score_bonus(offer_details.get('bonus', 0))
        scores['equity'] = self._score_equity(offer_details.get('equity', 0))
        scores['benefits'] = self._score_benefits(offer_details.get('benefits', []))
        scores['work_life_balance'] = self._score_work_life_balance(offer_details.get('wlb_features', []))
        scores['growth_opportunities'] = self._score_growth_opportunities(offer_details.get('growth_features', []))
        
        # Calculate weighted score
        weighted_score = sum(scores[k] * (normalized_weights[k] / 100) for k in scores)
        
        return {
            'overall_score': round(weighted_score, 1),
            'component_scores': scores,
            'weights_used': normalized_weights,
            'recommendations': self._generate_offer_recommendations(scores, offer_details)
        }
    
    def _normalize_key(self, text: str) -> str:
        """Normalize text for dictionary lookups"""
        return text.lower().replace(' ', '_').replace('-', '_') if text else ''
    
    def _load_salary_data(self) -> Dict[str, Any]:
        """Load salary data from file"""
        try:
            with open(self.salary_data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _initialize_salary_data(self):
        """Initialize default salary data"""
        if os.path.exists(self.salary_data_file):
            return
        
        default_data = {
            'roles': {
                'software_engineer': {
                    'base_salary': {'min': 70000, 'median': 95000, 'max': 180000},
                    'common_titles': ['Software Engineer', 'Software Developer', 'Full Stack Developer']
                },
                'data_scientist': {
                    'base_salary': {'min': 80000, 'median': 115000, 'max': 200000},
                    'common_titles': ['Data Scientist', 'Machine Learning Engineer', 'Data Analyst']
                },
                'product_manager': {
                    'base_salary': {'min': 85000, 'median': 125000, 'max': 220000},
                    'common_titles': ['Product Manager', 'Senior Product Manager', 'Product Owner']
                }
            },
            'location_multipliers': {
                'san_francisco': 1.4,
                'new_york': 1.3,
                'seattle': 1.2,
                'boston': 1.15,
                'chicago': 1.0,
                'austin': 1.05,
                'denver': 0.95,
                'atlanta': 0.9,
                'remote': 0.9
            },
            'experience_multipliers': {
                '0-1': 0.8,
                '2-3': 1.0,
                '4-6': 1.3,
                '7-10': 1.6,
                '11+': 2.0
            },
            'industry_multipliers': {
                'technology': 1.2,
                'finance': 1.3,
                'healthcare': 1.0,
                'consulting': 1.1,
                'government': 0.8,
                'non_profit': 0.7,
                'startup': 0.9
            }
        }
        
        with open(self.salary_data_file, 'w') as f:
            json.dump(default_data, f, indent=2)
    
    def _get_experience_multiplier(self, years: int) -> float:
        """Get salary multiplier based on years of experience"""
        if years <= 1:
            return 0.8
        elif years <= 3:
            return 1.0
        elif years <= 6:
            return 1.3
        elif years <= 10:
            return 1.6
        else:
            return 2.0
    
    def _get_location_multiplier(self, location_key: str) -> float:
        """Get salary multiplier based on location"""
        multipliers = self.salary_data.get('location_multipliers', {})
        return multipliers.get(location_key, 1.0)
    
    def _get_industry_multiplier(self, industry_key: str) -> float:
        """Get salary multiplier based on industry"""
        multipliers = self.salary_data.get('industry_multipliers', {})
        return multipliers.get(industry_key, 1.0)
    
    def _apply_multipliers(self, base_salary: Dict[str, int], exp_mult: float, 
                          loc_mult: float, ind_mult: float) -> Dict[str, int]:
        """Apply multipliers to base salary range"""
        combined_multiplier = exp_mult * loc_mult * ind_mult
        
        return {
            'min': int(base_salary['min'] * combined_multiplier),
            'median': int(base_salary['median'] * combined_multiplier),
            'max': int(base_salary['max'] * combined_multiplier)
        }
    
    def _get_generic_salary_range(self, experience_years: int) -> Dict[str, int]:
        """Get generic salary range when role data is not available"""
        base_ranges = {
            0: {'min': 45000, 'median': 55000, 'max': 70000},
            2: {'min': 55000, 'median': 70000, 'max': 90000},
            5: {'min': 75000, 'median': 95000, 'max': 130000},
            10: {'min': 100000, 'median': 130000, 'max': 180000}
        }
        
        # Find closest experience level
        closest_exp = min(base_ranges.keys(), key=lambda x: abs(x - experience_years))
        return base_ranges[closest_exp]
    
    def _calculate_percentiles(self, salary_range: Dict[str, int]) -> Dict[str, int]:
        """Calculate salary percentiles"""
        min_sal = salary_range['min']
        max_sal = salary_range['max']
        range_size = max_sal - min_sal
        
        return {
            '25th_percentile': int(min_sal + range_size * 0.25),
            '50th_percentile': salary_range['median'],
            '75th_percentile': int(min_sal + range_size * 0.75),
            '90th_percentile': int(min_sal + range_size * 0.9)
        }
    
    def _estimate_total_compensation(self, salary_range: Dict[str, int]) -> Dict[str, int]:
        """Estimate total compensation including benefits"""
        # Typical benefits add 20-40% to base salary
        benefit_multiplier = 1.3
        
        return {
            'min_total': int(salary_range['min'] * benefit_multiplier),
            'median_total': int(salary_range['median'] * benefit_multiplier),
            'max_total': int(salary_range['max'] * benefit_multiplier)
        }
    
    def _calculate_confidence_level(self, role_data: Dict[str, Any]) -> str:
        """Calculate confidence level of salary data"""
        if not role_data:
            return 'Low - Generic estimates used'
        elif 'base_salary' in role_data:
            return 'High - Role-specific data available'
        else:
            return 'Medium - Partial data available'
    
    def _get_role_specific_strategies(self, role: str) -> List[Dict[str, Any]]:
        """Get strategies specific to the role"""
        role_strategies = {
            'software_engineer': [
                {
                    'strategy': 'Technical Skills Premium',
                    'description': 'Highlight specialized technical skills',
                    'talking_points': ['Rare programming languages or frameworks', 'System design experience', 'Open source contributions']
                }
            ],
            'data_scientist': [
                {
                    'strategy': 'Business Impact Focus',
                    'description': 'Quantify the business impact of your models',
                    'talking_points': ['Revenue generated by your models', 'Cost savings from optimization', 'Process improvements']
                }
            ]
        }
        
        role_key = self._normalize_key(role)
        return role_strategies.get(role_key, [])
    
    def _get_company_specific_strategies(self, company: str) -> List[Dict[str, Any]]:
        """Get strategies specific to the company"""
        # This would be expanded with company-specific insights
        return []
    
    def _score_salary(self, salary: int) -> int:
        """Score base salary on 0-10 scale"""
        # This is simplified - would use market data in practice
        if salary >= 150000:
            return 10
        elif salary >= 100000:
            return 8
        elif salary >= 80000:
            return 6
        elif salary >= 60000:
            return 4
        else:
            return 2
    
    def _score_bonus(self, bonus: int) -> int:
        """Score bonus on 0-10 scale"""
        if bonus >= 20000:
            return 10
        elif bonus >= 10000:
            return 7
        elif bonus >= 5000:
            return 5
        elif bonus > 0:
            return 3
        else:
            return 0
    
    def _score_equity(self, equity: int) -> int:
        """Score equity on 0-10 scale"""
        if equity >= 50000:
            return 10
        elif equity >= 25000:
            return 7
        elif equity >= 10000:
            return 5
        elif equity > 0:
            return 3
        else:
            return 0
    
    def _score_benefits(self, benefits: List[str]) -> int:
        """Score benefits package on 0-10 scale"""
        benefit_scores = {
            'health_insurance': 2,
            'dental_insurance': 1,
            'vision_insurance': 1,
            '401k_match': 2,
            'unlimited_pto': 2,
            'remote_work': 2
        }
        
        total_score = sum(benefit_scores.get(benefit, 0) for benefit in benefits)
        return min(10, total_score)
    
    def _score_work_life_balance(self, wlb_features: List[str]) -> int:
        """Score work-life balance on 0-10 scale"""
        wlb_scores = {
            'flexible_hours': 3,
            'remote_work': 3,
            'unlimited_pto': 2,
            'wellness_programs': 1,
            'parental_leave': 1
        }
        
        total_score = sum(wlb_scores.get(feature, 0) for feature in wlb_features)
        return min(10, total_score)
    
    def _score_growth_opportunities(self, growth_features: List[str]) -> int:
        """Score growth opportunities on 0-10 scale"""
        growth_scores = {
            'mentorship': 2,
            'training_budget': 2,
            'clear_progression': 3,
            'leadership_opportunities': 2,
            'conference_attendance': 1
        }
        
        total_score = sum(growth_scores.get(feature, 0) for feature in growth_features)
        return min(10, total_score)
    
    def _generate_offer_recommendations(self, scores: Dict[str, int], offer_details: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on offer scores"""
        recommendations = []
        
        if scores['base_salary'] < 6:
            recommendations.append('Consider negotiating base salary - current offer appears below market rate')
        
        if scores['bonus'] < 5:
            recommendations.append('Explore bonus opportunities or performance incentives')
        
        if scores['equity'] < 5:
            recommendations.append('Discuss equity compensation, especially if this is a growing company')
        
        if scores['work_life_balance'] < 6:
            recommendations.append('Negotiate for better work-life balance features like flexible hours or remote work')
        
        return recommendations