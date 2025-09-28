# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import os
import sys
import threading
import time

from typing import Any

import httpx
import nest_asyncio
import uvicorn

from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import ( AgentCapabilities,AgentCard,AgentSkill,TransportProtocol,)

from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from dotenv import load_dotenv
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor, A2aAgentExecutorConfig
                
from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent # this needs a hotswap replaccemnt
#import RemoteA2aAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
import sys

from a2a.client import client as real_client_module
from a2a.client.card_resolver import A2ACardResolver

class PatchedClientModule:
    def __init__(self, real_module) -> None:
        for attr in dir(real_module):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(real_module, attr))
        self.A2ACardResolver = A2ACardResolver

patched_module = PatchedClientModule(real_client_module)
sys.modules['a2a.client.client'] = patched_module  # type: ignore



# Set Google Cloud Configuration
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'FALSE'
os.environ['GOOGLE_CLOUD_PROJECT'] = (
    '[1001848614995]'  # @param {type: "string", placeholder: "[your-project-id]", isTemplate: true}
)
os.environ['GOOGLE_CLOUD_LOCATION'] = (
    'us-central1'  # Replace with your location
)

load_dotenv()

print('Environment variables configured:')
print(f'GOOGLE_GENAI_USE_VERTEXAI: {os.environ["GOOGLE_GENAI_USE_VERTEXAI"]}')
print(f'GOOGLE_CLOUD_PROJECT: {os.environ["GOOGLE_CLOUD_PROJECT"]}')
print(f'GOOGLE_CLOUD_LOCATION: {os.environ["GOOGLE_CLOUD_LOCATION"]}')


# Authenticate your notebook environment (Colab only)
# if 'google.colab' in sys.modules:
#     from google.colab import auth

#     auth.authenticate_user(project_id=os.environ['GOOGLE_CLOUD_PROJECT'])

# Setup logging
# logging.basicConfig(
#     level=logging.ERROR,
#     format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
# )






class A2ASimpleClient:
    """A2A Simple to call A2A servers."""

    def __init__(self, default_timeout: float = 240.0):
        self._agent_info_cache: dict[
            str, dict[str, Any] | None
        ] = {}  # Cache for agent metadata
        self.default_timeout = default_timeout

    async def create_task(self, agent_url: str, message: str) -> str:
        """Send a message following the official A2A SDK pattern."""
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
                agent_card_response = await httpx_client.get(
                    f'{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}'
                )
                agent_card_data = self._agent_info_cache[agent_url] = (
                    agent_card_response.json()
                )

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
                except (AttributeError, IndexError):
                    return str(task)

            return 'No response received'


def create_agent_a2a_server(agent, agent_card):
        """Create an A2A server for any ADK agent.

        Args:
            agent: The ADK agent instance
            agent_card: The ADK agent card

        Returns:
            A2AStarletteApplication instance
        """
        runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

        config = A2aAgentExecutorConfig()
        executor = A2aAgentExecutor(runner=runner, config=config)

        request_handler = DefaultRequestHandler(
            agent_executor=executor,
            task_store=InMemoryTaskStore(),
        )

        # Create A2A application
        return A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

