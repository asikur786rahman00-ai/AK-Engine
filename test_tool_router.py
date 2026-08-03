from ak_engine.agents.tool_router import ToolRouter

router = ToolRouter()

tests = [
    "Write calculator code",
    "Run project",
    "Debug application",
    "Create project folder",
    "Install Flask",
]

for t in tests:
    print(f"{t} -> {router.route(t)}")
