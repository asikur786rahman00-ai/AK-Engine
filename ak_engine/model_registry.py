MODEL_REGISTRY = {

    "coding": {
        "primary": "kimi-k2.7-code",
        "fallback": [
            "qwen3.5:397b",
            "gpt-oss:120b",
        ],
    },

    "reasoning": {
        "primary": "glm-5.2",
        "fallback": [
            "qwen3.5:397b",
            "gpt-oss:120b",
        ],
    },

    "writing": {
        "primary": "gpt-oss:120b",
        "fallback": [
            "glm-5.2",
        ],
    },

    "general": {
        "primary": "gpt-oss:120b",
        "fallback": [],
    },
}
