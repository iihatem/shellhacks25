from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    """Main chat endpoint - communicates with the secretary agent"""
    # This is a placeholder implementation
    # In a real implementation, this would integrate with AI/LLM services
    
    secretary = next((a for a in agents_db if a["role"] == "secretary"), None)
    if not secretary:
        raise HTTPException(status_code=500, detail="Secretary agent not found")
    
    # Simple response logic (to be replaced with actual AI integration)
    response_text = f"Hello! I'm your {secretary['name']}. I've received your message: '{message.message}'. Let me analyze what needs to be done and delegate accordingly."
    
    return ChatResponse(
        response=response_text,
        agent_name=secretary["name"],
        action_taken="message_received"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
