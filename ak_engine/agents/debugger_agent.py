from ak_engine.providers.universal_provider import UniversalProvider


class DebuggerAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def fix_code(self, code, error, verification=None):
        verification_text = ""

        if verification:
            verification_text = f"""
DETERMINISTIC VERIFICATION FAILURE

Failed cases:
{verification.get("failed_cases", [])}

Verification summary:
{verification}

The deterministic engine is the authority.
Repair the implementation. Do not weaken the tests.
"""

        prompt = f"""
You are an expert autonomous Python debugger.

Repair this Python source code.

SOURCE:
{code}

RUNTIME ERROR:
{error}

{verification_text}

Rules:
- Return ONLY complete Python source code.
- No markdown.
- No explanations.
- Preserve existing functionality.
- Fix the root cause.
- Never hardcode test answers.
- Never remove validation.
- Never weaken tests.
"""

        fixed = self.provider.chat(
            prompt,
            task="debugging"
        ).strip()

        return self._clean(fixed)

    def fix_project(
        self,
        files,
        entrypoint,
        error,
        verification=None,
    ):
        """
        Project-aware repair.

        The model receives the project context and may return
        a repaired file map. The orchestrator remains responsible
        for validating the repaired project.
        """

        verification_text = ""

        if verification:
            verification_text = f"""
DETERMINISTIC FAILURE EVIDENCE:

{verification}

Failed cases are authoritative.
Do not modify the tests to make them pass.
"""

        project_text = []

        for path, content in files.items():
            project_text.append(
                f"""
===== FILE: {path} =====
{content}
"""
            )

        prompt = f"""
You are AK Engine's autonomous software repair engineer.

A generated Python project failed runtime verification.

ENTRYPOINT:
{entrypoint}

RUNTIME ERROR:
{error}

{verification_text}

PROJECT:

{"".join(project_text)}

Your job:

1. Diagnose the actual root cause.
2. Identify the smallest set of files that need modification.
3. Preserve all working functionality.
4. Fix the implementation.
5. Never fake expected output.
6. Never remove validation.
7. Never weaken the test contract.
8. Keep the project executable.

Return ONLY valid JSON:

{{
  "files": [
    {{
      "path": "relative/path.py",
      "content": "complete repaired source"
    }}
  ],
  "reason": "short root-cause explanation"
}}

Only return files that actually need modification.
"""

        reply = self.provider.chat(
            prompt,
            task="debugging"
        ).strip()

        return reply

    @staticmethod
    def _clean(text):
        if text.startswith("```python"):
            text = text[9:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()
