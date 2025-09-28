# A2A Agent Management Platform - Setup Guide

## 🎯 Overview

This is a complete implementation of an AI Agent Management Platform using Google's Agent2Agent (A2A) Protocol. The platform implements your requested secretary-employee-hiring manager workflow with full A2A compliance.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Secretary      │    │ Hiring Manager  │    │ Employee Agents │
│  Agent          │    │ Agent           │    │                 │
│  (Port 10000)   │    │ (Port 10001)    │    │ (Port 10002+)   │
│                 │    │                 │    │                 │
│ • Orchestrates  │    │ • Creates new   │    │ • Data Analyst  │
│ • Delegates     │    │   agents        │    │ • Content       │
│ • Coordinates   │    │ • Manages       │    │   Creator       │
│                 │    │   lifecycle     │    │ • Researcher    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Agent Registry  │
                    │ • Discovery     │
                    │ • Health checks │
                    │ • Management    │
                    └─────────────────┘
```

## 🚀 Quick Start

### 1. Set up Environment

```bash
cd "/Users/mac/Desktop/dev/shellhacks25/agent playground and testing/hatem"

# Copy and configure environment
cp env.example .env
# Edit .env with your Google API key or Vertex AI settings
```

### 2. Install Dependencies

Dependencies are already installed, but if needed:

```bash
pip install google-genai google-adk==1.9.0 a2a-sdk==0.3.0 uvicorn fastapi httpx pydantic python-dotenv nest-asyncio
```

**Note**: The platform includes a compatibility patch (`compatibility_patch.py`) to resolve import issues between `google-adk==1.9.0` and `a2a-sdk==0.3.0`.

### 3. Start the Platform

```bash
python start.py
```

The platform will start:

- **Secretary Agent**: http://127.0.0.1:10000
- **Hiring Manager**: http://127.0.0.1:10001
- **Employee Agents**: http://127.0.0.1:10002+

### 4. Test the Platform

In another terminal:

```bash
python run_tests.py
```

## 🤖 Agent Details

### Secretary Agent (Port 10000)

- **Role**: Main orchestrator and entry point
- **Capabilities**:
  - Delegates tasks to employee agents
  - Coordinates multi-agent workflows
  - Provides comprehensive responses
- **A2A Skills**: task_coordination, multi_agent_workflow, general_assistance

### Hiring Manager Agent (Port 10001)

- **Role**: Creates new employee agents on demand
- **Capabilities**:
  - Analyzes capability needs
  - Creates specialized agents
  - Manages agent lifecycle
- **A2A Skills**: agent_creation, agent_management, capability_assessment

### Employee Agents (Port 10002+)

#### Data Analyst Agent

- **Specialization**: Data analysis, statistics, insights
- **A2A Skills**: data_analysis, trend_analysis
- **Tools**: Google Search

#### Content Creator Agent

- **Specialization**: Writing, marketing, creative content
- **A2A Skills**: content_writing, social_media
- **Tools**: Google Search

#### Researcher Agent

- **Specialization**: Research, fact-checking, information synthesis
- **A2A Skills**: web_research, fact_checking
- **Tools**: Google Search

## 🔧 A2A Protocol Implementation

### Agent Discovery

Each agent exposes its capabilities via standard A2A agent cards at:

```
http://agent-url/.well-known/agent-card.json
```

### Communication Protocol

- **Transport**: JSON-RPC over HTTP/HTTPS
- **Streaming**: Real-time response streaming supported
- **Message Types**: Text, JSON, structured data

### Agent Registry

- Automatic agent discovery and registration
- Health monitoring and status tracking
- Skill-based agent matching

## 💡 Usage Examples

### Basic Task Delegation

```
User → Secretary: "I need market analysis and a blog post about it"
Secretary → Data Analyst: "Analyze current market trends"
Secretary → Content Creator: "Write blog post about these trends: [analysis]"
Secretary → User: [Combined response]
```

### Dynamic Agent Creation

```
User → Hiring Manager: "Create a research agent for technology trends"
Hiring Manager → Creates new specialized agent on port 10005
Hiring Manager → Registers agent with Secretary
User → Secretary: "Research latest AI developments"
Secretary → New Research Agent: [Delegates task]
```

### Multi-Agent Coordination

```
User → Secretary: "Research renewable energy, analyze the data, create social media content"
Secretary → Researcher: "Research renewable energy trends"
Secretary → Data Analyst: "Analyze this research data"
Secretary → Content Creator: "Create social media content from these insights"
Secretary → User: [Coordinated response]
```

## 🛠️ Configuration

### Environment Variables (.env)

```bash
# Google AI Configuration
GOOGLE_API_KEY=your_api_key_here
# OR for Vertex AI:
# GOOGLE_GENAI_USE_VERTEXAI=TRUE
# GOOGLE_CLOUD_PROJECT=your_project_id
# GOOGLE_CLOUD_LOCATION=us-central1

# Platform Configuration
PLATFORM_HOST=127.0.0.1
SECRETARY_PORT=10000
HIRING_MANAGER_PORT=10001
EMPLOYEE_BASE_PORT=10002
LOG_LEVEL=INFO
```

## 📊 Testing

The test suite validates:

- ✅ Agent discovery (agent cards)
- ✅ A2A communication protocol
- ✅ Secretary coordination
- ✅ Hiring manager capabilities
- ✅ Employee agent functionality
- ✅ Multi-agent workflows

## 🔒 Security Features

- Input validation for all agent communications
- Secure handling of external agent data
- Proper error handling and logging
- Agent health monitoring

## 🚀 Next Steps

1. **Frontend Integration**: The platform is ready to be integrated with your existing frontend
2. **Authentication**: Add authentication for production use
3. **Persistence**: Add database persistence for agent state and conversations
4. **Scaling**: Deploy agents to separate containers/services for production
5. **Monitoring**: Add comprehensive monitoring and analytics

## 🛠️ Troubleshooting

### Import Error: A2ACardResolver

If you see an import error related to `A2ACardResolver`, the compatibility patch should handle this automatically. If issues persist:

1. Make sure the compatibility patch is applied in `main.py`
2. Restart the platform
3. Check that all dependencies are correctly installed

### API Key Issues

- Make sure your `.env` file exists and contains a valid `GOOGLE_API_KEY`
- For Vertex AI, ensure you're authenticated with `gcloud auth login`

### Port Conflicts

If ports 10000-10002+ are in use:

- Modify the port settings in your `.env` file
- Kill existing processes: `lsof -ti:10000,10001,10002 | xargs kill -9`

## 🎉 Success!

You now have a fully functional A2A-compliant AI Agent Management Platform that implements:

- ✅ Secretary-Employee-Hiring Manager workflow
- ✅ Google A2A Protocol compliance
- ✅ Dynamic agent creation and discovery
- ✅ Multi-agent coordination and communication
- ✅ Comprehensive testing suite
- ✅ Production-ready architecture

The platform is ready for integration with your frontend and can be extended with additional agent types and capabilities as needed!