async def run_stuff():
    
    # Create the Trending Topics ADK Agent
    trending_agent = Agent(
        model='gemini-2.5-pro',
        name='trending_topics_agent',
        instruction="""
        You are a social media trends analyst. Your job is to search the web for current trending topics,
        particularly from social platforms.

        When asked about trends:
        1. Search for "trending topics today" or similar queries
        2. Extract the top 3 trending topics
        3. Return them in a JSON format

        Focus on current, real-time trends from the last 24 hours.

        You MUST return your response in the following JSON format:
        {
            "trends": [
                {
                    "topic": "Topic name",
                    "description": "Brief description (1-2 sentences)",
                    "reason": "Why it's trending"
                },
                {
                    "topic": "Topic name",
                    "description": "Brief description (1-2 sentences)",
                    "reason": "Why it's trending"
                },
                {
                    "topic": "Topic name",
                    "description": "Brief description (1-2 sentences)",
                    "reason": "Why it's trending"
                }
            ]
        }

        Only return the JSON object, no additional text.
        """,
        tools=[google_search],
    )

    print('Trending Topics Agent created successfully!')


    trending_agent_card = AgentCard(
        name='Trending Topics Agent',
        url='http://localhost:10020',
        description='Searches the web for current trending topics from social media',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='find_trends',
                name='Find Trending Topics',
                description='Searches for current trending topics on social media',
                tags=['trends', 'social media', 'twitter', 'current events'],
                examples=[
                    "What's trending today?",
                    'Show me current Twitter trends',
                    'What are people talking about on social media?',
                ],
            )
        ],
    )


    remote_trending_agent = RemoteA2aAgent(
        name='find_trends',
        description='Searches for current trending topics on social media',
        agent_card=f'http://localhost:10020{AGENT_CARD_WELL_KNOWN_PATH}',
    )


    # Create the Trend Analyzer ADK Agent
    analyzer_agent = Agent(
        model='gemini-2.5-pro',
        name='trend_analyzer_agent',
        instruction="""
        You are a data analyst specializing in trend analysis. When given a trending topic,
        perform deep research to find quantitative data and insights.

        For each trend you analyze:
        1. Search for statistics, numbers, and metrics related to the trend
        2. Look for:
        - Engagement metrics (views, shares, mentions)
        - Growth rates and timeline
        - Geographic distribution
        - Related hashtags or keywords
        3. Provide concrete numbers and data points

        Keep it somehow concise

        Always prioritize quantitative information over qualitative descriptions.
        """,
        tools=[google_search],
    )

    print('Trend Analyzer Agent created successfully!')


    analyzer_agent_card = AgentCard(
        name='Trend Analyzer Agent',
        url='http://localhost:10021',
        description='Performs deep analysis of trends with quantitative data',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='analyze_trend',
                name='Analyze Trend',
                description='Provides quantitative analysis of a specific trend',
                tags=['analysis', 'data', 'metrics', 'statistics'],
                examples=[
                    'Analyze the #ClimateChange trend',
                    'Get metrics for the Taylor Swift trend',
                    'Provide data analysis for AI adoption trend',
                ],
            )
        ],
    )


    remote_analyzer_agent = RemoteA2aAgent(
        name='analyze_trend',
        description='Provides quantitative analysis of a specific trend',
        agent_card=f'http://localhost:10021{AGENT_CARD_WELL_KNOWN_PATH}',
    )


    # Create the Host ADK Agent
    host_agent = SequentialAgent(
        name='trend_analysis_host',
        sub_agents=[remote_trending_agent, remote_analyzer_agent],
    )


    host_agent_card = AgentCard(
        name='Trend Analysis Host',
        url='http://localhost:10022',
        description='Orchestrates, sequentially, trend discovery and analysis using specialized agents',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['application/json'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='comprehensive_trend_analysis',
                name='Comprehensive Trend Analysis',
                description='Finds trending topics and provides deep analysis of the most relevant one',
                tags=['trends', 'analysis', 'orchestration', 'insights'],
                examples=[
                    'Analyze current trends',
                    "What's trending and why is it important?",
                    'Give me a comprehensive trend report',
                ],
            )
        ],
    )

    

    # Apply nest_asyncio
    nest_asyncio.apply()

    # Store server tasks
    server_tasks: list[asyncio.Task] = []


    async def run_agent_server(agent, agent_card, port) -> None:
        """Run a single agent server."""
        app = create_agent_a2a_server(agent, agent_card)

        config = uvicorn.Config(
            app.build(),
            host='127.0.0.1',
            port=port,
            log_level='warning',
            loop='none',  # Important: let uvicorn use the current loop
        )

        server = uvicorn.Server(config)
        await server.serve()


    async def start_all_servers() -> None:
        """Start all servers in the same event loop."""
        # Create tasks for all servers
        tasks = [
            asyncio.create_task(
                run_agent_server(trending_agent, trending_agent_card, 10020)
            ),
            asyncio.create_task(
                run_agent_server(analyzer_agent, analyzer_agent_card, 10021)
            ),
            asyncio.create_task(
                run_agent_server(host_agent, host_agent_card, 10022)
            ),
        ]

        # Give servers time to start
        await asyncio.sleep(2)

        print('✅ All agent servers started!')
        print('   - Trending Agent: http://127.0.0.1:10020')
        print('   - Analyzer Agent: http://127.0.0.1:10021')
        print('   - Host Agent: http://127.0.0.1:10022')

        # Keep servers running
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print('Shutting down servers...')


    # Run in a background thread


    def run_servers_in_background() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_all_servers())


    # Start the thread
    server_thread = threading.Thread(target=run_servers_in_background, daemon=True)
    server_thread.start()

    # Wait for servers to be ready
    time.sleep(3)

    a2a_client = A2ASimpleClient()


    async def test_trending_topics() -> None:
        """Test trending topics agent."""
        trending_topics = await a2a_client.create_task(
            'http://localhost:10020', "What's trending today?"
        )
        print(trending_topics)


    # Run the async function
    asyncio.run(test_trending_topics())


    async def test_analysis() -> None:
        """Test analysis agent."""
        analysis = await a2a_client.create_task(
            'http://localhost:10021', 'Analyze the trend AI in Social Media'
        )
        print(analysis)


    # Run the async function
    asyncio.run(test_analysis())


    async def test_host_analysis() -> None:
        """Test host analysis agent."""
        host_analysis = await a2a_client.create_task(
            'http://localhost:10022',
            'Find the most relevant trends in the web today, choose randomly one of the top '
            'trends, and give me a complete analysis of it with quantitative data',
        )
        print(host_analysis)


    # Run the async function
    asyncio.run(test_host_analysis())


    print("im here!")

    asyncio.sleep(60)

if __name__ == '__main__':
    try:
        asyncio.run(run_stuff())
    except Exception as e:
        print(e)