from ak_engine.providers.universal_provider import UniversalProvider


class InputAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def generate(self, goal, code):

        prompt = f"""
You are an expert software tester.

Goal:
{goal}

Python code:
{code}

Generate realistic console input for this program.

Rules:
- Return ONLY the input.
- One value per line.
- No explanations.
- No markdown.
"""

        return self.provider.chat(
            prompt,
            task="testing"
        ).strip()
