"""
AK Engine Canonical Smart Router.

Single source of truth for task -> model routing.
"""

from ak_engine.model_registry import MODEL_REGISTRY
from ak_engine.task_classifier import TaskClassifier


class SmartRouter:

    def __init__(self):
        self.classifier = TaskClassifier()

    def classify(self, message: str) -> str:
        return self.classifier.classify(message)

    def route(self, message: str, default_model=None) -> str:
        task = self.classify(message)

        config = MODEL_REGISTRY.get(
            task,
            MODEL_REGISTRY["general"],
        )

        primary = config.get("primary")

        if not primary:
            primary = default_model

        if not primary:
            raise RuntimeError(
                f"No primary model configured for task: {task}"
            )

        print(f"[AK Router] Task: {task}")
        print(f"[AK Router] Primary: {primary}")

        fallback = config.get("fallback", [])

        if fallback:
            print(
                f"[AK Router] Fallback: "
                f"{' -> '.join(fallback)}"
            )

        return primary

    def choose(self, message: str) -> str:
        """
        Backwards-compatible API.

        Older components call choose().
        New components should use route().
        """
        return self.route(message)

    def fallback_models(self, model: str):
        """
        Return configured fallback models for a primary model.
        """
        for config in MODEL_REGISTRY.values():

            if config.get("primary") == model:
                return list(
                    config.get("fallback", [])
                )

        return []

    def route_task(self, task: str) -> dict:
        """
        Route an explicit internal task without re-classifying
        the prompt.

        Used by agents that already know their task type.
        """
        if not isinstance(task, str):
            raise TypeError("task must be a string")

        task = task.strip().lower()

        if not task:
            task = "general"

        # Internal task aliases.
        aliases = {
            "planning": "reasoning",
            "debugging": "coding",
            "routing": "reasoning",
            "testing": "reasoning",
        }

        resolved_task = aliases.get(task, task)

        config = MODEL_REGISTRY.get(
            resolved_task,
            MODEL_REGISTRY["general"],
        )

        primary = config.get("primary")

        if not primary:
            raise RuntimeError(
                f"No primary model configured for task: {resolved_task}"
            )

        return {
            "task": task,
            "resolved_task": resolved_task,
            "primary": primary,
            "fallback": list(
                config.get("fallback", [])
            ),
        }

    def route_details(self, message: str) -> dict:
        """
        Return complete routing information without
        executing a provider request.
        """
        task = self.classify(message)

        config = MODEL_REGISTRY.get(
            task,
            MODEL_REGISTRY["general"],
        )

        return {
            "task": task,
            "primary": config.get("primary"),
            "fallback": list(
                config.get("fallback", [])
            ),
        }
