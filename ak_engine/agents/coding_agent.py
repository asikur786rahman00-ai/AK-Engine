from pathlib import Path
from ak_engine.providers.universal_provider import UniversalProvider

class CodingAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def generate_python(self, task):

        prompt = f"""
You are an expert Python developer.

Generate ONLY complete Python code.

Rules:
- Return ONLY Python code.
- No markdown.
- No explanations.
- No ``` blocks.
- Do NOT use input().
- Do NOT create infinite loops.
- The program must execute automatically and exit.
- Use sample values instead of asking the user for input.

Task:
{task}
"""

        code = self.provider.chat(
            prompt,
            task="coding"
        ).strip()

        if code.startswith("```python"):
            code = code[9:]

        if code.startswith("```"):
            code = code[3:]

        if code.endswith("```"):
            code = code[:-3]

        code = code.strip()

        Path("generated_project").mkdir(exist_ok=True)

        filename = "generated_project/main.py"

        Path(filename).write_text(code, encoding="utf-8")

        return filename
