import os
from some_llm_library import LLMClient  # Assuming a library for LLM calls

class BaseAgent:
    """
    A generic, configurable agent that uses an LLM to perform tasks.
    This agent is not specialized in its code. Instead, it is configured at runtime
    with a "personality" or a set of instructions.
    """

    def __init__(self, configuration):
        """
        Initializes the agent with a configuration.
        The configuration defines the agent's personality, purpose, tools, and sub-agents.
        
        :param configuration: A dictionary containing the agent's configuration.
        """
        self.configuration = configuration
        self.llm_client = LLMClient(api_key=os.environ.get("LLM_API_KEY"))
        self.sub_agents = self._load_sub_agents()

    def _load_sub_agents(self):
        """
        Loads and instantiates the sub-agents defined in the configuration.
        """
        sub_agents = {}
        if "sub_agents" in self.configuration:
            for agent_name in self.configuration["sub_agents"]:
                # In a real implementation, this would load the sub-agent's configuration
                # and create a new BaseAgent instance for it.
                print(f"Loading sub-agent: {agent_name}")
                # sub_agents[agent_name] = BaseAgent(load_config(f'config_{agent_name}.json'))
        return sub_agents

    def handle_request(self, user_request):
        """
        Handles a user request by using the LLM, the agent's configuration, and its tools.

        :param user_request: The user's request as a string or a dictionary.
        :return: The response from the agent.
        """

        # The core of the agent's logic is to use the LLM to decide what to do.
        # The prompt will be constructed from the agent's configuration and the user request.
        # The LLM's response will be a structured format (e.g., JSON) that indicates
        # which tool to use or which sub-agent to call.

        prompt = self._build_prompt(user_request)
        llm_response = self.llm_client.generate(prompt)

        # In a real implementation, we would parse the llm_response and execute the action.
        # For example, if the llm_response is: 
        # { "action": "call_sub_agent", "sub_agent": "BillingAgent", "input": { ... } }
        # we would call the BillingAgent.

        return f"LLM response: {llm_response}"

    def _build_prompt(self, user_request):
        """
        Builds a detailed prompt for the LLM.
        """
        
        agent_description = self.configuration.get("description", "You are a helpful assistant.")
        agent_tools = self.configuration.get("tools", [])
        agent_logic = self.configuration.get("logic", {})

        prompt = f"""You are {self.configuration.get('name', 'an agent')}. 
        {agent_description}

        You have access to the following tools: {', '.join(agent_tools)}
        You can delegate tasks to the following sub-agents: {', '.join(self.sub_agents.keys())}

        Your logic is defined as follows: {agent_logic}

        User request: "{user_request}"

        Based on the user's request and your logic, what is the next action to take? 
        Respond in a structured format (e.g., JSON) with the action and its parameters.
        """

        return prompt
