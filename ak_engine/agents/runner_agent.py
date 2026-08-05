import subprocess


class RunnerAgent:

    def run_python(self, filename, user_input=""):

        try:

            result = subprocess.run(
                ["python3", filename],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=20
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e)
            }
