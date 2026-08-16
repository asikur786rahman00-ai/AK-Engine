from pathlib import Path
from ak_engine.providers.universal_provider import UniversalProvider
from ak_engine.agents.dependency_agent import DependencyAgent


class CodingAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()
        self.dependency_agent = DependencyAgent()

    def extract_requirements(self, code):

        packages = set()

        stdlib = {
            "os","sys","json","time","math","random",
            "pathlib","typing","threading","subprocess",
            "datetime","collections","itertools",
            "functools","re","shutil","tempfile",
            "logging","asyncio","sqlite3"
        }

        for line in code.splitlines():

            line = line.strip()

            if line.startswith("import "):
                name = line.split()[1].split(".")[0]

                if name not in stdlib:
                    packages.add(name)

            elif line.startswith("from "):
                name = line.split()[1].split(".")[0]

                if name not in stdlib:
                    packages.add(name)

        return "\n".join(sorted(packages))

    def generate_python(
        self,
        goal,
        research="",
        memory="",
        packages=""
    ):

        prompt = f"""
You are an expert senior Python software engineer.

Goal:
{goal}

Research Notes:
{research}

Previous Knowledge:
{memory}

Required Packages:
{packages}

Rules:

- Return ONLY Python code.
- No markdown.
- No explanations.
- Produce production-quality code.
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

        # Analyze Python dependencies
        dependency_info = self.dependency_agent.analyze(code)

        project = Path("generated_project")
        project.mkdir(exist_ok=True)

        (project / "main.py").write_text(
            code,
            encoding="utf-8"
        )

        (project / "README.md").write_text(
            f"# {goal}\n",
            encoding="utf-8"
        )

        # Write only dependencies that are actually missing
        requirements = "\n".join(
            dependency_info["missing"]
        )

        (project / "requirements.txt").write_text(
            requirements,
            encoding="utf-8"
        )

        (project / "config.py").write_text(
            "# Configuration\n",
            encoding="utf-8"
        )

        return str(project / "main.py")
