from dataclasses import dataclass

@dataclass
class Plan:
    goal: str
    steps: list[str]

class PlannerV2:
    def create_plan(self, goal: str):
        goal_lower = goal.lower()
        steps = []

        if "create" in goal_lower or "build" in goal_lower:
            steps.append("file")
            steps.append("coding")
            steps.append("terminal")
            steps.append("runner")

        elif "fix" in goal_lower or "debug" in goal_lower:
            steps.append("debugger")
            steps.append("runner")

        elif "run" in goal_lower:
            steps.append("runner")

        else:
            steps.append("coding")

        return Plan(goal, steps)
