from abc import ABC, abstractmethod

class Agent(ABC):
    """
    Base class for all agents.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, task: str, **kwargs) -> str:
        """
        Runs the agent to perform a task.

        :param task: The task to perform.
        :param kwargs: Additional keyword arguments.
        :return: The result of the task.
        """
        pass
