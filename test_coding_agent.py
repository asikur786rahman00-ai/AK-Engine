from ak_engine.agents.coding_agent import CodingAgent
from ak_engine.providers.gemini import GeminiProvider

provider = GeminiProvider()

agent = CodingAgent(provider)

file = agent.generate_python(
    "Create a Python calculator with add, subtract, multiply and divide."
)

print()
print("Generated:")
print(file)
