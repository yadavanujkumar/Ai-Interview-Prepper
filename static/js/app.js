// AI Interview Prepper JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload drag and drop functionality
    initializeFileUpload();
    
    // Progress bar animations
    animateProgressBars();
    
    // Form validation
    initializeFormValidation();
});

function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const dropZone = input.closest('.upload-section');
        
        if (dropZone) {
            // Prevent default drag behaviors
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
            });

            // Highlight drop zone when item is dragged over it
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, highlight, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, unhighlight, false);
            });

            // Handle dropped files
            dropZone.addEventListener('drop', handleDrop, false);
        }

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        function highlight(e) {
            dropZone.classList.add('dragover');
        }

        function unhighlight(e) {
            dropZone.classList.remove('dragover');
        }

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                input.files = files;
                updateFileDisplay(input, files[0]);
            }
        }
    });
}

function updateFileDisplay(input, file) {
    const label = input.nextElementSibling;
    if (label && label.tagName === 'LABEL') {
        label.textContent = file.name;
        label.classList.add('text-success');
    }
}

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500);
    });
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
}

function validateForm(form) {
    let isValid = true;
    
    // Check if either file upload or text input is provided for JD
    const jdFile = form.querySelector('#jd_file');
    const jdText = form.querySelector('#jd_text');
    
    if (jdFile && jdText) {
        const hasJdFile = jdFile.files && jdFile.files.length > 0;
        const hasJdText = jdText.value.trim() !== '';
        
        if (!hasJdFile && !hasJdText) {
            showError('Please provide a job description either by uploading a file or pasting text.');
            isValid = false;
        }
    }
    
    // Check if either file upload or text input is provided for CV
    const cvFile = form.querySelector('#cv_file');
    const cvText = form.querySelector('#cv_text');
    
    if (cvFile && cvText) {
        const hasCvFile = cvFile.files && cvFile.files.length > 0;
        const hasCvText = cvText.value.trim() !== '';
        
        if (!hasCvFile && !hasCvText) {
            showError('Please provide your CV/resume either by uploading a file or pasting text.');
            isValid = false;
        }
    }
    
    return isValid;
}

function showError(message) {
    // Create or update error alert
    let errorAlert = document.querySelector('.alert-danger');
    
    if (!errorAlert) {
        errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger alert-dismissible fade show';
        errorAlert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(errorAlert, main.firstChild);
        }
    } else {
        errorAlert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
    }
    
    // Scroll to top to show error
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// File type validation
function validateFileType(file, allowedTypes) {
    const fileExtension = file.name.split('.').pop().toLowerCase();
    return allowedTypes.includes(fileExtension);
}

// File size validation (16MB limit)
function validateFileSize(file, maxSizeMB = 16) {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    return file.size <= maxSizeBytes;
}

// Add file validation to file inputs
document.addEventListener('change', function(e) {
    if (e.target.type === 'file') {
        const file = e.target.files[0];
        if (file) {
            const allowedTypes = ['pdf', 'docx', 'txt'];
            
            if (!validateFileType(file, allowedTypes)) {
                showError(`Invalid file type. Please upload a PDF, DOCX, or TXT file.`);
                e.target.value = '';
                return;
            }
            
            if (!validateFileSize(file)) {
                showError(`File size too large. Please upload a file smaller than 16MB.`);
                e.target.value = '';
                return;
            }
            
            // Clear any existing errors
            const errorAlert = document.querySelector('.alert-danger');
            if (errorAlert) {
                errorAlert.remove();
            }
        }
    }
});

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Add loading state to submit buttons
document.addEventListener('submit', function(e) {
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading"></span> Processing...';
        submitBtn.disabled = true;
        
        // Re-enable button after 30 seconds (failsafe)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 30000);
    }
});

// Copy to clipboard functionality
function copyToClipboard(text, buttonElement) {
    navigator.clipboard.writeText(text).then(function() {
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
        buttonElement.classList.add('btn-success');
        
        setTimeout(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.classList.remove('btn-success');
        }, 2000);
    });
}

// Dark mode toggle (if needed in future)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Initialize dark mode from localStorage
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Auto-save form data to localStorage
function autoSaveForm() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        // Load saved data
        const savedData = localStorage.getItem(`autosave_${textarea.id}`);
        if (savedData && !textarea.value) {
            textarea.value = savedData;
        }
        
        // Save data on input
        textarea.addEventListener('input', function() {
            localStorage.setItem(`autosave_${textarea.id}`, textarea.value);
        });
    });
}

// Clear auto-saved data when form is successfully submitted
function clearAutoSave() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        localStorage.removeItem(`autosave_${textarea.id}`);
    });
}

// Initialize auto-save
document.addEventListener('DOMContentLoaded', autoSaveForm);

// Analytics tracking (placeholder for future implementation)
function trackEvent(eventName, eventData = {}) {
    // Placeholder for analytics tracking
    console.log('Event tracked:', eventName, eventData);
}

// Track form submissions
document.addEventListener('submit', function(e) {
    trackEvent('form_submit', {
        form_id: e.target.id || 'unknown',
        timestamp: new Date().toISOString()
    });
});

// Track button clicks
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn')) {
        trackEvent('button_click', {
            button_text: e.target.textContent.trim(),
            timestamp: new Date().toISOString()
        });
    }
});