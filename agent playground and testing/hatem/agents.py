"""Employee agents for the A2A platform."""

import asyncio
import logging
from typing import AsyncIterable, Dict, Any, List, Optional
from collections.abc import AsyncIterable as AsyncIterableABC

from google.adk import Runner
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentSkill, AgentCapabilities, TransportProtocol

from config import DEFAULT_MODEL
from debug_utils import extract_message_content_safely

logger = logging.getLogger(__name__)

class EmployeeAgentExecutor(AgentExecutor):
    """Base executor for employee agents using Google ADK."""
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.user_id = 'a2a_platform'
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute the agent with the given context."""
        try:
            # Extract message content safely
            message_content = extract_message_content_safely(context, "EmployeeAgent")
            
            # Create session
            session_id = context.session_id or "default_session"
            session = await self.runner.session_service.get_session(
                app_name=self.agent.name,
                user_id=self.user_id,
                session_id=session_id,
            )
            
            if session is None:
                session = await self.runner.session_service.create_session(
                    app_name=self.agent.name,
                    user_id=self.user_id,
                    state={},
                    session_id=session_id,
                )
            
            # Create content for the agent
            content = types.Content(
                role='user', 
                parts=[types.Part.from_text(text=message_content)]
            )
            
            # Stream responses
            async for event in self.runner.run_async(
                user_id=self.user_id, 
                session_id=session.id, 
                new_message=content
            ):
                if event.is_final_response():
                    response_text = '\n'.join([
                        p.text for p in event.content.parts if p.text
                    ])
                    await event_queue.enqueue_event(new_agent_text_message(response_text))
                else:
                    # Send intermediate updates
                    await event_queue.enqueue_event(new_agent_text_message("🤔 Working..."))
                    
        except Exception as e:
            logger.error(f"Error in agent execution: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"Sorry, I encountered an error: {str(e)}")
            )
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel the current execution."""
        await event_queue.enqueue_event(
            new_agent_text_message("Task cancelled.")
        )

# Import individual agent definitions
from data_analyst_agent import root_agent as data_analyst_agent
from content_creator_agent import root_agent as content_creator_agent  
from researcher_agent import root_agent as researcher_agent

def get_data_analyst_card(port: int) -> AgentCard:
    return AgentCard(
        name='Data Analyst Agent',
        description='Specialized agent for data analysis, statistics, and insights generation',
        url=f'http://127.0.0.1:{port}',
        version='1.0.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='data_analysis',
                name='Data Analysis',
                description='Analyze datasets and generate insights',
                tags=['data', 'analysis', 'statistics', 'insights', 'reporting'],
                examples=[
                    'Analyze this sales data and identify trends',
                    'What insights can you provide from this dataset?',
                    'Create a statistical summary of this information'
                ]
            ),
            AgentSkill(
                id='trend_analysis',
                name='Trend Analysis',
                description='Identify patterns and trends in data over time',
                tags=['trends', 'patterns', 'forecasting', 'time-series'],
                examples=[
                    'Identify trends in this time series data',
                    'What patterns do you see in customer behavior?',
                    'Forecast future trends based on historical data'
                ]
            )
        ]
    )


def get_content_creator_card(port: int) -> AgentCard:
    return AgentCard(
        name='Content Creator Agent',
        description='Specialized agent for content creation, writing, and marketing communications',
        url=f'http://127.0.0.1:{port}',
        version='1.0.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='content_writing',
                name='Content Writing',
                description='Create engaging written content for various purposes',
                tags=['writing', 'content', 'blog', 'articles', 'copy'],
                examples=[
                    'Write a blog post about sustainable technology',
                    'Create marketing copy for a new product launch',
                    'Draft a newsletter for our customers'
                ]
            ),
            AgentSkill(
                id='social_media',
                name='Social Media Content',
                description='Create content optimized for social media platforms',
                tags=['social-media', 'marketing', 'engagement', 'campaigns'],
                examples=[
                    'Create a Twitter thread about AI trends',
                    'Write Instagram captions for a product showcase',
                    'Develop a LinkedIn post for thought leadership'
                ]
            )
        ]
    )


def get_researcher_card(port: int) -> AgentCard:
    return AgentCard(
        name='Research Agent',
        description='Specialized agent for comprehensive research, fact-checking, and information synthesis',
        url=f'http://127.0.0.1:{port}',
        version='1.0.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='web_research',
                name='Web Research',
                description='Conduct comprehensive research using web sources',
                tags=['research', 'web-search', 'information', 'investigation'],
                examples=[
                    'Research the latest developments in quantum computing',
                    'Find information about sustainable energy solutions',
                    'Investigate market trends in the tech industry'
                ]
            ),
            AgentSkill(
                id='fact_checking',
                name='Fact Checking',
                description='Verify information and check facts from reliable sources',
                tags=['fact-check', 'verification', 'accuracy', 'sources'],
                examples=[
                    'Verify these claims about climate change',
                    'Fact-check this news article',
                    'Confirm the accuracy of these statistics'
                ]
            )
        ]
    )

# Available employee agents
EMPLOYEE_AGENTS = {
    'data_analyst': {
        'agent': data_analyst_agent,
        'get_card': get_data_analyst_card
    },
    'content_creator': {
        'agent': content_creator_agent,
        'get_card': get_content_creator_card
    },
    'researcher': {
        'agent': researcher_agent,
        'get_card': get_researcher_card
    },
}
