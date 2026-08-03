from ak_engine.agents.validator_agent import ValidatorAgent

validator = ValidatorAgent()

good = """
def hello():
    print("Hello")
"""

bad = """
An elegant way to solve this problem is...
"""

print("Good Python:", validator.is_python(good))
print("Bad Python:", validator.is_python(bad))

print()

print("Looks like explanation:", validator.looks_like_explanation(bad))
