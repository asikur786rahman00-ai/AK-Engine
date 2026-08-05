from ak_engine.providers.gemini import GeminiProvider
from ak_engine.agents.coding_agent import CodingAgent

class ExecutorAgent:
    def __init__(self):
        provider = GeminiProvider()
        self.coder = CodingAgent(provider)

    def execute(self, steps, goal):
        print("[Executor] Generating code...")
        file = self.coder.generate_python(goal)
        print(f"[Executor] Generated: {file}")
