class ToolRouter:

    def route(self, task):

        task = task.lower()

        # File operations
        if any(word in task for word in [
            "file",
            "folder",
            "directory",
            "save",
            "read"
        ]):
            return "file"

        # Terminal operations
        if any(word in task for word in [
            "install",
            "package",
            "pip",
            "dependency",
            "terminal",
            "command"
        ]):
            return "terminal"

        # Debugging
        if any(word in task for word in [
            "debug",
            "fix",
            "repair",
            "error"
        ]):
            return "debugger"

        # Runner
        if any(word in task for word in [
            "run",
            "execute",
            "launch",
            "start"
        ]):
            return "runner"

        # Coding
        if any(word in task for word in [
            "code",
            "python",
            "develop",
            "implement",
            "program",
            "script",
            "write",
            "create"
        ]):
            return "coding"

        return "unknown"
