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

    # --- Task 3: Generate code and save it to a file ---
    print("--- Task 3: Generating and saving a script ---")
    code_generation_task = "generate a hello world python script"
    generated_code = orchestrator.delegate_task(code_generation_task)
    print(f"Generated code:\n{generated_code}")

    file_writing_task = "write file"
    result = orchestrator.delegate_task(
        file_writing_task, path="hello_world_from_agent.py", content=generated_code
    )
    print(result)

if __name__ == "__main__":
    main()
