"""A2A Client Service for communicating with agent servers."""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional
from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.types import AgentCard, TransportProtocol
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

logger = logging.getLogger(__name__)

class A2AClientService:
    """Service for communicating with A2A agents."""
    
    def __init__(self, default_timeout: float = 60.0):
        self._agent_info_cache: Dict[str, Dict[str, Any]] = {}
        self.default_timeout = default_timeout
        
        # Define agent endpoints
        self.agent_endpoints = {
            "secretary": "http://127.0.0.1:10020",
            "hiring_manager": "http://127.0.0.1:10021", 
            "data_analyst": "http://127.0.0.1:10022",
            "researcher": "http://127.0.0.1:10023",
            "content_creator": "http://127.0.0.1:10024",
            "orchestrator": "http://127.0.0.1:10025"
        }
    
    async def send_message_to_agent(self, agent_type: str, message: str) -> str:
        """Send a message to a specific agent type."""
        agent_url = self.agent_endpoints.get(agent_type)
        if not agent_url:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return await self._send_message(agent_url, message)
    
    async def send_message_to_secretary(self, message: str) -> str:
        """Send a message to the secretary agent (main orchestrator)."""
        return await self.send_message_to_agent("secretary", message)
    
    async def send_message_to_orchestrator(self, message: str) -> str:
        """Send a message to the master orchestrator for complex tasks."""
        return await self.send_message_to_agent("orchestrator", message)
    
    async def _send_message(self, agent_url: str, message: str) -> str:
        """Send a message to an A2A agent and return the response."""
        try:
            # Configure httpx client with timeout
            timeout_config = httpx.Timeout(
                timeout=self.default_timeout,
                connect=10.0,
                read=self.default_timeout,
                write=10.0,
                pool=5.0,
            )

            async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:
                # Check if we have cached agent card data
                if (
                    agent_url in self._agent_info_cache
                    and self._agent_info_cache[agent_url] is not None
                ):
                    agent_card_data = self._agent_info_cache[agent_url]
                else:
                    # Fetch the agent card
                    try:
                        agent_card_response = await httpx_client.get(
                            f'{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}'
                        )
                        agent_card_response.raise_for_status()
                        agent_card_data = self._agent_info_cache[agent_url] = (
                            agent_card_response.json()
                        )
                    except httpx.RequestError as e:
                        logger.error(f"Failed to fetch agent card from {agent_url}: {e}")
                        return f"I'm sorry, I'm having trouble connecting to the {agent_url.split('/')[-1]} agent. Please make sure the A2A agent servers are running."
                    except httpx.HTTPStatusError as e:
                        logger.error(f"HTTP error fetching agent card from {agent_url}: {e}")
                        return f"The {agent_url.split('/')[-1]} agent is not responding properly. Please check the server status."

                # Create AgentCard from data
                agent_card = AgentCard(**agent_card_data)

                # Create A2A client with the agent card
                config = ClientConfig(
                    httpx_client=httpx_client,
                    supported_transports=[
                        TransportProtocol.jsonrpc,
                        TransportProtocol.http_json,
                    ],
                    use_client_preference=True,
                )

                factory = ClientFactory(config)
                client = factory.create(agent_card)

                # Create the message object
                message_obj = create_text_message_object(content=message)

                # Send the message and collect responses
                responses = []
                async for response in client.send_message(message_obj):
                    responses.append(response)

                # The response is a tuple - get the first element (Task object)
                if (
                    responses
                    and isinstance(responses[0], tuple)
                    and len(responses[0]) > 0
                ):
                    task = responses[0][0]  # First element of the tuple

                    # Extract text: task.artifacts[0].parts[0].root.text
                    try:
                        return task.artifacts[0].parts[0].root.text
                    except (AttributeError, IndexError, TypeError):
                        # Fallback to string representation
                        return str(task)

                return 'No response received from the agent.'
                
        except Exception as e:
            logger.error(f"Error communicating with agent at {agent_url}: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    async def route_message(self, message: str, user_id: str = "user-123") -> tuple[str, str]:
        """
        Route a message to the appropriate agent based on content analysis.
        Returns (response, agent_name) tuple.
        """
        # Simple intent detection - in a real system this could be more sophisticated
        message_lower = message.lower()
        
        # Check for specific agent requests
        if any(word in message_lower for word in ["hire", "create agent", "new agent", "add agent"]):
            response = await self.send_message_to_agent("hiring_manager", message)
            return response, "Hiring Manager"
        
        elif any(word in message_lower for word in ["analyze", "data", "statistics", "metrics", "report"]):
            response = await self.send_message_to_agent("data_analyst", message)
            return response, "Data Analyst"
        
        elif any(word in message_lower for word in ["research", "find", "investigate", "fact check", "study"]):
            response = await self.send_message_to_agent("researcher", message)
            return response, "Researcher"
        
        elif any(word in message_lower for word in ["write", "content", "blog", "article", "marketing", "copy"]):
            response = await self.send_message_to_agent("content_creator", message)
            return response, "Content Creator"
        
        elif any(word in message_lower for word in ["complex", "multiple", "orchestrate", "coordinate"]):
            response = await self.send_message_to_orchestrator(message)
            return response, "Master Orchestrator"
        
        else:
            # Default to secretary for general queries and coordination
            response = await self.send_message_to_secretary(message)
            return response, "Executive Secretary"
    
    async def get_agent_status(self) -> Dict[str, bool]:
        """Check which agents are currently available."""
        status = {}
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            for agent_name, agent_url in self.agent_endpoints.items():
                try:
                    response = await client.get(f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}")
                    status[agent_name] = response.status_code == 200
                except:
                    status[agent_name] = False
        
        return status

# Global instance
a2a_client = A2AClientService()
