"""Agent registry for discovering and managing A2A agents."""

import asyncio
import logging
from typing import Dict, List, Optional
import httpx
from dataclasses import dataclass, field
from a2a.types import AgentCard
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

logger = logging.getLogger(__name__)

@dataclass
class RegisteredAgent:
    """Information about a registered agent."""
    agent_card: AgentCard
    url: str
    status: str = "active"  # active, inactive, error
    last_checked: Optional[float] = None
    error_message: Optional[str] = None

class AgentRegistry:
    """Registry for discovering and managing A2A agents."""
    
    def __init__(self):
        self._agents: Dict[str, RegisteredAgent] = {}
        self._httpx_client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._httpx_client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._httpx_client:
            await self._httpx_client.aclose()
    
    async def register_agent(self, agent_url: str) -> bool:
        """Register an agent by discovering its capabilities.
        
        Args:
            agent_url: Base URL of the agent
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not self._httpx_client:
                raise RuntimeError("AgentRegistry must be used as async context manager")
                
            # Fetch agent card
            card_url = f"{agent_url.rstrip('/')}{AGENT_CARD_WELL_KNOWN_PATH}"
            response = await self._httpx_client.get(card_url)
            response.raise_for_status()
            
            # Parse agent card
            card_data = response.json()
            agent_card = AgentCard(**card_data)
            
            # Register the agent
            agent_id = self._generate_agent_id(agent_card.name, agent_url)
            self._agents[agent_id] = RegisteredAgent(
                agent_card=agent_card,
                url=agent_url,
                status="active",
                last_checked=asyncio.get_event_loop().time()
            )
            
            logger.info(f"Registered agent: {agent_card.name} at {agent_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent at {agent_url}: {e}")
            # Store failed registration
            agent_id = self._generate_agent_id("unknown", agent_url)
            self._agents[agent_id] = RegisteredAgent(
                agent_card=AgentCard(name="unknown", url=agent_url, description="Failed to load"),
                url=agent_url,
                status="error",
                error_message=str(e),
                last_checked=asyncio.get_event_loop().time()
            )
            return False
    
    def _generate_agent_id(self, name: str, url: str) -> str:
        """Generate a unique agent ID."""
        return f"{name.lower().replace(' ', '_')}_{hash(url) % 10000}"
    
    def get_agent(self, agent_id: str) -> Optional[RegisteredAgent]:
        """Get a registered agent by ID."""
        return self._agents.get(agent_id)
    
    def get_agents_by_skill(self, skill_tags: List[str]) -> List[RegisteredAgent]:
        """Find agents that have skills matching the given tags.
        
        Args:
            skill_tags: List of skill tags to search for
            
        Returns:
            List of agents that have matching skills
        """
        matching_agents = []
        
        for agent in self._agents.values():
            if agent.status != "active":
                continue
                
            for skill in agent.agent_card.skills or []:
                if any(tag.lower() in [t.lower() for t in skill.tags or []] for tag in skill_tags):
                    matching_agents.append(agent)
                    break
        
        return matching_agents
    
    def list_all_agents(self) -> List[RegisteredAgent]:
        """Get all registered agents."""
        return list(self._agents.values())
    
    def list_active_agents(self) -> List[RegisteredAgent]:
        """Get all active registered agents."""
        return [agent for agent in self._agents.values() if agent.status == "active"]
    
    async def health_check_agents(self) -> Dict[str, bool]:
        """Perform health check on all registered agents.
        
        Returns:
            Dictionary mapping agent_id to health status
        """
        if not self._httpx_client:
            raise RuntimeError("AgentRegistry must be used as async context manager")
            
        health_status = {}
        
        for agent_id, agent in self._agents.items():
            try:
                # Try to fetch the agent card to check if it's still available
                card_url = f"{agent.url.rstrip('/')}{AGENT_CARD_WELL_KNOWN_PATH}"
                response = await self._httpx_client.get(card_url)
                response.raise_for_status()
                
                agent.status = "active"
                agent.error_message = None
                health_status[agent_id] = True
                
            except Exception as e:
                agent.status = "error"
                agent.error_message = str(e)
                health_status[agent_id] = False
                logger.warning(f"Health check failed for agent {agent_id}: {e}")
            
            agent.last_checked = asyncio.get_event_loop().time()
        
        return health_status
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry.
        
        Args:
            agent_id: ID of the agent to remove
            
        Returns:
            True if agent was removed, False if not found
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
            logger.info(f"Removed agent: {agent_id}")
            return True
        return False

# Global registry instance
_global_registry: Optional[AgentRegistry] = None

def get_global_registry() -> AgentRegistry:
    """Get the global agent registry instance."""
    global _global_registry
    if _global_registry is None:
        _global_registry = AgentRegistry()
    return _global_registry
