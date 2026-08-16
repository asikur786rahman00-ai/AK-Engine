"""
AK Engine logical model registry.

This registry defines preferred models and fallback models.
Concrete provider/model resolution is handled by the provider registry.
"""

MODEL_REGISTRY = {

    "coding": {
        "primary": "kimi-k2.7-code",
        "fallback": [
            "qwen3.5:397b",
            "gpt-oss:120b",
            "gemma4:31b-cloud",
        ],
    },

    "reasoning": {
        "primary": "glm-5.2",
        "fallback": [
            "qwen3.5:397b",
            "gpt-oss:120b",
            "gemma4:31b-cloud",
        ],
    },

    "writing": {
        "primary": "gpt-oss:120b",
        "fallback": [
            "glm-5.2",
            "gemma4:31b-cloud",
        ],
    },

    "general": {
        "primary": "gemma4:31b-cloud",
        "fallback": [],
    },
}
