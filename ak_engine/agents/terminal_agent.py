import subprocess

class TerminalAgent:

    def run(self, command):

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
            }
