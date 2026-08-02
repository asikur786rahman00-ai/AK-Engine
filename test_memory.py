from ak_engine.memory.manager import MemoryManager

memory = MemoryManager()

memory.remember("user", "name", "AK")
memory.remember("user", "favorite_model", "gpt-oss:120b")
memory.remember("project", "repo", "AK-Engine")

print(memory.recall("user", "name"))
print(memory.recall("user", "favorite_model"))
print(memory.recall("project", "repo"))

memory.forget("user", "name")

print(memory.recall("user", "name"))
