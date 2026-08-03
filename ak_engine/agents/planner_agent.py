from ak_engine.providers.universal_provider import UniversalProvider

class PlannerAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def plan(self, goal):

        prompt = f"""
You are an expert software planner.

Goal:
{goal}

Return ONLY a numbered list of implementation steps.

Rules:
- Return only the numbered list.
- No explanations.
- No markdown.
- Keep it concise.

Example:

1. Create project
2. Write code
3. Save files
4. Run project
5. Fix errors if needed
"""

        response = self.provider.chat(
            prompt,
            task="planning"
        )

        return [
            line.strip()
            for line in response.splitlines()
            if line.strip()
        ]
