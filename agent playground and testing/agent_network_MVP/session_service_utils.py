# @title Import necessary libraries
# pure script, not notebook
import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts

from google.adk.tools.tool_context import ToolContext

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from typing import Optional

from google.adk.tools.base_tool import BaseTool
#from google.adk.tools.tool_context import ToolContext
from typing import Optional, Dict, Any # For type hints


# --- Session Management --- we should make a new one each time we want a new chat
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
#session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

async def get_session_basic(APP_NAME, USER_ID, SESSION_ID, session_service):
    retrieved_session = await session_service.get_session(app_name=APP_NAME,
                                                                user_id=USER_ID,
                                                                session_id = SESSION_ID)
    return retrieved_session

async def create_basic_session(APP_NAME, USER_ID, SESSION_ID):
    # Create the specific session where the conversation will happen
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    return session

async def create_stateful_session(APP_NAME, USER_ID, SESSION_ID, initial_state):
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, # Use the consistent app name
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state # <<< Initialize state during creation
    )
    print(f"✅ Session '{SESSION_ID}' created for user '{USER_ID}'.")
    return session