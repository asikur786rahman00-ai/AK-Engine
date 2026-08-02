from pathlib import Path

class CodingAgent:
    def __init__(self, provider):
        self.provider = provider

    def generate_python(self, prompt, filename="main.py"):
        code = self.provider.chat(
            f"""
You are an expert Python programmer.

Return ONLY valid Python code.

Task:
{prompt}
"""
        )

        project = Path("generated_project")
        project.mkdir(exist_ok=True)

        file = project / filename
        file.write_text(code, encoding="utf-8")

        return file
