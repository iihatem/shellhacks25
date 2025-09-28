#!/usr/bin/env python3
"""Test startup without full platform run."""

import asyncio
import sys
import os
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compatibility_patch import apply_compatibility_patch
apply_compatibility_patch()

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_startup_components():
    """Test that all components can be imported and initialized."""
    
    print("🧪 Testing Platform Components...")
    print("=" * 40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from main import AgentPlatform
        from secretary_agent import SecretaryAgent
        from hiring_manager import HiringManagerExecutor
        from agents import EMPLOYEE_AGENTS, EmployeeAgentExecutor
        print("   ✅ All imports successful")
        
        # Test agent creation
        print("2. Testing agent creation...")
        for agent_type, agent_info in EMPLOYEE_AGENTS.items():
            agent = agent_info['agent']
            print(f"   ✅ {agent_type}: {agent.name}")
        
        # Test platform initialization
        print("3. Testing platform initialization...")
        platform = AgentPlatform()
        print("   ✅ Platform initialized")
        
        # Test secretary initialization
        print("4. Testing secretary initialization...")
        secretary = SecretaryAgent()
        print("   ✅ Secretary initialized")
        
        # Test hiring manager initialization
        print("5. Testing hiring manager initialization...")
        hiring_manager = HiringManagerExecutor()
        print("   ✅ Hiring manager initialized")
        
        print("=" * 40)
        print("🎉 All components test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_startup_components())
    sys.exit(0 if success else 1)
