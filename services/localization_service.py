"""
Multi-language Support Service
"""
import json
import os
from typing import Dict, List, Optional, Any

class LocalizationService:
    """Service for handling multi-language support"""
    
    def __init__(self, languages_dir: str = 'languages'):
        self.languages_dir = languages_dir
        self.supported_languages = {}
        self.default_language = 'en'
        self.current_language = 'en'
        
        # Ensure languages directory exists
        os.makedirs(languages_dir, exist_ok=True)
        
        # Initialize default languages
        self._initialize_default_languages()
        
        # Load all available languages
        self._load_languages()
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return {
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'zh': '中文',
            'ja': '日本語',
            'ko': '한국어',
            'ru': 'Русский'
        }
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key: str, language: Optional[str] = None, **kwargs) -> str:
        """Get localized text for a given key"""
        lang = language or self.current_language
        
        # Fallback to default language if requested language not available
        if lang not in self.supported_languages:
            lang = self.default_language
        
        # Navigate through nested keys (e.g., 'app.title')
        text = self.supported_languages.get(lang, {})
        keys = key.split('.')
        
        for k in keys:
            if isinstance(text, dict) and k in text:
                text = text[k]
            else:
                # Fallback to English if key not found
                text = self.supported_languages.get(self.default_language, {})
                for k2 in keys:
                    if isinstance(text, dict) and k2 in text:
                        text = text[k2]
                    else:
                        return f"[Missing: {key}]"
                break
        
        # Format text with provided arguments
        if isinstance(text, str) and kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        
        return str(text) if not isinstance(text, dict) else f"[Invalid key: {key}]"
    
    def get_localized_content(self, content_type: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Get localized content for specific content types"""
        lang = language or self.current_language
        
        content_maps = {
            'interview_questions': self._get_localized_interview_questions(lang),
            'study_materials': self._get_localized_study_materials(lang),
            'feedback_templates': self._get_localized_feedback_templates(lang),
            'recommendations': self._get_localized_recommendations(lang),
            'navigation': self._get_localized_navigation(lang)
        }
        
        return content_maps.get(content_type, {})
    
    def translate_interview_questions(self, questions: List[str], target_language: str) -> List[str]:
        """Translate interview questions to target language"""
        # This is a simplified implementation
        # In production, you'd want to use a proper translation service
        
        translations = self.get_localized_content('interview_questions', target_language)
        translated_questions = []
        
        for question in questions:
            # Try to find translation in our predefined translations
            translated = translations.get('technical', {}).get(question, question)
            if translated == question:
                translated = translations.get('behavioral', {}).get(question, question)
            
            translated_questions.append(translated)
        
        return translated_questions
    
    def get_language_specific_domains(self, language: str) -> Dict[str, str]:
        """Get domain names in specific language"""
        domain_translations = {
            'en': {
                'software_engineering': 'Software Engineering',
                'data_science': 'Data Science',
                'healthcare': 'Healthcare',
                'education': 'Education',
                'design': 'Design',
                'marketing': 'Marketing',
                'general': 'General'
            },
            'es': {
                'software_engineering': 'Ingeniería de Software',
                'data_science': 'Ciencia de Datos',
                'healthcare': 'Atención Médica',
                'education': 'Educación',
                'design': 'Diseño',
                'marketing': 'Marketing',
                'general': 'General'
            },
            'fr': {
                'software_engineering': 'Ingénierie Logicielle',
                'data_science': 'Science des Données',
                'healthcare': 'Soins de Santé',
                'education': 'Éducation',
                'design': 'Design',
                'marketing': 'Marketing',
                'general': 'Général'
            }
        }
        
        return domain_translations.get(language, domain_translations['en'])
    
    def _initialize_default_languages(self):
        """Initialize default language files"""
        default_languages = {
            'en': self._get_english_translations(),
            'es': self._get_spanish_translations(),
            'fr': self._get_french_translations()
        }
        
        for lang_code, translations in default_languages.items():
            lang_file = os.path.join(self.languages_dir, f'{lang_code}.json')
            if not os.path.exists(lang_file):
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, indent=2, ensure_ascii=False)
    
    def _load_languages(self):
        """Load all language files"""
        self.supported_languages = {}
        
        if not os.path.exists(self.languages_dir):
            return
        
        for filename in os.listdir(self.languages_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                lang_file = os.path.join(self.languages_dir, filename)
                
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.supported_languages[lang_code] = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    print(f"Error loading language file: {filename}")
    
    def _get_english_translations(self) -> Dict[str, Any]:
        """Get English translations (base language)"""
        return {
            'app': {
                'title': 'AI Interview Prepper',
                'subtitle': 'Ace Your Next Interview with AI-Powered Practice',
                'welcome': 'Welcome to AI Interview Prepper'
            },
            'navigation': {
                'home': 'Home',
                'practice': 'Practice',
                'progress': 'Progress',
                'study': 'Study Resources',
                'chat': 'AI Chat',
                'settings': 'Settings'
            },
            'buttons': {
                'start': 'Start',
                'submit': 'Submit',
                'next': 'Next',
                'previous': 'Previous',
                'save': 'Save',
                'cancel': 'Cancel',
                'upload': 'Upload',
                'analyze': 'Analyze',
                'practice': 'Practice',
                'end_session': 'End Session'
            },
            'forms': {
                'job_description': 'Job Description',
                'cv_resume': 'CV/Resume',
                'upload_file': 'Upload File',
                'paste_text': 'Paste Text',
                'difficulty': 'Difficulty Level',
                'domain': 'Domain'
            },
            'messages': {
                'upload_success': 'File uploaded successfully',
                'analysis_complete': 'Analysis completed',
                'session_started': 'Interview session started',
                'session_ended': 'Interview session ended',
                'progress_saved': 'Progress saved'
            },
            'errors': {
                'file_upload_failed': 'File upload failed',
                'analysis_failed': 'Analysis failed',
                'invalid_input': 'Invalid input',
                'session_not_found': 'Session not found'
            },
            'interview': {
                'technical_questions': 'Technical Questions',
                'behavioral_questions': 'Behavioral Questions',
                'follow_up': 'Follow-up Questions',
                'feedback': 'Feedback',
                'performance': 'Performance'
            },
            'progress': {
                'total_sessions': 'Total Sessions',
                'time_practiced': 'Time Practiced',
                'questions_answered': 'Questions Answered',
                'average_score': 'Average Score',
                'improvement': 'Improvement',
                'strengths': 'Strengths',
                'areas_to_improve': 'Areas to Improve'
            }
        }
    
    def _get_spanish_translations(self) -> Dict[str, Any]:
        """Get Spanish translations"""
        return {
            'app': {
                'title': 'Preparador de Entrevistas IA',
                'subtitle': 'Supera tu Próxima Entrevista con Práctica Potenciada por IA',
                'welcome': 'Bienvenido al Preparador de Entrevistas IA'
            },
            'navigation': {
                'home': 'Inicio',
                'practice': 'Práctica',
                'progress': 'Progreso',
                'study': 'Recursos de Estudio',
                'chat': 'Chat IA',
                'settings': 'Configuración'
            },
            'buttons': {
                'start': 'Comenzar',
                'submit': 'Enviar',
                'next': 'Siguiente',
                'previous': 'Anterior',
                'save': 'Guardar',
                'cancel': 'Cancelar',
                'upload': 'Subir',
                'analyze': 'Analizar',
                'practice': 'Practicar',
                'end_session': 'Terminar Sesión'
            },
            'forms': {
                'job_description': 'Descripción del Trabajo',
                'cv_resume': 'CV/Currículum',
                'upload_file': 'Subir Archivo',
                'paste_text': 'Pegar Texto',
                'difficulty': 'Nivel de Dificultad',
                'domain': 'Dominio'
            },
            'messages': {
                'upload_success': 'Archivo subido exitosamente',
                'analysis_complete': 'Análisis completado',
                'session_started': 'Sesión de entrevista iniciada',
                'session_ended': 'Sesión de entrevista terminada',
                'progress_saved': 'Progreso guardado'
            },
            'errors': {
                'file_upload_failed': 'Error al subir archivo',
                'analysis_failed': 'Error en el análisis',
                'invalid_input': 'Entrada inválida',
                'session_not_found': 'Sesión no encontrada'
            },
            'interview': {
                'technical_questions': 'Preguntas Técnicas',
                'behavioral_questions': 'Preguntas de Comportamiento',
                'follow_up': 'Preguntas de Seguimiento',
                'feedback': 'Retroalimentación',
                'performance': 'Rendimiento'
            },
            'progress': {
                'total_sessions': 'Sesiones Totales',
                'time_practiced': 'Tiempo Practicado',
                'questions_answered': 'Preguntas Respondidas',
                'average_score': 'Puntuación Promedio',
                'improvement': 'Mejora',
                'strengths': 'Fortalezas',
                'areas_to_improve': 'Áreas a Mejorar'
            }
        }
    
    def _get_french_translations(self) -> Dict[str, Any]:
        """Get French translations"""
        return {
            'app': {
                'title': 'Préparateur d\'Entretien IA',
                'subtitle': 'Réussissez Votre Prochain Entretien avec la Pratique Alimentée par l\'IA',
                'welcome': 'Bienvenue au Préparateur d\'Entretien IA'
            },
            'navigation': {
                'home': 'Accueil',
                'practice': 'Pratique',
                'progress': 'Progrès',
                'study': 'Ressources d\'Étude',
                'chat': 'Chat IA',
                'settings': 'Paramètres'
            },
            'buttons': {
                'start': 'Commencer',
                'submit': 'Soumettre',
                'next': 'Suivant',
                'previous': 'Précédent',
                'save': 'Sauvegarder',
                'cancel': 'Annuler',
                'upload': 'Télécharger',
                'analyze': 'Analyser',
                'practice': 'Pratiquer',
                'end_session': 'Terminer la Session'
            },
            'forms': {
                'job_description': 'Description du Poste',
                'cv_resume': 'CV/Curriculum Vitae',
                'upload_file': 'Télécharger un Fichier',
                'paste_text': 'Coller le Texte',
                'difficulty': 'Niveau de Difficulté',
                'domain': 'Domaine'
            },
            'messages': {
                'upload_success': 'Fichier téléchargé avec succès',
                'analysis_complete': 'Analyse terminée',
                'session_started': 'Session d\'entretien commencée',
                'session_ended': 'Session d\'entretien terminée',
                'progress_saved': 'Progrès sauvegardé'
            },
            'errors': {
                'file_upload_failed': 'Échec du téléchargement du fichier',
                'analysis_failed': 'Échec de l\'analyse',
                'invalid_input': 'Entrée invalide',
                'session_not_found': 'Session non trouvée'
            },
            'interview': {
                'technical_questions': 'Questions Techniques',
                'behavioral_questions': 'Questions Comportementales',
                'follow_up': 'Questions de Suivi',
                'feedback': 'Commentaires',
                'performance': 'Performance'
            },
            'progress': {
                'total_sessions': 'Sessions Totales',
                'time_practiced': 'Temps Pratiqué',
                'questions_answered': 'Questions Répondues',
                'average_score': 'Score Moyen',
                'improvement': 'Amélioration',
                'strengths': 'Forces',
                'areas_to_improve': 'Domaines à Améliorer'
            }
        }
    
    def _get_localized_interview_questions(self, language: str) -> Dict[str, Any]:
        """Get localized interview questions"""
        # This would contain question translations
        # For now, returning empty dict as questions would be quite extensive
        return {}
    
    def _get_localized_study_materials(self, language: str) -> Dict[str, Any]:
        """Get localized study materials"""
        return {}
    
    def _get_localized_feedback_templates(self, language: str) -> Dict[str, Any]:
        """Get localized feedback templates"""
        return {}
    
    def _get_localized_recommendations(self, language: str) -> Dict[str, Any]:
        """Get localized recommendations"""
        return {}
    
    def _get_localized_navigation(self, language: str) -> Dict[str, Any]:
        """Get localized navigation items"""
        return self.supported_languages.get(language, {}).get('navigation', {})