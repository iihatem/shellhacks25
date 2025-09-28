from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv
from a2a_client_service import a2a_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="AI Agent Management Platform",
    description="A platform for creating and managing AI agents to handle tasks and jobs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Agent(BaseModel):
    id: str
    name: str
    role: str
    capabilities: List[str]
    is_active: bool = True

class Task(BaseModel):
    id: str
    description: str
    assigned_agent_id: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    created_at: str

class ChatMessage(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    agent_name: str
    action_taken: Optional[str] = None

# In-memory storage (replace with database later)
agents_db = [
    {
        "id": "secretary-001",
        "name": "Executive Secretary",
        "role": "secretary",
        "capabilities": ["task_delegation", "communication", "scheduling"],
        "is_active": True
    },
    {
        "id": "hiring-manager-001", 
        "name": "Hiring Manager",
        "role": "hiring_manager",
        "capabilities": ["agent_creation", "skill_assessment", "recruitment"],
        "is_active": True
    }
]

tasks_db = []

@app.get("/")
async def root():
    return {"message": "AI Agent Management Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agents", response_model=List[Agent])
async def get_agents():
    """Get all agents in the workspace"""
    return agents_db

@app.post("/agents", response_model=Agent)
async def create_agent(agent: Agent):
    """Create a new agent"""
    # Check if agent ID already exists
    if any(a["id"] == agent.id for a in agents_db):
        raise HTTPException(status_code=400, detail="Agent ID already exists")
    
    agent_dict = agent.model_dump()
    agents_db.append(agent_dict)
    return agent_dict

@app.get("/agents/status")
async def get_agent_status():
    """Get the status of all A2A agents"""
    try:
        status = await a2a_client.get_agent_status()
        return {
            "agents": status,
            "total_agents": len(status),
            "active_agents": sum(1 for active in status.values() if active),
            "all_active": all(status.values())
        }
    except Exception as e:
        logging.error(f"Error checking agent status: {e}")
        return {
            "error": "Failed to check agent status",
            "agents": {},
            "total_agents": 0,
            "active_agents": 0,
            "all_active": False
        }

@app.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    agent = next((a for a in agents_db if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks_db

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    """Create a new task"""
    task_dict = task.model_dump()
    tasks_db.append(task_dict)
    return task_dict

@app.post("/chat", response_model=ChatResponse)
async def chat_with_secretary(message: ChatMessage):
    """Main chat endpoint - communicates with A2A agents"""
    try:
        # Route the message to the appropriate agent
        response_text, agent_name = await a2a_client.route_message(
            message.message, 
            message.user_id
        )
        
        # Determine action taken based on response content
        action_taken = "message_processed"
        if "task" in response_text.lower() and ("created" in response_text.lower() or "assigned" in response_text.lower()):
            action_taken = "task_created"
        elif "agent" in response_text.lower() and ("created" in response_text.lower() or "hired" in response_text.lower()):
            action_taken = "agent_created"
        elif "research" in response_text.lower() or "analysis" in response_text.lower():
            action_taken = "research_completed"
        elif "content" in response_text.lower() or "written" in response_text.lower():
            action_taken = "content_created"
        
        return ChatResponse(
            response=response_text,
            agent_name=agent_name,
            action_taken=action_taken
        )
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response="I'm sorry, I'm experiencing some technical difficulties. Please make sure the A2A agent servers are running and try again.",
            agent_name="System",
            action_taken="error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
