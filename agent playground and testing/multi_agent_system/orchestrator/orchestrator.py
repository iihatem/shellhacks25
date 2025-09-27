from typing import List, Dict
from multi_agent_system.agents.base import Agent

class Orchestrator:
    """
    The orchestrator for the multi-agent system.
    """
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent):
        """
        Registers an agent with the orchestrator.

        :param agent: The agent to register.
        """
        self.agents[agent.name] = agent

    def delegate_task(self, task: str, **kwargs) -> str:
        """
        Delegates a task to the appropriate agent.

        :param task: The task to delegate.
        :return: The result of the task.
        """
        # For now, use a simple keyword matching to find the right agent.
        for agent_name, agent in self.agents.items():
            if any(keyword in task.lower() for keyword in agent.description.lower().split()):
                return agent.run(task, **kwargs)
        return "No suitable agent found for the task."
