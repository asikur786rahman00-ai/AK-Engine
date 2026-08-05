from ak_engine.agents.planner_agent import PlannerAgent
from ak_engine.agents.coding_agent import CodingAgent
from ak_engine.agents.runner_agent import RunnerAgent
from ak_engine.agents.debugger_agent import DebuggerAgent
from ak_engine.agents.file_agent import FileAgent
from ak_engine.agents.terminal_agent import TerminalAgent
from ak_engine.agents.git_agent import GitAgent
from ak_engine.agents.memory_agent import MemoryAgent
from ak_engine.agents.input_agent import InputAgent


class Orchestrator:

    def __init__(self):

        self.planner = PlannerAgent()
        self.coder = CodingAgent()
        self.runner = RunnerAgent()
        self.debugger = DebuggerAgent()
        self.files = FileAgent()
        self.terminal = TerminalAgent()
        self.git = GitAgent()
        self.memory = MemoryAgent()
        self.input_agent = InputAgent()

    def execute(self, goal):

        print(f"\n🎯 Goal: {goal}\n")

        self.memory.remember("last_goal", goal)

        print("[Planner]")
        plan = self.planner.plan(goal)

        for step in plan:
            print(step)

        print("\n[Coder]")
        filename = self.coder.generate_python(goal)
        print(f"Generated: {filename}")

        for attempt in range(1, 4):

            print(f"\n========== Attempt {attempt} ==========\n")

            code = self.files.read_file(filename)

            print("[Input Agent]")
            sample_input = self.input_agent.generate(goal, code)

            print(sample_input)

            print("\n[Runner]")

            result = self.runner.run_python(
                filename,
                sample_input
            )

            if result["success"]:
                print(result["stdout"])
                print("\n✅ Project completed successfully.")
                return

            print(result["stderr"])

            print("\n[Debugger]")

            fixed = self.debugger.fix_code(
                code,
                result["stderr"]
            )

            self.files.write_file(filename, fixed)

            print("🔧 Code updated.")

        print("\n❌ Failed after 3 repair attempts.")
