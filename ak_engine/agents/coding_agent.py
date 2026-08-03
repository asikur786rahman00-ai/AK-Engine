from pathlib import Path
import re
from ak_engine.providers.universal_provider import UniversalProvider

class CodingAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def extract_requirements(self, code):

        packages = set()

        for line in code.splitlines():

            line = line.strip()

            if line.startswith("import "):
                name = line.split()[1].split(".")[0]
                packages.add(name)

            elif line.startswith("from "):
                name = line.split()[1].split(".")[0]
                packages.add(name)

        stdlib = {
            "os","sys","json","time","math","random",
            "pathlib","typing","threading","subprocess",
            "datetime","collections","itertools","functools",
            "re","shutil","tempfile","logging","asyncio"
        }

        packages = sorted(
            p for p in packages
            if p not in stdlib
        )

        return "\n".join(packages)

    def generate_python(self, task):

        prompt = f"""
Return ONLY complete Python code.

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

        project = Path("generated_project")
        project.mkdir(exist_ok=True)

        (project/"main.py").write_text(
            code,
            encoding="utf-8"
        )

        (project/"README.md").write_text(
            f"# {task}\n",
            encoding="utf-8"
        )

        requirements = self.extract_requirements(code)

        (project/"requirements.txt").write_text(
            requirements,
            encoding="utf-8"
        )

        (project/"config.py").write_text(
            "# Configuration\n",
            encoding="utf-8"
        )

        return str(project/"main.py")
