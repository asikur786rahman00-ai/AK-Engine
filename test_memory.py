from ak_engine.memory.memory import Memory

memory = Memory()

memory.clear()

memory.save("user", "Create calculator")

memory.save("assistant", "Calculator created")

print(memory.load())
