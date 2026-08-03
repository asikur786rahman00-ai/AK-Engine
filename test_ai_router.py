from ak_engine.agents.ai_router import AIRouter

router = AIRouter()

tests = [
    "Write a calculator",
    "Run the project",
    "Fix this bug",
    "Create README.md",
    "Install flask"
]

for t in tests:
    print(f"{t} -> {router.route(t)}")
