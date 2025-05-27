"""
Crew Generator - Dynamic CrewAI crew creation
Analyzes tasks and generates appropriate multi-agent teams
"""

import time
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, Process
from langchain.tools import BaseTool

from llm_selector import LLMSelector
from task_parser import TaskParser
from config.agent_templates import AgentTemplateManager
from config.task_templates import TaskTemplateManager

class MetaCrewSpawner:
    """Main class for dynamic crew generation and execution"""
    
    def __init__(self):
        self.llm_selector = LLMSelector()
        self.task_parser = TaskParser()
        self.agent_templates = AgentTemplateManager()
        self.task_templates = TaskTemplateManager()
        
        # Current configuration
        self.current_llm_provider = None
        self.current_model = None
        self.current_llm = None
        
        # Execution tracking
        self.last_agents = []
        self.last_execution_time = 0
        
        # Initialize with default LLM
        try:
            default_provider = self.llm_selector.get_default_provider()
            self.configure_llm(default_provider)
        except ValueError as e:
            print(f"Warning: {e}")
    
    def configure_llm(self, provider: str, model: str = None):
        """Configure the LLM provider and model"""
        self.current_llm_provider = provider
        self.current_model = model
        self.current_llm = self.llm_selector.create_llm_instance(provider, model)
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze task and suggest agent configuration"""
        if not self.current_llm:
            raise ValueError("No LLM configured. Please configure an LLM provider first.")
        
        # Parse task using task parser
        analysis = self.task_parser.parse_task(task_description, self.current_llm)
        
        # Get suggested agents based on analysis
        suggested_agents = self.agent_templates.suggest_agents(analysis)
        
        return {
            'task_type': analysis.get('task_type'),
            'complexity': analysis.get('complexity'),
            'domain': analysis.get('domain'),
            'suggested_agents': suggested_agents,
            'estimated_time': analysis.get('estimated_time'),
            'requirements': analysis.get('requirements', [])
        }
    
    def generate_crew(self, task_description: str, analysis: Dict[str, Any] = None) -> Crew:
        """Generate a crew based on task analysis"""
        if not self.current_llm:
            raise ValueError("No LLM configured. Please configure an LLM provider first.")
        
        if not analysis:
            analysis = self.analyze_task(task_description)
        
        # Generate agents
        agents = self._create_agents(analysis)
        
        # Generate tasks
        tasks = self._create_tasks(task_description, agents, analysis)
        
        # Create crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Store agent info for tracking
        self.last_agents = [
            {
                'role': agent.role,
                'goal': agent.goal,
                'backstory': agent.backstory[:100] + '...' if len(agent.backstory) > 100 else agent.backstory
            }
            for agent in agents
        ]
        
        return crew
    
    def _create_agents(self, analysis: Dict[str, Any]) -> List[Agent]:
        """Create agents based on analysis"""
        agents = []
        suggested_agents = analysis.get('suggested_agents', [])
        
        for agent_config in suggested_agents:
            template = self.agent_templates.get_template(agent_config['type'])
            
            agent = Agent(
                role=template['role'],
                goal=template['goal'],
                backstory=template['backstory'],
                llm=self.current_llm,
                verbose=True,
                allow_delegation=template.get('allow_delegation', False),
                tools=self._get_agent_tools(agent_config['type'])
            )
            agents.append(agent)
        
        return agents
    
    def _create_tasks(self, task_description: str, agents: List[Agent], analysis: Dict[str, Any]) -> List[Task]:
        """Create tasks for the crew"""
        tasks = []
        task_type = analysis.get('task_type', 'general')
        
        # Get task template
        task_template = self.task_templates.get_template(task_type)
        
        # Create tasks based on template and agents
        for i, agent in enumerate(agents):
            if i < len(task_template['subtasks']):
                subtask = task_template['subtasks'][i]
                
                task = Task(
                    description=f"{subtask['description']}\n\nOriginal request: {task_description}",
                    expected_output=subtask['expected_output'],
                    agent=agent
                )
                tasks.append(task)
            else:
                # Fallback task for additional agents
                task = Task(
                    description=f"Support the team in completing: {task_description}",
                    expected_output="A comprehensive contribution to the overall objective",
                    agent=agent
                )
                tasks.append(task)
        
        return tasks
    
    def _get_agent_tools(self, agent_type: str) -> List[BaseTool]:
        """Get tools for specific agent types"""
        # Basic implementation - can be extended with custom tools
        tools = []
        
        # Add tools based on agent type
        if agent_type == 'researcher':
            # Add research tools if available
            pass
        elif agent_type == 'writer':
            # Add writing tools if available
            pass
        elif agent_type == 'analyst':
            # Add analysis tools if available
            pass
        
        return tools
    
    def process_task(self, task_description: str) -> str:
        """Complete process: analyze, generate crew, and execute"""
        start_time = time.time()
        
        try:
            # Analyze task
            analysis = self.analyze_task(task_description)
            
            # Generate crew
            crew = self.generate_crew(task_description, analysis)
            
            # Execute crew
            result = crew.kickoff()
            
            self.last_execution_time = time.time() - start_time
            
            return str(result)
            
        except Exception as e:
            self.last_execution_time = time.time() - start_time
            raise Exception(f"Error processing task: {str(e)}")
    
    def get_last_agents_info(self) -> List[Dict[str, str]]:
        """Get information about the last generated agents"""
        return self.last_agents
    
    def get_last_execution_time(self) -> float:
        """Get the execution time of the last task"""
        return self.last_execution_time
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get available LLM providers"""
        return self.llm_selector.get_available_providers()
