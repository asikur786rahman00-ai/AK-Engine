import importlib.util
import subprocess
import sys

from ak_engine.agents.dependency_agent import DependencyAgent


class ToolAgent:

    def __init__(self):
        self.dependency_agent = DependencyAgent()

    def analyze_code(self, code):
        print("[ToolAgent] Scanning project imports...")

        result = self.dependency_agent.classify(code)

        print("[ToolAgent] Standard library:", result["stdlib"])
        print("[ToolAgent] Already installed:", result["installed"])
        print("[ToolAgent] Missing:", result["missing"])

        return result

    def install_missing(self, packages):

        if not packages:
            print("[ToolAgent] ✅ No dependencies to install.")
            return

        for package in packages:

            # Extra safety check
            if importlib.util.find_spec(package) is not None:
                print(f"[ToolAgent] ✅ Already available: {package}")
                continue

            print(f"[ToolAgent] 📦 Installing: {package}")

            subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=False
            )

    def detect_packages(self, goal):
        """
        Kept for backwards compatibility.

        Package detection should happen from generated code,
        not from the natural-language goal.
        """
        print("[ToolAgent] Goal-based package guessing disabled.")
        return []
