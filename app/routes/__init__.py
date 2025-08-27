"""
Blueprint registration for modular route organization
"""
from flask import Flask


def register_blueprints(app: Flask):
    """Register all application blueprints"""
    
    # Core application routes
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # API routes (import here to avoid circular imports)
    from api import api_v1, study_resources_bp, interview_bp
    
    # Import routes to register them with blueprints
    import api.analysis_routes
    import api.study_resources_routes
    import api.interview_routes
    import api.chat_routes
    import api.job_board_routes
    import api.analytics_routes
    import api.company_routes
    import api.salary_routes
    import api.localization_routes
    
    app.register_blueprint(api_v1)
    app.register_blueprint(study_resources_bp)
    app.register_blueprint(interview_bp)
    
    # Additional feature routes
    from app.routes.features import features_bp
    app.register_blueprint(features_bp)
    
    return app