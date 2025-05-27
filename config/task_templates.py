"""
Task Templates - Pre-configured task definitions
Provides templates for different types of tasks and workflows
"""

from typing import Dict, List, Any

class TaskTemplateManager:
    """Manages task templates for different use cases"""
    
    def __init__(self):
        self.templates = {
            'research': {
                'name': 'Research Task',
                'description': 'Comprehensive research and analysis workflow',
                'subtasks': [
                    {
                        'description': 'Conduct comprehensive research on the given topic. Gather information from multiple reliable sources, verify facts, and compile findings.',
                        'expected_output': 'A detailed research report with sources, key findings, and relevant data points'
                    },
                    {
                        'description': 'Analyze the research findings, identify patterns, trends, and key insights. Provide strategic recommendations based on the data.',
                        'expected_output': 'An analytical summary with key insights, trends, and actionable recommendations'
                    }
                ]
            },
            
            'content_creation': {
                'name': 'Content Creation Task',
                'description': 'Content development and creation workflow',
                'subtasks': [
                    {
                        'description': 'Research the topic and gather relevant information, examples, and supporting data for content creation.',
                        'expected_output': 'Research brief with key information, target audience insights, and content requirements'
                    },
                    {
                        'description': 'Create engaging, well-structured content based on the research. Ensure the content meets the specified requirements and resonates with the target audience.',
                        'expected_output': 'High-quality content that meets all requirements and is ready for publication or use'
                    }
                ]
            },
            
            'analysis': {
                'name': 'Analysis Task',
                'description': 'Comprehensive analysis and evaluation workflow',
                'subtasks': [
                    {
                        'description': 'Gather and organize all relevant data, information, and materials needed for the analysis.',
                        'expected_output': 'Organized dataset and information summary ready for analysis'
                    },
                    {
                        'description': 'Conduct thorough analysis, identify patterns, evaluate options, and provide evidence-based conclusions and recommendations.',
                        'expected_output': 'Comprehensive analysis report with findings, conclusions, and actionable recommendations'
                    }
                ]
            },
            
            'planning': {
                'name': 'Strategic Planning Task',
                'description': 'Strategic planning and project organization workflow',
                'subtasks': [
                    {
                        'description': 'Analyze requirements, constraints, and objectives. Identify key stakeholders, resources, and success criteria.',
                        'expected_output': 'Requirements analysis with clear objectives, constraints, and success criteria'
                    },
                    {
                        'description': 'Develop a comprehensive strategic plan with timeline, milestones, resource allocation, and risk mitigation strategies.',
                        'expected_output': 'Detailed strategic plan with timeline, milestones, resource requirements, and implementation roadmap'
                    },
                    {
                        'description': 'Coordinate plan implementation, monitor progress, and ensure all elements work together effectively.',
                        'expected_output': 'Implementation framework with monitoring protocols and coordination guidelines'
                    }
                ]
            },
            
            'problem_solving': {
                'name': 'Problem Solving Task',
                'description': 'Problem identification and solution development workflow',
                'subtasks': [
                    {
                        'description': 'Analyze the problem, identify root causes, understand constraints, and define success criteria for solutions.',
                        'expected_output': 'Problem analysis with root cause identification and solution requirements'
                    },
                    {
                        'description': 'Develop and evaluate multiple solution options. Select the best approach and create an implementation plan.',
                        'expected_output': 'Solution recommendation with implementation plan, timeline, and expected outcomes'
                    }
                ]
            },
            
            'creative': {
                'name': 'Creative Task',
                'description': 'Creative ideation and development workflow',
                'subtasks': [
                    {
                        'description': 'Research inspiration, analyze requirements, and explore creative possibilities. Generate multiple creative concepts and ideas.',
                        'expected_output': 'Creative brief with multiple concepts, inspiration sources, and initial ideas'
                    },
                    {
                        'description': 'Develop and refine the best creative concepts. Create detailed proposals with visual or written descriptions of the creative solution.',
                        'expected_output': 'Refined creative solution with detailed descriptions, rationale, and implementation guidance'
                    }
                ]
            },
            
            'general': {
                'name': 'General Task',
                'description': 'Flexible workflow for various task types',
                'subtasks': [
                    {
                        'description': 'Analyze the task requirements, gather necessary information, and plan the approach for completion.',
                        'expected_output': 'Task analysis with clear understanding of requirements and planned approach'
                    },
                    {
                        'description': 'Execute the planned approach, complete the task objectives, and deliver the required outcomes.',
                        'expected_output': 'Completed task deliverables that meet all specified requirements'
                    }
                ]
            }
        }
    
    def get_template(self, task_type: str) -> Dict[str, Any]:
        """Get task template by type"""
        if task_type not in self.templates:
            task_type = 'general'  # fallback to general template
        return self.templates[task_type].copy()
    
    def get_available_types(self) -> List[str]:
        """Get list of available task types"""
        return list(self.templates.keys())
    
    def customize_template(self, task_type: str, specific_requirements: List[str]) -> Dict[str, Any]:
        """Customize template based on specific requirements"""
        template = self.get_template(task_type)
        
        # Add requirement-specific modifications
        for requirement in specific_requirements:
            if 'urgent' in requirement.lower():
                template['priority'] = 'high'
            elif 'detailed' in requirement.lower():
                # Add more detailed expectations
                for subtask in template['subtasks']:
                    subtask['expected_output'] += '. Provide detailed explanations and comprehensive coverage.'
        
        return template
    
    def validate_template(self, task_type: str) -> bool:
        """Validate if template exists and is properly configured"""
        if task_type not in self.templates:
            return False
        
        template = self.templates[task_type]
        
        # Check required fields
        required_fields = ['name', 'description', 'subtasks']
        for field in required_fields:
            if field not in template:
                return False
        
        # Check subtasks structure
        for subtask in template['subtasks']:
            if 'description' not in subtask or 'expected_output' not in subtask:
                return False
        
        return True
