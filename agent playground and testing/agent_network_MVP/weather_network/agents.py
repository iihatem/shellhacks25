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
from weather_tools import get_weather, say_goodbye, say_hello, get_weather_stateful, block_keyword_guardrail, block_paris_tool_guardrail

MODEL_GEMINI_2_0_FLASH = "gemini-2.5-pro"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

# def get_weather_agent():
def get_weather_agent() -> Agent:
    # @title Define the Weather Agent
    weather_agent = Agent(
        name="weather_agent_v1",
        model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
        description="Provides weather information for specific cities.",
        instruction="You are a helpful weather assistant. "
                    "When the user asks for the weather in a specific city, "
                    "use the 'get_weather' tool to find the information. "
                    "If the tool returns an error, inform the user politely. "
                    "If the tool is successful, present the weather report clearly.",
        tools=[get_weather], # Pass the function directly
        sub_agents=[get_greeting_agent(), get_farewell_agent()]
    )


    return weather_agent

# def get_greeting_agent():
def get_greeting_agent() -> Agent:
    greeting_agent = Agent(
        # Using a potentially different/cheaper model for a simple task
        model = AGENT_MODEL,
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
    return greeting_agent

    # minimized creation critera:
    # instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    # description="Handles simple greetings and hellos using the 'say_hello' tool.",


# def get_farewell_agent():
def get_farewell_agent() -> Agent:
    farewell_agent = Agent(
        # Can use the same or a different model
        model = AGENT_MODEL,
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
    
    #minimized creation critera
    # instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    # description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",

    return farewell_agent



# def get_weather_agent_2():
def get_weather_agent_2() -> Agent:
    weather_agent_team = Agent(
        name="weather_agent_v2", # Give it a new version name
        model=AGENT_MODEL,
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
        sub_agents=[get_greeting_agent(), get_farewell_agent()],
    )
    print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{AGENT_MODEL}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")
    return weather_agent_team



# def get_weather_agent_5():
def get_weather_agent_5() -> Agent:
    root_agent_model_guardrail = Agent(
        name="weather_agent_v5_model_guardrail", # New version name for clarity
        model=AGENT_MODEL,
        description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather_stateful],
        sub_agents=[get_greeting_agent(), get_farewell_agent()], # Reference the redefined sub-agents
        output_key="last_weather_report", # Keep output_key from Step 4
        before_model_callback=block_keyword_guardrail # <<< Assign the guardrail callback
    )
    print(f"✅ Root Agent '{root_agent_model_guardrail.name}' created with before_model_callback.")
    return root_agent_model_guardrail

# def get_weather_agent_6():
def get_weather_agent_6() -> Agent:
    root_agent_tool_guardrail = Agent(
        name="weather_agent_v6_tool_guardrail", # New version name
        model=AGENT_MODEL,
        description="Main agent: Handles weather, delegates, includes input AND tool guardrails.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather, greetings, and farewells.",
        tools=[get_weather_stateful],
        sub_agents=[get_greeting_agent(), get_farewell_agent()],
        output_key="last_weather_report",
        before_model_callback=block_keyword_guardrail, # Keep model guardrail
        before_tool_callback=block_paris_tool_guardrail # <<< Add tool guardrail
    )
    print(f"✅ Root Agent '{root_agent_tool_guardrail.name}' created with BOTH callbacks.")
    return root_agent_tool_guardrail