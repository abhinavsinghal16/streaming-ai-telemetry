"""
Static provider catalog.

This module contains immutable reference data describing
which language models are available for each provider.

Behavior (latency, failures, cache hit rates, etc.)
belongs in Simulation Profiles, not here.
"""

PROVIDERS: dict[str, tuple[str, ...]] = {
    "OpenAI": (
        "gpt-4o",
        "gpt-4o-mini",
    ),
    "Anthropic": (
        "Claude Sonnet",
        "Claude Opus",
    ),
    "Google": (
        "Gemini 2.5 Pro",
        "Gemini 2.5 Flash",
    ),
}
