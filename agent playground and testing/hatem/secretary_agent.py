"""Secretary agent - the main orchestrator for the A2A platform."""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional

from google.adk.agents import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from a2a.types import AgentCard, AgentSkill, AgentCapabilities, TransportProtocol
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

from agent_registry import get_global_registry
from config import SECRETARY_PORT

logger = logging.getLogger(__name__)

class SecretaryAgent:
    """Secretary agent that orchestrates tasks to employee agents."""
    
    def __init__(self):
        self.registry = get_global_registry()
        self._remote_agents: Dict[str, RemoteA2aAgent] = {}
        self._sequential_agent: Optional[SequentialAgent] = None
    
    async def initialize(self):
        """Initialize the secretary agent with available employee agents."""
        async with self.registry:
            # Get all active agents
            active_agents = self.registry.list_active_agents()
            
            # Create remote A2A agents for each employee
            remote_agents = []
            for registered_agent in active_agents:
                try:
                    # Create RemoteA2aAgent
                    remote_agent = RemoteA2aAgent(
                        name=registered_agent.agent_card.name.lower().replace(' ', '_'),
                        description=registered_agent.agent_card.description,
                        agent_card=f"{registered_agent.url}{AGENT_CARD_WELL_KNOWN_PATH}",
                    )
                    remote_agents.append(remote_agent)
                    self._remote_agents[registered_agent.agent_card.name] = remote_agent
                    logger.info(f"Added remote agent: {registered_agent.agent_card.name}")
                    
                except Exception as e:
                    logger.error(f"Failed to create remote agent for {registered_agent.agent_card.name}: {e}")
            
            # Create sequential agent if we have remote agents
            if remote_agents:
                self._sequential_agent = SequentialAgent(
                    name='secretary_orchestrator',
                    sub_agents=remote_agents,
                )
                logger.info(f"Secretary agent initialized with {len(remote_agents)} employee agents")
            else:
                logger.warning("No employee agents available - secretary will work standalone")
    
    def get_sequential_agent(self) -> Optional[SequentialAgent]:
        """Get the underlying sequential agent."""
        return self._sequential_agent
    
    def get_available_agents(self) -> List[str]:
        """Get list of available employee agent names."""
        return list(self._remote_agents.keys())
    
    async def refresh_agents(self):
        """Refresh the list of available agents."""
        logger.info("Refreshing available agents...")
        await self.initialize()
    
    @staticmethod
    def get_agent_card() -> AgentCard:
        """Get the agent card for the Secretary agent."""
        return AgentCard(
            name='Secretary Agent',
            description='Main orchestrator that coordinates and delegates tasks to specialized employee agents',
            url=f'http://127.0.0.1:{SECRETARY_PORT}',
            version='1.0.0',
            capabilities=AgentCapabilities(streaming=True),
            default_input_modes=['text/plain'],
            default_output_modes=['text/plain'],
            preferred_transport=TransportProtocol.jsonrpc,
            skills=[
                AgentSkill(
                    id='task_coordination',
                    name='Task Coordination',
                    description='Coordinate and delegate tasks to specialized employee agents',
                    tags=['coordination', 'delegation', 'orchestration', 'management'],
                    examples=[
                        'I need a market analysis report with creative marketing suggestions',
                        'Research this topic and create content about it',
                        'Analyze this data and write a summary for executives'
                    ]
                ),
                AgentSkill(
                    id='multi_agent_workflow',
                    name='Multi-Agent Workflow',
                    description='Manage complex workflows involving multiple specialized agents',
                    tags=['workflow', 'multi-agent', 'complex-tasks', 'coordination'],
                    examples=[
                        'Research renewable energy trends, analyze the data, and create a blog post',
                        'Fact-check this information and create social media content about it',
                        'Analyze our sales data and create marketing content based on insights'
                    ]
                ),
                AgentSkill(
                    id='general_assistance',
                    name='General Assistance',
                    description='Provide general assistance and route requests to appropriate specialists',
                    tags=['help', 'assistance', 'routing', 'general'],
                    examples=[
                        'Help me with my project',
                        'I need assistance with data analysis',
                        'Can you help me create content for my business?'
                    ]
                )
            ]
        )
