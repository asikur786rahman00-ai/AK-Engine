from ak_engine.agents.terminal_agent import TerminalAgent

agent = TerminalAgent()

tests = [
    "pwd",
    "ls",
    "python3 --version",
]

for cmd in tests:
    print(f"\n$ {cmd}")
    result = agent.run(cmd)
    print(result)
