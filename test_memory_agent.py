from ak_engine.agents.memory_agent import MemoryAgent

memory = MemoryAgent()

memory.remember("project", "Calculator")
memory.remember("language", "Python")
memory.remember("author", "AK")

print(memory.recall("project"))
print(memory.recall("language"))
print(memory.recall("author"))

print()

print(memory.show())
