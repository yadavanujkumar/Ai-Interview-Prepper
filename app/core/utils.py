"""
Core utilities and helpers
"""
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def process_file_upload(file, doc_processor, allowed_extensions):
    """Process uploaded file and extract text"""
    import tempfile
    import os
    
    if not file or not file.filename:
        return None
        
    if not allowed_file(file.filename, allowed_extensions):
        return None
        
    try:
        with tempfile.NamedTemporaryFile(delete=False, 
                                       suffix='.' + file.filename.rsplit('.', 1)[1].lower()) as temp_file:
            file.save(temp_file.name)
            text = doc_processor.extract_text(temp_file.name)
            os.unlink(temp_file.name)
            return text
    except Exception:
        return None