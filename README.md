# Meta-Crew Spawner

A dynamic AI crew generator using the CrewAI framework that accepts natural language tasks and spawns appropriate multi-agent teams with configurable LLM backends.

## 🚀 Features

- **Natural Language Task Input**: Describe your task in plain English
- **Dynamic Agent Generation**: Automatically creates appropriate AI agents based on task requirements
- **Multi-LLM Support**: Choose from OpenAI, Anthropic, Groq, or Mistral APIs
- **Intelligent Task Analysis**: Analyzes task complexity, domain, and requirements
- **Real-time Execution**: Watch your AI crew work together to complete objectives
- **Web Interface**: User-friendly web application for easy interaction
- **Enterprise Ready**: Built for professional workflows and scalable deployments

## 🏗️ Architecture

The Meta-Crew Spawner uses a modular architecture:

- **Task Parser**: Analyzes natural language input to determine task type, complexity, and requirements
- **LLM Selector**: Manages multiple LLM providers and configurations
- **Crew Generator**: Dynamically creates CrewAI crews with appropriate agents and tasks
- **Agent Templates**: Pre-configured agent roles (Researcher, Writer, Analyst, etc.)
- **Task Templates**: Structured workflows for different task types

## 📋 Prerequisites

- Python 3.10 or higher
- API keys for at least one supported LLM provider:
  - OpenAI API key
  - Anthropic API key
  - Groq API key
  - Mistral API key

## 🛠️ Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install crewai python-dotenv flask langchain-openai langchain-anthropic langchain-groq langchain-mistralai pydantic
