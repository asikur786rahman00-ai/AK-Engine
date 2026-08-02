from ak_engine.memory.manager import MemoryManager
from ak_engine.router.router import SmartRouter
from ak_engine.providers.gemini import GeminiProvider

class AKAssistant:
    def __init__(self):
        self.memory = MemoryManager()
        self.router = SmartRouter()
        self.gemini = GeminiProvider()

    def chat(self, message):
        self.memory.add_message("user", message)
        self.memory.auto_remember(message)

        provider = self.router.choose(message)

        print(f"[Router] Selected: {provider}")

        if provider == "gemini":
            reply = self.gemini.chat(message)

        elif provider in [
            "gpt-oss:120b",
            "deepseek",
            "claude",
            "gpt",
        ]:
            print(f"[Fallback] {provider} -> Gemini")
            reply = self.gemini.chat(message)

        else:
            reply = self.gemini.chat(message)

        self.memory.add_message("assistant", reply)
        return reply
