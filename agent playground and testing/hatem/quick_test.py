#!/usr/bin/env python3
"""Quick test to verify the platform is working."""

import asyncio
import httpx
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compatibility_patch import apply_compatibility_patch
apply_compatibility_patch()

async def test_agents():
    """Test that all agents are reachable."""
    agents = {
        'Secretary': 'http://127.0.0.1:10000',
        'Hiring Manager': 'http://127.0.0.1:10001', 
        'Data Analyst': 'http://127.0.0.1:10002',
        'Content Creator': 'http://127.0.0.1:10003',
        'Researcher': 'http://127.0.0.1:10004',
    }
    
    print("🔍 Testing Agent Reachability...")
    print("=" * 40)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        all_good = True
        for name, url in agents.items():
            try:
                response = await client.get(f"{url}/.well-known/agent-card.json")
                if response.status_code == 200:
                    card = response.json()
                    print(f" {name}: {card.get('name', 'Unknown')}")
                else:
                    print(f"❌ {name}: HTTP {response.status_code}")
                    all_good = False
            except Exception as e:
                print(f"❌ {name}: {str(e)}")
                all_good = False
        
        print("=" * 40)
        if all_good:
            print("🎉 All agents are reachable!")
            return True
        else:
            print("⚠️  Some agents are not reachable")
            return False

if __name__ == "__main__":
    print("🧪 Quick Platform Test")
    print("Make sure the platform is running (python start.py)")
    print()
    
    success = asyncio.run(test_agents())
    sys.exit(0 if success else 1)
