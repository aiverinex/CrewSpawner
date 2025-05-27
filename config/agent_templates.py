"""
Agent Templates - Pre-configured agent definitions
Provides templates for different types of AI agents
"""

from typing import Dict, List, Any

class AgentTemplateManager:
    """Manages agent templates for different use cases"""
    
    def __init__(self):
        self.templates = {
            'researcher': {
                'role': 'Senior Research Analyst',
                'goal': 'Conduct thorough research and gather comprehensive information on the given topic',
                'backstory': 'You are an experienced researcher with expertise in information gathering, data analysis, and source verification. You excel at finding relevant, accurate, and up-to-date information from multiple sources.',
                'allow_delegation': False,
                'skills': ['research', 'analysis', 'fact-checking'],
                'best_for': ['research', 'investigation', 'data gathering']
            },
            
            'writer': {
                'role': 'Expert Content Writer',
                'goal': 'Create clear, engaging, and well-structured written content based on provided information',
                'backstory': 'You are a skilled writer with expertise in various content formats. You excel at transforming complex information into clear, engaging content that resonates with the target audience.',
                'allow_delegation': False,
                'skills': ['writing', 'editing', 'content creation'],
                'best_for': ['content_creation', 'writing', 'documentation']
            },
            
            'analyst': {
                'role': 'Strategic Data Analyst',
                'goal': 'Analyze information, identify patterns, and provide actionable insights',
                'backstory': 'You are an analytical expert who excels at processing complex information, identifying trends, and providing strategic recommendations based on data-driven insights.',
                'allow_delegation': False,
                'skills': ['analysis', 'pattern recognition', 'strategic thinking'],
                'best_for': ['analysis', 'evaluation', 'decision making']
            },
            
            'strategist': {
                'role': 'Strategic Planning Expert',
                'goal': 'Develop comprehensive strategies and actionable plans',
                'backstory': 'You are a strategic planning professional with extensive experience in developing and implementing successful strategies across various domains.',
                'allow_delegation': True,
                'skills': ['strategic planning', 'project management', 'leadership'],
                'best_for': ['planning', 'strategy', 'project management']
            },
            
            'creative': {
                'role': 'Creative Innovation Specialist',
                'goal': 'Generate creative solutions and innovative ideas',
                'backstory': 'You are a creative professional who excels at thinking outside the box, generating innovative ideas, and finding unique solutions to complex challenges.',
                'allow_delegation': False,
                'skills': ['creativity', 'innovation', 'brainstorming'],
                'best_for': ['creative', 'innovation', 'brainstorming']
            },
            
            'problem_solver': {
                'role': 'Solution Architect',
                'goal': 'Identify problems and develop practical, implementable solutions',
                'backstory': 'You are a problem-solving expert who excels at breaking down complex challenges, identifying root causes, and developing practical solutions.',
                'allow_delegation': False,
                'skills': ['problem solving', 'critical thinking', 'solution design'],
                'best_for': ['problem_solving', 'troubleshooting', 'optimization']
            },
            
            'coordinator': {
                'role': 'Project Coordinator',
                'goal': 'Coordinate team efforts and ensure project objectives are met',
                'backstory': 'You are an experienced project coordinator who excels at managing workflows, facilitating communication, and ensuring all team members work effectively toward common goals.',
                'allow_delegation': True,
                'skills': ['coordination', 'communication', 'project management'],
                'best_for': ['coordination', 'management', 'oversight']
            },
            
            'quality_assurance': {
                'role': 'Quality Assurance Specialist',
                'goal': 'Review and validate work quality, ensuring high standards are met',
                'backstory': 'You are a quality assurance expert who meticulously reviews work products, identifies areas for improvement, and ensures deliverables meet the highest standards.',
                'allow_delegation': False,
                'skills': ['quality control', 'review', 'validation'],
                'best_for': ['review', 'validation', 'quality control']
            }
        }
        
        self.task_to_agents = {
            'research': ['researcher', 'analyst'],
            'content_creation': ['writer', 'creative'],
            'analysis': ['analyst', 'researcher'],
            'planning': ['strategist', 'coordinator'],
            'problem_solving': ['problem_solver', 'analyst'],
            'creative': ['creative', 'writer'],
            'general': ['researcher', 'analyst']
        }
    
    def get_template(self, agent_type: str) -> Dict[str, Any]:
        """Get agent template by type"""
        if agent_type not in self.templates:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return self.templates[agent_type].copy()
    
    def suggest_agents(self, task_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest agents based on task analysis"""
        task_type = task_analysis.get('task_type', 'general')
        complexity = task_analysis.get('complexity', 'medium')
        domain = task_analysis.get('domain', 'general')
        
        # Get base agents for task type
        base_agents = self.task_to_agents.get(task_type, ['researcher', 'analyst'])
        
        suggested = []
        
        # Add base agents
        for agent_type in base_agents:
            suggested.append({
                'type': agent_type,
                'priority': 'high',
                'reason': f'Essential for {task_type} tasks'
            })
        
        # Add domain-specific agents
        if domain == 'creative' and 'creative' not in [a['type'] for a in suggested]:
            suggested.append({
                'type': 'creative',
                'priority': 'medium',
                'reason': 'Specialized for creative domain'
            })
        
        # Add complexity-based agents
        if complexity == 'complex':
            if 'coordinator' not in [a['type'] for a in suggested]:
                suggested.append({
                    'type': 'coordinator',
                    'priority': 'medium',
                    'reason': 'Needed for complex task coordination'
                })
            
            if 'quality_assurance' not in [a['type'] for a in suggested]:
                suggested.append({
                    'type': 'quality_assurance',
                    'priority': 'low',
                    'reason': 'Quality validation for complex deliverables'
                })
        
        # Limit number of agents (max 4 for performance)
        max_agents = 4 if complexity == 'complex' else 3
        
        # Sort by priority and take top agents
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        suggested.sort(key=lambda x: priority_order[x['priority']], reverse=True)
        
        return suggested[:max_agents]
    
    def get_available_types(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.templates.keys())
    
    def validate_agent_combination(self, agent_types: List[str]) -> Dict[str, Any]:
        """Validate if agent combination makes sense"""
        if not agent_types:
            return {'valid': False, 'reason': 'No agents specified'}
        
        if len(agent_types) > 5:
            return {'valid': False, 'reason': 'Too many agents (max 5)'}
        
        # Check for essential combinations
        if len(agent_types) > 1:
            # For multi-agent crews, ensure we have complementary skills
            skills = set()
            for agent_type in agent_types:
                if agent_type in self.templates:
                    skills.update(self.templates[agent_type]['skills'])
            
            if len(skills) < 2:
                return {
                    'valid': True, 
                    'warning': 'Agents have overlapping skills - consider diversifying'
                }
        
        return {'valid': True, 'reason': 'Valid agent combination'}
