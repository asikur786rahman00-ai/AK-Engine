from ak_engine.agents.terminal_agent import TerminalAgent

agent = TerminalAgent()

commands = [
    "pwd",
    "ls",
    "python3 --version"
]

for cmd in commands:

    print("=" * 50)
    print("Running:", cmd)

    result = agent.run(cmd)

    print("Success:", result["success"])
    print(result["stdout"])

    if result["stderr"]:
        print(result["stderr"])
