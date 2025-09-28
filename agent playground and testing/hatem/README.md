# Hatem's AI Agent Management Platform

A multi-agent system built using Google's Agent2Agent (A2A) Protocol that implements a secretary-employee-hiring manager workflow.

## Architecture

- **Secretary Agent**: Acts as the main orchestrator, receives user requests and delegates to employee agents
- **Employee Agents**: Specialized agents that handle specific tasks (e.g., data analysis, content creation, research)
- **Hiring Manager Agent**: Creates new employee agents when needed capabilities don't exist

## Features

- Dynamic agent discovery and registration
- A2A protocol compliance for inter-agent communication
- Scalable microservices architecture
- Task delegation and coordination
- Real-time streaming responses

## Quick Start

1. Install dependencies:

   ```bash
   pip install -e .
   ```

2. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Start the agent platform:

   ```bash
   python start.py
   ```

   **Note**: Startup takes 10-15 seconds as agents start sequentially and register with each other.

## Agent Endpoints

- Secretary Agent: http://localhost:10000
- Hiring Manager: http://localhost:10001
- Employee Agents: http://localhost:10002+

## Testing

Run the test suite:

```bash
# Quick test (check if agents are reachable)
python quick_test.py

# Full test suite (comprehensive A2A testing)
python run_tests.py
```

**Note**: Make sure the platform is running first, and allow 15-20 seconds for all agents to be ready before testing.

## ADK Integration

The agents are also available for ADK's web interface:

```bash
# Start ADK web interface to see individual agents
adk web
```

Individual agent files that ADK can detect:

- `data_analyst_agent.py`
- `content_creator_agent.py`
- `researcher_agent.py`
- `secretary_agent_adk.py`
- `hiring_manager_adk.py`
