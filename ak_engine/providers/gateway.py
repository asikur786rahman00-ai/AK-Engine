"""
AK Engine Provider Gateway.

Responsibilities:
- model -> provider resolution
- provider health
- retries
- exponential backoff
- cooldown
- model-level fallback
- provider fallback
- safe status reporting
"""

import time
from dataclasses import dataclass

from ak_engine.providers.model_registry import get_deployment


@dataclass
class ProviderState:
    name: str
    provider: object
    failures: int = 0
    successes: int = 0
    total_requests: int = 0
    cooldown_until: float = 0.0
    last_error: str = ""
    last_latency: float = 0.0

    @property
    def available(self):
        return time.monotonic() >= self.cooldown_until


class ProviderGateway:

    def __init__(
        self,
        providers=None,
        max_retries=2,
        cooldown_seconds=30,
    ):
        self.max_retries = max(0, int(max_retries))
        self.cooldown_seconds = max(1, int(cooldown_seconds))

        self.states = {}

        for provider in providers or []:
            name = provider.__class__.__name__

            self.states[name] = ProviderState(
                name=name,
                provider=provider,
            )

    # --------------------------------------------------
    # Model resolution
    # --------------------------------------------------

    def resolve_model(self, model):
        deployment = get_deployment(model)

        state = self.states.get(
            deployment.provider
        )

        if state is None:
            raise RuntimeError(
                f"Provider {deployment.provider} "
                f"is not loaded for model {model}"
            )

        return deployment, state

    # --------------------------------------------------
    # Health
    # --------------------------------------------------

    def _cooldown(self, state, error):
        state.failures += 1
        state.last_error = str(error)

        state.cooldown_until = (
            time.monotonic()
            + self.cooldown_seconds
        )

        print(
            f"[Provider Gateway] "
            f"{state.name} cooldown "
            f"{self.cooldown_seconds}s"
        )

    def _success(self, state, latency):
        state.successes += 1
        state.last_latency = latency
        state.last_error = ""
        state.cooldown_until = 0.0

    # --------------------------------------------------
    # Single model execution
    # --------------------------------------------------

    def _execute_model(
        self,
        model,
        prompt,
        task,
    ):
        deployment, state = self.resolve_model(model)

        if not state.available:
            raise RuntimeError(
                f"Provider {state.name} "
                f"is currently cooling down."
            )

        # Model availability is checked separately from provider health.
        # A missing Ollama model must NOT put the whole Ollama provider
        # into cooldown.
        if hasattr(state.provider, "has_model"):
            try:
                if not state.provider.has_model(
                    deployment.model
                ):
                    raise RuntimeError(
                        f"Model {deployment.model} "
                        f"is not installed/available"
                    )
            except RuntimeError:
                raise
            except Exception as exc:
                raise RuntimeError(
                    f"Unable to check model availability: {exc}"
                )

        attempts = self.max_retries + 1
        last_error = None

        for attempt in range(1, attempts + 1):

            state.total_requests += 1

            print(
                f"[Provider Gateway] "
                f"{model} -> {state.name} "
                f"attempt {attempt}/{attempts}"
            )

            started = time.monotonic()

            try:
                result = state.provider.chat(
                    prompt,
                    task=task,
                    model=deployment.model,
                )

                latency = (
                    time.monotonic()
                    - started
                )

                if not result:
                    raise RuntimeError(
                        "Provider returned empty response."
                    )

                self._success(
                    state,
                    latency,
                )

                print(
                    f"[Provider Gateway] "
                    f"{model} succeeded "
                    f"({latency:.2f}s)"
                )

                return result

            except Exception as exc:
                last_error = exc

                print(
                    f"[Provider Gateway] "
                    f"{model} failed: {exc}"
                )

                if attempt < attempts:
                    delay = 2 ** (attempt - 1)

                    print(
                        f"[Provider Gateway] "
                        f"Retrying in {delay}s..."
                    )

                    time.sleep(delay)

        self._cooldown(
            state,
            last_error,
        )

        raise RuntimeError(
            f"Model {model} failed. "
            f"Last error: {last_error}"
        )

    # --------------------------------------------------
    # Model-level failover
    # --------------------------------------------------

    def chat(
        self,
        model,
        prompt,
        task="general",
        fallback_models=None,
    ):
        candidates = [model]

        for fallback in fallback_models or []:
            if fallback not in candidates:
                candidates.append(fallback)

        errors = []

        for candidate in candidates:

            print(
                f"[Provider Gateway] "
                f"Trying model: {candidate}"
            )

            try:
                return self._execute_model(
                    candidate,
                    prompt,
                    task,
                )

            except Exception as exc:
                errors.append(
                    f"{candidate}: {exc}"
                )

                print(
                    f"[Provider Gateway] "
                    f"Model {candidate} unavailable. "
                    f"Trying next fallback..."
                )

        raise RuntimeError(
            "All configured models failed.\n"
            + "\n".join(errors)
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def status(self):

        now = time.monotonic()

        return {
            name: {
                "available": (
                    now >= state.cooldown_until
                ),
                "failures": state.failures,
                "successes": state.successes,
                "total_requests": state.total_requests,
                "last_latency": state.last_latency,
                "last_error": state.last_error,
            }
            for name, state in self.states.items()
        }
