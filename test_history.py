from ak_engine.memory.manager import MemoryManager

memory = MemoryManager()

memory.add_message("user", "Hello")
memory.add_message("assistant", "Hi AK!")

memory.add_message("user", "My name is AK")
memory.auto_remember("My name is AK")

memory.add_message("assistant", "Nice to meet you!")

memory.add_message("user", "I'm building AK Engine")
memory.auto_remember("I'm building AK Engine")

print("=== Conversation ===")
for msg in memory.conversation():
    print(f'{msg["role"]}: {msg["content"]}')

print()

print("=== Stored Project Memory ===")
for key, value in memory.list_category("project"):
    print(f"{key} = {value}")
