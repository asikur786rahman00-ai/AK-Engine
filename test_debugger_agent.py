from ak_engine.providers.gemini import GeminiProvider
from ak_engine.agents.debugger_agent import DebuggerAgent

provider = GeminiProvider()
debugger = DebuggerAgent(provider)

bad_code = """
print("Hello"
"""

error = """
SyntaxError: '(' was never closed
"""

fixed = debugger.fix_code(bad_code, error)

print(fixed)
