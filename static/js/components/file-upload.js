/**
 * Modern File Upload Component
 * Handles drag & drop, progress tracking, and validation
 */

export class FileUploadComponent {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            maxSize: 16 * 1024 * 1024, // 16MB
            allowedTypes: ['txt', 'pdf', 'docx'],
            multiple: false,
            ...options
        };
        
        this.files = [];
        this.isUploading = false;
    }

    init() {
        this.createElements();
        this.bindEvents();
        this.addStyles();
    }

    createElements() {
        this.container.innerHTML = `
            <div class="file-upload-area" data-state="idle">
                <div class="file-upload-content">
                    <i class="fas fa-cloud-upload-alt file-upload-icon"></i>
                    <h4 class="file-upload-title">Drop files here or click to browse</h4>
                    <p class="file-upload-subtitle">
                        Supported formats: ${this.options.allowedTypes.join(', ').toUpperCase()}
                        <br>Maximum size: ${this.formatFileSize(this.options.maxSize)}
                    </p>
                    <input type="file" class="file-upload-input" 
                           accept=".${this.options.allowedTypes.join(',.')}"
                           ${this.options.multiple ? 'multiple' : ''}>
                    <button type="button" class="btn btn-primary file-upload-button">
                        <i class="fas fa-folder-open me-2"></i>Choose Files
                    </button>
                </div>
                
                <div class="file-upload-progress" style="display: none;">
                    <div class="progress">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                             role="progressbar" style="width: 0%"></div>
                    </div>
                    <p class="progress-text">Uploading...</p>
                </div>
                
                <div class="file-upload-files"></div>
            </div>
        `;

        this.elements = {
            area: this.container.querySelector('.file-upload-area'),
            input: this.container.querySelector('.file-upload-input'),
            button: this.container.querySelector('.file-upload-button'),
            progress: this.container.querySelector('.file-upload-progress'),
            progressBar: this.container.querySelector('.progress-bar'),
            progressText: this.container.querySelector('.progress-text'),
            filesList: this.container.querySelector('.file-upload-files')
        };
    }

    bindEvents() {
        const { area, input, button } = this.elements;

        // Drag & drop events
        area.addEventListener('dragover', this.handleDragOver.bind(this));
        area.addEventListener('dragleave', this.handleDragLeave.bind(this));
        area.addEventListener('drop', this.handleDrop.bind(this));

        // Click events
        area.addEventListener('click', this.handleAreaClick.bind(this));
        button.addEventListener('click', this.handleButtonClick.bind(this));
        
        // File input change
        input.addEventListener('change', this.handleFileSelect.bind(this));
    }

    handleDragOver(event) {
        event.preventDefault();
        this.elements.area.classList.add('drag-over');
        this.elements.area.setAttribute('data-state', 'drag-over');
    }

    handleDragLeave(event) {
        event.preventDefault();
        this.elements.area.classList.remove('drag-over');
        this.elements.area.setAttribute('data-state', 'idle');
    }

    handleDrop(event) {
        event.preventDefault();
        this.elements.area.classList.remove('drag-over');
        this.elements.area.setAttribute('data-state', 'idle');
        
        const files = Array.from(event.dataTransfer.files);
        this.processFiles(files);
    }

    handleAreaClick(event) {
        if (event.target === this.elements.area || 
            event.target.closest('.file-upload-content')) {
            this.elements.input.click();
        }
    }

    handleButtonClick(event) {
        event.stopPropagation();
        this.elements.input.click();
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.processFiles(files);
    }

    processFiles(files) {
        const validFiles = files.filter(file => this.validateFile(file));
        
        if (validFiles.length === 0) {
            return;
        }

        if (!this.options.multiple) {
            this.files = [validFiles[0]];
        } else {
            this.files = [...this.files, ...validFiles];
        }

        this.renderFilesList();
        this.emitChange();
    }

    validateFile(file) {
        // Check file size
        if (file.size > this.options.maxSize) {
            this.showError(`File "${file.name}" is too large. Maximum size is ${this.formatFileSize(this.options.maxSize)}.`);
            return false;
        }

        // Check file type
        const extension = file.name.split('.').pop().toLowerCase();
        if (!this.options.allowedTypes.includes(extension)) {
            this.showError(`File type "${extension}" is not supported. Allowed types: ${this.options.allowedTypes.join(', ')}.`);
            return false;
        }

        return true;
    }

    renderFilesList() {
        const { filesList } = this.elements;
        
        if (this.files.length === 0) {
            filesList.innerHTML = '';
            return;
        }

        filesList.innerHTML = this.files.map((file, index) => `
            <div class="file-item" data-index="${index}">
                <div class="file-info">
                    <i class="fas fa-file-alt file-icon"></i>
                    <div class="file-details">
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${this.formatFileSize(file.size)}</div>
                    </div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger file-remove" 
                        data-index="${index}">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');

        // Bind remove events
        filesList.querySelectorAll('.file-remove').forEach(button => {
            button.addEventListener('click', (e) => {
                const index = parseInt(e.target.dataset.index || e.target.closest('[data-index]').dataset.index);
                this.removeFile(index);
            });
        });
    }

    removeFile(index) {
        this.files.splice(index, 1);
        this.renderFilesList();
        this.emitChange();
    }

    showProgress(percent) {
        this.elements.progress.style.display = 'block';
        this.elements.progressBar.style.width = `${percent}%`;
        this.elements.progressText.textContent = `Uploading... ${Math.round(percent)}%`;
    }

    hideProgress() {
        this.elements.progress.style.display = 'none';
    }

    showError(message) {
        window.App?.events?.emit('error', { message });
    }

    emitChange() {
        window.App?.events?.emit('file-upload-change', {
            component: this,
            files: this.files
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    addStyles() {
        if (document.getElementById('file-upload-styles')) return;

        const styles = `
            <style id="file-upload-styles">
                .file-upload-area {
                    border: 2px dashed #dee2e6;
                    border-radius: 8px;
                    padding: 2rem;
                    text-align: center;
                    transition: all 0.3s ease;
                    cursor: pointer;
                    background: #f8f9fa;
                }

                .file-upload-area:hover,
                .file-upload-area.drag-over {
                    border-color: #007bff;
                    background: #e3f2fd;
                }

                .file-upload-icon {
                    font-size: 3rem;
                    color: #6c757d;
                    margin-bottom: 1rem;
                }

                .file-upload-title {
                    color: #495057;
                    margin-bottom: 0.5rem;
                }

                .file-upload-subtitle {
                    color: #6c757d;
                    font-size: 0.9rem;
                    margin-bottom: 1.5rem;
                }

                .file-upload-input {
                    display: none;
                }

                .file-upload-progress {
                    margin-top: 1rem;
                }

                .progress-text {
                    margin-top: 0.5rem;
                    font-size: 0.9rem;
                    color: #6c757d;
                }

                .file-upload-files {
                    margin-top: 1rem;
                }

                .file-item {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0.75rem;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    margin-bottom: 0.5rem;
                    background: white;
                }

                .file-info {
                    display: flex;
                    align-items: center;
                }

                .file-icon {
                    color: #007bff;
                    margin-right: 0.75rem;
                    font-size: 1.2rem;
                }

                .file-name {
                    font-weight: 500;
                    color: #495057;
                }

                .file-size {
                    font-size: 0.85rem;
                    color: #6c757d;
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    // Public API
    getFiles() {
        return this.files;
    }

    clearFiles() {
        this.files = [];
        this.renderFilesList();
        this.emitChange();
    }

    destroy() {
        // Clean up event listeners and DOM
        this.container.innerHTML = '';
    }
}