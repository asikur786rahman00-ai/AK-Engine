from ak_engine.agents.router_agent import RouterAgent

router = RouterAgent()

tests = [
    "Create a calculator",
    "Create README.md",
    "Run ls",
    "Show current folder",
    "Build a Python app"
]

for task in tests:
    print(task, "->", router.route(task))
