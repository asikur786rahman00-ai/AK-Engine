from ak_engine.agents.task_queue import TaskQueue

queue = TaskQueue()

queue.add("Create project")
queue.add("Generate code")
queue.add("Run project")

while True:

    task = queue.next()

    if not task:
        break

    print(f"Running: {task['task']}")

    queue.complete(task)

print("All tasks completed!")
