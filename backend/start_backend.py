#!/usr/bin/env python3
"""
Backend Server Starter
Starts the FastAPI backend server that communicates with A2A agents.
"""

import os
import sys
import time
import threading
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_backend_server():
    """Start the FastAPI backend server."""
    try:
        import uvicorn
        from main import app
        
        logger.info("🚀 Starting FastAPI backend server...")
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
        
    except Exception as e:
        logger.error(f"❌ Failed to start backend server: {e}")
        sys.exit(1)

def main():
    """Main function."""
    # Load environment variables
    load_dotenv()
    
    logger.info("🎯 Starting AI Agent Management Platform Backend")
    logger.info("📡 Backend will be available at: http://localhost:8001")
    logger.info("📋 API Documentation: http://localhost:8001/docs")
    logger.info("🤖 Agent Status: http://localhost:8001/agents/status")
    logger.info("💬 Chat Endpoint: http://localhost:8001/chat")
    logger.info("")
    
    # Start the backend server
    start_backend_server()

if __name__ == "__main__":
    main()
