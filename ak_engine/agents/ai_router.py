from ak_engine.providers.universal_provider import UniversalProvider

class AIRouter:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def route(self, task):

        prompt = f"""
You are a task router.

Available agents:

coding
runner
debugger
file
terminal

Task:
{task}

Reply with ONLY one word.
"""

        agent = self.provider.chat(
            prompt,
            task="routing"
        ).strip().lower()

        valid = {
            "coding",
            "runner",
            "debugger",
            "file",
            "terminal"
        }

        if agent not in valid:
            return "unknown"

        return agent
