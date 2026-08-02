from ak_engine.agents.file_agent import FileAgent

agent = FileAgent()

files = agent.create_project("CalculatorApp")

print("Project created!")

for file in files:
    print("✓", file)
