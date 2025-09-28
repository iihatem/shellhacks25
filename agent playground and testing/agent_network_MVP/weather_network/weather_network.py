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

#custom functions
from agent_utils import create_project_manager, run_agent
import agents
import weather_tools
from session_service_utils import create_basic_session, create_stateful_session, get_session_basic


# async def call_agent_async(query: str, runner, user_id, session_id):
#   """Sends a query to the agent and prints the final response."""
#   print(f"\n>>> User Query: {query}")

#   # Prepare the user's message in ADK format
#   content = types.Content(role='user', parts=[types.Part(text=query)])

#   final_response_text = "Agent did not produce a final response." # Default
#   print("did we get here?")
#   # Key Concept: run_async executes the agent logic and yields Events.
#   # We iterate through events to find the final answer.
#   async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
#       # You can uncomment the line below to see *all* events during execution
#       # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

#       # Key Concept: is_final_response() marks the concluding message for the turn.
#       if event.is_final_response():
#           if event.content and event.content.parts:
#              # Assuming text response in the first part
#              final_response_text = event.content.parts[0].text
#           elif event.actions and event.actions.escalate: # Handle potential errors/escalations
#              final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
#           # Add more checks here if needed (e.g., specific error codes)
#           break # Stop processing events once the final response is found

#   print(f"<<< Agent Response: {final_response_text}")


# # @title Define the get_weather Tool
# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Args:
#         city (str): The name of the city (e.g., "New York", "London", "Tokyo").

#     Returns:
#         dict: A dictionary containing the weather information.
#               Includes a 'status' key ('success' or 'error').
#               If 'success', includes a 'report' key with weather details.
#               If 'error', includes an 'error_message' key.
#     """
#     print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
#     city_normalized = city.lower().replace(" ", "") # Basic normalization

#     # Mock weather data
#     mock_weather_db = {
#         "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
#         "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
#         "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
#     }

#     if city_normalized in mock_weather_db:
#         return mock_weather_db[city_normalized]
#     else:
#         return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")



# Gemini API Key (Get from Google AI Studio: https://aistudio.google.com/app/apikey)
os.environ["GOOGLE_API_KEY"] = "AIzaSyDNBCWaQeoef0XkzIgvlr-9tXJvFW7MFZE" # <--- REPLACE

