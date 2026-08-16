import json
import os


class LearningMemory:

    def __init__(self, filename="learning_memory.json"):

        self.filename = filename

        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump([], f)

    def remember(self, goal, packages, success):

        with open(self.filename, "r") as f:
            data = json.load(f)

        data.append({
            "goal": goal,
            "packages": packages,
            "success": success
        })

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def search(self, goal):

        with open(self.filename) as f:
            data = json.load(f)

        return [
            item for item in data
            if goal.lower() in item["goal"].lower()
        ]
