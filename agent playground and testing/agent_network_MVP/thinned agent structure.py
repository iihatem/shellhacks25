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



import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")


# @title Configure API Keys (Replace with your actual keys!)

# --- IMPORTANT: Replace placeholders with your real API keys ---

# Gemini API Key (Get from Google AI Studio: https://aistudio.google.com/app/apikey)
os.environ["GOOGLE_API_KEY"] = "AIzaSyDNBCWaQeoef0XkzIgvlr-9tXJvFW7MFZE" # <--- REPLACE

# [Optional]
# OpenAI API Key (Get from OpenAI Platform: https://platform.openai.com/api-keys)
os.environ['OPENAI_API_KEY'] = 'YOUR_OPENAI_API_KEY' # <--- REPLACE

# [Optional]
# Anthropic API Key (Get from Anthropic Console: https://console.anthropic.com/settings/keys)
os.environ['ANTHROPIC_API_KEY'] = 'YOUR_ANTHROPIC_API_KEY' # <--- REPLACE

# --- Verify Keys (Optional Check) ---
print("API Keys Set:")
print(f"Google API Key set: {'Yes' if os.environ.get('GOOGLE_API_KEY') and os.environ['GOOGLE_API_KEY'] != 'YOUR_GOOGLE_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"OpenAI API Key set: {'Yes' if os.environ.get('OPENAI_API_KEY') and os.environ['OPENAI_API_KEY'] != 'YOUR_OPENAI_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"Anthropic API Key set: {'Yes' if os.environ.get('ANTHROPIC_API_KEY') and os.environ['ANTHROPIC_API_KEY'] != 'YOUR_ANTHROPIC_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

# Configure ADK to use API keys directly (not Vertex AI for this multi-model setup)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


# @markdown **Security Note:** It's best practice to manage API keys securely (e.g., using Colab Secrets or environment variables) rather than hardcoding them directly in the notebook. Replace the placeholder strings above.


# --- Define Model Constants for easier use ---

# More supported models can be referenced here: https://ai.google.dev/gemini-api/docs/models#model-variations
MODEL_GEMINI_2_0_FLASH = "gemini-2.5-pro"

# More supported models can be referenced here: https://docs.litellm.ai/docs/providers/openai#openai-chat-completion-models
# MODEL_GPT_4O = "openai/gpt-4.1" # You can also try: gpt-4.1-mini, gpt-4o etc.

# # More supported models can be referenced here: https://docs.litellm.ai/docs/providers/anthropic
# MODEL_CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514" # You can also try: claude-opus-4-20250514 , claude-3-7-sonnet-20250219 etc

print("\nEnvironment configured.")

# @title Define Tools for Greeting and Farewell Agents, which are SPECIALIST AGENTS
from typing import Optional # Make sure to import Optional
def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        greeting = "Hello there!" # Default greeting if name is None or not explicitly passed
        print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
    return greeting

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."


# @title Define the get_weather Tool
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    city_normalized = city.lower().replace(" ", "") # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# title - State Aware get_weather_tool
def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32 # Calculate Fahrenheit
            temp_unit = "°F"
        else: # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}


def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for 'BLOCK'. If found, blocks the LLM call
    and returns a predefined LlmResponse. Otherwise, returns None to proceed.
    """
    agent_name = callback_context.agent_name # Get the name of the agent whose model call is being intercepted
    print(f"--- Callback: block_keyword_guardrail running for agent: {agent_name} ---")

    # Extract the text from the latest user message in the request history
    last_user_message_text = ""
    if llm_request.contents:
        # Find the most recent message with role 'user'
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                # Assuming text is in the first part for simplicity
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break # Found the last user message text

    print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---") # Log first 100 chars

    # --- Guardrail Logic ---
    keyword_to_block = "BLOCK"
    if keyword_to_block in last_user_message_text.upper(): # Case-insensitive check
        print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")
        # Optionally, set a flag in state to record the block event
        callback_context.state["guardrail_block_keyword_triggered"] = True
        print(f"--- Callback: Set state 'guardrail_block_keyword_triggered': True ---")

        # Construct and return an LlmResponse to stop the flow and send this back instead
        return LlmResponse(
            content=types.Content(
                role="model", # Mimic a response from the agent's perspective
                parts=[types.Part(text=f"I cannot process this request because it contains the blocked keyword '{keyword_to_block}'.")],
            )
            # Note: You could also set an error_message field here if needed
        )
    else:
        # Keyword not found, allow the request to proceed to the LLM
        print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
        return None # Returning None signals ADK to continue normally


def block_paris_tool_guardrail(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """
    Checks if 'get_weather_stateful' is called for 'Paris'.
    If so, blocks the tool execution and returns a specific error dictionary.
    Otherwise, allows the tool call to proceed by returning None.
    """
    tool_name = tool.name
    agent_name = tool_context.agent_name # Agent attempting the tool call
    print(f"--- Callback: block_paris_tool_guardrail running for tool '{tool_name}' in agent '{agent_name}' ---")
    print(f"--- Callback: Inspecting args: {args} ---")

    # --- Guardrail Logic ---
    target_tool_name = "get_weather_stateful" # Match the function name used by FunctionTool
    blocked_city = "paris"

    # Check if it's the correct tool and the city argument matches the blocked city
    if tool_name == target_tool_name:
        city_argument = args.get("city", "") # Safely get the 'city' argument
        if city_argument and city_argument.lower() == blocked_city:
            print(f"--- Callback: Detected blocked city '{city_argument}'. Blocking tool execution! ---")
            # Optionally update state
            tool_context.state["guardrail_tool_block_triggered"] = True
            print(f"--- Callback: Set state 'guardrail_tool_block_triggered': True ---")

            # Return a dictionary matching the tool's expected output format for errors
            # This dictionary becomes the tool's result, skipping the actual tool run.
            return {
                "status": "error",
                "error_message": f"Policy restriction: Weather checks for '{city_argument.capitalize()}' are currently disabled by a tool guardrail."
            }
        else:
             print(f"--- Callback: City '{city_argument}' is allowed for tool '{tool_name}'. ---")
    else:
        print(f"--- Callback: Tool '{tool_name}' is not the target tool. Allowing. ---")


    # If the checks above didn't return a dictionary, allow the tool to execute
    print(f"--- Callback: Allowing tool '{tool_name}' to proceed. ---")
    return None # Returning None allows the actual tool function to run


async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")




    


# @title Run the Initial Conversation

# We need an async function to await our interaction helper
async def run_conversation():
    # @title Define the Weather Agent
    # Use one of the model constants defined earlier
    AGENT_MODEL = MODEL_GEMINI_2_0_FLASH # Starting with Gemini

    
    # @title Setup Session Service and Runner

    # --- Session Management ---
    # Key Concept: SessionService stores conversation history & state.
    # InMemorySessionService is simple, non-persistent storage for this tutorial.
    session_service = InMemorySessionService()

    # Define constants for identifying the interaction context
    APP_NAME = "weather_tutorial_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001" # Using a fixed ID for simplicity

    # Create the specific session where the conversation will happen
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    # --- Runner ---
    # Key Concept: Runner orchestrates the agent execution loop.
    runner = Runner(
        agent=weather_agent, # The agent we want to run
        app_name=APP_NAME,   # Associates runs with our app
        session_service=session_service # Uses our session manager
    )
    print(f"Runner created for agent '{runner.agent.name}'.")
    
    # --- Greeting Agent ---
    greeting_agent = None
    try:
        greeting_agent = Agent(
            # Using a potentially different/cheaper model for a simple task
            model = MODEL_GEMINI_2_0_FLASH,
            # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
            name="greeting_agent",
            instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                        "Use the 'say_hello' tool to generate the greeting. "
                        "If the user provides their name, make sure to pass it to the tool. "
                        "Do not engage in any other conversation or tasks.",
            description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
            tools=[say_hello],
        )
        print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")
    except Exception as e:
        print(f"❌ Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}")

    # --- Farewell Agent ---
    farewell_agent = None
    try:
        farewell_agent = Agent(
            # Can use the same or a different model
            model = MODEL_GEMINI_2_0_FLASH,
            # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
            name="farewell_agent",
            instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                        "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                        "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                        "Do not perform any other actions.",
            description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
            tools=[say_goodbye],
        )
        print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
    except Exception as e:
        print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")

    
    # @title Define the Root Agent with Sub-Agents
    # Ensure sub-agents were created successfully before defining the root agent.
    # Also ensure the original 'get_weather' tool is defined.
    root_agent = None
    runner_root = None # Initialize runner
    
    if greeting_agent and farewell_agent:
        # Let's use a capable Gemini model for the root agent to handle orchestration
        root_agent_model = MODEL_GEMINI_2_0_FLASH
        

        weather_agent_team = Agent(
            name="weather_agent_v2", # Give it a new version name
            model=root_agent_model,
            description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
            instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                        "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                        "You have specialized sub-agents: "
                        "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                        "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                        "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                        "If it's a weather request, handle it yourself using 'get_weather'. "
                        "For anything else, respond appropriately or state you cannot handle it.",
            tools=[get_weather], # Root agent still needs the weather tool for its core task
            # Key change: Link the sub-agents here!
            sub_agents=[greeting_agent, farewell_agent]
        )
        print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")

    else:
        print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
        if not greeting_agent: print(" - Greeting Agent is missing.")
        if not farewell_agent: print(" - Farewell Agent is missing.")
        if 'get_weather' not in globals(): print(" - get_weather function is missing.")




    # Ensure the root agent (e.g., 'weather_agent_team' or 'root_agent' from the previous cell) is defined.
    # Ensure the call_agent_async function is defined.

    # Check if the root agent variable exists before defining the conversation function
    root_agent_var_name = 'root_agent' # Default name from Step 3 guide
    if weather_agent_team: # Check if user used this name instead
        root_agent_var_name = 'weather_agent_team'
    elif not root_agent:
        print("⚠️ Root agent ('root_agent' or 'weather_agent_team') not found. Cannot define run_team_conversation.")
        # Assign a dummy value to prevent NameError later if the code block runs anyway
        root_agent = None # Or set a flag to prevent execution
    print("here!")
    # Only define and run if the root agent exists
    if root_agent_var_name:
        # Define the main async function for the conversation logic.
        # The 'await' keywords INSIDE this function are necessary for async operations.
        print("here2")
        #async def run_team_conversation():
        print("\n--- Testing Agent Team Delegation ---")
        session_service = InMemorySessionService()
        APP_NAME = "weather_tutorial_agent_team"
        USER_ID = "user_1_agent_team"
        SESSION_ID = "session_001_agent_team"
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

        actual_root_agent = weather_agent_team #globals()[root_agent_var_name]
        print("here3")
        runner_agent_team = Runner( # Or use InMemoryRunner
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        print(f"Runner created for agent '{actual_root_agent.name}'.")

        # --- Interactions using await (correct within async def) ---
        await call_agent_async(query = "Hello there!",
                            runner=runner_agent_team,
                            user_id=USER_ID,
                            session_id=SESSION_ID)
        await call_agent_async(query = "What is the weather in New York?",
                            runner=runner_agent_team,
                            user_id=USER_ID,
                            session_id=SESSION_ID)
        await call_agent_async(query = "Thanks, bye!",
                            runner=runner_agent_team,
                            user_id=USER_ID,
                            session_id=SESSION_ID)

        # Create a NEW session service instance for this state demonstration
        session_service_stateful = InMemorySessionService()
        print("✅ New InMemorySessionService created for state demonstration.")

        # Define a NEW session ID for this part of the tutorial
        SESSION_ID_STATEFUL = "session_state_demo_001"
        USER_ID_STATEFUL = "user_state_demo"

        # Define initial state data - user prefers Celsius initially
        initial_state = {
            "user_preference_temperature_unit": "Celsius"
        }

        # Create the session, providing the initial state
        session_stateful = await session_service_stateful.create_session(
            app_name=APP_NAME, # Use the consistent app name
            user_id=USER_ID_STATEFUL,
            session_id=SESSION_ID_STATEFUL,
            state=initial_state # <<< Initialize state during creation
        )
        print(f"✅ Session '{SESSION_ID_STATEFUL}' created for user '{USER_ID_STATEFUL}'.")

        # Verify the initial state was set correctly
        retrieved_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                                user_id=USER_ID_STATEFUL,
                                                                session_id = SESSION_ID_STATEFUL)
        print("\n--- Initial Session State ---")
        if retrieved_session:
            print(retrieved_session.state)
        else:
            print("Error: Could not retrieve session.")

        # --- Redefine Greeting Agent (from Step 3) ---
        greeting_agent = None
        try:
            greeting_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="greeting_agent",
                instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
                description="Handles simple greetings and hellos using the 'say_hello' tool.",
                tools=[say_hello],
            )
            print(f"✅ Agent '{greeting_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Greeting agent. Error: {e}")

        # --- Redefine Farewell Agent (from Step 3) ---
        farewell_agent = None
        try:
            farewell_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="farewell_agent",
                instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
                description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
                tools=[say_goodbye],
            )
            print(f"✅ Agent '{farewell_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Farewell agent. Error: {e}")

        # --- Define the Updated Root Agent ---
        root_agent_stateful = None
        runner_root_stateful = None # Initialize runner

        # Check prerequisites before creating the root agent
        if greeting_agent and farewell_agent and 'get_weather_stateful' in globals():

            root_agent_model = MODEL_GEMINI_2_0_FLASH # Choose orchestration model

            root_agent_stateful = Agent(
                name="weather_agent_v4_stateful", # New version name
                model=root_agent_model,
                description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state.",
                instruction="You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
                            "The tool will format the temperature based on user preference stored in state. "
                            "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                            "Handle only weather requests, greetings, and farewells.",
                tools=[get_weather_stateful], # Use the state-aware tool
                sub_agents=[greeting_agent, farewell_agent], # Include sub-agents
                output_key="last_weather_report" # <<< Auto-save agent's final weather response
            )
            print(f"✅ Root Agent '{root_agent_stateful.name}' created using stateful tool and output_key.")

            # --- Create Runner for this Root Agent & NEW Session Service ---
            runner_root_stateful = Runner(
                agent=root_agent_stateful,
                app_name=APP_NAME,
                session_service=session_service_stateful # Use the NEW stateful session service
            )
            print(f"✅ Runner created for stateful root agent '{runner_root_stateful.agent.name}' using stateful session service.")

        else:
            print("❌ Cannot create stateful root agent. Prerequisites missing.")
            if not greeting_agent: print(" - greeting_agent definition missing.")
            if not farewell_agent: print(" - farewell_agent definition missing.")
            if 'get_weather_stateful' not in globals(): print(" - get_weather_stateful tool missing.")
            
        # Define the main async function for the stateful conversation logic.
        # The 'await' keywords INSIDE this function are necessary for async operations.
        #async def run_stateful_conversation():
        # print("\n--- Testing State: Temp Unit Conversion & output_key ---")

        # # 1. Check weather (Uses initial state: Celsius)
        # print("--- Turn 1: Requesting weather in London (expect Celsius) ---")
        # await call_agent_async(query= "What's the weather in London?",
        #                     runner=runner_root_stateful,
        #                     user_id=USER_ID_STATEFUL,
        #                     session_id=SESSION_ID_STATEFUL
        #                     )

        # # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
        # print("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
        # try:
        #     # Access the internal storage directly - THIS IS SPECIFIC TO InMemorySessionService for testing
        #     # NOTE: In production with persistent services (Database, VertexAI), you would
        #     # typically update state via agent actions or specific service APIs if available,
        #     # not by direct manipulation of internal storage.
        #     stored_session = session_service_stateful.sessions[APP_NAME][USER_ID_STATEFUL][SESSION_ID_STATEFUL]
        #     stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
        #     # Optional: You might want to update the timestamp as well if any logic depends on it
        #     # import time
        #     # stored_session.last_update_time = time.time()
        #     print(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state.get('user_preference_temperature_unit', 'Not Set')} ---") # Added .get for safety
        # except KeyError:
        #     print(f"--- Error: Could not retrieve session '{SESSION_ID_STATEFUL}' from internal storage for user '{USER_ID_STATEFUL}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
        # except Exception as e:
        #     print(f"--- Error updating internal session state: {e} ---")

        # # 3. Check weather again (Tool should now use Fahrenheit)
        # # This will also update 'last_weather_report' via output_key
        # print("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
        # await call_agent_async(query= "Tell me the weather in New York.",
        #                     runner=runner_root_stateful,
        #                     user_id=USER_ID_STATEFUL,
        #                     session_id=SESSION_ID_STATEFUL
        #                     )

        # # 4. Test basic delegation (should still work)
        # # This will update 'last_weather_report' again, overwriting the NY weather report
        # print("\n--- Turn 3: Sending a greeting ---")
        # await call_agent_async(query= "Hi!",
        #                     runner=runner_root_stateful,
        #                     user_id=USER_ID_STATEFUL,
        #                     session_id=SESSION_ID_STATEFUL
        #                     )
        
        # # --- Inspect final session state after the conversation ---
        # # This block runs after either execution method completes.
        # print("\n--- Inspecting Final Session State ---")
        # final_session = await session_service_stateful.get_session(app_name=APP_NAME,
        #                                                     user_id= USER_ID_STATEFUL,
        #                                                     session_id=SESSION_ID_STATEFUL)
        # if final_session:
        #     # Use .get() for safer access to potentially missing keys
        #     print(f"Final Preference: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}")
        #     print(f"Final Last Weather Report (from output_key): {final_session.state.get('last_weather_report', 'Not Set')}")
        #     print(f"Final Last City Checked (by tool): {final_session.state.get('last_city_checked_stateful', 'Not Set')}")
        #     # Print full state for detailed view
        #     print(f"Full State Dict: {final_session.state}") # For detailed view
        # else:
        #     print("\n❌ Error: Could not retrieve final session state.")




        # --- Redefine Sub-Agents (Ensures they exist in this context) ---
        greeting_agent = None
        try:
            # Use a defined model constant
            greeting_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="greeting_agent", # Keep original name for consistency
                instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
                description="Handles simple greetings and hellos using the 'say_hello' tool.",
                tools=[say_hello],
            )
            print(f"✅ Sub-Agent '{greeting_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Greeting agent. Check Model/API Key ({greeting_agent.model}). Error: {e}")

        farewell_agent = None
        try:
            # Use a defined model constant
            farewell_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="farewell_agent", # Keep original name
                instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
                description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
                tools=[say_goodbye],
            )
            print(f"✅ Sub-Agent '{farewell_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Farewell agent. Check Model/API Key ({farewell_agent.model}). Error: {e}")


        # --- Define the Root Agent with the Callback ---
        root_agent_model_guardrail = None
        runner_root_model_guardrail = None

        # Check all components before proceeding
        if greeting_agent and farewell_agent:

            # Use a defined model constant
            root_agent_model = MODEL_GEMINI_2_0_FLASH

            root_agent_model_guardrail = Agent(
                name="weather_agent_v5_model_guardrail", # New version name for clarity
                model=root_agent_model,
                description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
                instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                            "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                            "Handle only weather requests, greetings, and farewells.",
                tools=[get_weather_stateful],
                sub_agents=[greeting_agent, farewell_agent], # Reference the redefined sub-agents
                output_key="last_weather_report", # Keep output_key from Step 4
                before_model_callback=block_keyword_guardrail # <<< Assign the guardrail callback
            )
            print(f"✅ Root Agent '{root_agent_model_guardrail.name}' created with before_model_callback.")

            # --- Create Runner for this Agent, Using SAME Stateful Session Service ---
            # Ensure session_service_stateful exists from Step 4
            #if 'session_service_stateful' in globals():
            try:
                runner_root_model_guardrail = Runner(
                    agent=root_agent_model_guardrail,
                    app_name=APP_NAME, # Use consistent APP_NAME
                    session_service=session_service_stateful # <<< Use the service from Step 4
                )
                print(f"✅ Runner created for guardrail agent '{runner_root_model_guardrail.agent.name}', using stateful session service.")
            #else:
            except Exception as e:
                print("❌ Cannot create runner. 'session_service_stateful' from Step 4 is missing.")
                print(e)

        else:
            print("❌ Cannot create root agent with model guardrail. One or more prerequisites are missing or failed initialization:")
            if not greeting_agent: print("   - Greeting Agent")
            if not farewell_agent: print("   - Farewell Agent")
            if 'get_weather_stateful' not in globals(): print("   - 'get_weather_stateful' tool")
            if 'block_keyword_guardrail' not in globals(): print("   - 'block_keyword_guardrail' callback")

        print("\n--- Testing Model Input Guardrail ---")

        # Use the runner for the agent with the callback and the existing stateful session ID
        # Define a helper lambda for cleaner interaction calls
        interaction_func = lambda query: call_agent_async(query,
                                                         runner_root_model_guardrail,
                                                         USER_ID_STATEFUL, # Use existing user ID
                                                         SESSION_ID_STATEFUL # Use existing session ID
                                                        )
        # 1. Normal request (Callback allows, should use Fahrenheit from previous state change)
        print("--- Turn 1: Requesting weather in London (expect allowed, Fahrenheit) ---")
        await interaction_func("What is the weather in London?")

        # 2. Request containing the blocked keyword (Callback intercepts)
        print("\n--- Turn 2: Requesting with blocked keyword (expect blocked) ---")
        await interaction_func("BLOCK the request for weather in Tokyo") # Callback should catch "BLOCK"

        # 3. Normal greeting (Callback allows root agent, delegation happens)
        print("\n--- Turn 3: Sending a greeting (expect allowed) ---")
        await interaction_func("Hello again")


        print("\n--- Inspecting Final Session State (After Guardrail Test) ---")
        # Use the session service instance associated with this stateful session
        final_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                            user_id=USER_ID_STATEFUL,
                                                            session_id=SESSION_ID_STATEFUL)
        if final_session:
            # Use .get() for safer access
            print(f"Guardrail Triggered Flag: {final_session.state.get('guardrail_block_keyword_triggered', 'Not Set (or False)')}")
            print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}") # Should be London weather if successful
            print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}") # Should be Fahrenheit
            # print(f"Full State Dict: {final_session.state}") # For detailed view
        else:
            print("\n❌ Error: Could not retrieve final session state.")


        # --- Redefine Sub-Agents (Ensures they exist in this context) ---
        greeting_agent = None
        try:
            # Use a defined model constant
            greeting_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="greeting_agent", # Keep original name for consistency
                instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
                description="Handles simple greetings and hellos using the 'say_hello' tool.",
                tools=[say_hello],
            )
            print(f"✅ Sub-Agent '{greeting_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Greeting agent. Check Model/API Key ({greeting_agent.model}). Error: {e}")

        farewell_agent = None
        try:
            # Use a defined model constant
            farewell_agent = Agent(
                model=MODEL_GEMINI_2_0_FLASH,
                name="farewell_agent", # Keep original name
                instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
                description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
                tools=[say_goodbye],
            )
            print(f"✅ Sub-Agent '{farewell_agent.name}' redefined.")
        except Exception as e:
            print(f"❌ Could not redefine Farewell agent. Check Model/API Key ({farewell_agent.model}). Error: {e}")

        # --- Define the Root Agent with Both Callbacks ---
        root_agent_tool_guardrail = None
        runner_root_tool_guardrail = None

    
        root_agent_model = MODEL_GEMINI_2_0_FLASH

        root_agent_tool_guardrail = Agent(
            name="weather_agent_v6_tool_guardrail", # New version name
            model=root_agent_model,
            description="Main agent: Handles weather, delegates, includes input AND tool guardrails.",
            instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                        "Delegate greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                        "Handle only weather, greetings, and farewells.",
            tools=[get_weather_stateful],
            sub_agents=[greeting_agent, farewell_agent],
            output_key="last_weather_report",
            before_model_callback=block_keyword_guardrail, # Keep model guardrail
            before_tool_callback=block_paris_tool_guardrail # <<< Add tool guardrail
        )
        print(f"✅ Root Agent '{root_agent_tool_guardrail.name}' created with BOTH callbacks.")

        # --- Create Runner, Using SAME Stateful Session Service ---
        try:
            runner_root_tool_guardrail = Runner(
                agent=root_agent_tool_guardrail,
                app_name=APP_NAME,
                session_service=session_service_stateful # <<< Use the service from Step 4/5
            )
            print(f"✅ Runner created for tool guardrail agent '{runner_root_tool_guardrail.agent.name}', using stateful session service.")
        except Exception as e:  
            print("❌ Cannot create runner. 'session_service_stateful' from Step 4/5 is missing.")
            print(e)

        # Define the main async function for the tool guardrail test conversation.
        # The 'await' keywords INSIDE this function are necessary for async operations.
        #async def run_tool_guardrail_test():
        print("\n--- Testing Tool Argument Guardrail ('Paris' blocked) ---")

        # Use the runner for the agent with both callbacks and the existing stateful session
        # Define a helper lambda for cleaner interaction calls
        interaction_func = lambda query: call_agent_async(query,
                                                         runner_root_tool_guardrail,
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
        final_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                            user_id=USER_ID_STATEFUL,
                                                            session_id= SESSION_ID_STATEFUL)
        if final_session:
            # Use .get() for safer access
            print(f"Tool Guardrail Triggered Flag: {final_session.state.get('guardrail_tool_block_triggered', 'Not Set (or False)')}")
            print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}") # Should be London weather if successful
            print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}") # Should be Fahrenheit
            # print(f"Full State Dict: {final_session.state}") # For detailed view
        else:
            print("\n❌ Error: Could not retrieve final session state.")
        

    else:
        # This message prints if the root agent variable wasn't found earlier
        print("\n⚠️ Skipping agent team conversation execution as the root agent was not successfully defined in a previous step.")


# Execute the conversation using await in an async context (like Colab/Jupyter)


# --- OR ---

# Uncomment the following lines if running as a standard Python script (.py file):
import asyncio
if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")