from ak_engine.agents.planner_agent import PlannerAgent
from ak_engine.agents.coding_agent import CodingAgent
from ak_engine.agents.runner_agent import RunnerAgent
from ak_engine.agents.debugger_agent import DebuggerAgent
from ak_engine.agents.file_agent import FileAgent

class ManagerAgent:

    def __init__(self):
        self.planner = PlannerAgent()
        self.coder = CodingAgent()
        self.runner = RunnerAgent()
        self.debugger = DebuggerAgent()
        self.files = FileAgent()

    def run(self, goal):

        print(f"\n[Manager] Goal: {goal}\n")

        print("[Planner] Creating plan...\n")
        plan = self.planner.plan(goal)

        for step in plan:
            print(step)

        print("\n[Manager] Generating project...\n")

        filename = self.coder.generate_python(goal)

        for attempt in range(3):

            print(f"\n===== Attempt {attempt+1} =====")

            result = self.runner.run_python(filename)

            if result["success"]:
                print("\n✅ Project completed successfully.")
                return

            print(result["stderr"])

            code = self.files.read_file(filename)

            fixed = self.debugger.fix_code(
                code,
                result["stderr"]
            )

            self.files.write_file(filename, fixed)

            print("🔧 Code fixed.")

        print("\n❌ Failed after 3 attempts.")
