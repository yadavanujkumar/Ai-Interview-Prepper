/**
 * Interview Questions Component
 * Handles enhanced interview question functionality
 */

class InterviewQuestionsComponent {
    constructor() {
        this.currentQuestions = null;
        this.userAnswers = {};
        this.timer = null;
        this.currentQuestionIndex = 0;
        this.practiceMode = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStyles();
        this.initializePracticeMode();
    }

    bindEvents() {
        // Question navigation
        document.addEventListener('click', (e) => {
            if (e.target.matches('.next-question-btn')) {
                this.nextQuestion();
            }
            if (e.target.matches('.prev-question-btn')) {
                this.prevQuestion();
            }
            if (e.target.matches('.practice-mode-btn')) {
                this.togglePracticeMode();
            }
        });

        // Answer recording
        document.addEventListener('click', (e) => {
            if (e.target.matches('.record-answer-btn')) {
                this.toggleAnswerRecording(e.target);
            }
            if (e.target.matches('.save-answer-btn')) {
                this.saveAnswer(e.target);
            }
        });

        // Timer controls
        document.addEventListener('click', (e) => {
            if (e.target.matches('.start-timer-btn')) {
                this.startTimer(e.target);
            }
            if (e.target.matches('.stop-timer-btn')) {
                this.stopTimer();
            }
        });

        // Question difficulty adjustment
        document.addEventListener('change', (e) => {
            if (e.target.matches('.difficulty-selector')) {
                this.adjustDifficulty(e.target.value);
            }
        });

        // Question category filters
        document.addEventListener('click', (e) => {
            if (e.target.matches('.category-filter-btn')) {
                this.filterByCategory(e.target.dataset.category);
            }
        });
    }

