import subprocess

class RunnerAgent:

    def run_python(self, filepath, input_data=None, timeout=10):

        print(f"[Runner] Running {filepath}")

        try:

            result = subprocess.run(
                ["python3", str(filepath)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Program timed out."
            }
