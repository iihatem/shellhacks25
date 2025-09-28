"""Hiring Manager agent - creates new employee agents when needed."""

import asyncio
import json
import logging
import uvicorn
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from google.adk.agents import Agent
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentSkill, AgentCapabilities, TransportProtocol

from agents import EMPLOYEE_AGENTS, EmployeeAgentExecutor
from agent_registry import get_global_registry
from config import DEFAULT_MODEL, HIRING_MANAGER_PORT, EMPLOYEE_BASE_PORT, PLATFORM_HOST
from debug_utils import extract_message_content_safely

logger = logging.getLogger(__name__)

@dataclass
class AgentCreationRequest:
    """Request for creating a new agent."""
    agent_type: str
    specialization: str
    port: int
    description: str

class HiringManagerExecutor(AgentExecutor):
    """Executor for the Hiring Manager agent."""
    
    def __init__(self):
        self.agent = Agent(
            model=DEFAULT_MODEL,
            name='hiring_manager',
            instruction="""
            You are the Hiring Manager agent responsible for creating new employee agents when needed.
            
            Your capabilities include:
            - Analyzing requests to determine if new agents are needed
            - Creating specialized employee agents with specific skills
            - Managing the agent creation process
            - Providing information about available agent types
            
            Available agent types you can create:
            1. data_analyst - For data analysis, statistics, and insights
            2. content_creator - For writing, marketing, and creative content
            3. researcher - For research, fact-checking, and information gathering
            
            When you receive a request:
            1. Determine if existing agents can handle the task
            2. If not, identify what type of new agent is needed
            3. Create the appropriate agent with specialized instructions
            4. Confirm the agent creation and provide details
            
            You should only create new agents when:
            - The requested capability doesn't exist in current agents
            - A specialized version of an existing agent type is needed
            - The workload requires additional agents of the same type
            
            Always explain your reasoning and provide clear information about the created agent.
            """,
            description='Creates and manages new employee agents based on organizational needs'
        )
        self.created_agents: Dict[int, Dict[str, Any]] = {}
        self.next_port = EMPLOYEE_BASE_PORT
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute the hiring manager logic."""
        try:
            # Extract message content
            message_content = self._extract_message_content(context)
            
            # Analyze the request
            await event_queue.enqueue_event(
                new_agent_text_message("🤔 Analyzing your request for new agent capabilities...")
            )
            
            # Check if this is a request to create a new agent
            if any(keyword in message_content.lower() for keyword in [
                'create agent', 'new agent', 'hire agent', 'add agent', 'need agent'
            ]):
                await self._handle_agent_creation_request(message_content, event_queue)
            elif any(keyword in message_content.lower() for keyword in [
                'list agents', 'available agents', 'what agents', 'agent types'
            ]):
                await self._handle_list_agents_request(event_queue)
            elif any(keyword in message_content.lower() for keyword in [
                'created agents', 'my agents', 'active agents'
            ]):
                await self._handle_list_created_agents_request(event_queue)
            else:
                # General inquiry - provide guidance
                await self._handle_general_inquiry(message_content, event_queue)
                
        except Exception as e:
            logger.error(f"Error in hiring manager execution: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"Sorry, I encountered an error: {str(e)}")
            )
    
    def _extract_message_content(self, context: RequestContext) -> str:
        """Extract message content from context."""
        return extract_message_content_safely(context, "HiringManager")
    
    async def _handle_agent_creation_request(self, message: str, event_queue: EventQueue):
        """Handle request to create a new agent."""
        # Determine agent type from message
        agent_type = None
        specialization = ""
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ['data', 'analysis', 'analytics', 'statistics']):
            agent_type = 'data_analyst'
            specialization = 'data analysis and statistics'
        elif any(keyword in message_lower for keyword in ['content', 'writing', 'marketing', 'creative']):
            agent_type = 'content_creator'
            specialization = 'content creation and marketing'
        elif any(keyword in message_lower for keyword in ['research', 'fact', 'information', 'investigate']):
            agent_type = 'researcher'
            specialization = 'research and fact-checking'
        
        if not agent_type:
            # Ask for clarification
            response = """
I can help you create a new employee agent! I can create these types of agents:

🔍 **Research Agent** - For web research, fact-checking, and information gathering
📊 **Data Analyst Agent** - For data analysis, statistics, and insights generation  
✍️ **Content Creator Agent** - For writing, marketing copy, and creative content

Which type of agent would you like me to create? Please specify the type and any special requirements.

Example: "Create a research agent specialized in technology trends"
            """
            await event_queue.enqueue_event(new_agent_text_message(response.strip()))
            return
        
        # Create the agent
        try:
            port = self.next_port
            self.next_port += 1
            
            await event_queue.enqueue_event(
                new_agent_text_message(f"🚀 Creating a new {agent_type.replace('_', ' ').title()} specialized in {specialization}...")
            )
            
            # Start the agent in background
            asyncio.create_task(self._deploy_agent(agent_type, port))
            
            # Store agent info
            self.created_agents[port] = {
                'type': agent_type,
                'specialization': specialization,
                'port': port,
                'status': 'starting'
            }
            
            response = f"""
✅ **Agent Created Successfully!**

**Agent Type:** {agent_type.replace('_', ' ').title()}
**Specialization:** {specialization}
**URL:** http://{PLATFORM_HOST}:{port}
**Status:** Starting up...

The agent will be available shortly and will automatically register with the Secretary Agent for task delegation.

