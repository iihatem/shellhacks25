"""Test script for the A2A Agent Management Platform."""

# Apply compatibility patch first
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compatibility_patch import apply_compatibility_patch
apply_compatibility_patch()

import asyncio
import httpx
import json
import logging
import time
from typing import Dict, Any, List

from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.types import AgentCard, TransportProtocol
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

from config import PLATFORM_HOST, SECRETARY_PORT, HIRING_MANAGER_PORT, EMPLOYEE_BASE_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class A2APlatformTester:
    """Test suite for the A2A platform."""
    
    def __init__(self):
        self.base_urls = {
            'secretary': f'http://{PLATFORM_HOST}:{SECRETARY_PORT}',
            'hiring_manager': f'http://{PLATFORM_HOST}:{HIRING_MANAGER_PORT}',
            'data_analyst': f'http://{PLATFORM_HOST}:{EMPLOYEE_BASE_PORT}',
            'content_creator': f'http://{PLATFORM_HOST}:{EMPLOYEE_BASE_PORT + 1}',
            'researcher': f'http://{PLATFORM_HOST}:{EMPLOYEE_BASE_PORT + 2}',
        }
        self.httpx_client: httpx.AsyncClient = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.httpx_client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.httpx_client:
            await self.httpx_client.aclose()
    
    async def test_agent_discovery(self) -> Dict[str, bool]:
        """Test agent card discovery for all agents."""
        results = {}
        
        for agent_name, base_url in self.base_urls.items():
            try:
                card_url = f"{base_url}{AGENT_CARD_WELL_KNOWN_PATH}"
                response = await self.httpx_client.get(card_url)
                response.raise_for_status()
                
                card_data = response.json()
                agent_card = AgentCard(**card_data)
                
                print(f" {agent_name}: {agent_card.name}")
                print(f"   Description: {agent_card.description}")
                print(f"   Skills: {len(agent_card.skills or [])} skills")
                print()
                
                results[agent_name] = True
                
            except Exception as e:
                print(f"❌ {agent_name}: Failed to discover - {e}")
                results[agent_name] = False
        
        return results
    
    async def test_agent_communication(self, agent_name: str, message: str) -> bool:
        """Test communication with a specific agent."""
        try:
            base_url = self.base_urls[agent_name]
            
            # Get agent card
            card_url = f"{base_url}{AGENT_CARD_WELL_KNOWN_PATH}"
            response = await self.httpx_client.get(card_url)
            response.raise_for_status()
            
            agent_card = AgentCard(**response.json())
            
            # Create A2A client
            config = ClientConfig(
                httpx_client=self.httpx_client,
                supported_transports=[TransportProtocol.jsonrpc],
                use_client_preference=True,
            )
            
            factory = ClientFactory(config)
            client = factory.create(agent_card)
            
            # Send message
            message_obj = create_text_message_object(content=message)
            
            print(f"🔄 Testing {agent_name} with message: '{message}'")
            
            responses = []
            async for response in client.send_message(message_obj):
                responses.append(response)
            
            if responses and isinstance(responses[0], tuple) and len(responses[0]) > 0:
                task = responses[0][0]
                try:
                    response_text = task.artifacts[0].parts[0].root.text
                    print(f" {agent_name} response: {response_text[:200]}...")
                    return True
                except (AttributeError, IndexError):
                    print(f" {agent_name} responded (could not extract text)")
                    return True
            else:
                print(f"❌ {agent_name}: No response received")
                return False
                
        except Exception as e:
            print(f"❌ {agent_name}: Communication failed - {e}")
            return False
    
    async def test_secretary_coordination(self) -> bool:
        """Test Secretary agent's coordination capabilities."""
        test_messages = [
            "I need help with data analysis and creating content about the results",
            "Research renewable energy trends and write a summary",
            "What can you help me with?",
        ]
        
        success_count = 0
        for message in test_messages:
            if await self.test_agent_communication('secretary', message):
                success_count += 1
            await asyncio.sleep(2)  # Give time between requests
        
        return success_count == len(test_messages)
    
    async def test_hiring_manager_capabilities(self) -> bool:
        """Test Hiring Manager's agent creation capabilities."""
        test_messages = [
            "What agent types can you create?",
            "Show me the agents you've created",
            "I need help understanding your capabilities",
        ]
        
        success_count = 0
        for message in test_messages:
            if await self.test_agent_communication('hiring_manager', message):
                success_count += 1
            await asyncio.sleep(2)
        
        return success_count == len(test_messages)
    
    async def test_employee_agents(self) -> Dict[str, bool]:
        """Test individual employee agent capabilities."""
        test_cases = {
            'data_analyst': "Analyze the trend of AI adoption in businesses over the last 5 years",
            'content_creator': "Write a short blog post about the benefits of renewable energy",
            'researcher': "Research the latest developments in quantum computing",
        }
        
        results = {}
        for agent_name, message in test_cases.items():
            results[agent_name] = await self.test_agent_communication(agent_name, message)
            await asyncio.sleep(2)
        
        return results
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all tests and return results."""
        print("🧪 Starting A2A Platform Comprehensive Tests")
        print("=" * 50)
        
        results = {
            'discovery': {},
            'secretary': False,
            'hiring_manager': False,
            'employees': {},
            'overall_success': False
        }
        
        # Test 1: Agent Discovery
        print("1. Testing Agent Discovery...")
        results['discovery'] = await self.test_agent_discovery()
        
        # Test 2: Secretary Agent
        print("2. Testing Secretary Agent Coordination...")
        results['secretary'] = await self.test_secretary_coordination()
        
        # Test 3: Hiring Manager
        print("3. Testing Hiring Manager...")
        results['hiring_manager'] = await self.test_hiring_manager_capabilities()
        
        # Test 4: Employee Agents
        print("4. Testing Employee Agents...")
        results['employees'] = await self.test_employee_agents()
        
        # Calculate overall success
        discovery_success = all(results['discovery'].values())
        employees_success = all(results['employees'].values())
        
        results['overall_success'] = (
            discovery_success and 
            results['secretary'] and 
            results['hiring_manager'] and 
            employees_success
        )
        
        # Print summary
        print("\n" + "=" * 50)
        print("🏁 Test Results Summary")
        print("=" * 50)
        
        print(f"Agent Discovery: {' PASS' if discovery_success else '❌ FAIL'}")
        print(f"Secretary Agent: {' PASS' if results['secretary'] else '❌ FAIL'}")
        print(f"Hiring Manager: {' PASS' if results['hiring_manager'] else '❌ FAIL'}")
        print(f"Employee Agents: {' PASS' if employees_success else '❌ FAIL'}")
        print()
        print(f"Overall Result: {'🎉 ALL TESTS PASSED' if results['overall_success'] else '⚠️  SOME TESTS FAILED'}")
        
        return results

async def main():
    """Main test function."""
    print("Waiting for platform to start up...")
    print("(This may take 15-20 seconds for all agents to be ready)")
    await asyncio.sleep(15)  # Give platform time to start properly
    
    async with A2APlatformTester() as tester:
        results = await tester.run_comprehensive_tests()
        
        if results['overall_success']:
            print("\n🎉 A2A Platform is working correctly!")
        else:
            print("\n⚠️  Some issues were found. Check the logs above.")
            return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
