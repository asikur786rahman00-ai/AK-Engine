class TaskQueue:

    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append({
            "task": task,
            "status": "pending"
        })

    def next(self):

        for task in self.tasks:
            if task["status"] == "pending":
                task["status"] = "running"
                return task

        return None

    def complete(self, task):

        task["status"] = "done"

    def failed(self, task):

        task["status"] = "failed"

    def empty(self):

        return all(
            task["status"] == "done"
            for task in self.tasks
        )
