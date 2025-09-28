#!/usr/bin/env python3
"""
AI Agent Management Platform Startup Script
Starts both A2A agents and the FastAPI backend server with proper threading.
"""

import os
import sys
import time
import threading
import logging
import signal
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlatformManager:
    """Manages the entire AI Agent Management Platform."""
    
    def __init__(self):
        self.agent_manager = None
        self.backend_thread = None
        self.running = False
        
    def start_agents(self):
        """Start A2A agents in a separate thread."""
        try:
            from start_a2a_agents import A2AAgentManager
            
            logger.info("🤖 Starting A2A agents...")
            self.agent_manager = A2AAgentManager()
            
            if self.agent_manager.start():
                logger.info("✅ A2A agents started successfully")
                return True
            else:
                logger.error("❌ Failed to start A2A agents")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting A2A agents: {e}")
            return False
    
    def start_backend(self):
        """Start the FastAPI backend server in a separate thread."""
        try:
            import uvicorn
            from main import app
            
            logger.info("🚀 Starting FastAPI backend server...")
            uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
            
        except Exception as e:
            logger.error(f"❌ Error starting backend server: {e}")
    
    def start_backend_thread(self):
        """Start backend server in a background thread."""
        self.backend_thread = threading.Thread(target=self.start_backend, daemon=True)
        self.backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        if self.backend_thread.is_alive():
            logger.info("✅ Backend server started successfully")
            return True
        else:
            logger.error("❌ Backend server failed to start")
            return False
    
    def start_platform(self):
        """Start the entire platform."""
        logger.info("🎯 Starting AI Agent Management Platform...")
        logger.info("=" * 60)
        
        # Load environment variables
        load_dotenv()
        
        # Start A2A agents
        if not self.start_agents():
            logger.error("❌ Cannot start platform without A2A agents")
            return False
        
        # Start backend server
        if not self.start_backend_thread():
            logger.error("❌ Cannot start platform without backend server")
            return False
        
        self.running = True
        
        # Display platform information
        self.display_platform_info()
        
        return True
    
    def display_platform_info(self):
        """Display platform information and endpoints."""
        logger.info("")
        logger.info("🎉 AI Agent Management Platform is now running!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("📡 Backend API:")
        logger.info("   • Main API: http://localhost:8001")
        logger.info("   • API Docs: http://localhost:8001/docs")
        logger.info("   • Agent Status: http://localhost:8001/agents/status")
        logger.info("   • Chat Endpoint: http://localhost:8001/chat")
        logger.info("")
        logger.info("🤖 A2A Agents:")
        logger.info("   • Secretary Agent: http://127.0.0.1:10020")
        logger.info("   • Hiring Manager: http://127.0.0.1:10021")
        logger.info("   • Data Analyst: http://127.0.0.1:10022")
        logger.info("   • Researcher: http://127.0.0.1:10023")
        logger.info("   • Content Creator: http://127.0.0.1:10024")
        logger.info("")
        logger.info("🌐 Frontend:")
        logger.info("   • Start frontend: cd frontend && npm run dev")
        logger.info("   • Frontend URL: http://localhost:3000")
        logger.info("")
        logger.info("💡 Usage:")
        logger.info("   • Chat with agents through the frontend interface")
        logger.info("   • Messages are automatically routed to appropriate agents")
        logger.info("   • Use Ctrl+C to stop the platform")
        logger.info("")
        logger.info("🔄 Platform is running... Press Ctrl+C to stop")
        logger.info("=" * 60)
    
    def stop_platform(self):
        """Stop the entire platform."""
        logger.info("🛑 Stopping AI Agent Management Platform...")
        self.running = False
        
        if self.agent_manager:
            self.agent_manager.stop()
        
        logger.info("✅ Platform stopped successfully")
    
    def run(self):
        """Run the platform."""
        if not self.start_platform():
            logger.error("❌ Failed to start platform")
            sys.exit(1)
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_platform()

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info("🛑 Received shutdown signal...")
    if 'platform_manager' in globals():
        platform_manager.stop_platform()
    sys.exit(0)

def main():
    """Main function."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run platform manager
    global platform_manager
    platform_manager = PlatformManager()
    platform_manager.run()

if __name__ == "__main__":
    main()