    async generateQuestions(jobDescription, cv, difficulty = 2) {
        try {
            const response = await fetch('/interview/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    job_description: jobDescription,
                    cv_text: cv,
                    difficulty: difficulty
                })
            });

            if (!response.ok) throw new Error('Failed to generate questions');
            
            const data = await response.json();
            this.currentQuestions = data.questions;
            this.renderQuestions();
            this.updateMetadata(data.metadata);
        } catch (error) {
            console.error('Error generating questions:', error);
            this.showError('Failed to generate interview questions. Please try again.');
        }
    }

    renderQuestions() {
        if (!this.currentQuestions) return;

        Object.entries(this.currentQuestions).forEach(([category, questions]) => {
            this.renderCategoryQuestions(category, questions);
        });

        this.addNavigationControls();
        this.loadSavedAnswers();
    }

    renderCategoryQuestions(category, questions) {
        const container = document.getElementById(`${category}-questions-container`);
        if (!container) return;

        const questionsHtml = questions.map((question, index) => `
            <div class="question-card mb-4 p-3 border rounded" data-category="${category}" data-index="${index}">
                <div class="d-flex align-items-start">
                    <span class="badge bg-${this.getCategoryColor(category)} me-3 mt-1">${index + 1}</span>
                    <div class="flex-grow-1">
                        <div class="question-header d-flex justify-content-between align-items-start mb-3">
                            <p class="question-text mb-0 flex-grow-1">${question}</p>
                            <div class="question-controls ms-3">
                                <button class="btn btn-sm btn-outline-primary start-timer-btn" 
                                        data-category="${category}" data-index="${index}">
                                    <i class="fas fa-clock me-1"></i>Start Timer
                                </button>
                                <button class="btn btn-sm btn-outline-secondary record-answer-btn" 
                                        data-category="${category}" data-index="${index}">
                                    <i class="fas fa-microphone me-1"></i>Record
                                </button>
                            </div>
                        </div>
                        
                        <!-- Timer Display -->
                        <div class="timer-display mb-3" id="timer-${category}-${index}" style="display: none;">
                            <div class="alert alert-info d-flex justify-content-between align-items-center">
                                <span>Time: <strong class="timer-value">00:00</strong></span>
                                <button class="btn btn-sm btn-outline-danger stop-timer-btn">
                                    <i class="fas fa-stop me-1"></i>Stop
                                </button>
                            </div>
                        </div>

                        <!-- Answer Input Area -->
                        <div class="answer-input-area mb-3" id="answer-${category}-${index}">
                            <textarea class="form-control answer-textarea" 
                                      placeholder="Type your answer here or use the record button..."
                                      rows="4"></textarea>
                            <div class="mt-2">
                                <button class="btn btn-sm btn-success save-answer-btn" 
                                        data-category="${category}" data-index="${index}">
                                    <i class="fas fa-save me-1"></i>Save Answer
                                </button>
                                <button class="btn btn-sm btn-outline-info" onclick="this.getQuestionTips('${category}')">
                                    <i class="fas fa-lightbulb me-1"></i>Get Tips
                                </button>
                            </div>
                        </div>

                        <!-- Answer Tips Section -->
                        <div class="answer-section">
                            <button class="btn btn-outline-secondary btn-sm" 
                                    onclick="toggleAnswer(${index + 1}, '${category}')">
                                <i class="fas fa-lightbulb me-1"></i>Show Tips
                            </button>
                            <div id="${category}-answer-${index + 1}" class="answer-tips mt-3" style="display: none;">
                                ${this.getAnswerTips(category)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = questionsHtml;
    }

    getCategoryColor(category) {
        const colors = {
            'technical': 'primary',
            'behavioral': 'success',
            'situational': 'warning',
            'personalized': 'info'
        };
        return colors[category] || 'secondary';
    }

    getAnswerTips(category) {
        const tips = {
            'technical': `
                <div class="alert alert-light">
                    <h6>🔧 Technical Question Tips:</h6>
                    <ul class="mb-0">
                        <li><strong>Think Out Loud:</strong> Explain your reasoning process</li>
                        <li><strong>Break It Down:</strong> Divide complex problems into smaller parts</li>
                        <li><strong>Consider Trade-offs:</strong> Discuss different approaches and their pros/cons</li>
                        <li><strong>Ask Questions:</strong> Clarify requirements and constraints</li>
                        <li><strong>Test Your Solution:</strong> Walk through examples to verify correctness</li>
                    </ul>
                </div>
            `,
            'behavioral': `
                <div class="alert alert-light">
                    <h6>🌟 STAR Method Framework:</h6>
                    <ul class="mb-0">
                        <li><strong>Situation:</strong> Set the context and background</li>
                        <li><strong>Task:</strong> Describe what you needed to accomplish</li>
                        <li><strong>Action:</strong> Explain the specific actions you took</li>
                        <li><strong>Result:</strong> Share the outcomes and what you learned</li>
                    </ul>
                </div>
            `,
            'situational': `
                <div class="alert alert-light">
                    <h6>🎯 Problem-Solving Framework:</h6>
                    <ul class="mb-0">
                        <li><strong>Understand:</strong> Clarify the problem and constraints</li>
                        <li><strong>Analyze:</strong> Consider different approaches and trade-offs</li>
                        <li><strong>Plan:</strong> Outline your proposed solution</li>
                        <li><strong>Execute:</strong> Explain implementation steps</li>
                        <li><strong>Evaluate:</strong> Discuss how you'd measure success</li>
                    </ul>
                </div>
            `,
            'personalized': `
                <div class="alert alert-light">
                    <h6>💡 Personalized Answer Tips:</h6>
                    <ul class="mb-0">
                        <li><strong>Be Specific:</strong> Draw from your actual experience with concrete examples</li>
                        <li><strong>Show Impact:</strong> Quantify results and demonstrate the value you delivered</li>
                        <li><strong>Connect to Role:</strong> Explicitly link your experience to the job requirements</li>
                        <li><strong>Show Growth:</strong> Highlight what you learned and how you've improved</li>
                        <li><strong>Be Authentic:</strong> Share genuine challenges and how you overcame them</li>
                    </ul>
                </div>
            `
        };
        return tips[category] || tips['technical'];
    }

    async getQuestionTips(category) {
        try {
            const response = await fetch(`/interview/question-tips/${category}`);
            if (!response.ok) throw new Error('Failed to get tips');
            
            const tips = await response.json();
            this.showTipsModal(category, tips);
        } catch (error) {
            console.error('Error getting question tips:', error);
            this.showError('Failed to load question tips.');
        }
    }

    showTipsModal(category, tips) {
        const modalHtml = `
            <div class="modal fade" id="tipsModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Tips for ${category.charAt(0).toUpperCase() + category.slice(1)} Questions</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-primary">
                                <h6><strong>Approach:</strong> ${tips.approach}</h6>
                            </div>
                            <h6>Key Tips:</h6>
                            <ul>
                                ${tips.tips.map(tip => `<li>${tip}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('tipsModal'));
        modal.show();

        document.getElementById('tipsModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }

    startTimer(button) {
        const category = button.dataset.category;
        const index = button.dataset.index;
        const timerId = `timer-${category}-${index}`;
        const timerDisplay = document.getElementById(timerId);
        const timerValue = timerDisplay.querySelector('.timer-value');
        
        timerDisplay.style.display = 'block';
        button.disabled = true;
        
        let seconds = 0;
        this.timer = setInterval(() => {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            timerValue.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        
        // Re-enable all timer buttons
        document.querySelectorAll('.start-timer-btn').forEach(btn => {
            btn.disabled = false;
        });
    }

    toggleAnswerRecording(button) {
        const category = button.dataset.category;
        const index = button.dataset.index;
        
        if (button.classList.contains('recording')) {
            this.stopRecording(button);
        } else {
            this.startRecording(button, category, index);
        }
    }

    startRecording(button, category, index) {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            this.showError('Voice recording is not supported in your browser.');
            return;
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                button.classList.add('recording');
                button.innerHTML = '<i class="fas fa-stop me-1"></i>Stop Recording';
                button.classList.remove('btn-outline-secondary');
                button.classList.add('btn-danger');

                // Here you would implement actual recording logic
                // For now, we'll simulate it
                this.showInfo('Voice recording started. (Simulated - actual implementation would record audio)');
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                this.showError('Could not access microphone. Please check permissions.');
            });
    }

    stopRecording(button) {
        button.classList.remove('recording');
        button.innerHTML = '<i class="fas fa-microphone me-1"></i>Record';
        button.classList.remove('btn-danger');
        button.classList.add('btn-outline-secondary');

        this.showSuccess('Recording stopped. (In a real implementation, this would process the audio)');
    }

    saveAnswer(button) {
        const category = button.dataset.category;
        const index = button.dataset.index;
        const questionCard = button.closest('.question-card');
        const textarea = questionCard.querySelector('.answer-textarea');
        const answer = textarea.value.trim();

        if (!answer) {
            this.showError('Please provide an answer before saving.');
            return;
        }

        // Save to local storage
        const answerKey = `${category}-${index}`;
        const savedAnswers = JSON.parse(localStorage.getItem('interviewAnswers') || '{}');
        savedAnswers[answerKey] = {
            answer: answer,
            timestamp: new Date().toISOString(),
            category: category,
            questionIndex: index
        };
        localStorage.setItem('interviewAnswers', JSON.stringify(savedAnswers));

        // Visual feedback
        button.innerHTML = '<i class="fas fa-check me-1"></i>Saved';
        button.classList.remove('btn-success');
        button.classList.add('btn-outline-success');
        
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-save me-1"></i>Save Answer';
            button.classList.remove('btn-outline-success');
            button.classList.add('btn-success');
        }, 2000);

        this.showSuccess('Answer saved successfully!');
    }

    loadSavedAnswers() {
        const savedAnswers = JSON.parse(localStorage.getItem('interviewAnswers') || '{}');
        
        Object.entries(savedAnswers).forEach(([key, data]) => {
            const textarea = document.querySelector(`[data-category="${data.category}"][data-index="${data.questionIndex}"]`)
                ?.closest('.question-card')?.querySelector('.answer-textarea');
            
            if (textarea) {
                textarea.value = data.answer;
                textarea.style.borderColor = '#28a745'; // Green border for saved answers
            }
        });
    }

    togglePracticeMode() {
        this.practiceMode = !this.practiceMode;
        
        if (this.practiceMode) {
            this.enterPracticeMode();
        } else {
            this.exitPracticeMode();
        }
    }

    enterPracticeMode() {
        // Hide all questions except the current one
        const questionCards = document.querySelectorAll('.question-card');
        questionCards.forEach((card, index) => {
            card.style.display = index === this.currentQuestionIndex ? 'block' : 'none';
        });

        // Add practice mode controls
        this.addPracticeControls();
        this.showSuccess('Practice mode enabled. Focus on one question at a time!');
    }

    exitPracticeMode() {
        // Show all questions
        document.querySelectorAll('.question-card').forEach(card => {
            card.style.display = 'block';
        });

        // Remove practice mode controls
        this.removePracticeControls();
        this.showInfo('Practice mode disabled. All questions are now visible.');
    }

    addPracticeControls() {
        const controlsHtml = `
            <div class="practice-controls card mb-4 bg-light">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">Practice Mode</h6>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-primary prev-question-btn">
                                <i class="fas fa-arrow-left me-1"></i>Previous
                            </button>
                            <button class="btn btn-sm btn-outline-primary next-question-btn">
                                <i class="fas fa-arrow-right me-1"></i>Next
                            </button>
                            <button class="btn btn-sm btn-outline-secondary practice-mode-btn">
                                <i class="fas fa-eye me-1"></i>Show All
                            </button>
                        </div>
                    </div>
                    <div class="progress mt-2">
                        <div class="progress-bar practice-progress" style="width: 0%"></div>
                    </div>
                    <small class="text-muted">Question <span class="current-question">1</span> of <span class="total-questions">0</span></small>
                </div>
            </div>
        `;

        const firstQuestionCard = document.querySelector('.question-card');
        if (firstQuestionCard) {
            firstQuestionCard.insertAdjacentHTML('beforebegin', controlsHtml);
            this.updatePracticeProgress();
        }
    }

    removePracticeControls() {
        const controls = document.querySelector('.practice-controls');
        if (controls) {
            controls.remove();
        }
    }

    nextQuestion() {
        const totalQuestions = document.querySelectorAll('.question-card').length;
        if (this.currentQuestionIndex < totalQuestions - 1) {
            this.currentQuestionIndex++;
            this.updateQuestionDisplay();
        }
    }

    prevQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.updateQuestionDisplay();
        }
    }

    updateQuestionDisplay() {
        const questionCards = document.querySelectorAll('.question-card');
        questionCards.forEach((card, index) => {
            card.style.display = index === this.currentQuestionIndex ? 'block' : 'none';
        });
        this.updatePracticeProgress();
    }

    updatePracticeProgress() {
        const totalQuestions = document.querySelectorAll('.question-card').length;
        const progressPercent = ((this.currentQuestionIndex + 1) / totalQuestions) * 100;
        
        const progressBar = document.querySelector('.practice-progress');
        const currentSpan = document.querySelector('.current-question');
        const totalSpan = document.querySelector('.total-questions');
        
        if (progressBar) progressBar.style.width = `${progressPercent}%`;
        if (currentSpan) currentSpan.textContent = this.currentQuestionIndex + 1;
        if (totalSpan) totalSpan.textContent = totalQuestions;
    }

    filterByCategory(category) {
        const allCards = document.querySelectorAll('.question-card');
        allCards.forEach(card => {
            if (category === 'all' || card.dataset.category === category) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        // Update filter button states
        document.querySelectorAll('.category-filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');
    }

    adjustDifficulty(newDifficulty) {
        // In a real implementation, this would regenerate questions with new difficulty
        this.showInfo(`Difficulty adjusted to level ${newDifficulty}. Regenerate questions to see changes.`);
    }

    initializePracticeMode() {
        // Add practice mode toggle button if it doesn't exist
        const existingButton = document.querySelector('.practice-mode-btn');
        if (!existingButton && document.querySelector('.question-card')) {
            const buttonHtml = `
                <div class="text-center mb-4">
                    <button class="btn btn-outline-primary practice-mode-btn">
                        <i class="fas fa-user-graduate me-1"></i>Enable Practice Mode
                    </button>
                </div>
            `;
            const firstCard = document.querySelector('.question-card');
            firstCard.insertAdjacentHTML('beforebegin', buttonHtml);
        }
    }

    addNavigationControls() {
        const controlsHtml = `
            <div class="interview-controls card mb-4 bg-light">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-6">
                            <h6 class="mb-0">Question Controls</h6>
                            <small class="text-muted">Use these controls to enhance your practice session</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <div class="btn-group me-2">
                                <button class="btn btn-sm btn-outline-secondary category-filter-btn active" data-category="all">
                                    All
                                </button>
                                <button class="btn btn-sm btn-outline-primary category-filter-btn" data-category="technical">
                                    Technical
                                </button>
                                <button class="btn btn-sm btn-outline-success category-filter-btn" data-category="behavioral">
                                    Behavioral
                                </button>
                                <button class="btn btn-sm btn-outline-warning category-filter-btn" data-category="situational">
                                    Situational
                                </button>
                                <button class="btn btn-sm btn-outline-info category-filter-btn" data-category="personalized">
                                    Personal
                                </button>
                            </div>
                            <select class="form-select form-select-sm d-inline-block w-auto difficulty-selector">
                                <option value="1">Easy</option>
                                <option value="2" selected>Medium</option>
                                <option value="3">Hard</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const questionsContainer = document.querySelector('.question-card');
        if (questionsContainer) {
            questionsContainer.insertAdjacentHTML('beforebegin', controlsHtml);
        }
    }

    updateMetadata(metadata) {
        // Update question statistics
        const statsHtml = `
            <div class="interview-stats alert alert-info">
                <div class="row text-center">
                    <div class="col-md-3">
                        <h5>${metadata.total_questions}</h5>
                        <small>Total Questions</small>
                    </div>
                    <div class="col-md-3">
                        <h5>${metadata.difficulty}</h5>
                        <small>Difficulty Level</small>
                    </div>
                    <div class="col-md-3">
                        <h5>${metadata.categories.length}</h5>
                        <small>Categories</small>
                    </div>
                    <div class="col-md-3">
                        <h5>~${Math.ceil(metadata.total_questions * 5)}</h5>
                        <small>Minutes (Est.)</small>
                    </div>
                </div>
            </div>
        `;

        const container = document.querySelector('.interview-questions-container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', statsHtml);
        }
    }

    // Utility methods for notifications
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
                    <strong class="me-auto">Interview Practice</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">${message}</div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }

    loadStyles() {
        const styles = `
            <style>
                .question-card {
                    transition: all 0.3s ease;
                }
                .question-card:hover {
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                .recording {
                    animation: pulse 1.5s infinite;
                }
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.5; }
                    100% { opacity: 1; }
                }
                .answer-textarea {
                    transition: border-color 0.3s ease;
                }
                .practice-controls {
                    border-left: 4px solid #007bff;
                }
                .category-filter-btn.active {
                    background-color: var(--bs-primary);
                    color: white;
                }
                .timer-display .alert {
                    margin-bottom: 0;
                }
            </style>
        `;
        
        if (!document.getElementById('interview-questions-styles')) {
            const styleElement = document.createElement('div');
            styleElement.id = 'interview-questions-styles';
            styleElement.innerHTML = styles;
            document.head.appendChild(styleElement);
        }
    }
}

// Initialize the component when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.interview-questions-component')) {
        window.interviewQuestionsComponent = new InterviewQuestionsComponent();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InterviewQuestionsComponent;
}