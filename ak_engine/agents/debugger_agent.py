from ak_engine.providers.universal_provider import UniversalProvider

class DebuggerAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def fix_code(self, code, error):

        prompt = f"""
You are an expert Python debugger.

Your task is to fix the Python code.

Rules:
- Return ONLY complete Python code.
- No explanations.
- No markdown.
- No ``` blocks.
- Preserve the original functionality.
- Fix all errors.

Python Code:

{code}

Error:

{error}
"""

        fixed = self.provider.chat(
            prompt,
            task="debugging"
        ).strip()

        if fixed.startswith("```python"):
            fixed = fixed[9:]

        if fixed.startswith("```"):
            fixed = fixed[3:]

        if fixed.endswith("```"):
            fixed = fixed[:-3]

        return fixed.strip()
