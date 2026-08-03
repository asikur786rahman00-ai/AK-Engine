from pathlib import Path

from ak_engine.providers.gemini import GeminiProvider
from ak_engine.agents.runner_agent import RunnerAgent
from ak_engine.agents.debugger_agent import DebuggerAgent

provider = GeminiProvider()
runner = RunnerAgent()
debugger = DebuggerAgent(provider)

file = Path("generated_project/main.py")

for attempt in range(3):

    print(f"\n===== Attempt {attempt+1} =====")

    result = runner.run_python(file)

    if result["success"]:
        print("SUCCESS!")
        break

    print(result["stderr"])

    code = file.read_text()

    fixed = debugger.fix_code(
        code,
        result["stderr"]
    )

    file.write_text(fixed)

    print("Code updated.")

print("Finished.")
