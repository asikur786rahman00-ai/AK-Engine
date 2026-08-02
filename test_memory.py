from ak_engine.memory.manager import MemoryManager

memory = MemoryManager()

# Save memories
memory.remember("user", "name", "AK")
memory.remember("user", "model", "gpt-oss:120b")
memory.remember("project", "name", "AK-Engine")
memory.remember("project", "language", "Python")

print("=== Recall ===")
print(memory.recall("user", "name"))
print(memory.recall("user", "model"))

print("\n=== User Memories ===")
for key, value in memory.list_category("user"):
    print(f"{key} = {value}")

print("\n=== Project Memories ===")
for key, value in memory.list_category("project"):
    print(f"{key} = {value}")

print("\n=== Search: AK ===")
for category, key, value in memory.search("AK"):
    print(f"[{category}] {key} = {value}")

print("\n=== Search: Python ===")
for category, key, value in memory.search("Python"):
    print(f"[{category}] {key} = {value}")

print("\n=== Search: gpt ===")
for category, key, value in memory.search("gpt"):
    print(f"[{category}] {key} = {value}")
