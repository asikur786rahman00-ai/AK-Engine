"""
AK Engine Universal Provider.

Thin provider facade used by all AI agents.

Provider selection, retries, cooldowns, health tracking,
and fallback are delegated to ProviderGateway.
"""

from dotenv import load_dotenv

load_dotenv()

from ak_engine.providers.gemini import GeminiProvider
from ak_engine.providers.groq import GroqProvider
from ak_engine.providers.openrouter import OpenRouterProvider
from ak_engine.providers.ollama import OllamaProvider
from ak_engine.providers.gateway import ProviderGateway
from ak_engine.smart_router import SmartRouter


class UniversalProvider:

    def __init__(
        self,
        providers=None,
        max_retries=2,
        cooldown_seconds=30,
    ):
        if providers is None:
            providers = []

            provider_classes = [
                ("Ollama", OllamaProvider),
                ("Gemini", GeminiProvider),
                ("Groq", GroqProvider),
                ("OpenRouter", OpenRouterProvider),
            ]

            for name, provider_class in provider_classes:
                try:
                    provider = provider_class()
                    providers.append(provider)
                    print(f"[Provider] Loaded {name}")

                except Exception as exc:
                    print(
                        f"[Provider] Skipping {name}: {exc}"
                    )

        self.providers = providers
        self.router = SmartRouter()

        self.gateway = ProviderGateway(
            providers=self.providers,
            max_retries=max_retries,
            cooldown_seconds=cooldown_seconds,
        )

    def chat(self, prompt, task="general"):
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("prompt cannot be empty")

        details = self.router.route_details(prompt)

        model = details["primary"]
        fallback_models = details.get("fallback", [])

        print(
            f"[UniversalProvider] Task: {task}"
        )

        print(
            f"[UniversalProvider] Model: {model}"
        )

        return self.gateway.chat(
            model=model,
            prompt=prompt,
            task=task,
            fallback_models=fallback_models,
        )

    def status(self):
        return self.gateway.status()
