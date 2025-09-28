"""Main application for the A2A Agent Management Platform."""

# Apply compatibility patch first, before any other A2A imports
from compatibility_patch import apply_compatibility_patch
apply_compatibility_patch()

import asyncio
import logging
import signal
import sys
import threading
import time
import uvicorn
from typing import List, Optional

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from google.adk.a2a.executor.a2a_agent_executor import (
    A2aAgentExecutor,
    A2aAgentExecutorConfig,
)
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService

from config import (
    validate_config, 
    SECRETARY_PORT, 
    HIRING_MANAGER_PORT, 
    EMPLOYEE_BASE_PORT,
    PLATFORM_HOST,
    LOG_LEVEL
)
from secretary_agent import SecretaryAgent
from hiring_manager import HiringManagerAgent, HiringManagerExecutor
from agents import EMPLOYEE_AGENTS, EmployeeAgentExecutor
from agent_registry import get_global_registry

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentPlatform:
    """Main platform for managing A2A agents."""
    
    def __init__(self):
        self.servers: List[uvicorn.Server] = []
        self.server_tasks: List[asyncio.Task] = []
        self.registry = get_global_registry()
        self.secretary = SecretaryAgent()
        self.shutdown_event = asyncio.Event()
    
    async def start_hiring_manager(self):
        """Start the Hiring Manager agent server."""
        try:
            logger.info("Starting Hiring Manager agent...")
            
            # Create executor
            executor = HiringManagerExecutor()
            
            # Create request handler
            request_handler = DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore(),
            )
            
            # Create agent card
            agent_card = HiringManagerAgent.get_agent_card()
            
            # Create A2A application
            app = A2AStarletteApplication(
                agent_card=agent_card,
                http_handler=request_handler,
            )
            
            # Create and start server
            config = uvicorn.Config(
                app.build(),
                host=PLATFORM_HOST,
                port=HIRING_MANAGER_PORT,
                log_level='warning',
            )
            
            server = uvicorn.Server(config)
            self.servers.append(server)
            
            # Start server in background first
            server_task = asyncio.create_task(server.serve())
            self.server_tasks.append(server_task)
            
            # Wait for server to be ready
            await asyncio.sleep(2)
            
            # Register with global registry after server is ready
            try:
                async with self.registry:
                    success = await self.registry.register_agent(f"http://{PLATFORM_HOST}:{HIRING_MANAGER_PORT}")
                    if success:
                        logger.info(f"Hiring Manager started and registered on http://{PLATFORM_HOST}:{HIRING_MANAGER_PORT}")
                    else:
                        logger.warning(f"Hiring Manager started but registration failed")
            except Exception as reg_error:
                logger.error(f"Failed to register Hiring Manager: {reg_error}")
            
            # Wait for the server task to complete (or be cancelled)
            await server_task
            
        except Exception as e:
            logger.error(f"Failed to start Hiring Manager: {e}")
            raise
    
    async def start_secretary_agent(self):
        """Start the Secretary agent server."""
        try:
            logger.info("Starting Secretary agent...")
            
            # Initialize secretary with available agents
            await self.secretary.initialize()
            sequential_agent = self.secretary.get_sequential_agent()
            
            if not sequential_agent:
                logger.warning("Secretary agent has no employee agents - starting with limited functionality")
                # Create a basic agent for standalone operation
                from google.adk.agents import Agent
                standalone_agent = Agent(
                    model="gemini-2.0-flash-001",
                    name='secretary_standalone',
                    instruction="""
                    You are the Secretary Agent operating in standalone mode.
                    
                    Currently, no employee agents are available, but you can still:
                    1. Provide general assistance and guidance
                    2. Help users understand what the platform can do
                    3. Direct them to the Hiring Manager to create new agents
                    
                    Let users know that they can create specialized agents via the Hiring Manager
                    at http://127.0.0.1:10001 for more advanced capabilities.
                    """
                )
                sequential_agent = standalone_agent
            
            # Create runner for the sequential agent
            runner = Runner(
                app_name='secretary_agent',
                agent=sequential_agent,
                artifact_service=InMemoryArtifactService(),
                session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService(),
            )
            
            # Create A2A executor
            config = A2aAgentExecutorConfig()
            executor = A2aAgentExecutor(runner=runner, config=config)
            
            # Create request handler
            request_handler = DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore(),
            )
            
            # Create agent card
            agent_card = SecretaryAgent.get_agent_card()
            
            # Create A2A application
            app = A2AStarletteApplication(
                agent_card=agent_card,
                http_handler=request_handler,
            )
            
            # Create and start server
            config = uvicorn.Config(
                app.build(),
                host=PLATFORM_HOST,
                port=SECRETARY_PORT,
                log_level='warning',
            )
            
            server = uvicorn.Server(config)
            self.servers.append(server)
            
            # Start server in background
            server_task = asyncio.create_task(server.serve())
            self.server_tasks.append(server_task)
            
            logger.info(f"Secretary Agent started on http://{PLATFORM_HOST}:{SECRETARY_PORT}")
            
            # Wait for the server task to complete (or be cancelled)
            await server_task
            
        except Exception as e:
            logger.error(f"Failed to start Secretary Agent: {e}")
            raise
    
    async def start_sample_employee_agents(self):
        """Start sample employee agents."""
        try:
            logger.info("Starting sample employee agents...")
            
            port = EMPLOYEE_BASE_PORT
            
            for agent_type, agent_info in EMPLOYEE_AGENTS.items():
                try:
                    logger.info(f"Starting {agent_type} agent on port {port}...")
                    
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
                    
                    # Create server task
                    config = uvicorn.Config(
                        app.build(),
                        host=PLATFORM_HOST,
                        port=port,
                        log_level='warning',
                    )
                    
                    server = uvicorn.Server(config)
                    self.servers.append(server)
                    
                    # Start server in background
                    task = asyncio.create_task(server.serve())
                    self.server_tasks.append(task)
                    
                    # Wait for server to be ready
                    await asyncio.sleep(2)
                    
                    # Register with global registry after server is ready
                    try:
                        async with self.registry:
                            success = await self.registry.register_agent(f"http://{PLATFORM_HOST}:{port}")
                            if success:
                                logger.info(f"{agent_type} agent started and registered on http://{PLATFORM_HOST}:{port}")
                            else:
                                logger.warning(f"{agent_type} agent started but registration failed on port {port}")
                    except Exception as reg_error:
                        logger.error(f"Failed to register {agent_type} agent: {reg_error}")
                    
                    port += 1
                    
                except Exception as e:
                    logger.error(f"Failed to start {agent_type} agent: {e}")
                    port += 1
                    continue
            
            logger.info("Sample employee agents startup completed")
            
        except Exception as e:
            logger.error(f"Failed to start sample employee agents: {e}")
    
    async def start_platform(self):
        """Start the entire platform."""
        try:
            logger.info("🚀 Starting A2A Agent Management Platform...")
            
            # Validate configuration
            validate_config()
            
            # Start sample employee agents first
            await self.start_sample_employee_agents()
            
            # Give agents more time to be fully ready
            logger.info("Waiting for employee agents to be fully ready...")
            await asyncio.sleep(5)
            
            # Start hiring manager first
            logger.info("Starting Hiring Manager...")
            hiring_task = asyncio.create_task(self.start_hiring_manager())
            
            # Give hiring manager time to start
            await asyncio.sleep(3)
            
            # Start secretary agent last (it needs to discover other agents)
            logger.info("Starting Secretary Agent...")
            secretary_task = asyncio.create_task(self.start_secretary_agent())
            
            # Wait for shutdown signal
            await self.shutdown_event.wait()
            
            # Cancel all tasks
            hiring_task.cancel()
            secretary_task.cancel()
            for task in self.server_tasks:
                task.cancel()
            
            logger.info("Platform shutdown completed")
            
        except Exception as e:
            logger.error(f"Platform startup failed: {e}")
            raise
    
    def shutdown(self):
        """Initiate platform shutdown."""
        logger.info("Initiating platform shutdown...")
        self.shutdown_event.set()

def signal_handler(signum, frame, platform):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    platform.shutdown()

async def main():
    """Main entry point."""
    platform = AgentPlatform()
    
    # Set up signal handlers
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, lambda s, f: signal_handler(s, f, platform))
    
    try:
        print("🤖 A2A Agent Management Platform")
        print("=" * 40)
        print(f"Secretary Agent: http://{PLATFORM_HOST}:{SECRETARY_PORT}")
        print(f"Hiring Manager: http://{PLATFORM_HOST}:{HIRING_MANAGER_PORT}")
        print(f"Employee Agents: http://{PLATFORM_HOST}:{EMPLOYEE_BASE_PORT}+")
        print("=" * 40)
        print("Press Ctrl+C to stop")
        print()
        
        await platform.start_platform()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Platform error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
        sys.exit(0)
