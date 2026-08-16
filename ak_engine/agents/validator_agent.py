from ak_engine.providers.universal_provider import UniversalProvider


class ValidatorAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def validate(self, goal, code, output):

        prompt = f"""
You are an expert software QA engineer.

Goal:
{goal}

Program:
{code}

Console Output:
{output}

Did the program successfully achieve the goal?

Rules:
Return ONLY one word.

SUCCESS
or
FAIL
"""

        result = self.provider.chat(
            prompt,
            task="reasoning"
        ).strip().upper()

        return "SUCCESS" in result
