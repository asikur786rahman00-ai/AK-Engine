from ak_engine.agents.git_agent import GitAgent

git = GitAgent()

print("\n=== ADD ===")
print(git.add())

print("\n=== STATUS ===")
print(git.status())
