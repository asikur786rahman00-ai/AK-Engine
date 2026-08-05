"""
AK Engine Hermes Bridge
"""

from ak_engine.config import AK_ENGINE_ENABLED
from ak_engine.smart_router import SmartRouter


def resolve_model(
    message: str,
    current_model: str,
    runtime: dict | None = None,
) -> str:
    """
    Resolve the best model for this request.
    Runtime is accepted for future routing logic.
    """

    if not AK_ENGINE_ENABLED:
        return current_model

    runtime = runtime or {}

    # Future:
    # provider = runtime.get("provider")
    # base_url = runtime.get("base_url")
    # api_key = runtime.get("api_key")

    router = SmartRouter()

    return router.route(
        message=message,
        default_model=current_model,
    )
