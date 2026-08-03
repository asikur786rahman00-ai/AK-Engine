from ak_engine.agents.runner_agent import RunnerAgent

runner = RunnerAgent()

result = runner.run_python("generated_project/main.py")

print(result)
