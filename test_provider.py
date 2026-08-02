import os
from ak_engine.providers.openrouter import OpenRouterProvider

provider = OpenRouterProvider(os.environ["OPENROUTER_API_KEY"])

reply = provider.chat(
    "deepseek/deepseek-chat-v3-0324",
    "Reply with exactly: Hello AK, your engine is alive!"
)

print("\n=== AI Reply ===")
print(reply)
