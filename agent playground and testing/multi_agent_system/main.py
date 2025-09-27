from multi_agent_system.orchestrator.orchestrator import Orchestrator
from multi_agent_system.agents.file_system_agent import FileSystemAgent
from multi_agent_system.agents.code_agent import CodeAgent

def main():
    """
    Main function to run the multi-agent system.
    """
    # Create an orchestrator
    orchestrator = Orchestrator()

    # Create and register agents
    file_system_agent = FileSystemAgent()
    code_agent = CodeAgent()
    orchestrator.register_agent(file_system_agent)
    orchestrator.register_agent(code_agent)

    # Delegate a task
    task = "list all files in the multi_agent_system directory"
    result = orchestrator.delegate_task(task, path="multi_agent_system")
    print(result)

    task = "read the file multi_agent_system/main.py"
    result = orchestrator.delegate_task(task, path="multi_agent_system/main.py")
    print(result)

    task = "write a hello world python script"
    result = orchestrator.delegate_task(task, path="hello_world.py", content="print('Hello, World!')")
    print(result)

if __name__ == "__main__":
    main()
