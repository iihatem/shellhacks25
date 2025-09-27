import os
from multi_agent_system.agents.base import Agent

class FileSystemAgent(Agent):
    """
    Agent for interacting with the file system.
    """
    def __init__(self):
        super().__init__(
            name="FileSystemAgent",
            description="Handles file system operations. Keywords: list, read, write file, directory."
        )

    def run(self, task: str, **kwargs) -> str:
        """
        Runs the agent to perform a task.

        :param task: The task to perform.
        :param kwargs: Additional keyword arguments.
        :return: The result of the task.
        """
        if "list" in task.lower():
            path = kwargs.get("path", ".")
            return self._list_files(path)
        elif "read" in task.lower():
            path = kwargs.get("path")
            if path:
                return self._read_file(path)
            else:
                return "Error: Path not specified for read operation."
        elif "write" in task.lower():
            path = kwargs.get("path")
            content = kwargs.get("content")
            if path and content:
                return self._write_file(path, content)
            else:
                return "Error: Path or content not specified for write operation."
        else:
            return f"Unknown task: {task}"

    def _list_files(self, path: str) -> str:
        try:
            files = os.listdir(path)
            return "\n".join(files)
        except Exception as e:
            return f"Error listing files: {e}"

    def _read_file(self, path: str) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def _write_file(self, path: str, content: str) -> str:
        try:
            with open(path, "w") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing to file: {e}"
