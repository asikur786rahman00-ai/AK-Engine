import os
import shlex
import subprocess
import sys


class RunnerAgent:

    def __init__(self, timeout=20):
        self.timeout = timeout

    def syntax_check(self, filename):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", filename],
                capture_output=True,
                text=True,
                timeout=10
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
                "stderr": "Syntax check timed out."
            }

        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e)
            }

    def run_python(self, filename, user_input="", args=None):
        if not os.path.exists(filename):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"File not found: {filename}",
                "stage": "runner"
            }

        syntax = self.syntax_check(filename)

        if not syntax["success"]:
            return {
                "success": False,
                "stdout": syntax["stdout"],
                "stderr": syntax["stderr"],
                "stage": "syntax"
            }

        try:
            filename = os.path.abspath(filename)
            project_dir = os.path.dirname(filename)
            script_name = os.path.basename(filename)

            command = [sys.executable, script_name]

            if args:
                if isinstance(args, str):
                    command.extend(shlex.split(args))
                elif isinstance(args, list):
                    command.extend(str(x) for x in args)

            if user_input and not user_input.endswith("\n"):
                user_input += "\n"

            result = subprocess.run(
                command,
                input=user_input if user_input else None,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=project_dir
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "stage": "runtime",
                "command": command,
                "cwd": project_dir
            }

        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = e.stderr or ""

            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors="replace")

            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors="replace")

            return {
                "success": False,
                "stdout": stdout,
                "stderr": (
                    stderr +
                    f"\nProgram timed out after {self.timeout} seconds."
                ),
                "stage": "timeout"
            }

        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "stage": "runner"
            }

