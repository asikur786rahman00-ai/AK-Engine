from ak_engine.agents.planner_agent import PlannerAgent

planner = PlannerAgent()

steps = planner.plan("Create a Python calculator")

for step in steps:
    print(step)
