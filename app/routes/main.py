"""
Main application routes (API endpoints)
"""
from flask import Blueprint, request, jsonify, current_app
from app.core.utils import process_file_upload

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage - Simple HTML interface"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Interview Prepper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: none; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; }
        .feature-card { transition: transform 0.2s; }
        .feature-card:hover { transform: translateY(-5px); }
    </style>
</head>
<body>
    <header class="header text-white py-4">
        <div class="container">
            <h1 class="mb-0"><i class="fas fa-brain me-2"></i>AI Interview Prepper</h1>
            <p class="mb-0">Intelligent interview preparation with AI-powered analysis</p>
        </div>
    </header>

    <div class="container my-5">
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Upload Documents for Analysis</h3>
                    </div>
                    <div class="card-body">
                        <form id="analysisForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Job Description</label>
                                    <textarea class="form-control" id="jd_text" rows="6" placeholder="Paste job description here..."></textarea>
                                    <small class="text-muted">Or upload a file:</small>
                                    <input type="file" class="form-control mt-1" id="jd_file" accept=".txt,.pdf,.docx">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">CV/Resume</label>
                                    <textarea class="form-control" id="cv_text" rows="6" placeholder="Paste your CV/resume here..."></textarea>
                                    <small class="text-muted">Or upload a file:</small>
                                    <input type="file" class="form-control mt-1" id="cv_file" accept=".txt,.pdf,.docx">
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary btn-lg">Analyze Fit</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-lg-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-chart-line fa-3x text-primary mb-3"></i>
                        <h5>CV Analysis</h5>
                        <p>Get detailed analysis of how well your CV matches the job requirements</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-question-circle fa-3x text-primary mb-3"></i>
                        <h5>Interview Questions</h5>
                        <p>Generate personalized interview questions based on the job description</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-graduation-cap fa-3x text-primary mb-3"></i>
                        <h5>Study Resources</h5>
                        <p>Get curated learning materials to improve your skills</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="results" class="mt-5" style="display: none;">
            <div class="card">
                <div class="card-header">
                    <h3 class="mb-0">Analysis Results</h3>
                </div>
                <div class="card-body" id="resultsContent">
                    <!-- Results will be loaded here -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://kit.fontawesome.com/31b1be0e29.js" crossorigin="anonymous"></script>
    <script>
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const jdText = document.getElementById('jd_text').value;
            const cvText = document.getElementById('cv_text').value;
            
            if (!jdText || !cvText) {
                alert('Please provide both job description and CV text');
                return;
            }
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        job_description: jdText,
                        cv_text: cvText
                    })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                alert('Error analyzing documents: ' + error.message);
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('resultsContent');
            
            let html = '<div class="row">';
            
            // Overall fit score
            if (data.overall_fit_score) {
                const score = Math.round(data.overall_fit_score * 100);
                const color = score >= 70 ? 'success' : score >= 50 ? 'warning' : 'danger';
                html += `<div class="col-md-12 mb-3">
                    <div class="alert alert-${color}">
                        <h5>Overall Fit Score: ${score}%</h5>
                    </div>
                </div>`;
            }
            
            // Skills analysis
            if (data.skills_analysis) {
                html += '<div class="col-md-6 mb-3"><div class="card"><div class="card-header"><h5>Skills Analysis</h5></div><div class="card-body">';
                if (data.skills_analysis.matching_skills) {
                    html += '<h6 class="text-success">Matching Skills:</h6><ul>';
                    data.skills_analysis.matching_skills.forEach(skill => {
                        html += `<li>${skill}</li>`;
                    });
                    html += '</ul>';
                }
                if (data.skills_analysis.missing_skills) {
                    html += '<h6 class="text-warning">Missing Skills:</h6><ul>';
                    data.skills_analysis.missing_skills.forEach(skill => {
                        html += `<li>${skill}</li>`;
                    });
                    html += '</ul>';
                }
                html += '</div></div></div>';
            }
            
            // Recommendations
            if (data.recommendations) {
                html += '<div class="col-md-6 mb-3"><div class="card"><div class="card-header"><h5>Recommendations</h5></div><div class="card-body">';
                if (data.recommendations.skills_to_develop) {
                    html += '<h6>Skills to Develop:</h6><ul>';
                    data.recommendations.skills_to_develop.forEach(skill => {
                        html += `<li>${skill}</li>`;
                    });
                    html += '</ul>';
                }
                html += '</div></div></div>';
            }
            
            html += '</div>';
            
            // Add interview questions button
            html += `<div class="mt-3">
                <button class="btn btn-primary" onclick="generateQuestions()">Generate Interview Questions</button>
                <button class="btn btn-secondary ms-2" onclick="viewStudyResources()">View Study Resources</button>
            </div>`;
            
            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }
        
        async function generateQuestions() {
            const jdText = document.getElementById('jd_text').value;
            const cvText = document.getElementById('cv_text').value;
            
            try {
                const response = await fetch('/interview/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        job_description: jdText,
                        cv_text: cvText,
                        difficulty: 2
                    })
                });
                
                const data = await response.json();
                displayQuestions(data);
            } catch (error) {
                alert('Error generating questions: ' + error.message);
            }
        }
        
        function displayQuestions(data) {
            const contentDiv = document.getElementById('resultsContent');
            let html = '<h4>Interview Questions</h4>';
            
            Object.entries(data.questions).forEach(([category, questions]) => {
                html += `<div class="card mb-3">
                    <div class="card-header"><h5>${category.charAt(0).toUpperCase() + category.slice(1)} Questions</h5></div>
                    <div class="card-body"><ol>`;
                questions.forEach(question => {
                    html += `<li class="mb-2">${question}</li>`;
                });
                html += '</ol></div></div>';
            });
            
            contentDiv.innerHTML = html;
        }
        
        function viewStudyResources() {
            window.open('/api/study-resources?domain=general', '_blank');
        }
    </script>
</body>
</html>
'''


@main_bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for CV/JD analysis"""
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


@main_bp.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and analysis"""
    try:
        # Check if files are present
        if 'jd_file' not in request.files and 'jd_text' not in request.form:
            return jsonify({'error': 'No job description provided'}), 400
        
        if 'cv_file' not in request.files and 'cv_text' not in request.form:
            return jsonify({'error': 'No CV/resume provided'}), 400

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
            return jsonify({'error': 'Could not extract text from uploaded files'}), 400

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
        
        return jsonify({
            'analysis': analysis_result,
            'study_resources': study_recommendations,
            'interview_guide': interview_guide
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/generate_interview/<int:difficulty>')
def generate_interview(difficulty):
    """Generate interview questions API"""
    try:
        # Get stored analysis from session or request
        jd_text = request.args.get('jd', '')
        cv_text = request.args.get('cv', '')
        
        if not jd_text or not cv_text:
            return jsonify({'error': 'Job description and CV required for interview generation'}), 400
        
        questions = current_app.interview_gen.generate_questions(jd_text, cv_text, difficulty)
        
        return jsonify({
            'questions': questions, 
            'difficulty': difficulty,
            'metadata': {
                'total_questions': sum(len(q) for q in questions.values()),
                'categories': list(questions.keys())
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500