# --- Verify Keys (Optional Check) ---
print("API Keys Set:")
print(f"Google API Key set: {'Yes' if os.environ.get('GOOGLE_API_KEY') and os.environ['GOOGLE_API_KEY'] != 'YOUR_GOOGLE_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

# --- Define Model Constants for easier use ---

# More supported models can be referenced here: https://ai.google.dev/gemini-api/docs/models#model-variations
MODEL_GEMINI_2_0_FLASH = "gemini-2.5-pro"

AGENT_MODEL = MODEL_GEMINI_2_0_FLASH # Starting with Gemini

# async def run_conversation():
async def run_conversation() -> None:
    # --- Session Management ---
    # Key Concept: SessionService stores conversation history & state.
    # InMemorySessionService is simple, non-persistent storage for this tutorial.
    session_service = InMemorySessionService()

    # Define constants for identifying the interaction context
    APP_NAME = "weather_tutorial_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001" # Using a fixed ID for simplicity

    # --- Session Management ---
    # Key Concept: SessionService stores conversation history & state.
    # InMemorySessionService is simple, non-persistent storage for this tutorial.
    # Create the specific session where the conversation will happen
    [current_session, current_session_service] = await create_basic_session(APP_NAME, USER_ID, SESSION_ID)
    # current_session_service = InMemorySessionService()
    # current_session = await current_session_service.create_session(
    #         app_name=APP_NAME, # Use the consistent app name
    #         user_id=USER_ID,
    #         session_id=SESSION_ID
            
    #     )
    # print(f"✅ Session '{SESSION_ID}' created for user '{USER_ID}'.")

    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    # --- Agent ----
    # Key Concept:
    # agent that is created to do the task/recieve query
    weather_agent = agents.get_weather_agent()

    # --- Runner ---
    # Key Concept: Runner orchestrates the agent execution loop.
    # this is used for running agents properly
    runner = create_project_manager(weather_agent, APP_NAME, current_session_service)
    print(f"Runner created for agent '{runner.agent.name}'.")

    query = "What is the weather in New York?"
    #print("we got here")
    #await run_agent(query, runner, USER_ID, SESSION_ID)
    #print("we got here!")


    # using a team based system with subagents
    # new session:
    # APP_NAME = "weather_tutorial_agent_team"
    # USER_ID = "user_1_agent_team"
    # SESSION_ID = "session_001_agent_team"
    # [current_session, current_session_service] = [None, None]
    [current_session, current_session_service] = await create_basic_session(APP_NAME, USER_ID, SESSION_ID)
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    # creates agent with subagents
    weather_agent_team = agents.get_weather_agent_2()
    #print("FUCK ME!")
    runner_agent_team = create_project_manager(weather_agent_team, APP_NAME, current_session_service)
    print(f"Runner created for agent '{weather_agent_team.name}'.")

    # we can look into something called InMemoryRunner
    # this runs the triple system to demonstrate the fact that it can minimize 
    # actual agents in use!
    query = "Hello there!"
    await run_agent(query, runner_agent_team, USER_ID, SESSION_ID)
    query = "What is the weather in New York?!"
    await run_agent(query, runner_agent_team, USER_ID, SESSION_ID)
    query = "Thanks, bye!"
    await run_agent(query, runner_agent_team, USER_ID, SESSION_ID)


    


    # now we are going to do  a few things that make it obvious we are doing something that takes in a state system
    # this is a longer one, and we also add guardrails and other things
    #classification stuff to do state by state
    SESSION_ID_STATEFUL = "session_state_demo_001"
    USER_ID_STATEFUL = "user_state_demo"

    # Define initial state data - user prefers Celsius initially
    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }

    # Create the session, providing the initial state
    [session_stateful, session_stateful_service]= await create_stateful_session(APP_NAME, USER_ID_STATEFUL, SESSION_ID_STATEFUL, initial_state)

    # now check to see what the state is:
    # Verify the initial state was set correctly
    retrieved_session = await get_session_basic(APP_NAME, USER_ID_STATEFUL, SESSION_ID_STATEFUL, session_stateful_service)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

    weather_agent_team_guardrail = agents.get_weather_agent_5()

    runner_root_model_guardrail = create_project_manager(weather_agent_team_guardrail, APP_NAME, session_stateful_service)

    # now this how you do bulk, repeated queries with differnt systems

    interaction_func = lambda query: run_agent(query,
                                                            runner_root_model_guardrail,
                                                            USER_ID_STATEFUL, # Use existing user ID
                                                            SESSION_ID_STATEFUL # Use existing session ID
                                                            )

    print("--- Turn 1: Requesting weather in London (expect allowed, Fahrenheit) ---")
    await interaction_func("What is the weather in London?")

    # 2. Request containing the blocked keyword (Callback intercepts)
    print("\n--- Turn 2: Requesting with blocked keyword (expect blocked) ---")
    await interaction_func("BLOCK the request for weather in Tokyo") # Callback should catch "BLOCK"

    # 3. Normal greeting (Callback allows root agent, delegation happens)
    print("\n--- Turn 3: Sending a greeting (expect allowed) ---")
    await interaction_func("Hello again")


    final_session = await get_session_basic(APP_NAME, USER_ID_STATEFUL, SESSION_ID_STATEFUL, session_stateful_service)
    


    # now lets try and do the agent with subagents, statefulness, model_callback and tool_callback
    # This should be the base model structure we need to confirm having
    default_weather_agent = agents.get_weather_agent_6()

    final_runner = create_project_manager(default_weather_agent, APP_NAME, session_stateful_service)
    interaction_func = lambda query: run_agent(query,
                                                            final_runner,
                                                            USER_ID_STATEFUL, # Use existing user ID
                                                            SESSION_ID_STATEFUL # Use existing session ID
                                                            )

    # 1. Allowed city (Should pass both callbacks, use Fahrenheit state)
    print("--- Turn 1: Requesting weather in New York (expect allowed) ---")
    await interaction_func("What's the weather in New York?")

    # 2. Blocked city (Should pass model callback, but be blocked by tool callback)
    print("\n--- Turn 2: Requesting weather in Paris (expect blocked by tool guardrail) ---")
    await interaction_func("How about Paris?") # Tool callback should intercept this

    # 3. Another allowed city (Should work normally again)
    print("\n--- Turn 3: Requesting weather in London (expect allowed) ---")
    await interaction_func("Tell me the weather in London.")

    print("\n--- Inspecting Final Session State (After Tool Guardrail Test) ---")
    # Use the session service instance associated with this stateful session
                                            #APP_NAME: str, USER_ID: str, SESSION_ID: str, SESSION_SERVICE
    final_session = await get_session_basic(APP_NAME,USER_ID_STATEFUL,SESSION_ID_STATEFUL, session_stateful_service)
    if final_session:
        # Use .get() for safer access
        print(f"Tool Guardrail Triggered Flag: {final_session.state.get('guardrail_tool_block_triggered', 'Not Set (or False)')}")
        print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}") # Should be London weather if successful
        print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}") # Should be Fahrenheit
        # print(f"Full State Dict: {final_session.state}") # For detailed view

# Uncomment the following lines if running as a standard Python script (.py file):
import asyncio
if __name__ == "__main__":
    asyncio.run(run_conversation())
    # try:
    #     asyncio.run(run_conversation())
    # except Exception as e:
    #     print(f"An error occurred: {e}")