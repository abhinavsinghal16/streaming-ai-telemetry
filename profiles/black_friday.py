from .profile_schema import Range, SimulationProfile


BLACK_FRIDAY_PROFILE = SimulationProfile(
    name="Black Friday",

    event_count=10_000,

    provider_distribution={
        "OpenAI": 0.60,
        "Anthropic": 0.30,
        "Google": 0.10,
    },

    prompt_token_range=Range(
        min_value=1_000,
        max_value=2_500,
    ),

    retrieved_chunk_range=Range(
        min_value=5,
        max_value=12,
    ),

    cache_hit_rate=0.45,

    retrieval_latency_range_ms=Range(
        min_value=20,
        max_value=80,
    ),

    rerank_latency_range_ms=Range(
        min_value=15,
        max_value=40,
    ),

    llm_latency_range_ms=Range(
        min_value=400,
        max_value=1_200,
    ),

    failure_rate=0.04,
)
