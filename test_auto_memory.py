from ak_engine.memory.manager import MemoryManager

memory = MemoryManager()

memory.auto_remember("My name is AK")
memory.auto_remember("My favorite language is Python")
memory.auto_remember("I'm building AK Engine")
memory.auto_remember("I like Linux")

print("=== User Memories ===")
for key, value in memory.list_category("user"):
    print(f"{key} = {value}")

print()

print("=== Project Memories ===")
for key, value in memory.list_category("project"):
    print(f"{key} = {value}")

print()

print("=== Search: AK ===")
for category, key, value in memory.search("AK"):
    print(f"[{category}] {key} = {value}")

print()

print("=== Search: Python ===")
for category, key, value in memory.search("Python"):
    print(f"[{category}] {key} = {value}")

print()

print("=== Search: Linux ===")
for category, key, value in memory.search("Linux"):
    print(f"[{category}] {key} = {value}")
