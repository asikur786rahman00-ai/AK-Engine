from ak_engine.agents.runner_agent import RunnerAgent

runner = RunnerAgent()

result = runner.run_python(
    "generated_project/main.py",
    input_data="5\n"
)

print("Success:", result["success"])
print()

print("STDOUT:")
print(result["stdout"])

print()

print("STDERR:")
print(result["stderr"])
