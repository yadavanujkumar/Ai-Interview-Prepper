/**
 * Study Resources Component
 * Handles displaying and interacting with study resources
 */

class StudyResourcesComponent {
    constructor() {
        this.currentDomain = 'general';
        this.resources = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStyles();
    }

    bindEvents() {
        // Domain filter functionality
        document.addEventListener('change', (e) => {
            if (e.target.matches('.domain-filter')) {
                this.filterByDomain(e.target.value);
            }
        });

        // Resource type toggles
        document.addEventListener('click', (e) => {
            if (e.target.matches('.resource-toggle')) {
                this.toggleResourceSection(e.target);
            }
        });

        // External link tracking
        document.addEventListener('click', (e) => {
            if (e.target.matches('.external-resource-link')) {
                this.trackResourceClick(e.target);
            }
        });

        // Progress tracking for learning paths
        document.addEventListener('change', (e) => {
            if (e.target.matches('.topic-checkbox')) {
                this.updateProgress(e.target);
            }
        });
    }

    async loadResourcesForDomain(domain) {
        try {
            const response = await fetch(`/study-resources/domains/${domain}`);
            if (!response.ok) throw new Error('Failed to load resources');
            
            this.resources = await response.json();
            this.currentDomain = domain;
            this.renderResources();
        } catch (error) {
            console.error('Error loading study resources:', error);
            this.showError('Failed to load study resources. Please try again.');
        }
    }

