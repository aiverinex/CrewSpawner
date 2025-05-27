"""
Meta-Crew Spawner - Web Interface
Flask web application for dynamic AI crew generation
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from crew_generator import MetaCrewSpawner
from llm_selector import LLMSelector

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'meta-crew-spawner-secret-key-change-in-production')

# Initialize components
spawner = MetaCrewSpawner()
llm_selector = LLMSelector()

@app.route('/')
def index():
    """Main page with task input interface"""
    available_providers = llm_selector.get_available_providers()
    return render_template('index.html', providers=available_providers)

@app.route('/api/providers')
def get_providers():
    """Get available LLM providers"""
    try:
        providers = llm_selector.get_available_providers()
        return jsonify({'success': True, 'providers': providers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process-task', methods=['POST'])
def process_task():
    """Process a natural language task and generate crew"""
    try:
        data = request.get_json()
        task = data.get('task', '').strip()
        llm_provider = data.get('llm_provider', 'openai')
        model = data.get('model', '')
        
        if not task:
            return jsonify({'success': False, 'error': 'Task description is required'}), 400
        
        # Set LLM configuration for this session
        session['llm_provider'] = llm_provider
        session['model'] = model
        
        # Configure spawner with selected LLM
        spawner.configure_llm(llm_provider, model)
        
        # Process the task
        result = spawner.process_task(task)
        
        return jsonify({
            'success': True,
            'result': result,
            'agents_created': spawner.get_last_agents_info(),
            'execution_time': spawner.get_last_execution_time()
        })
        
    except Exception as e:
        app.logger.error(f"Error processing task: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/task-analysis', methods=['POST'])
def analyze_task():
    """Analyze task and suggest agent configuration"""
    try:
        data = request.get_json()
        task = data.get('task', '').strip()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task description is required'}), 400
        
        analysis = spawner.analyze_task(task)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
