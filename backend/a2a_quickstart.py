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
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Import existing ADK agents
from adk_agents.secretary.agent import root_agent as secretary_base_agent
from adk_agents.hiring_manager.agent import root_agent as hiring_manager_base_agent
from adk_agents.data_analyst.agent import root_agent as data_analyst_base_agent
from adk_agents.researcher.agent import root_agent as researcher_base_agent
from adk_agents.content_creator.agent import root_agent as content_creator_base_agent
from adk_agents.adk_agent_builder_assistant.agent import root_agent as agent_builder_base_agent
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

async def run_stuff():
    patched_module = PatchedClientModule(real_client_module)
    sys.modules['a2a.client.client'] = patched_module  # type: ignore



    # Load environment variables first
    load_dotenv()
    
    # Set Google Cloud Configuration
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')
    os.environ['GOOGLE_CLOUD_LOCATION'] = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    
    # Check for required API key
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print('❌ ERROR: Missing Google API Key!')
        print('Please create a .env file with your GOOGLE_API_KEY:')
        print('GOOGLE_API_KEY=your_actual_api_key_here')
        print('\nGet your API key from: https://aistudio.google.com/apikey')
        return

    print(' Environment variables configured:')
    print(f'GOOGLE_GENAI_USE_VERTEXAI: {os.environ["GOOGLE_GENAI_USE_VERTEXAI"]}')
    print(f'GOOGLE_CLOUD_PROJECT: {os.environ["GOOGLE_CLOUD_PROJECT"]}')
    print(f'GOOGLE_CLOUD_LOCATION: {os.environ["GOOGLE_CLOUD_LOCATION"]}')
    print(f'GOOGLE_API_KEY: {" Set" if google_api_key else "❌ Missing"}')


    # Authenticate your notebook environment (Colab only)
    # if 'google.colab' in sys.modules:
    #     from google.colab import auth

    #     auth.authenticate_user(project_id=os.environ['GOOGLE_CLOUD_PROJECT'])

    # Setup logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )




    # Use existing ADK agents from the platform
    secretary_agent = secretary_base_agent
    hiring_manager_agent = hiring_manager_base_agent
    data_analyst_agent = data_analyst_base_agent
    researcher_agent = researcher_base_agent
    content_creator_agent = content_creator_base_agent
    agent_builder_agent = agent_builder_base_agent

    print('Platform agents loaded successfully!')


    # Create Agent Cards for platform agents
    secretary_agent_card = AgentCard(
        name='Secretary Agent',
        url='http://localhost:10020',
        description='Main orchestrator that coordinates and delegates tasks to specialized employee agents',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='coordinate_tasks',
                name='Coordinate Tasks',
                description='Understands user requests and routes them to appropriate specialists',
                tags=['coordination', 'routing', 'assistance', 'guidance'],
                examples=[
                    'I need help with data analysis',
                    'Can you help me create content for my blog?',
                    'What can this platform do?',
                ],
            )
        ],
    )

    hiring_manager_agent_card = AgentCard(
        name='Hiring Manager Agent',
        url='http://localhost:10021',
        description='Creates and manages new employee agents based on organizational needs',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='create_agents',
                name='Create New Agents',
                description='Analyzes needs and creates specialized agents with specific capabilities',
                tags=['agent creation', 'specialization', 'management', 'workforce'],
                examples=[
                    'I need a specialized marketing agent',
                    'Create an agent for financial analysis',
                    'We need more research capabilities',
                ],
            )
        ],
    )

    data_analyst_agent_card = AgentCard(
        name='Data Analyst Agent',
        url='http://localhost:10022',
        description='Analyzes data, generates insights, and creates statistical reports',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['application/json'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='analyze_data',
                name='Analyze Data',
                description='Performs statistical analysis, identifies patterns, and generates insights',
                tags=['data analysis', 'statistics', 'insights', 'reporting', 'trends'],
                examples=[
                    'Analyze this sales data for trends',
                    'Generate a statistical report on user behavior',
                    'What patterns do you see in this dataset?',
                ],
            )
        ],
    )

    researcher_agent_card = AgentCard(
        name='Researcher Agent',
        url='http://localhost:10023',
        description='Conducts comprehensive research, fact-checking, and information synthesis',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='conduct_research',
                name='Conduct Research',
                description='Performs thorough research, fact-checking, and information gathering',
                tags=['research', 'fact-checking', 'information', 'sources', 'verification'],
                examples=[
                    'Research the latest developments in AI',
                    'Fact-check this information about climate change',
                    'Find authoritative sources on renewable energy',
                ],
            )
        ],
    )

    content_creator_agent_card = AgentCard(
        name='Content Creator Agent',
        url='http://localhost:10024',
        description='Creates engaging content, marketing copy, and creative communications',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='create_content',
                name='Create Content',
                description='Writes blog posts, marketing copy, social media content, and creative communications',
                tags=['content creation', 'writing', 'marketing', 'social media', 'creative'],
                examples=[
                    'Write a blog post about sustainable technology',
                    'Create social media content for our product launch',
                    'Help me improve this marketing copy',
                ],
            )
        ],
    )

    agent_builder_agent_card = AgentCard(
        name='Agent Builder Assistant',
        url='http://localhost:10026',
        description='Intelligent assistant for building ADK multi-agent systems using YAML configurations',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='build_agents',
                name='Build Agent Systems',
                description='Creates and configures ADK multi-agent systems with YAML configurations',
                tags=['agent building', 'system design', 'yaml configuration', 'multi-agent', 'architecture'],
                examples=[
                    'Help me build a multi-agent system for customer support',
                    'Create a YAML configuration for a data processing pipeline',
                    'Design an agent architecture for content management',
                ],
            )
        ],
    )


    # Create Remote A2A Agents for inter-agent communication
    remote_secretary_agent = RemoteA2aAgent(
        name='coordinate_tasks',
        description='Main orchestrator that coordinates and delegates tasks to specialized employee agents',
        agent_card=f'http://localhost:10020{AGENT_CARD_WELL_KNOWN_PATH}',
    )

    remote_hiring_manager_agent = RemoteA2aAgent(
        name='create_agents',
        description='Creates and manages new employee agents based on organizational needs',
        agent_card=f'http://localhost:10021{AGENT_CARD_WELL_KNOWN_PATH}',
    )

    remote_data_analyst_agent = RemoteA2aAgent(
        name='analyze_data',
        description='Analyzes data, generates insights, and creates statistical reports',
        agent_card=f'http://localhost:10022{AGENT_CARD_WELL_KNOWN_PATH}',
    )

    remote_researcher_agent = RemoteA2aAgent(
        name='conduct_research',
        description='Conducts comprehensive research, fact-checking, and information synthesis',
        agent_card=f'http://localhost:10023{AGENT_CARD_WELL_KNOWN_PATH}',
    )

    remote_content_creator_agent = RemoteA2aAgent(
        name='create_content',
        description='Creates engaging content, marketing copy, and creative communications',
        agent_card=f'http://localhost:10024{AGENT_CARD_WELL_KNOWN_PATH}',
    )

    remote_agent_builder_agent = RemoteA2aAgent(
        name='build_agents',
        description='Intelligent assistant for building ADK multi-agent systems using YAML configurations',
        agent_card=f'http://localhost:10026{AGENT_CARD_WELL_KNOWN_PATH}',
    )


    # Create the Master Orchestrator Agent
    master_orchestrator_agent = SequentialAgent(
        name='platform_orchestrator',
        sub_agents=[
            remote_secretary_agent,
            remote_hiring_manager_agent,
            remote_data_analyst_agent,
            remote_researcher_agent,
            remote_content_creator_agent,
            remote_agent_builder_agent,
        ],
    )

    master_orchestrator_agent_card = AgentCard(
        name='Platform Orchestrator',
        url='http://localhost:10025',
        description='Master orchestrator that coordinates all platform agents for complex multi-step tasks',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['application/json'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='orchestrate_platform',
                name='Orchestrate Platform Tasks',
                description='Coordinates complex tasks across multiple specialized agents',
                tags=['orchestration', 'coordination', 'multi-agent', 'workflow', 'delegation'],
                examples=[
                    'Research AI trends and create a comprehensive report',
                    'Analyze market data and create marketing content based on insights',
                    'Help me understand and delegate this complex project',
                ],
            )
        ],
    )

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
        # Create tasks for all platform agents
        tasks = [
            asyncio.create_task(
                run_agent_server(secretary_agent, secretary_agent_card, 10020)
            ),
            asyncio.create_task(
                run_agent_server(hiring_manager_agent, hiring_manager_agent_card, 10021)
            ),
            asyncio.create_task(
                run_agent_server(data_analyst_agent, data_analyst_agent_card, 10022)
            ),
            asyncio.create_task(
                run_agent_server(researcher_agent, researcher_agent_card, 10023)
            ),
            asyncio.create_task(
                run_agent_server(content_creator_agent, content_creator_agent_card, 10024)
            ),
            asyncio.create_task(
                run_agent_server(agent_builder_agent, agent_builder_agent_card, 10026)
            ),
            asyncio.create_task(
                run_agent_server(master_orchestrator_agent, master_orchestrator_agent_card, 10025)
            ),
        ]

        # Give servers time to start
        await asyncio.sleep(3)

        print(' All platform agent servers started!')
        print('   - Secretary Agent: http://127.0.0.1:10020')
        print('   - Hiring Manager Agent: http://127.0.0.1:10021')
        print('   - Data Analyst Agent: http://127.0.0.1:10022')
        print('   - Researcher Agent: http://127.0.0.1:10023')
        print('   - Content Creator Agent: http://127.0.0.1:10024')
        print('   - Master Orchestrator: http://127.0.0.1:10025')

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
    time.sleep(4)

    a2a_client = A2ASimpleClient()

    print('\n🧪 Testing Platform Agents via A2A Protocol...\n')

    async def test_secretary_agent() -> None:
        """Test secretary agent."""
        print('📋 Testing Secretary Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10020', 'I need help with data analysis and content creation for my business.'
        )
        print(f'Secretary Response: {response}\n')

    async def test_hiring_manager_agent() -> None:
        """Test hiring manager agent."""
        print('🏢 Testing Hiring Manager Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10021', 'I need a specialized agent for financial analysis and budgeting.'
        )
        print(f'Hiring Manager Response: {response}\n')

    async def test_data_analyst_agent() -> None:
        """Test data analyst agent."""
        print('📊 Testing Data Analyst Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10022', 'Analyze the performance trends of e-commerce companies in Q4 2024.'
        )
        print(f'Data Analyst Response: {response}\n')

    async def test_researcher_agent() -> None:
        """Test researcher agent."""
        print('🔍 Testing Researcher Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10023', 'Research the latest developments in sustainable energy technologies.'
        )
        print(f'Researcher Response: {response}\n')

    async def test_content_creator_agent() -> None:
        """Test content creator agent."""
        print('✍️ Testing Content Creator Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10024', 'Create a compelling blog post about the future of AI in healthcare.'
        )
        print(f'Content Creator Response: {response}\n')

    async def test_master_orchestrator() -> None:
        """Test master orchestrator agent."""
        print('🎭 Testing Master Orchestrator Agent...')
        response = await a2a_client.create_task(
            'http://localhost:10025',
            'Research current AI trends, analyze the market data, and create a comprehensive report with marketing content.'
        )
        print(f'Master Orchestrator Response: {response}\n')

    # Run all tests
    asyncio.run(test_secretary_agent())
    asyncio.run(test_hiring_manager_agent())
    asyncio.run(test_data_analyst_agent())
    asyncio.run(test_researcher_agent())
    asyncio.run(test_content_creator_agent())
    asyncio.run(test_master_orchestrator())

    print(' All agent tests completed!')

if __name__ == '__main__':
    asyncio.run(run_stuff())