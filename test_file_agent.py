from ak_engine.agents.file_agent import FileAgent

agent = FileAgent()

agent.write_file("hello.txt", "Hermes AI")

print(agent.read_file("hello.txt"))
