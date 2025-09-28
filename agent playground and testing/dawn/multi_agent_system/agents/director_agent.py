from typing import List, Dict
from multi_agent_system.agents.base import Agent
from multi_agent_system.agents.project_manager_agent import ProjectManagerAgent

class DirectorAgent(Agent):
    """
    The Director agent that oversees the entire operation.
    It creates and manages Project Manager agents.
    """
    def __init__(self, tool_agents: List[Agent]):
        super().__init__("DirectorAgent", "Delegates projects to Project Managers.")
        self.tool_agents = tool_agents

    def run(self, high_level_goal: str, **kwargs) -> str:
        """
        Runs the Director to achieve a high-level goal.
        """
        print(f"[{self.name}] received high-level goal: {high_level_goal}")

        # In a real system, this would involve complex logic to select/create the right PM.
        # For now, we create one PM for the goal.
        print(f"[{self.name}] Creating a Project Manager for this goal.")
        project_manager = ProjectManagerAgent(
            name="WebApp_PM",
            description="Manages web app development projects.",
            tool_agents=self.tool_agents
        )

        # Delegate the project to the newly created PM
        result = project_manager.run(high_level_goal)
        return result
