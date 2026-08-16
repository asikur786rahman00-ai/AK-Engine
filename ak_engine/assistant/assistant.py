"""
AK Engine Assistant.

High-level conversational interface.

Architecture:

AKAssistant
    -> SmartRouter
    -> UniversalProvider
    -> ProviderGateway
    -> Model Registry
    -> Concrete Provider
"""

from ak_engine.memory.manager import MemoryManager
from ak_engine.smart_router import SmartRouter
from ak_engine.providers.universal_provider import UniversalProvider


class AKAssistant:

    def __init__(self, provider=None, router=None):
        self.memory = MemoryManager()

        self.router = router or SmartRouter()

        self.provider = provider or UniversalProvider()

    def chat(self, message):

        if not isinstance(message, str):
            raise TypeError("message must be a string")

        message = message.strip()

        if not message:
            raise ValueError("message cannot be empty")

        self.memory.add_message(
            "user",
            message,
        )

        self.memory.auto_remember(
            message
        )

        # Resolve the logical model through the
        # centralized SmartRouter.
        details = self.router.route_details(
            message
        )

        task = details["task"]
        model = details["primary"]
        fallback_models = details.get(
            "fallback",
            [],
        )

        print(
            f"[Assistant] Task: {task}"
        )

        print(
            f"[Assistant] Model: {model}"
        )

        # UniversalProvider owns the Gateway.
        # Gateway owns provider execution,
        # retries, cooldown and deployment resolution.
        reply = self.provider.gateway.chat(
            model,
            message,
            task=task,
            fallback_models=fallback_models,
        )

        self.memory.add_message(
            "assistant",
            reply,
        )

        return reply

    def status(self):
        return self.provider.status()
