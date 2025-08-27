"""
Progress Tracking and Analytics Service
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import statistics

class AnalyticsService:
    """Service for tracking user progress and providing analytics"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.user_data_file = os.path.join(data_dir, 'user_data.json')
        self.session_data_file = os.path.join(data_dir, 'session_data.json')
        self.analytics_data_file = os.path.join(data_dir, 'analytics.json')
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self._initialize_data_files()
    
    def track_user_session(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """Track a user session for analytics"""
        try:
            # Load existing data
            sessions = self._load_json_file(self.session_data_file)
            
            # Add session data
            session_entry = {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'session_id': session_data.get('session_id'),
                'activity_type': session_data.get('activity_type', 'unknown'),
                'duration_minutes': session_data.get('duration_minutes', 0),
                'questions_answered': session_data.get('questions_answered', 0),
                'scores': session_data.get('scores', {}),
                'domain': session_data.get('domain', 'general'),
                'difficulty': session_data.get('difficulty', 'medium'),
                'completion_status': session_data.get('completion_status', 'partial')
            }
            
            sessions.append(session_entry)
            
            # Save updated data
            self._save_json_file(self.session_data_file, sessions)
            
            # Update user progress
            self._update_user_progress(user_id, session_entry)
            
            return True
            
        except Exception as e:
            print(f"Error tracking session: {str(e)}")
            return False
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive progress data for a user"""
        try:
            # Load user data
            users = self._load_json_file(self.user_data_file)
            user_data = users.get(user_id, {})
            
            # Load sessions for this user
            sessions = self._load_json_file(self.session_data_file)
            user_sessions = [s for s in sessions if s.get('user_id') == user_id]
            
            # Calculate progress metrics
            progress_data = {
                'user_id': user_id,
                'profile': user_data.get('profile', {}),
                'statistics': self._calculate_user_statistics(user_sessions),
                'recent_activity': self._get_recent_activity(user_sessions),
                'skill_progress': self._calculate_skill_progress(user_sessions),
                'recommendations': self._generate_progress_recommendations(user_sessions),
                'achievements': self._check_achievements(user_sessions),
                'streaks': self._calculate_streaks(user_sessions)
            }
            
            return progress_data
            
        except Exception as e:
            return {'error': f'Failed to get progress: {str(e)}'}
    
    def get_analytics_dashboard(self, user_id: str, time_range: str = '30d') -> Dict[str, Any]:
        """Get analytics dashboard data"""
        try:
            # Load sessions for this user
            sessions = self._load_json_file(self.session_data_file)
            user_sessions = [s for s in sessions if s.get('user_id') == user_id]
            
            # Filter by time range
            filtered_sessions = self._filter_sessions_by_time(user_sessions, time_range)
            
            dashboard_data = {
                'time_range': time_range,
                'session_count': len(filtered_sessions),
                'total_time_minutes': sum(s.get('duration_minutes', 0) for s in filtered_sessions),
                'total_questions': sum(s.get('questions_answered', 0) for s in filtered_sessions),
                'average_session_duration': self._calculate_average_duration(filtered_sessions),
                'domain_distribution': self._calculate_domain_distribution(filtered_sessions),
                'difficulty_progression': self._calculate_difficulty_progression(filtered_sessions),
                'performance_trends': self._calculate_performance_trends(filtered_sessions),
                'weekly_activity': self._calculate_weekly_activity(filtered_sessions),
                'completion_rates': self._calculate_completion_rates(filtered_sessions)
            }
            
            return dashboard_data
            
        except Exception as e:
            return {'error': f'Failed to get dashboard: {str(e)}'}
    
    def track_interview_performance(self, user_id: str, interview_data: Dict[str, Any]) -> bool:
        """Track interview performance specifically"""
        try:
            session_data = {
                'session_id': interview_data.get('session_id'),
                'activity_type': 'interview_practice',
                'duration_minutes': interview_data.get('duration_minutes', 0),
                'questions_answered': interview_data.get('questions_answered', 0),
                'domain': interview_data.get('domain', 'general'),
                'difficulty': interview_data.get('difficulty', 'medium'),
                'completion_status': interview_data.get('completion_status', 'completed'),
                'scores': {
                    'overall_rating': interview_data.get('overall_rating', 0),
                    'communication_score': interview_data.get('communication_score', 0),
                    'technical_score': interview_data.get('technical_score', 0),
                    'confidence_level': interview_data.get('confidence_level', 0)
                }
            }
            
            return self.track_user_session(user_id, session_data)
            
        except Exception as e:
            print(f"Error tracking interview performance: {str(e)}")
            return False
    
    def get_performance_insights(self, user_id: str) -> Dict[str, Any]:
        """Get AI-generated insights about user performance"""
        try:
            # Get user progress data
            progress = self.get_user_progress(user_id)
            sessions = self._load_json_file(self.session_data_file)
            user_sessions = [s for s in sessions if s.get('user_id') == user_id]
            
            # Generate insights
            insights = {
                'strengths': self._identify_strengths(user_sessions),
                'improvement_areas': self._identify_improvement_areas(user_sessions),
                'learning_patterns': self._analyze_learning_patterns(user_sessions),
                'goal_suggestions': self._suggest_goals(user_sessions),
                'next_steps': self._recommend_next_steps(user_sessions)
            }
            
            return insights
            
        except Exception as e:
            return {'error': f'Failed to generate insights: {str(e)}'}
    
    def _initialize_data_files(self):
        """Initialize data files if they don't exist"""
        default_files = {
            self.user_data_file: {},
            self.session_data_file: [],
            self.analytics_data_file: {'created_at': datetime.now().isoformat()}
        }
        
        for file_path, default_data in default_files.items():
            if not os.path.exists(file_path):
                self._save_json_file(file_path, default_data)
    
    def _load_json_file(self, file_path: str) -> Any:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if 'user_data' in file_path else []
    
    def _save_json_file(self, file_path: str, data: Any):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _update_user_progress(self, user_id: str, session_entry: Dict[str, Any]):
        """Update user progress based on session"""
        users = self._load_json_file(self.user_data_file)
        
        if user_id not in users:
            users[user_id] = {
                'created_at': datetime.now().isoformat(),
                'total_sessions': 0,
                'total_time_minutes': 0,
                'total_questions': 0,
                'domains_practiced': set(),
                'last_active': None
            }
        
        user = users[user_id]
        user['total_sessions'] += 1
        user['total_time_minutes'] += session_entry.get('duration_minutes', 0)
        user['total_questions'] += session_entry.get('questions_answered', 0)
        user['last_active'] = session_entry['timestamp']
        
        # Handle sets for JSON serialization
        domains = set(user.get('domains_practiced', []))
        domains.add(session_entry.get('domain', 'general'))
        user['domains_practiced'] = list(domains)
        
        self._save_json_file(self.user_data_file, users)
    
    def _calculate_user_statistics(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate user statistics from sessions"""
        if not sessions:
            return {}
        
        total_time = sum(s.get('duration_minutes', 0) for s in sessions)
        total_questions = sum(s.get('questions_answered', 0) for s in sessions)
        completed_sessions = len([s for s in sessions if s.get('completion_status') == 'completed'])
        
        return {
            'total_sessions': len(sessions),
            'total_time_minutes': total_time,
            'total_questions_answered': total_questions,
            'average_session_duration': total_time / len(sessions) if sessions else 0,
            'completion_rate': (completed_sessions / len(sessions)) * 100 if sessions else 0,
            'average_questions_per_session': total_questions / len(sessions) if sessions else 0
        }
    
    def _get_recent_activity(self, sessions: List[Dict[str, Any]], days: int = 7) -> List[Dict[str, Any]]:
        """Get recent activity for the user"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in sessions 
            if datetime.fromisoformat(s['timestamp']) > cutoff_date
        ]
        
        return sorted(recent_sessions, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    def _calculate_skill_progress(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate skill progress across different domains"""
        domain_sessions = defaultdict(list)
        
        for session in sessions:
            domain = session.get('domain', 'general')
            domain_sessions[domain].append(session)
        
        skill_progress = {}
        for domain, domain_session_list in domain_sessions.items():
            if len(domain_session_list) >= 2:
                # Calculate improvement over time
                recent_scores = [s.get('scores', {}).get('overall_rating', 0) 
                               for s in domain_session_list[-5:]]  # Last 5 sessions
                early_scores = [s.get('scores', {}).get('overall_rating', 0) 
                              for s in domain_session_list[:5]]   # First 5 sessions
                
                if recent_scores and early_scores:
                    recent_avg = statistics.mean([s for s in recent_scores if s > 0])
                    early_avg = statistics.mean([s for s in early_scores if s > 0])
                    
                    skill_progress[domain] = {
                        'sessions_count': len(domain_session_list),
                        'recent_average': recent_avg,
                        'early_average': early_avg,
                        'improvement': recent_avg - early_avg if recent_avg and early_avg else 0,
                        'trend': 'improving' if recent_avg > early_avg else 'stable'
                    }
        
        return skill_progress
    
    def _generate_progress_recommendations(self, sessions: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on progress"""
        recommendations = []
        
        if not sessions:
            return ['Start practicing with some basic interview questions!']
        
        # Analyze patterns and generate recommendations
        domain_counts = defaultdict(int)
        difficulty_counts = defaultdict(int)
        
        for session in sessions:
            domain_counts[session.get('domain', 'general')] += 1
            difficulty_counts[session.get('difficulty', 'medium')] += 1
        
        # Domain recommendations
        if len(domain_counts) == 1:
            recommendations.append('Try practicing questions from different domains to broaden your skills.')
        
        # Difficulty recommendations
        if difficulty_counts.get('easy', 0) > difficulty_counts.get('medium', 0) * 2:
            recommendations.append('Consider increasing difficulty level to challenge yourself more.')
        
        # Consistency recommendations
        recent_sessions = self._get_recent_activity(sessions, days=7)
        if len(recent_sessions) < 3:
            recommendations.append('Try to practice more regularly for better improvement.')
        
        # Session length recommendations
        avg_duration = statistics.mean([s.get('duration_minutes', 0) for s in sessions])
        if avg_duration < 10:
            recommendations.append('Consider longer practice sessions for more comprehensive preparation.')
        
        return recommendations
    
    def _check_achievements(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check and return user achievements"""
        achievements = []
        
        # Session count achievements
        session_count = len(sessions)
        if session_count >= 1:
            achievements.append({'name': 'First Steps', 'description': 'Completed your first practice session', 'earned': True})
        if session_count >= 10:
            achievements.append({'name': 'Dedicated Learner', 'description': 'Completed 10 practice sessions', 'earned': True})
        if session_count >= 50:
            achievements.append({'name': 'Practice Master', 'description': 'Completed 50 practice sessions', 'earned': True})
        
        # Time achievements
        total_time = sum(s.get('duration_minutes', 0) for s in sessions)
        if total_time >= 60:
            achievements.append({'name': 'Hour of Practice', 'description': 'Practiced for over 1 hour total', 'earned': True})
        if total_time >= 300:
            achievements.append({'name': 'Five Hour Club', 'description': 'Practiced for over 5 hours total', 'earned': True})
        
        # Domain achievements
        domains = set(s.get('domain', 'general') for s in sessions)
        if len(domains) >= 3:
            achievements.append({'name': 'Versatile Learner', 'description': 'Practiced questions from 3+ different domains', 'earned': True})
        
        return achievements
    
    def _calculate_streaks(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate practice streaks"""
        if not sessions:
            return {'current_streak': 0, 'longest_streak': 0}
        
        # Sort sessions by date
        sorted_sessions = sorted(sessions, key=lambda x: x['timestamp'])
        
        # Group sessions by date
        session_dates = set()
        for session in sorted_sessions:
            date = datetime.fromisoformat(session['timestamp']).date()
            session_dates.add(date)
        
        # Calculate streaks
        dates = sorted(session_dates)
        current_streak = 0
        longest_streak = 0
        temp_streak = 1
        
        if dates:
            # Check current streak
            today = datetime.now().date()
            if dates[-1] == today or dates[-1] == today - timedelta(days=1):
                current_streak = 1
                for i in range(len(dates) - 2, -1, -1):
                    if (dates[i + 1] - dates[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            
            # Calculate longest streak
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
                    temp_streak += 1
                    longest_streak = max(longest_streak, temp_streak)
                else:
                    temp_streak = 1
            
            longest_streak = max(longest_streak, temp_streak)
        
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'total_practice_days': len(dates)
        }
    
    def _filter_sessions_by_time(self, sessions: List[Dict[str, Any]], time_range: str) -> List[Dict[str, Any]]:
        """Filter sessions by time range"""
        days_map = {'7d': 7, '30d': 30, '90d': 90, '1y': 365}
        days = days_map.get(time_range, 30)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return [s for s in sessions if datetime.fromisoformat(s['timestamp']) > cutoff_date]
    
    def _calculate_average_duration(self, sessions: List[Dict[str, Any]]) -> float:
        """Calculate average session duration"""
        if not sessions:
            return 0
        
        durations = [s.get('duration_minutes', 0) for s in sessions]
        return statistics.mean(durations) if durations else 0
    
    def _calculate_domain_distribution(self, sessions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate distribution of practice across domains"""
        domain_counts = defaultdict(int)
        for session in sessions:
            domain = session.get('domain', 'general')
            domain_counts[domain] += 1
        
        return dict(domain_counts)
    
    def _calculate_difficulty_progression(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate how difficulty has progressed over time"""
        if not sessions:
            return {}
        
        sorted_sessions = sorted(sessions, key=lambda x: x['timestamp'])
        difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
        
        recent_sessions = sorted_sessions[-10:]  # Last 10 sessions
        early_sessions = sorted_sessions[:10]   # First 10 sessions
        
        recent_avg = statistics.mean([difficulty_map.get(s.get('difficulty', 'medium'), 2) for s in recent_sessions])
        early_avg = statistics.mean([difficulty_map.get(s.get('difficulty', 'medium'), 2) for s in early_sessions])
        
        return {
            'recent_average_difficulty': recent_avg,
            'early_average_difficulty': early_avg,
            'progression': recent_avg - early_avg,
            'trend': 'increasing' if recent_avg > early_avg else 'stable'
        }
    
    def _calculate_performance_trends(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance trends over time"""
        if not sessions:
            return {}
        
        sorted_sessions = sorted(sessions, key=lambda x: x['timestamp'])
        
        # Group sessions by week
        weekly_performance = defaultdict(list)
        for session in sorted_sessions:
            date = datetime.fromisoformat(session['timestamp']).date()
            week_start = date - timedelta(days=date.weekday())
            overall_rating = session.get('scores', {}).get('overall_rating', 0)
            if overall_rating > 0:
                weekly_performance[week_start.isoformat()].append(overall_rating)
        
        # Calculate weekly averages
        weekly_averages = {}
        for week, ratings in weekly_performance.items():
            weekly_averages[week] = statistics.mean(ratings)
        
        return weekly_averages
    
    def _calculate_weekly_activity(self, sessions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate weekly activity pattern"""
        weekly_counts = defaultdict(int)
        
        for session in sessions:
            date = datetime.fromisoformat(session['timestamp']).date()
            week_start = date - timedelta(days=date.weekday())
            weekly_counts[week_start.isoformat()] += 1
        
        return dict(weekly_counts)
    
    def _calculate_completion_rates(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate completion rates"""
        if not sessions:
            return {}
        
        completed = len([s for s in sessions if s.get('completion_status') == 'completed'])
        total = len(sessions)
        
        return {
            'overall_completion_rate': (completed / total) * 100,
            'completed_sessions': completed,
            'total_sessions': total
        }
    
    def _identify_strengths(self, sessions: List[Dict[str, Any]]) -> List[str]:
        """Identify user strengths based on performance"""
        strengths = []
        
        if not sessions:
            return strengths
        
        # Analyze domain performance
        domain_performance = defaultdict(list)
        for session in sessions:
            domain = session.get('domain', 'general')
            score = session.get('scores', {}).get('overall_rating', 0)
            if score > 0:
                domain_performance[domain].append(score)
        
        # Find domains with high average performance
        for domain, scores in domain_performance.items():
            if len(scores) >= 3 and statistics.mean(scores) >= 7:
                strengths.append(f'Strong performance in {domain} questions')
        
        # Analyze consistency
        completion_rate = len([s for s in sessions if s.get('completion_status') == 'completed']) / len(sessions)
        if completion_rate >= 0.8:
            strengths.append('Excellent session completion rate')
        
        # Analyze practice frequency
        recent_sessions = self._get_recent_activity(sessions, days=14)
        if len(recent_sessions) >= 7:
            strengths.append('Consistent practice schedule')
        
        return strengths
    
    def _identify_improvement_areas(self, sessions: List[Dict[str, Any]]) -> List[str]:
        """Identify areas for improvement"""
        areas = []
        
        if not sessions:
            return ['Start practicing regularly to track improvement areas']
        
        # Analyze domain performance
        domain_performance = defaultdict(list)
        for session in sessions:
            domain = session.get('domain', 'general')
            score = session.get('scores', {}).get('overall_rating', 0)
            if score > 0:
                domain_performance[domain].append(score)
        
        # Find domains with low performance
        for domain, scores in domain_performance.items():
            if len(scores) >= 3 and statistics.mean(scores) < 5:
                areas.append(f'Focus more on {domain} questions')
        
        # Analyze completion rate
        completion_rate = len([s for s in sessions if s.get('completion_status') == 'completed']) / len(sessions)
        if completion_rate < 0.6:
            areas.append('Try to complete more sessions fully')
        
        # Analyze session length
        avg_duration = statistics.mean([s.get('duration_minutes', 0) for s in sessions])
        if avg_duration < 10:
            areas.append('Consider longer practice sessions')
        
        return areas
    
    def _analyze_learning_patterns(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user learning patterns"""
        if not sessions:
            return {}
        
        # Time of day analysis
        hour_counts = defaultdict(int)
        for session in sessions:
            hour = datetime.fromisoformat(session['timestamp']).hour
            hour_counts[hour] += 1
        
        peak_hour = max(hour_counts.keys(), key=hour_counts.get) if hour_counts else 12
        
        # Day of week analysis
        weekday_counts = defaultdict(int)
        for session in sessions:
            weekday = datetime.fromisoformat(session['timestamp']).weekday()
            weekday_counts[weekday] += 1
        
        peak_weekday = max(weekday_counts.keys(), key=weekday_counts.get) if weekday_counts else 0
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        return {
            'preferred_hour': peak_hour,
            'preferred_day': weekday_names[peak_weekday],
            'sessions_per_weekday': dict(weekday_counts),
            'sessions_per_hour': dict(hour_counts)
        }
    
    def _suggest_goals(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggest goals based on current progress"""
        goals = []
        
        session_count = len(sessions)
        if session_count < 10:
            goals.append({
                'type': 'practice_frequency',
                'title': 'Complete 10 Practice Sessions',
                'description': 'Build a foundation with regular practice',
                'target': 10,
                'current': session_count
            })
        
        # Time-based goals
        total_time = sum(s.get('duration_minutes', 0) for s in sessions)
        if total_time < 120:
            goals.append({
                'type': 'practice_time',
                'title': 'Practice for 2 Hours Total',
                'description': 'Increase your total practice time',
                'target': 120,
                'current': total_time
            })
        
        # Domain diversity goals
        domains = set(s.get('domain', 'general') for s in sessions)
        if len(domains) < 3:
            goals.append({
                'type': 'domain_diversity',
                'title': 'Practice 3 Different Domains',
                'description': 'Broaden your skills across different areas',
                'target': 3,
                'current': len(domains)
            })
        
        return goals
    
    def _recommend_next_steps(self, sessions: List[Dict[str, Any]]) -> List[str]:
        """Recommend next steps for the user"""
        if not sessions:
            return [
                'Start with some basic interview questions',
                'Try questions from your field of interest',
                'Practice regularly to build confidence'
            ]
        
        recommendations = []
        
        # Analyze recent performance
        recent_sessions = self._get_recent_activity(sessions, days=7)
        if len(recent_sessions) < 2:
            recommendations.append('Practice more frequently - aim for 2-3 sessions per week')
        
        # Domain recommendations
        domain_counts = defaultdict(int)
        for session in sessions:
            domain_counts[session.get('domain', 'general')] += 1
        
        if len(domain_counts) == 1:
            recommendations.append('Try practicing questions from different domains')
        
        # Difficulty recommendations
        recent_difficulties = [s.get('difficulty', 'medium') for s in recent_sessions]
        if recent_difficulties.count('easy') > len(recent_difficulties) * 0.7:
            recommendations.append('Consider trying medium or hard difficulty questions')
        
        # Performance-based recommendations
        recent_scores = [s.get('scores', {}).get('overall_rating', 0) for s in recent_sessions if s.get('scores', {}).get('overall_rating', 0) > 0]
        if recent_scores and statistics.mean(recent_scores) >= 7:
            recommendations.append('Your performance is improving! Try more challenging questions')
        elif recent_scores and statistics.mean(recent_scores) < 5:
            recommendations.append('Focus on fundamentals and consider easier questions to build confidence')
        
        return recommendations