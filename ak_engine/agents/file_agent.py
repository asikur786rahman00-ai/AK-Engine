from pathlib import Path

class FileAgent:

    def create_file(self, filename, content=""):
        Path(filename).write_text(content, encoding="utf-8")
        return filename

    def read_file(self, filename):
        return Path(filename).read_text(encoding="utf-8")

    def run(self, task):

        task = task.lower()

        if ".py" in task:
            filename = task.split("`")[1] if "`" in task else "main.py"
            self.create_file(filename)
            print(f"[FileAgent] Created {filename}")

        elif ".md" in task:
            filename = task.split("`")[1] if "`" in task else "README.md"
            self.create_file(filename)
            print(f"[FileAgent] Created {filename}")

        else:
            print("[FileAgent] Nothing to do.")
