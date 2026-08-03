from ak_engine.agents.planner_agent import PlannerAgent
from ak_engine.agents.executor_agent import ExecutorAgent

planner = PlannerAgent()
executor = ExecutorAgent()

goal = "Create a calculator"

print("Goal:", goal)
print()

steps = planner.plan(goal)

print("Plan:")
for step in steps:
    print("-", step)

print()
print("Executing...")
print()

executor.execute(steps, goal)
