class SmartRouter:
    def choose(self, task):
        task = task.lower()

        if any(x in task for x in [
            "python",
            "code",
            "bug",
            "error",
            "terminal",
            "linux",
            "program"
        ]):
            return "deepseek"

        if any(x in task for x in [
            "story",
            "poem",
            "creative",
            "write"
        ]):
            return "claude"

        if any(x in task for x in [
            "image",
            "photo",
            "draw",
            "picture"
        ]):
            return "gemini"

        if any(x in task for x in [
            "math",
            "calculate"
        ]):
            return "gpt"

        return "gpt-oss:120b"
