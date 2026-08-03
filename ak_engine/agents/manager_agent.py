from ak_engine.agents.planner_agent import PlannerAgent
from ak_engine.agents.coding_agent import CodingAgent
from ak_engine.agents.runner_agent import RunnerAgent
from ak_engine.agents.task_queue import TaskQueue

class ManagerAgent:

    def __init__(self):
        self.planner = PlannerAgent()
        self.coder = CodingAgent()
        self.runner = RunnerAgent()
        self.queue = TaskQueue()

    def run(self, goal):

        print(f"\n[Manager] Goal: {goal}\n")

        print("[Planner] Creating plan...\n")

        steps = self.planner.plan(goal)

        for step in steps:
            self.queue.add(step)

        while True:

            task = self.queue.next()

            if task is None:
                break

            print(f"\n[Task] {task['task']}")

            if "code" in task["task"].lower():
                filename = self.coder.generate_python(goal)
                print(f"Generated: {filename}")

            self.queue.complete(task)

        print("\n✅ Project workflow completed.")
