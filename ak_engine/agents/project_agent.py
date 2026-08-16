import json
import os
import re

from ak_engine.providers.universal_provider import UniversalProvider


class ProjectAgent:

    MAX_ATTEMPTS = 3

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def _clean_reply(self, reply):
        reply = reply.strip()

        reply = re.sub(
            r"^\s*```(?:json)?\s*",
            "",
            reply,
            flags=re.IGNORECASE
        )

        reply = re.sub(
            r"\s*```\s*$",
            "",
            reply
        )

        return reply.strip()

    def _extract_json(self, reply):

        reply = self._clean_reply(reply)

        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            pass

        start = reply.find("{")

        if start == -1:
            raise RuntimeError(
                "No JSON object found.\n\n"
                f"Model returned:\n{reply}"
            )

        depth = 0
        in_string = False
        escaped = False

        for i in range(start, len(reply)):

            char = reply[i]

            if escaped:
                escaped = False
                continue

            if char == "\\" and in_string:
                escaped = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            if char == "{":
                depth += 1

            elif char == "}":
                depth -= 1

                if depth == 0:

                    candidate = reply[start:i + 1]

                    try:
                        return json.loads(candidate)

                    except json.JSONDecodeError as e:
                        raise RuntimeError(
                            "Model returned malformed JSON.\n\n"
                            f"JSON error: {e}\n\n"
                            f"Model returned:\n{reply}"
                        ) from e

        raise RuntimeError(
            f"Unclosed JSON object.\n\n"
            f"Model returned:\n{reply}"
        )

    def _validate_project(self, project, goal):

        if not isinstance(project, dict):
            return False, "Project is not a dictionary."

        if not project.get("entrypoint"):
            return False, "Missing entrypoint."

        files = project.get("files")

        if not isinstance(files, list) or not files:
            return False, "Project contains no files."

        file_map = {}

        for file in files:

            if not isinstance(file, dict):
                return False, "Invalid file definition."

            path = file.get("path")
            content = file.get("content")

            if not path or not isinstance(content, str):
                return False, "Every file needs path and content."

            file_map[path] = content

        entrypoint = project["entrypoint"]

        if entrypoint not in file_map:
            return False, f"Entrypoint {entrypoint} does not exist."

        main_code = file_map[entrypoint].strip()

        if len(main_code) < 30:
            return False, "Entrypoint is suspiciously small."

        combined = "\n".join(file_map.values()).lower()

        # Detect obvious placeholder projects.
        placeholder_patterns = [
            "todo: implement",
            "not implemented",
            "coming soon",
            "example project",
            "calculator started",
        ]

        for pattern in placeholder_patterns:

            if pattern in combined:
                return False, (
                    f"Generated project contains placeholder text: "
                    f"{pattern}"
                )

        # The entrypoint may be intentionally small when functionality
        # is split across multiple modules. Validate the whole project.
        meaningful_lines = [
            line.strip()
            for line in main_code.splitlines()
            if line.strip()
            and not line.strip().startswith("#")
        ]

        if len(meaningful_lines) < 2 and len(file_map) == 1:
            return False, "Entrypoint contains too little real functionality."

        total_meaningful_lines = sum(
            len([
                line for line in content.splitlines()
                if line.strip()
                and not line.strip().startswith("#")
            ])
            for content in file_map.values()
        )

        if total_meaningful_lines < 5:
            return False, "Project contains too little real functionality."

        # Special quality checks for calculator projects.
        if "calculator" in goal.lower():

            arithmetic_found = any(
                token in combined
                for token in [
                    "def add",
                    "def subtract",
                    "def multiply",
                    "def divide",
                    "operator",
                    " + ",
                    " - ",
                    " * ",
                    " / "
                ]
            )

            if not arithmetic_found:
                return False, (
                    "Calculator does not contain real arithmetic functionality."
                )

            interaction_found = any(
                token in combined
                for token in [
                    "input(",
                    "argparse",
                    "sys.argv"
                ]
            )

            if not interaction_found:
                return False, (
                    "Calculator has no usable user input or command-line interface."
                )

        return True, "Project structure looks valid."

    def generate(
        self,
        goal,
        research="",
        memory="",
        packages="",
    ):

        feedback = ""

        for attempt in range(1, self.MAX_ATTEMPTS + 1):

            print(
                f"[ProjectAgent] Generation attempt {attempt}"
            )

            prompt = f"""
You are the primary autonomous software engineer.

Build a REAL, COMPLETE, EXECUTABLE Python project.

Goal:
{goal}

Research:
{research}

Previous project memory:
{memory}

Packages:
{packages}

Previous generation feedback:
{feedback}

IMPORTANT:

The project must actually accomplish the user's goal.

DO NOT create:
- placeholder programs
- demo-only programs
- fake implementations
- "Project started" programs
- "Calculator started" programs
- TODO implementations
- empty functions
- meaningless print statements
- code that only describes the project

The entrypoint must actually execute the requested functionality.

For interactive programs:
- implement real input handling
- implement validation
- implement error handling
- provide a valid exit path

For a calculator:
- implement addition
- implement subtraction
- implement multiplication
- implement division
- handle division by zero
- accept real user input
- provide a valid quit/exit option
- actually calculate and print results

Keep the project practical.
Do not add GUI functionality unless the goal specifically requests a GUI.

Use Python standard library whenever possible.
Do not invent unnecessary dependencies.

Return ONLY valid JSON.

JSON format:

{{
  "entrypoint": "main.py",
  "files": [
    {{
      "path": "main.py",
      "content": "complete Python source code"
    }}
  ]
}}

CRITICAL JSON RULES:

1. Valid JSON only.
2. Every content value must be a JSON string.
3. Escape newlines correctly.
4. Escape double quotes correctly.
5. No markdown.
6. No ``` blocks.
7. No explanations before or after JSON.
"""

            try:

                reply = self.provider.chat(
                    prompt,
                    task="coding"
                ).strip()

                project = self._extract_json(reply)

                valid, reason = self._validate_project(
                    project,
                    goal
                )

                if not valid:

                    print(
                        f"[ProjectAgent] Rejected: {reason}"
                    )

                    feedback = (
                        f"The previous project was rejected because: "
                        f"{reason}. "
                        f"Generate a real working implementation."
                    )

                    continue

                return project

            except Exception as e:

                print(
                    f"[ProjectAgent] Attempt {attempt} failed: {e}"
                )

                feedback = (
                    "Previous generation failed. "
                    "Return strict valid JSON and a complete working project."
                )

        raise RuntimeError(
            "ProjectAgent failed to generate a valid project "
            f"after {self.MAX_ATTEMPTS} attempts."
        )

    def write_project(self, project):

        if not isinstance(project, dict):
            raise ValueError(
                "Project must be a dictionary."
            )

        if "entrypoint" not in project:
            raise ValueError(
                "Project is missing 'entrypoint'."
            )

        if "files" not in project:
            raise ValueError(
                "Project is missing 'files'."
            )

        root = "generated_project"

        os.makedirs(root, exist_ok=True)

        safe_root = os.path.abspath(root)

        for file in project["files"]:

            if (
                "path" not in file
                or "content" not in file
            ):
                raise ValueError(
                    "Every project file must contain "
                    "'path' and 'content'."
                )

            path = os.path.join(
                root,
                file["path"]
            )

            safe_path = os.path.abspath(path)

            if not (
                safe_path == safe_root
                or safe_path.startswith(
                    safe_root + os.sep
                )
            ):
                raise ValueError(
                    f"Unsafe project path: {file['path']}"
                )

            parent = os.path.dirname(path)

            if parent:
                os.makedirs(
                    parent,
                    exist_ok=True
                )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(file["content"])

        return os.path.join(
            root,
            project["entrypoint"]
        )
