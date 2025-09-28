from multi_agent_system.agents.base import Agent

class CodeAgent(Agent):
    """
    Agent for writing and executing code.
    """
    def __init__(self):
        super().__init__(
            name="CodeAgent",
            description="Generates code based on a prompt. Keywords: code, generate, script."
        )

    def run(self, task: str, **kwargs) -> str:
        """
        Runs the agent to perform a task.

        :param task: The task to perform.
        :param kwargs: Additional keyword arguments.
        :return: The result of the task.
        """
        # In a real implementation, this would use an LLM to generate code.
        # For now, we'll simulate it by returning a hardcoded script based on the task.
        if "hello world" in task.lower():
            return "print('Hello, World from the Code Agent!')"
        else:
            return f"# Code for task: {task}\npass"