    async getPersonalizedRecommendations(domain, missingSkills, experienceLevel) {
        try {
            const response = await fetch('/study-resources/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    domain,
                    missing_skills: missingSkills,
                    experience_level: experienceLevel
                })
            });

            if (!response.ok) throw new Error('Failed to get recommendations');
            
            const recommendations = await response.json();
            this.renderPersonalizedRecommendations(recommendations);
        } catch (error) {
            console.error('Error getting personalized recommendations:', error);
            this.showError('Failed to get personalized recommendations.');
        }
    }

    renderResources() {
        if (!this.resources) return;

        // Render learning paths
        this.renderLearningPaths();
        
        // Render books
        this.renderBooks();
        
        // Render online platforms
        this.renderOnlinePlatforms();
        
        // Render practice projects
        this.renderPracticeProjects();
    }

    renderLearningPaths() {
        const container = document.getElementById('learning-paths-container');
        if (!container || !this.resources.learning_paths) return;

        const pathsHtml = this.resources.learning_paths.map(path => `
            <div class="learning-path-card card mb-3">
                <div class="card-header">
                    <h5 class="mb-0">${path.title}</h5>
                    <div class="text-muted">
                        <small>${path.duration} • ${path.difficulty}</small>
                    </div>
                </div>
                <div class="card-body">
                    <div class="topics-checklist">
                        ${path.topics.map((topic, index) => `
                            <div class="form-check mb-2">
                                <input class="form-check-input topic-checkbox" type="checkbox" 
                                       id="topic-${index}" data-path="${path.title}" data-topic="${topic}">
                                <label class="form-check-label" for="topic-${index}">
                                    ${topic}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                    <div class="progress mt-3">
                        <div class="progress-bar" role="progressbar" style="width: 0%">
                            <span class="progress-text">0% Complete</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = pathsHtml;
    }

    renderBooks() {
        const container = document.getElementById('books-container');
        if (!container || !this.resources.books) return;

        const booksHtml = this.resources.books.map(book => `
            <div class="col-md-4 mb-3">
                <div class="card h-100 book-card">
                    <div class="card-body">
                        <h6 class="card-title">${book.title}</h6>
                        <p class="card-text">
                            <small class="text-muted">by ${book.author}</small><br>
                            <span class="badge bg-secondary">${book.difficulty}</span><br>
                            <strong>Focus:</strong> ${book.focus}
                        </p>
                        <button class="btn btn-outline-primary btn-sm" onclick="this.addToWishlist('${book.title}')">
                            <i class="fas fa-bookmark me-1"></i>Add to Wishlist
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = `<div class="row">${booksHtml}</div>`;
    }

    renderOnlinePlatforms() {
        const container = document.getElementById('platforms-container');
        if (!container || !this.resources.online_platforms) return;

        const platformsHtml = this.resources.online_platforms.map(platform => `
            <div class="col-md-6 mb-3">
                <div class="card platform-card">
                    <div class="card-body">
                        <h6 class="card-title">${platform.name}</h6>
                        <p class="card-text">
                            <strong>Type:</strong> ${platform.type}<br>
                            <strong>Focus:</strong> ${platform.focus}<br>
                            <strong>Cost:</strong> <span class="badge bg-info">${platform.cost}</span>
                        </p>
                        <a href="${platform.url}" target="_blank" 
                           class="btn btn-outline-primary btn-sm external-resource-link" 
                           data-platform="${platform.name}">
                            <i class="fas fa-external-link-alt me-1"></i>Visit Platform
                        </a>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = `<div class="row">${platformsHtml}</div>`;
    }

    renderPracticeProjects() {
        const container = document.getElementById('projects-container');
        if (!container || !this.resources.practice_projects) return;

        const projectsHtml = this.resources.practice_projects.map((project, index) => `
            <div class="card mb-3 project-card">
                <div class="card-body">
                    <h6 class="card-title">${project.title}</h6>
                    <p class="card-text">${project.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <span class="badge bg-secondary me-2">${project.difficulty}</span>
                            ${project.technologies.map(tech => 
                                `<span class="badge bg-outline-primary me-1">${tech}</span>`
                            ).join('')}
                        </div>
                        <button class="btn btn-sm btn-outline-success" onclick="this.startProject(${index})">
                            <i class="fas fa-play me-1"></i>Start Project
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = projectsHtml;
    }

    updateProgress(checkbox) {
        const pathTitle = checkbox.dataset.path;
        const pathContainer = checkbox.closest('.learning-path-card');
        const checkboxes = pathContainer.querySelectorAll('.topic-checkbox');
        const progressBar = pathContainer.querySelector('.progress-bar');
        const progressText = pathContainer.querySelector('.progress-text');

        const totalTopics = checkboxes.length;
        const completedTopics = Array.from(checkboxes).filter(cb => cb.checked).length;
        const progressPercent = Math.round((completedTopics / totalTopics) * 100);

        progressBar.style.width = `${progressPercent}%`;
        progressText.textContent = `${progressPercent}% Complete`;

        // Store progress in localStorage
        this.saveProgress(pathTitle, completedTopics, totalTopics);
    }

    saveProgress(pathTitle, completed, total) {
        const progress = JSON.parse(localStorage.getItem('studyProgress') || '{}');
        progress[pathTitle] = { completed, total, lastUpdated: new Date().toISOString() };
        localStorage.setItem('studyProgress', JSON.stringify(progress));
    }

    loadProgress() {
        const progress = JSON.parse(localStorage.getItem('studyProgress') || '{}');
        
        Object.entries(progress).forEach(([pathTitle, data]) => {
            // Restore checkbox states and progress bars
            const pathCards = document.querySelectorAll('.learning-path-card');
            pathCards.forEach(card => {
                const title = card.querySelector('.card-header h5').textContent;
                if (title === pathTitle) {
                    const checkboxes = card.querySelectorAll('.topic-checkbox');
                    const progressBar = card.querySelector('.progress-bar');
                    const progressText = card.querySelector('.progress-text');
                    
                    // Check the appropriate number of checkboxes
                    for (let i = 0; i < data.completed; i++) {
                        if (checkboxes[i]) checkboxes[i].checked = true;
                    }
                    
                    // Update progress bar
                    const progressPercent = Math.round((data.completed / data.total) * 100);
                    progressBar.style.width = `${progressPercent}%`;
                    progressText.textContent = `${progressPercent}% Complete`;
                }
            });
        });
    }

    trackResourceClick(link) {
        const platform = link.dataset.platform;
        console.log(`User clicked on ${platform} resource`);
        
        // Send analytics event (implement as needed)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'resource_click', {
                'platform': platform,
                'domain': this.currentDomain
            });
        }
    }

    addToWishlist(bookTitle) {
        const wishlist = JSON.parse(localStorage.getItem('bookWishlist') || '[]');
        if (!wishlist.includes(bookTitle)) {
            wishlist.push(bookTitle);
            localStorage.setItem('bookWishlist', JSON.stringify(wishlist));
            this.showSuccess(`"${bookTitle}" added to your wishlist!`);
        } else {
            this.showInfo(`"${bookTitle}" is already in your wishlist.`);
        }
    }

    startProject(projectIndex) {
        const project = this.resources.practice_projects[projectIndex];
        this.showProjectModal(project);
    }

    showProjectModal(project) {
        const modalHtml = `
            <div class="modal fade" id="projectModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${project.title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${project.description}</p>
                            <h6>Technologies:</h6>
                            <div class="mb-3">
                                ${project.technologies.map(tech => 
                                    `<span class="badge bg-primary me-1">${tech}</span>`
                                ).join('')}
                            </div>
                            <h6>Getting Started:</h6>
                            <ol>
                                <li>Set up your development environment</li>
                                <li>Plan your project structure</li>
                                <li>Start with the core functionality</li>
                                <li>Add features incrementally</li>
                                <li>Test and refine your solution</li>
                            </ol>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" onclick="this.markProjectStarted('${project.title}')">
                                Mark as Started
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('projectModal'));
        modal.show();

        // Clean up modal after hiding
        document.getElementById('projectModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }

    markProjectStarted(projectTitle) {
        const startedProjects = JSON.parse(localStorage.getItem('startedProjects') || '[]');
        if (!startedProjects.includes(projectTitle)) {
            startedProjects.push(projectTitle);
            localStorage.setItem('startedProjects', JSON.stringify(startedProjects));
            this.showSuccess(`Project "${projectTitle}" marked as started!`);
        }
    }

    filterByDomain(domain) {
        this.currentDomain = domain;
        this.loadResourcesForDomain(domain);
    }

    toggleResourceSection(button) {
        const targetId = button.dataset.target;
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            const isHidden = targetElement.style.display === 'none';
            targetElement.style.display = isHidden ? 'block' : 'none';
            button.innerHTML = isHidden ? 
                '<i class="fas fa-eye-slash me-1"></i>Hide' : 
                '<i class="fas fa-eye me-1"></i>Show';
        }
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showInfo(message) {
        this.showToast(message, 'info');
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type) {
        // Create toast if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        const toastHtml = `
            <div class="toast" role="alert">
                <div class="toast-header">
                    <i class="fas fa-${type === 'success' ? 'check-circle text-success' : 
                                     type === 'error' ? 'exclamation-circle text-danger' : 
                                     'info-circle text-info'} me-2"></i>
                    <strong class="me-auto">Study Resources</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">${message}</div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }

    loadStyles() {
        // Add component-specific styles
        const styles = `
            <style>
                .learning-path-card {
                    transition: transform 0.2s ease;
                }
                .learning-path-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                .book-card:hover, .platform-card:hover, .project-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    transition: all 0.2s ease;
                }
                .progress-text {
                    font-size: 0.8rem;
                    font-weight: bold;
                }
                .topic-checkbox:checked + label {
                    text-decoration: line-through;
                    color: #6c757d;
                }
                .resource-section {
                    border-left: 4px solid #007bff;
                    padding-left: 1rem;
                    margin-bottom: 2rem;
                }
            </style>
        `;
        
        if (!document.getElementById('study-resources-styles')) {
            const styleElement = document.createElement('div');
            styleElement.id = 'study-resources-styles';
            styleElement.innerHTML = styles;
            document.head.appendChild(styleElement);
        }
    }
}

// Initialize the component when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.study-resources-component')) {
        window.studyResourcesComponent = new StudyResourcesComponent();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StudyResourcesComponent;
}