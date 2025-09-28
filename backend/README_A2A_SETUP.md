# A2A Agent Setup Guide

This guide explains how to start and manage the A2A agents for the AI Agent Management Platform.

## 🚀 Quick Start

### Option 1: Start Everything (Recommended)

```bash
cd backend
source venv/bin/activate
python start_platform.py
```

This will start:

- All 5 A2A agents on ports 10020-10024
- FastAPI backend server on port 8001
- Proper threading and lifecycle management

### Option 2: Start Components Separately

#### Start A2A Agents Only

```bash
cd backend
source venv/bin/activate
python start_a2a_agents.py
```

#### Start Backend Server Only

```bash
cd backend
source venv/bin/activate
python start_backend.py
```

## 🔧 Prerequisites

### 1. Google API Key Setup

Create a `.env` file in the backend directory:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 2. Get API Key

- Visit: https://aistudio.google.com/apikey
- Create a new API key
- Add it to your `.env` file

## 📡 Endpoints

### Backend API (Port 8001)

- **Main API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Agent Status**: http://localhost:8001/agents/status
- **Chat Endpoint**: http://localhost:8001/chat

### A2A Agents (Ports 10020-10024)

- **Secretary Agent**: http://127.0.0.1:10020
- **Hiring Manager**: http://127.0.0.1:10021
- **Data Analyst**: http://127.0.0.1:10022
- **Researcher**: http://127.0.0.1:10023
- **Content Creator**: http://127.0.0.1:10024

## 🎯 How It Works

### 1. Agent Communication

- A2A agents run as independent HTTP servers
- Each agent exposes an Agent Card at `/.well-known/agent_card`
- Agents communicate via JSON-RPC over HTTP

### 2. Message Routing

The backend intelligently routes user messages:

- **Data analysis** → Data Analyst Agent
- **Research requests** → Researcher Agent
- **Content creation** → Content Creator Agent
- **Agent hiring** → Hiring Manager Agent
- **General queries** → Secretary Agent

### 3. Frontend Integration

- Frontend sends messages to `/chat` endpoint
- Backend routes to appropriate A2A agent
- Agent processes request and returns response
- Frontend displays response with agent name

## 🧪 Testing

### Test Agent Status

```bash
curl http://localhost:8001/agents/status
```

### Test Chat Endpoint

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with data analysis", "user_id": "test-user"}'
```

### Test Individual Agents

```bash
curl http://127.0.0.1:10020/.well-known/agent_card
```

## 🛑 Stopping the Platform

- Press `Ctrl+C` to stop all services gracefully
- The platform will shut down all agents and servers

## 🔍 Troubleshooting

### Agents Not Starting

1. Check if Google API key is set in `.env`
2. Verify virtual environment is activated
3. Check logs for specific error messages

### Port Conflicts

- Kill existing processes: `lsof -ti:8001 | xargs kill -9`
- Or use different ports in the configuration

### Agent Communication Issues

1. Verify agents are running: `curl http://127.0.0.1:10020/.well-known/agent_card`
2. Check agent status: `curl http://localhost:8001/agents/status`
3. Review backend logs for connection errors

## 📝 Logs

- **Agent logs**: Displayed in the terminal where agents are started
- **Backend logs**: Available at http://localhost:8001/docs
- **Error handling**: Graceful fallbacks when agents are unavailable

## 🎉 Success Indicators

When everything is working correctly, you should see:

- ✅ All agent servers started messages
- ✅ Backend server running on port 8001
- ✅ Agent status endpoint returning all agents as active
- ✅ Chat endpoint routing messages to correct agents
