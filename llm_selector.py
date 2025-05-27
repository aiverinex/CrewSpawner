"""
LLM Selector - Multi-provider LLM management
Handles configuration and initialization of different LLM providers
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7

class LLMSelector:
    """Manages multiple LLM providers and configurations"""
    
    def __init__(self):
        self.providers = {
            'openai': {
                'models': ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'],
                'api_key_env': 'OPENAI_API_KEY',
                'default_model': 'gpt-4o'  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            },
            'anthropic': {
                'models': ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307', 'claude-3-opus-20240229'],
                'api_key_env': 'ANTHROPIC_API_KEY',
                'default_model': 'claude-3-5-sonnet-20241022'  # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
            },
            'groq': {
                'models': ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768'],
                'api_key_env': 'GROQ_API_KEY',
                'default_model': 'llama-3.1-70b-versatile'
            },
            'mistral': {
                'models': ['mistral-large-latest', 'mistral-medium-latest', 'mistral-small-latest'],
                'api_key_env': 'MISTRAL_API_KEY',
                'default_model': 'mistral-large-latest'
            }
        }
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available providers with their models"""
        available = []
        
        for provider, config in self.providers.items():
            api_key = os.getenv(config['api_key_env'])
            if api_key:
                available.append({
                    'name': provider,
                    'models': config['models'],
                    'default_model': config['default_model'],
                    'available': True
                })
            else:
                available.append({
                    'name': provider,
                    'models': config['models'],
                    'default_model': config['default_model'],
                    'available': False,
                    'error': f'Missing {config["api_key_env"]} environment variable'
                })
        
        return available
    
    def get_llm_config(self, provider: str, model: str = None) -> LLMConfig:
        """Get LLM configuration for specified provider and model"""
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        config = self.providers[provider]
        api_key = os.getenv(config['api_key_env'])
        
        if not api_key:
            raise ValueError(f"Missing API key for {provider}. Set {config['api_key_env']} environment variable.")
        
        if not model:
            model = config['default_model']
        
        if model not in config['models']:
            raise ValueError(f"Unsupported model {model} for provider {provider}")
        
        return LLMConfig(
            provider=provider,
            model=model,
            api_key=api_key
        )
    
    def create_llm_instance(self, provider: str, model: str = None, **kwargs):
        """Create LLM instance for CrewAI"""
        config = self.get_llm_config(provider, model)
        
        # Set default parameters
        llm_kwargs = {
            'model': config.model,
            'temperature': kwargs.get('temperature', config.temperature),
            'max_tokens': kwargs.get('max_tokens', config.max_tokens)
        }
        
        if provider == 'openai':
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=config.api_key,
                **llm_kwargs
            )
        
        elif provider == 'anthropic':
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                api_key=config.api_key,
                **llm_kwargs
            )
        
        elif provider == 'groq':
            from langchain_groq import ChatGroq
            return ChatGroq(
                api_key=config.api_key,
                **llm_kwargs
            )
        
        elif provider == 'mistral':
            from langchain_mistralai import ChatMistralAI
            return ChatMistralAI(
                api_key=config.api_key,
                **llm_kwargs
            )
        
        else:
            raise ValueError(f"LLM instance creation not implemented for provider: {provider}")
    
    def validate_provider(self, provider: str) -> bool:
        """Validate if provider is available and configured"""
        if provider not in self.providers:
            return False
        
        api_key = os.getenv(self.providers[provider]['api_key_env'])
        return bool(api_key)
    
    def get_default_provider(self) -> str:
        """Get the first available provider as default"""
        for provider in ['openai', 'anthropic', 'groq', 'mistral']:
            if self.validate_provider(provider):
                return provider
        
        raise ValueError("No LLM providers are configured. Please set at least one API key.")