You can now ask the Secretary Agent to use this new agent for tasks requiring {specialization}.
            """
            
            await event_queue.enqueue_event(new_agent_text_message(response.strip()))
            
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ Failed to create agent: {str(e)}")
            )
    
    async def _deploy_agent(self, agent_type: str, port: int):
        """Deploy a new agent on the specified port."""
        try:
            if agent_type not in EMPLOYEE_AGENTS:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            agent_info = EMPLOYEE_AGENTS[agent_type]
            
            # Create the agent
            agent = agent_info['agent']
            agent_card = agent_info['get_card'](port)
            
            # Create executor
            executor = EmployeeAgentExecutor(agent)
            
            # Create request handler
            request_handler = DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore(),
            )
            
            # Create A2A application
            app = A2AStarletteApplication(
                agent_card=agent_card,
                http_handler=request_handler,
            )
            
            # Start server
            config = uvicorn.Config(
                app.build(),
                host=PLATFORM_HOST,
                port=port,
                log_level='warning',
            )
            
            server = uvicorn.Server(config)
            
            # Update status
            if port in self.created_agents:
                self.created_agents[port]['status'] = 'running'
            
            logger.info(f"Started {agent_type} agent on port {port}")
            
            # Register with global registry
            registry = get_global_registry()
            async with registry:
                await registry.register_agent(f"http://{PLATFORM_HOST}:{port}")
            
            # Run server
            await server.serve()
            
        except Exception as e:
            logger.error(f"Failed to deploy agent {agent_type} on port {port}: {e}")
            if port in self.created_agents:
                self.created_agents[port]['status'] = 'error'
    
    async def _handle_list_agents_request(self, event_queue: EventQueue):
        """Handle request to list available agent types."""
        response = """
🤖 **Available Agent Types I Can Create:**

🔍 **Research Agent**
- Web research and information gathering
- Fact-checking and verification
- Synthesizing information from multiple sources
- Expert opinion finding

📊 **Data Analyst Agent**  
- Data analysis and pattern identification
- Statistical summaries and reports
- Trend analysis and forecasting
- Data-driven recommendations

✍️ **Content Creator Agent**
- Blog posts and articles
- Marketing copy and campaigns  
- Social media content
- Creative writing and editing

To create a new agent, just ask me like:
"Create a research agent for technology trends"
"I need a data analyst agent for sales analysis"
"Create a content creator for social media"
        """
        
        await event_queue.enqueue_event(new_agent_text_message(response.strip()))
    
    async def _handle_list_created_agents_request(self, event_queue: EventQueue):
        """Handle request to list created agents."""
        if not self.created_agents:
            response = "No agents have been created yet. Would you like me to create one?"
        else:
            response = "🤖 **Agents I've Created:**\n\n"
            for port, info in self.created_agents.items():
                status_emoji = "✅" if info['status'] == 'running' else "🚀" if info['status'] == 'starting' else "❌"
                response += f"{status_emoji} **{info['type'].replace('_', ' ').title()}**\n"
                response += f"   - Specialization: {info['specialization']}\n"
                response += f"   - URL: http://{PLATFORM_HOST}:{port}\n"
                response += f"   - Status: {info['status']}\n\n"
        
        await event_queue.enqueue_event(new_agent_text_message(response.strip()))
    
    async def _handle_general_inquiry(self, message: str, event_queue: EventQueue):
        """Handle general inquiries about the hiring manager."""
        response = """
👋 **Hello! I'm the Hiring Manager Agent**

I'm responsible for creating new employee agents when you need additional capabilities. Here's what I can help you with:

🆕 **Create New Agents** - I can create specialized agents for:
- Research and fact-checking
- Data analysis and statistics  
- Content creation and marketing

📋 **Manage Agents** - I keep track of all agents I've created and their status

❓ **Get Information** - Ask me about available agent types or created agents

**How to work with me:**
- "Create a research agent for market analysis"
- "I need a data analyst for financial reports"  
- "What agent types can you create?"
- "Show me the agents you've created"

What would you like me to help you with today?
        """
        
        await event_queue.enqueue_event(new_agent_text_message(response.strip()))
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel the current execution."""
        await event_queue.enqueue_event(
            new_agent_text_message("Task cancelled.")
        )

class HiringManagerAgent:
    """Hiring Manager agent for creating new employee agents."""
    
    @staticmethod
    def get_agent_card() -> AgentCard:
        """Get the agent card for the Hiring Manager."""
        return AgentCard(
            name='Hiring Manager Agent',
            description='Creates and manages new employee agents based on organizational needs and workload requirements',
            url=f'http://{PLATFORM_HOST}:{HIRING_MANAGER_PORT}',
            version='1.0.0',
            capabilities=AgentCapabilities(streaming=True),
            default_input_modes=['text/plain'],
            default_output_modes=['text/plain'],
            preferred_transport=TransportProtocol.jsonrpc,
            skills=[
                AgentSkill(
                    id='agent_creation',
                    name='Agent Creation',
                    description='Create new specialized employee agents',
                    tags=['creation', 'hiring', 'agents', 'specialization'],
                    examples=[
                        'Create a research agent for market analysis',
                        'I need a data analyst for financial reports',
                        'Create a content creator for social media campaigns'
                    ]
                ),
                AgentSkill(
                    id='agent_management',
                    name='Agent Management',
                    description='Manage and monitor created agents',
                    tags=['management', 'monitoring', 'status', 'agents'],
                    examples=[
                        'What agents have you created?',
                        'Show me the status of all agents',
                        'List available agent types'
                    ]
                ),
                AgentSkill(
                    id='capability_assessment',
                    name='Capability Assessment',
                    description='Assess organizational needs and recommend new agents',
                    tags=['assessment', 'needs', 'recommendations', 'capabilities'],
                    examples=[
                        'What type of agent do I need for this task?',
                        'Assess if we need additional capabilities',
                        'Recommend agents for our workflow'
                    ]
                )
            ]
        )
