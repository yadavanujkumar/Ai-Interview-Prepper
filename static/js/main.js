/**
 * Main JavaScript entry point for AI Interview Prepper
 * Modern ES6+ modular architecture
 */

// Import core utilities
import { APIClient } from './core/api-client.js';
import { EventBus } from './core/event-bus.js';
import { ComponentRegistry } from './core/component-registry.js';

// Import components
import { FileUploadComponent } from './components/file-upload.js';

// Initialize global app state
window.App = {
    api: new APIClient(),
    events: new EventBus(),
    components: new ComponentRegistry()
};

/**
 * Application initialization
 */
class Application {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;

        console.log('🚀 Initializing AI Interview Prepper...');

        // Register components
        this.registerComponents();
        
        // Initialize components based on current page
        this.initializePageComponents();
        
        // Set up global event listeners
        this.setupGlobalEvents();
        
        // Auto-save functionality
        this.initAutoSave();
        
        this.initialized = true;
        console.log('✅ Application initialized successfully');
    }

    registerComponents() {
        const { components } = window.App;
        
        components.register('file-upload', FileUploadComponent);
    }

    initializePageComponents() {
        const { components } = window.App;
        
        // Auto-initialize components based on DOM elements
        components.initializeAll();
    }

    setupGlobalEvents() {
        // Global error handling
        window.addEventListener('error', this.handleGlobalError);
        
        // Form validation
        document.addEventListener('submit', this.handleFormSubmit);
        
        // Navigation tracking
        document.addEventListener('click', this.handleNavigation);
    }

    initAutoSave() {
        const textareas = document.querySelectorAll('textarea');
        
        textareas.forEach(textarea => {
            // Load saved data
            const savedData = localStorage.getItem(`autosave_${textarea.id}`);
            if (savedData && !textarea.value) {
                textarea.value = savedData;
            }
            
            // Save data on input
            textarea.addEventListener('input', function() {
                localStorage.setItem(`autosave_${textarea.id}`, this.value);
            });
        });
    }

    handleGlobalError(event) {
        console.error('Global error:', event.error);
        // Show user-friendly error message
        window.App.events.emit('error', {
            message: 'An unexpected error occurred. Please try again.',
            details: event.error
        });
    }

    handleFormSubmit(event) {
        const form = event.target;
        if (!form.matches('form')) return;

        // Basic form validation
        if (!this.validateForm(form)) {
            event.preventDefault();
            return false;
        }
    }

    validateForm(form) {
        let isValid = true;
        
        // Check if either file upload or text input is provided for JD
        const jdFile = form.querySelector('#jd_file');
        const jdText = form.querySelector('#jd_text');
        
        if (jdFile && jdText) {
            const hasJdFile = jdFile.files && jdFile.files.length > 0;
            const hasJdText = jdText.value.trim() !== '';
            
            if (!hasJdFile && !hasJdText) {
                this.showError('Please provide a job description either by uploading a file or pasting text.');
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
                this.showError('Please provide your CV/resume either by uploading a file or pasting text.');
                isValid = false;
            }
        }
        
        return isValid;
    }

    handleNavigation(event) {
        const link = event.target.closest('a[href]');
        if (!link) return;

        // Track navigation for analytics
        window.App.events.emit('navigation', {
            href: link.href,
            text: link.textContent.trim()
        });
    }

    showError(message) {
        window.App.events.emit('error', { message });
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new Application();
    app.init();
});

// Export for module usage
export { Application };