import os

from ak_engine.providers.manager import ProviderManager
from ak_engine.providers.openrouter import OpenRouterProvider

manager = ProviderManager()

manager.add(
    OpenRouterProvider(os.environ["OPENROUTER_API_KEY"]),
    "OpenRouter"
)

reply = manager.chat(
    "deepseek/deepseek-chat-v3-0324",
    "Say hello to AK."
)

print("\nReply:")
print(reply)
