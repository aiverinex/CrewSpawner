/**
 * Meta-Crew Spawner Frontend JavaScript
 * Handles user interactions and API communication
 */

class MetaCrewSpawner {
    constructor() {
        this.providers = [];
        this.currentTask = '';
        this.isProcessing = false;
        
        this.init();
    }

    init() {
        this.loadProviders();
        this.setupEventListeners();
        this.updateUIState();
    }

    setupEventListeners() {
        // LLM Provider selection
        document.getElementById('llmProvider').addEventListener('change', (e) => {
            this.onProviderChange(e.target.value);
        });

        // Task input
        document.getElementById('taskInput').addEventListener('input', (e) => {
            this.currentTask = e.target.value.trim();
            this.updateUIState();
        });

        // Buttons
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzeTask();
        });

        document.getElementById('processBtn').addEventListener('click', () => {
            this.processTask();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                if (!this.isProcessing && this.currentTask) {
                    this.processTask();
                }
            }
        });
    }

    async loadProviders() {
        try {
            const response = await fetch('/api/providers');
            const data = await response.json();
            
            if (data.success) {
                this.providers = data.providers;
                this.populateProviderSelect();
            } else {
                this.showError('Failed to load providers: ' + data.error);
            }
        } catch (error) {
            this.showError('Failed to load providers: ' + error.message);
        }
    }

    populateProviderSelect() {
        const select = document.getElementById('llmProvider');
        const currentValue = select.value;
        
        // Clear existing options except first
        select.innerHTML = '<option value="">Select Provider...</option>';
        
        this.providers.forEach(provider => {
            const option = document.createElement('option');
            option.value = provider.name;
            option.textContent = this.capitalize(provider.name);
            option.disabled = !provider.available;
            
            if (!provider.available) {
                option.textContent += ' (Not Available)';
            }
            
            select.appendChild(option);
        });
        
        // Restore selection if valid
        if (currentValue && this.providers.find(p => p.name === currentValue && p.available)) {
            select.value = currentValue;
            this.onProviderChange(currentValue);
        }
    }

    onProviderChange(providerName) {
        const modelSelect = document.getElementById('llmModel');
        modelSelect.innerHTML = '<option value="">Select model...</option>';
        
        if (!providerName) {
            modelSelect.disabled = true;
            this.updateUIState();
            return;
        }
        
        const provider = this.providers.find(p => p.name === providerName);
        if (provider && provider.available) {
            modelSelect.disabled = false;
            
            // Add default model option
            const defaultOption = document.createElement('option');
            defaultOption.value = provider.default_model;
            defaultOption.textContent = `${provider.default_model} (Recommended)`;
            defaultOption.selected = true;
            modelSelect.appendChild(defaultOption);
            
            // Add other models
            provider.models.forEach(model => {
                if (model !== provider.default_model) {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    modelSelect.appendChild(option);
                }
            });
        } else {
            modelSelect.disabled = true;
        }
        
        this.updateUIState();
    }

    updateUIState() {
        const hasTask = this.currentTask.length > 0;
        const hasProvider = document.getElementById('llmProvider').value !== '';
        const canExecute = hasTask && hasProvider && !this.isProcessing;
        
        document.getElementById('analyzeBtn').disabled = !canExecute;
        document.getElementById('processBtn').disabled = !canExecute;
        
        // Update button text based on state
        const processBtn = document.getElementById('processBtn');
        if (this.isProcessing) {
            processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        } else {
            processBtn.innerHTML = '<i class="fas fa-play me-2"></i>Generate & Execute Crew';
        }
    }

    async analyzeTask() {
        if (!this.currentTask) return;
        
        try {
            this.showLoading('Analyzing task...');
            
            const response = await fetch('/api/task-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task: this.currentTask
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayAnalysis(data.analysis);
            } else {
                this.showError('Analysis failed: ' + data.error);
            }
        } catch (error) {
            this.showError('Analysis failed: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async processTask() {
        if (!this.currentTask || this.isProcessing) return;
        
        this.isProcessing = true;
        this.updateUIState();
        
        try {
            this.showLoading('Processing task...');
            this.startProgressAnimation();
            
            const response = await fetch('/api/process-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task: this.currentTask,
                    llm_provider: document.getElementById('llmProvider').value,
                    model: document.getElementById('llmModel').value
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data);
            } else {
                this.showError('Processing failed: ' + data.error);
            }
        } catch (error) {
            this.showError('Processing failed: ' + error.message);
        } finally {
            this.isProcessing = false;
            this.updateUIState();
            this.hideLoading();
        }
    }

    displayAnalysis(analysis) {
        const card = document.getElementById('analysisCard');
        const content = document.getElementById('analysisContent');
        
        let html = '';
        
        // Task Type
        if (analysis.task_type) {
            html += this.createAnalysisItem('Task Type', this.capitalize(analysis.task_type));
        }
        
        // Complexity
        if (analysis.complexity) {
            html += this.createAnalysisItem('Complexity', this.capitalize(analysis.complexity));
        }
        
        // Domain
        if (analysis.domain) {
            html += this.createAnalysisItem('Domain', this.capitalize(analysis.domain));
        }
        
        // Estimated Time
        if (analysis.estimated_time) {
            html += this.createAnalysisItem('Estimated Time', analysis.estimated_time);
        }
        
        // Suggested Agents
        if (analysis.suggested_agents && analysis.suggested_agents.length > 0) {
            const agents = analysis.suggested_agents.map(agent => 
                `${this.capitalize(agent.type)} (${agent.priority})`
            ).join(', ');
            html += this.createAnalysisItem('Suggested Agents', agents);
        }
        
        // Requirements
        if (analysis.requirements && analysis.requirements.length > 0) {
            html += this.createAnalysisItem('Requirements', analysis.requirements.join(', '));
        }
        
        content.innerHTML = html;
        card.style.display = 'block';
        card.classList.add('fade-in');
    }

    createAnalysisItem(label, value) {
        return `
            <div class="analysis-item">
                <div class="analysis-label">${label}</div>
                <div class="analysis-value">${value}</div>
            </div>
        `;
    }

    displayResults(data) {
        const card = document.getElementById('resultsCard');
        const resultContent = document.getElementById('resultContent');
        const executionTime = document.getElementById('executionTime');
        
        // Display execution time
        if (data.execution_time) {
            executionTime.textContent = `Completed in ${data.execution_time.toFixed(1)}s`;
        }
        
        // Display agents
        if (data.agents_created && data.agents_created.length > 0) {
            this.displayAgents(data.agents_created);
        }
        
        // Display result
        resultContent.textContent = data.result;
        
        // Show results card
        card.style.display = 'block';
        card.classList.add('fade-in');
        
        // Scroll to results
        card.scrollIntoView({ behavior: 'smooth' });
    }

    displayAgents(agents) {
        const section = document.getElementById('agentsSection');
        const content = document.getElementById('agentsContent');
        
        let html = '';
        
        agents.forEach((agent, index) => {
            html += `
                <div class="col-md-6 mb-3">
                    <div class="agent-card">
                        <div class="agent-role">
                            <i class="fas fa-user-tie me-2"></i>
                            ${agent.role}
                        </div>
                        <div class="agent-goal">
                            <strong>Goal:</strong> ${agent.goal}
                        </div>
                        <div class="agent-backstory">
                            <strong>Background:</strong> ${agent.backstory}
                        </div>
                    </div>
                </div>
            `;
        });
        
        content.innerHTML = html;
        section.style.display = 'block';
    }

    showLoading(message = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const messageEl = overlay.querySelector('h5');
        
        if (messageEl) {
            messageEl.textContent = message;
        }
        
        overlay.style.display = 'block';
        overlay.classList.add('fade-in');
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = 'none';
        overlay.classList.remove('fade-in');
    }

    startProgressAnimation() {
        const progressBar = document.getElementById('progressBar');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            progressBar.style.width = progress + '%';
            
            if (!this.isProcessing) {
                clearInterval(interval);
                progressBar.style.width = '100%';
                setTimeout(() => {
                    progressBar.style.width = '0%';
                }, 500);
            }
        }, 500);
    }

    showError(message) {
        // Create and show error alert
        const alertHtml = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Insert at top of main container
        const container = document.querySelector('.col-lg-8');
        container.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, ' ');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.metaCrewSpawner = new MetaCrewSpawner();
});
