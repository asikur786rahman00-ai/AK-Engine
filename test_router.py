from ak_engine.router.router import SmartRouter

router = SmartRouter()

tasks = [
    "Write a Python script",
    "Create an image",
    "Write a poem",
    "Calculate 25*47",
    "Tell me a joke"
]

for task in tasks:
    print(f"{task} -> {router.choose(task)}")
