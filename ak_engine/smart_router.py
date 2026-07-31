"""
AK Engine Smart Router
"""

from ak_engine.model_registry import MODEL_REGISTRY
from ak_engine.task_classifier import TaskClassifier


class SmartRouter:
    def __init__(self):
        self.classifier = TaskClassifier()

    def route(self, message: str, default_model: str = "gpt-oss:120b") -> str:
        task = self.classifier.classify(message)

        config = MODEL_REGISTRY.get(task, MODEL_REGISTRY["general"])

        primary = config["primary"]
        fallback = config.get("fallback", [])

        print(f"[AK Engine] Task: {task}")
        print(f"[AK Engine] Primary: {primary}")

        if fallback:
            print(f"[AK Engine] Fallback: {' -> '.join(fallback)}")

        return primary

    def fallback_models(self, model: str):
        for cfg in MODEL_REGISTRY.values():
            if cfg["primary"] == model:
                return cfg.get("fallback", [])
        return []
