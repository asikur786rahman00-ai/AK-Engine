from ak_engine.providers.gemini import GeminiProvider
from ak_engine.providers.openrouter import OpenRouterProvider
from ak_engine.providers.groq import GroqProvider


class UniversalProvider:

    def __init__(self):

        self.gemini = GeminiProvider()
        self.openrouter = OpenRouterProvider()
        self.groq = GroqProvider()

    def chat(self, prompt, task="general"):

        if task == "planning":
            providers = [
                self.gemini,
                self.groq,
                self.openrouter,
            ]

        elif task in ("coding", "debugging"):
            providers = [
                self.groq,
                self.openrouter,
                self.gemini,
            ]

        else:
            providers = [
                self.groq,
                self.gemini,
                self.openrouter,
            ]

        last_error = None

        for provider in providers:

            print(f"[Provider] Trying {provider.__class__.__name__} ({task})")

            try:
                return provider.chat(prompt)

            except Exception as e:

                print(f"[Provider] {provider.__class__.__name__} failed")

                print(e)

                last_error = e

        raise last_error
