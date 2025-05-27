"""
Task Parser - Natural language task analysis
Analyzes user input to determine appropriate crew configuration
"""

import json
import re
from typing import Dict, Any, List
from langchain.schema import HumanMessage, SystemMessage

class TaskParser:
    """Parses natural language tasks and extracts structured information"""
    
    def __init__(self):
        self.task_types = {
            'research': ['research', 'investigate', 'study', 'analyze', 'explore', 'examine'],
            'content_creation': ['write', 'create', 'generate', 'produce', 'draft', 'compose'],
            'analysis': ['analyze', 'evaluate', 'assess', 'review', 'compare', 'examine'],
            'planning': ['plan', 'strategy', 'organize', 'design', 'outline', 'schedule'],
            'problem_solving': ['solve', 'fix', 'resolve', 'troubleshoot', 'debug', 'optimize'],
            'creative': ['design', 'creative', 'brainstorm', 'innovate', 'imagine', 'conceptualize']
        }
        
        self.complexity_indicators = {
            'simple': ['simple', 'basic', 'quick', 'brief', 'short'],
            'medium': ['detailed', 'comprehensive', 'thorough', 'complete'],
            'complex': ['complex', 'advanced', 'in-depth', 'extensive', 'sophisticated']
        }
        
        self.domain_keywords = {
            'technology': ['tech', 'software', 'programming', 'AI', 'machine learning', 'data'],
            'business': ['business', 'marketing', 'sales', 'finance', 'strategy', 'management'],
            'science': ['science', 'research', 'study', 'experiment', 'hypothesis'],
            'creative': ['creative', 'design', 'art', 'content', 'writing', 'storytelling'],
            'education': ['education', 'learning', 'teaching', 'curriculum', 'training'],
            'health': ['health', 'medical', 'wellness', 'fitness', 'healthcare']
        }
    
    def parse_task(self, task_description: str, llm) -> Dict[str, Any]:
        """Parse task description and extract structured information"""
        # Basic rule-based analysis
        basic_analysis = self._basic_analysis(task_description)
        
        # Enhanced analysis using LLM
        enhanced_analysis = self._llm_analysis(task_description, llm)
        
        # Combine both analyses
        return {**basic_analysis, **enhanced_analysis}
    
    def _basic_analysis(self, task_description: str) -> Dict[str, Any]:
        """Perform basic rule-based task analysis"""
        task_lower = task_description.lower()
        
        # Determine task type
        task_type = 'general'
        for t_type, keywords in self.task_types.items():
            if any(keyword in task_lower for keyword in keywords):
                task_type = t_type
                break
        
        # Determine complexity
        complexity = 'medium'  # default
        for comp_level, indicators in self.complexity_indicators.items():
            if any(indicator in task_lower for indicator in indicators):
                complexity = comp_level
                break
        
        # Determine domain
        domain = 'general'
        for dom, keywords in self.domain_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                domain = dom
                break
        
        # Estimate time based on complexity and length
        word_count = len(task_description.split())
        if complexity == 'simple' or word_count < 20:
            estimated_time = '5-15 minutes'
        elif complexity == 'complex' or word_count > 50:
            estimated_time = '30-60 minutes'
        else:
            estimated_time = '15-30 minutes'
        
        return {
            'task_type': task_type,
            'complexity': complexity,
            'domain': domain,
            'estimated_time': estimated_time,
            'word_count': word_count
        }
    
    def _llm_analysis(self, task_description: str, llm) -> Dict[str, Any]:
        """Use LLM for enhanced task analysis"""
        try:
            system_prompt = """You are an expert task analyzer for AI crew generation. 
            Analyze the given task and provide a JSON response with the following structure:
            {
                "specific_requirements": ["list", "of", "specific", "requirements"],
                "key_skills_needed": ["skill1", "skill2", "skill3"],
                "deliverables": ["what", "should", "be", "delivered"],
                "challenges": ["potential", "challenges"],
                "success_criteria": ["how", "to", "measure", "success"]
            }
            
            Focus on practical aspects that would help determine what types of AI agents would be most effective."""
            
            user_prompt = f"Analyze this task: {task_description}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = llm.invoke(messages)
            
            # Try to parse JSON from response
            try:
                # Extract JSON from response content
                content = response.content
                # Find JSON in the response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return analysis
                else:
                    # Fallback if no JSON found
                    return {'llm_analysis': content}
            except json.JSONDecodeError:
                return {'llm_analysis': response.content}
                
        except Exception as e:
            print(f"Warning: LLM analysis failed: {e}")
            return {'llm_analysis_error': str(e)}
    
    def extract_requirements(self, task_description: str) -> List[str]:
        """Extract specific requirements from task description"""
        requirements = []
        
        # Look for explicit requirements
        requirement_patterns = [
            r'must\s+(\w+(?:\s+\w+)*)',
            r'should\s+(\w+(?:\s+\w+)*)',
            r'need(?:s)?\s+to\s+(\w+(?:\s+\w+)*)',
            r'require(?:s)?\s+(\w+(?:\s+\w+)*)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, task_description.lower())
            requirements.extend(matches)
        
        return requirements
    
    def get_suggested_agent_count(self, task_type: str, complexity: str) -> int:
        """Suggest number of agents based on task type and complexity"""
        base_counts = {
            'research': 2,
            'content_creation': 2,
            'analysis': 2,
            'planning': 3,
            'problem_solving': 2,
            'creative': 2,
            'general': 2
        }
        
        base_count = base_counts.get(task_type, 2)
        
        # Adjust based on complexity
        if complexity == 'simple':
            return max(1, base_count - 1)
        elif complexity == 'complex':
            return min(5, base_count + 1)
        else:
            return base_count
