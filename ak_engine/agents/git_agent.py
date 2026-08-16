import subprocess

class GitAgent:

    def run(self, command):

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def init(self):
        return self.run("git init")

    def add(self):
        return self.run("git add .")

    def commit(self, message):
        return self.run(f'git commit -m "{message}"')

    def status(self):
        return self.run("git status")

    def push(self):
        return self.run("git push")
