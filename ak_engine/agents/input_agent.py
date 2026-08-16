import re
from ak_engine.providers.universal_provider import UniversalProvider


class InputAgent:

    def __init__(self, provider=None):
        self.provider = provider or UniversalProvider()

    def _extract_interactive_inputs(self, code):
        """
        Extract visible input() prompts from generated Python code.
        This is deterministic evidence used before asking the LLM
        to design a test sequence.
        """
        prompts = re.findall(
            r"""input\s*\(\s*(?:f)?["']([^"']*)["']\s*\)""",
            code,
            flags=re.IGNORECASE,
        )

        return prompts

    def generate(self, goal, code):
        prompts = self._extract_interactive_inputs(code)

        prompt_evidence = "\n".join(
            f"{i + 1}. {prompt!r}"
            for i, prompt in enumerate(prompts)
        )

        prompt = f"""
You are AK Engine's deterministic test designer.

Goal:
{goal}

Generated Python program:
{code}

Detected input() prompts:
{prompt_evidence or "No literal input() prompts detected."}

Your job is to create ONE COMPLETE stdin test sequence for the ACTUAL
program.

CRITICAL RULES:

1. Read the Python code carefully.
2. Follow the REAL input() order.
3. Every input() call receives exactly ONE line.
4. NEVER output a multi-line conceptual test such as:
   add
   10
   5
   unless the program actually calls input() separately for each value.
5. If the program expects an expression such as:
   10 + 5
   provide exactly:
   10 + 5
6. If the program expects a menu choice, provide the actual menu value.
7. Do not invent commands.
8. Test the main functionality.
9. Include one useful edge case when possible.
10. If there is a valid exit/quit command, use it at the end.
11. Never leave the program waiting for more input.
12. Return ONLY raw stdin.
13. One input value per line.
14. No explanations.
15. No markdown.
16. No code fences.

Generate the test sequence now.
"""

        print("[InputAgent] Generating contract-aware test input...")

        result = self.provider.chat(
            prompt,
            task="testing"
        ).strip()

        # Remove accidental markdown fences from weak model responses.
        if result.startswith("```"):
            result = re.sub(r"^```[a-zA-Z0-9_+-]*\s*", "", result)
            result = re.sub(r"\s*```$", "", result)

        return result.strip()
