class RouterAgent:

    def route(self, task):
        task = task.lower()

        # File tasks
        if any(word in task for word in [
            ".py", ".txt", ".md", "readme",
            "file", "folder", "read", "write"
        ]):
            return "file"

        # Terminal tasks
        if any(word in task for word in [
            "terminal", "command", "ls",
            "pwd", "pip"
        ]):
            return "terminal"

        # Coding tasks
        if any(word in task for word in [
            "create", "build", "code",
            "python", "app"
        ]):
            return "coding"

        return "unknown"
