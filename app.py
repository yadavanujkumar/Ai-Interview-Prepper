from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
from utils.document_processor import DocumentProcessor
from utils.ai_analyzer import AIAnalyzer
from utils.interview_generator import InterviewGenerator
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize processors
doc_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()
interview_gen = InterviewGenerator()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check if files are present
        if 'jd_file' not in request.files and 'jd_text' not in request.form:
            flash('No job description provided')
            return redirect(url_for('index'))
        
        if 'cv_file' not in request.files and 'cv_text' not in request.form:
            flash('No CV/resume provided')
            return redirect(url_for('index'))

        # Process Job Description
        jd_text = ""
        if request.form.get('jd_text'):
            jd_text = request.form['jd_text']
        elif request.files['jd_file'].filename:
            jd_file = request.files['jd_file']
            if allowed_file(jd_file.filename):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.' + jd_file.filename.rsplit('.', 1)[1].lower()) as temp_file:
                    jd_file.save(temp_file.name)
                    jd_text = doc_processor.extract_text(temp_file.name)
                    os.unlink(temp_file.name)

        # Process CV/Resume
        cv_text = ""
        if request.form.get('cv_text'):
            cv_text = request.form['cv_text']
        elif request.files['cv_file'].filename:
            cv_file = request.files['cv_file']
            if allowed_file(cv_file.filename):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.' + cv_file.filename.rsplit('.', 1)[1].lower()) as temp_file:
                    cv_file.save(temp_file.name)
                    cv_text = doc_processor.extract_text(temp_file.name)
                    os.unlink(temp_file.name)

        if not jd_text or not cv_text:
            flash('Could not extract text from uploaded files')
            return redirect(url_for('index'))

        # Perform AI analysis
        analysis_result = ai_analyzer.analyze_fit(jd_text, cv_text)
        
        return render_template('results.html', 
                             jd_text=jd_text[:500] + "..." if len(jd_text) > 500 else jd_text,
                             cv_text=cv_text[:500] + "..." if len(cv_text) > 500 else cv_text,
                             analysis=analysis_result)

    except Exception as e:
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('index'))

@app.route('/interview/<int:difficulty>')
def generate_interview(difficulty):
    try:
        # Get stored analysis from session or request
        jd_text = request.args.get('jd', '')
        cv_text = request.args.get('cv', '')
        
        if not jd_text or not cv_text:
            flash('Job description and CV required for interview generation')
            return redirect(url_for('index'))
        
        questions = interview_gen.generate_questions(jd_text, cv_text, difficulty)
        
        return render_template('interview.html', questions=questions, difficulty=difficulty)
    
    except Exception as e:
        flash(f'Error generating interview: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for analysis"""
    try:
        data = request.get_json()
        jd_text = data.get('job_description', '')
        cv_text = data.get('cv_text', '')
        
        if not jd_text or not cv_text:
            return jsonify({'error': 'Job description and CV text required'}), 400
        
        result = ai_analyzer.analyze_fit(jd_text, cv_text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)