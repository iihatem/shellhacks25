"""Simple startup script for the A2A platform."""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    print("🤖 A2A Agent Management Platform")
    print("=" * 40)
    print("Starting up...")
    print()
    print("📋 Startup sequence:")
    print("1. Employee agents (ports 10002-10004)")
    print("2. Hiring Manager (port 10001)")  
    print("3. Secretary Agent (port 10000)")
    print()
    print("⏳ This may take 10-15 seconds...")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutdown complete")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
