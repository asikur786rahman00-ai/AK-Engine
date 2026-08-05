from ak_engine.providers.openrouter import OpenRouterProvider

class ProviderManager:
    def __init__(self):
        self.providers = []

    def add(self, provider, name):
        self.providers.append((name, provider))

    def chat(self, model, message):
        last_error = None

        for name, provider in self.providers:
            try:
                print(f"Trying {name}...")
                reply = provider.chat(model, message)
                if reply:
                    print(f"✓ {name} succeeded")
                    return reply
            except Exception as e:
                print(f"✗ {name} failed: {e}")
                last_error = e

        raise RuntimeError(f"All providers failed. Last error: {last_error}")
