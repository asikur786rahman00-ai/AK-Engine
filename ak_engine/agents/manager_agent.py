from ak_engine.agents.planner_agent import PlannerAgent
from ak_engine.agents.coding_agent import CodingAgent
from ak_engine.agents.runner_agent import RunnerAgent
from ak_engine.providers.gemini import GeminiProvider


class ManagerAgent:

    def __init__(self):
        provider = GeminiProvider()
        self.planner = PlannerAgent()
        self.coder = CodingAgent(provider)
        self.runner = RunnerAgent()

    def run(self, goal):
        print(f"[Manager] Goal: {goal}\n")

        print("[Planner] Creating plan...\n")
        plan = self.planner.plan(goal)

        for step in plan:
            print(step)

        print("\n[Manager] Generating project...\n")

        filename = self.coder.generate_python(goal)

        print(f"[Manager] Generated: {filename}")

        print("\n[Manager] Running project...\n")

        result = self.runner.run_python(filename)

        print(result)
