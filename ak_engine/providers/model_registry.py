"""
AK Engine Model -> Provider Registry.

Maps logical model names to concrete providers and provider-specific
model identifiers.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ModelDeployment:
    name: str
    provider: str
    model: str
    enabled: bool = True


MODEL_DEPLOYMENTS = {

    "gemma4:31b-cloud": ModelDeployment(
        name="gemma4:31b-cloud",
        provider="OllamaProvider",
        model="gemma4:31b-cloud",
    ),

    # --------------------------------------------------
    # Ollama
    # --------------------------------------------------

    "gpt-oss:120b": ModelDeployment(
        name="gpt-oss:120b",
        provider="OllamaProvider",
        model="gpt-oss:120b",
    ),

    "qwen3.5:397b": ModelDeployment(
        name="qwen3.5:397b",
        provider="OllamaProvider",
        model="qwen3.5:397b",
    ),

    # --------------------------------------------------
    # OpenRouter
    # --------------------------------------------------

    "kimi-k2.7-code": ModelDeployment(
        name="kimi-k2.7-code",
        provider="OpenRouterProvider",
        model=os.getenv(
            "KIMI_MODEL",
            "moonshotai/kimi-k2.5",
        ),
    ),

    # --------------------------------------------------
    # Gemini
    # --------------------------------------------------

    "gemini": ModelDeployment(
        name="gemini",
        provider="GeminiProvider",
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash",
        ),
    ),

    # --------------------------------------------------
    # Groq
    # --------------------------------------------------

    "groq": ModelDeployment(
        name="groq",
        provider="GroqProvider",
        model=os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        ),
    ),
}


def get_deployment(model: str) -> ModelDeployment:
    """
    Resolve a logical model name into a concrete deployment.
    """

    deployment = MODEL_DEPLOYMENTS.get(model)

    if deployment is None:
        raise KeyError(
            f"Unknown AK Engine model: {model}"
        )

    if not deployment.enabled:
        raise RuntimeError(
            f"Model deployment disabled: {model}"
        )

    return deployment


def list_models():
    """
    Return all registered model deployments.
    """

    return dict(MODEL_DEPLOYMENTS)
