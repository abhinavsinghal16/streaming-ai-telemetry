from .profile_schema import Range, SimulationProfile


PEAK_HOURS_PROFILE = SimulationProfile(
    name="Peak Hours",

    event_count=10_000,

    provider_distribution={
        "OpenAI": 0.60,
        "Anthropic": 0.30,
        "Google": 0.10,
    },

    prompt_token_range=Range(
        min_value=800,
        max_value=2_000,
    ),

    retrieved_chunk_range=Range(
        min_value=4,
        max_value=10,
    ),

    cache_hit_rate=0.40,

    retrieval_latency_range_ms=Range(
        min_value=15,
        max_value=60,
    ),

    rerank_latency_range_ms=Range(
        min_value=10,
        max_value=30,
    ),

    llm_latency_range_ms=Range(
        min_value=250,
        max_value=700,
    ),

    failure_rate=0.02,
)
