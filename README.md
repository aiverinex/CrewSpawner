# Meta-Crew Spawner

Transform any natural language task into a powerful multi-agent AI crew. The Meta-Crew Spawner automatically analyzes your requirements and dynamically generates specialized CrewAI teams with the perfect combination of agents to tackle complex challenges across research, content creation, analysis, planning, and problem-solving domains.

## What This Crew Does

The Meta-Crew Spawner solves the challenge of manually configuring AI agent teams by intelligently analyzing task requirements and automatically assembling the optimal crew configuration. Simply describe what you want to accomplish in natural language, and watch as specialized AI agents collaborate to deliver comprehensive results.

### Key Capabilities

- **Intelligent Task Analysis**: Automatically determines task type, complexity, domain, and specific requirements
- **Dynamic Agent Generation**: Creates specialized agents (Researchers, Writers, Analysts, Strategists, etc.) based on your needs
- **Multi-LLM Flexibility**: Choose from OpenAI, Anthropic, Groq, or Mistral models to power your agents
- **Adaptive Workflows**: Generates appropriate task sequences and agent interactions for optimal results
- **Enterprise-Grade Execution**: Handles complex, multi-step processes with real-time monitoring

## Example Use Cases

### Business Strategy
**Input**: "Analyze the competitive landscape for sustainable packaging solutions and create a market entry strategy"
**Generated Crew**: Research Analyst + Strategic Planner + Market Analyst
**Output**: Comprehensive market analysis with actionable entry strategy

### Content Creation
**Input**: "Research emerging AI trends and write a technical whitepaper for enterprise decision-makers"
**Generated Crew**: Senior Researcher + Expert Writer + Quality Assurance Specialist
**Output**: Professional whitepaper with research citations and executive summary

### Problem Solving
**Input**: "Identify bottlenecks in our customer onboarding process and propose optimization solutions"
**Generated Crew**: Process Analyst + Solution Architect + Implementation Coordinator
**Output**: Detailed analysis with prioritized improvement recommendations

### Creative Innovation
**Input**: "Brainstorm innovative product features for a fitness app targeting remote workers"
**Generated Crew**: Creative Specialist + Market Researcher + UX Strategist
**Output**: Feature concepts with market validation and implementation roadmap

## Dependencies

### Required Python Packages
- `crewai` - Core multi-agent framework
- `langchain-openai` - OpenAI model integration
- `langchain-anthropic` - Anthropic Claude integration  
- `langchain-groq` - Groq model integration
- `langchain-mistralai` - Mistral model integration
- `flask` - Web interface framework
- `python-dotenv` - Environment configuration
- `pydantic` - Data validation

### External Services
- **OpenAI API** (recommended) - Access to GPT-4 and other models
- **Anthropic API** (optional) - Claude model access
- **Groq API** (optional) - Fast inference models
- **Mistral AI API** (optional) - European AI models

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system.

```bash
pip install crewai python-dotenv flask langchain-openai langchain-anthropic langchain-groq langchain-mistralai pydantic
```

## Configuration Instructions

### 1. Environment Setup

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here

# Application settings
SECRET_KEY=your_secure_secret_key
DEBUG=False
PORT=5000
```

### 2. API Key Setup

#### OpenAI (Recommended)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Add to `.env` as `OPENAI_API_KEY`

#### Anthropic (Optional)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Generate API key in account settings
4. Add to `.env` as `ANTHROPIC_API_KEY`

#### Groq (Optional)
1. Visit [Groq Console](https://console.groq.com/)
2. Create account and verify email
3. Generate API key
4. Add to `.env` as `GROQ_API_KEY`

#### Mistral AI (Optional)
1. Visit [Mistral AI Platform](https://console.mistral.ai/)
2. Register and verify account
3. Create API key
4. Add to `.env` as `MISTRAL_API_KEY`

## Usage Examples

### Web Interface

Start the web application:

```bash
python app.py
```

Visit `http://localhost:5000` and:

1. **Select LLM Provider**: Choose from available configured providers
2. **Enter Task Description**: Describe your objective in natural language
3. **Analyze Task** (optional): Preview suggested agent configuration
4. **Generate & Execute Crew**: Watch your AI team work

### Command Line Interface

Run tasks directly from command line:

```bash
# Interactive mode
python main.py

# Direct task execution
python main.py "Create a comprehensive market analysis for electric vehicles in Europe"
```

### Sample Task Inputs

**Research & Analysis**
```
"Research the latest developments in quantum computing and analyze their potential impact on cybersecurity"
```

**Strategic Planning**
```
"Develop a 12-month digital transformation roadmap for a mid-size manufacturing company"
```

**Content Creation**
```
"Write a comprehensive technical documentation for an API integration, including code examples and troubleshooting guide"
```

