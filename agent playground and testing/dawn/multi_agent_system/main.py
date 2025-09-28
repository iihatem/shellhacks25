from agents.director_agent import DirectorAgent
from agents.file_system_agent import FileSystemAgent
from agents.code_agent import CodeAgent

def main():
    """
    Main function to run the multi-agent system.
    """
    # 1. Create the pool of available Tool Agents (Tier 3)
    file_system_agent = FileSystemAgent()
    code_agent = CodeAgent()
    tool_agents = [file_system_agent, code_agent]

    # 2. Create the Director Agent and provide it with the tool agents (Tier 1)
    director = DirectorAgent(tool_agents=tool_agents)

    # 3. Define a high-level goal and delegate it to the Director
    goal = "generate and save a python script"
    result = director.run(goal)

    print(f"\n--- Final Result ---\n{result}")

if __name__ == "__main__":
    main()