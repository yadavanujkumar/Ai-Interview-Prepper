"""
Main application routes (core functionality)
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from app.core.utils import process_file_upload

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@main_bp.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and analysis"""
    try:
        # Check if files are present
        if 'jd_file' not in request.files and 'jd_text' not in request.form:
            flash('No job description provided')
            return redirect(url_for('main.index'))
        
        if 'cv_file' not in request.files and 'cv_text' not in request.form:
            flash('No CV/resume provided')
            return redirect(url_for('main.index'))

        # Process Job Description
        jd_text = ""
        if request.form.get('jd_text'):
            jd_text = request.form['jd_text']
        elif request.files['jd_file'].filename:
            jd_file = request.files['jd_file']
            jd_text = process_file_upload(jd_file, current_app.doc_processor, 
                                        current_app.config['ALLOWED_EXTENSIONS'])

        # Process CV/Resume
        cv_text = ""
        if request.form.get('cv_text'):
            cv_text = request.form['cv_text']
        elif request.files['cv_file'].filename:
            cv_file = request.files['cv_file']
            cv_text = process_file_upload(cv_file, current_app.doc_processor,
                                        current_app.config['ALLOWED_EXTENSIONS'])

        if not jd_text or not cv_text:
            flash('Could not extract text from uploaded files')
            return redirect(url_for('main.index'))

        # Perform AI analysis
        analysis_result = current_app.ai_analyzer.analyze_fit(jd_text, cv_text)
        
        # Enhance with study resources
        domain = analysis_result.get('job_analysis', {}).get('domain', 'general')
        missing_skills = analysis_result.get('recommendations', {}).get('skills_to_develop', [])
        
        # Add comprehensive study resources
        study_recommendations = current_app.study_service.get_personalized_recommendations(
            domain, missing_skills, 'intermediate'
        )
        
        # Add interview preparation guide
        interview_guide = current_app.study_service.get_interview_preparation_guide(domain)
        
        return render_template('results.html', 
                             jd_text=jd_text[:500] + "..." if len(jd_text) > 500 else jd_text,
                             cv_text=cv_text[:500] + "..." if len(cv_text) > 500 else cv_text,
                             analysis=analysis_result,
                             study_resources=study_recommendations,
                             interview_guide=interview_guide)

    except Exception as e:
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('main.index'))


@main_bp.route('/interview/<int:difficulty>')
def generate_interview(difficulty):
    """Generate interview questions"""
    try:
        # Get stored analysis from session or request
        jd_text = request.args.get('jd', '')
        cv_text = request.args.get('cv', '')
        
        if not jd_text or not cv_text:
            flash('Job description and CV required for interview generation')
            return redirect(url_for('main.index'))
        
        questions = current_app.interview_gen.generate_questions(jd_text, cv_text, difficulty)
        
        return render_template('interview.html', questions=questions, difficulty=difficulty)
    
    except Exception as e:
        flash(f'Error generating interview: {str(e)}')
        return redirect(url_for('main.index'))


@main_bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for analysis"""
    try:
        data = request.get_json()
        jd_text = data.get('job_description', '')
        cv_text = data.get('cv_text', '')
        
        if not jd_text or not cv_text:
            return jsonify({'error': 'Job description and CV text required'}), 400
        
        result = current_app.ai_analyzer.analyze_fit(jd_text, cv_text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500