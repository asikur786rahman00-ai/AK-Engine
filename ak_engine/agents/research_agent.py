from ak_engine.providers.universal_provider import UniversalProvider


class ResearchAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def research(self, goal):

        prompt = f"""
You are a senior software architect.

Goal:
{goal}

Before writing code:

Return concise development notes.

Include:
- Recommended framework
- Best practices
- Common mistakes
- Suggested project structure

Return plain text only.
"""

        return self.provider.chat(
            prompt,
            task="reasoning"
        )
