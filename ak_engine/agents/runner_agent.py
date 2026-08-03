import subprocess

class RunnerAgent:

    def run_python(self, filename):

        try:

            result = subprocess.run(
                ["python3", filename],
                input="5\n3\n+\nexit\n",
                capture_output=True,
                text=True,
                timeout=20
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Program timed out. It may be waiting for user input or stuck in an infinite loop."
            }

        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e)
            }
