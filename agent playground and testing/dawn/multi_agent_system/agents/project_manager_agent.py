from typing import List, Dict
from multi_agent_system.agents.base import Agent

class ProjectManagerAgent(Agent):
    """
    A project manager agent that breaks down a project into a plan and executes it.
    """
    def __init__(self, name: str, description: str, tool_agents: List[Agent]):
        super().__init__(name, description)
        self.tool_agents: Dict[str, Agent] = {agent.name: agent for agent in tool_agents}

    def run(self, project_goal: str, **kwargs) -> str:
        """
        Runs the project manager to achieve a goal.

        For now, we will use a simple plan based on the project goal.
        A real implementation would use an LLM to generate a detailed plan.
        """
        print(f"[{self.name}] received project goal: {project_goal}")

        # Simplified planning based on goal
        if "generate and save" in project_goal.lower():
            plan = [
                {"task": "generate a hello world python script", "agent": "CodeAgent"},
                {"task": "write file", "agent": "FileSystemAgent"}
            ]
        else:
            return f"[{self.name}] cannot create a plan for the goal: {project_goal}"

        # Execute the plan
        results = {}
        for i, step in enumerate(plan):
            print(f"[{self.name}] Executing step {i+1}: {step['task']}")
            agent = self.tool_agents.get(step["agent"])
            if not agent:
                return f"Error: Tool agent '{step['agent']}' not found."

            # This is a simplification. A real system needs better data passing.
            if step['task'] == "write file":
                result = agent.run(step['task'], path="pm_generated_script.py", content=results.get("step_0"))
            else:
                result = agent.run(step['task'])
            
            results[f"step_{i}"] = result
            print(f"[{self.name}] Step {i+1} result: {result}")

        return f"[{self.name}] Project completed successfully."