**Problem Solving**
```
"Analyze our customer churn data and recommend retention strategies with implementation timelines"
```

**Creative Innovation**
```
"Design a user experience workflow for a mobile banking app focusing on accessibility and security"
```

## How It Works

### 1. Task Analysis Phase
- **Natural Language Processing**: Parses task description to identify key requirements
- **Domain Classification**: Categorizes task into research, analysis, creative, planning, or problem-solving
- **Complexity Assessment**: Determines task complexity and estimated completion time
- **Requirement Extraction**: Identifies specific deliverables and success criteria

### 2. Crew Generation Phase
- **Agent Selection**: Chooses optimal agent types based on task analysis
- **Role Assignment**: Assigns specific roles, goals, and backstories to each agent
- **Task Distribution**: Creates subtasks aligned with agent capabilities
- **Workflow Design**: Establishes collaboration patterns and dependencies

### 3. Execution Phase
- **Sequential Processing**: Agents work through tasks in logical order
- **Collaboration**: Agents share information and build upon each other's work
- **Quality Control**: Built-in validation and review processes
- **Result Compilation**: Aggregates individual outputs into final deliverable

## Agent Types

### Core Agents

| Agent Type | Role | Best For |
|------------|------|----------|
| **Senior Research Analyst** | Information gathering and verification | Market research, data collection, fact-checking |
| **Expert Content Writer** | Content creation and editing | Reports, documentation, communications |
| **Strategic Data Analyst** | Pattern recognition and insights | Data analysis, trend identification, recommendations |
| **Strategic Planning Expert** | Strategy development and planning | Roadmaps, project plans, strategic initiatives |
| **Solution Architect** | Problem solving and optimization | Process improvement, technical solutions |
| **Creative Innovation Specialist** | Ideation and creative solutions | Product design, innovation, brainstorming |
| **Project Coordinator** | Team coordination and oversight | Complex projects, quality assurance |

### Dynamic Agent Selection

The system intelligently selects 2-4 agents based on:
- **Task Complexity**: Simple tasks use fewer agents, complex tasks employ full teams
- **Domain Requirements**: Specialized agents added for specific domains
- **Deliverable Types**: Agent mix optimized for expected outputs

## Customization Options

### LLM Provider Selection
- **OpenAI GPT-4o**: Optimal for complex reasoning and analysis
- **Anthropic Claude**: Excellent for nuanced content and ethical considerations
- **Groq Models**: Fast inference for time-sensitive tasks
- **Mistral Models**: Privacy-focused European AI solutions

### Template Customization

Modify agent and task templates in `/config/`:
- `agent_templates.py`: Customize agent roles, goals, and capabilities
- `task_templates.py`: Modify workflow patterns and task structures

### Advanced Configuration

Environment variables for fine-tuning:
```env
# Performance settings
MAX_CONCURRENT_CREWS=5
MAX_REQUESTS_PER_MINUTE=60

# Caching options
ENABLE_CACHE=True
CACHE_TTL=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=meta_crew_spawner.log
```

## Enterprise Features

### Security
- **API Key Management**: Secure environment-based key storage
- **Request Validation**: Input sanitization and validation
- **Rate Limiting**: Configurable request throttling

### Scalability
- **Multi-Provider Support**: Automatic failover between LLM providers
- **Concurrent Processing**: Multiple crew execution support
- **Resource Management**: Efficient memory and API usage

### Monitoring
- **Execution Tracking**: Real-time crew status and progress
- **Performance Metrics**: Completion times and success rates
- **Error Handling**: Comprehensive error reporting and recovery

## Troubleshooting

### Common Issues

**"No LLM providers configured"**
- Ensure at least one API key is set in `.env`
- Verify API key format and validity
- Check provider service status

**"Task analysis failed"**
- Verify LLM provider connectivity
- Check API key permissions and quotas
- Ensure task description is clear and specific

**"Agent generation errors"**
- Review agent template configurations
- Check for conflicting agent combinations
- Verify task complexity assessment

### Performance Optimization

- Use **OpenAI GPT-4o** for best results with complex tasks
- Enable caching for repeated similar tasks
- Limit concurrent crews based on system resources
- Monitor API usage to avoid rate limits

## Support and Contributing

This Meta-Crew Spawner template demonstrates the power of dynamic multi-agent systems. For enterprise deployments, consider:

- Load balancing across multiple LLM providers
- Custom agent template development
- Integration with existing business systems
- Advanced monitoring and analytics

## License

This project is provided as a CrewAI marketplace template. See LICENSE for details.

---

**Ready to transform your workflows with intelligent AI crews?** Configure your API keys and start describing your challenges in natural language. Watch as specialized agents collaborate to deliver professional-grade results.
