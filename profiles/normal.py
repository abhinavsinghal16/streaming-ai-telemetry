from .profile_schema import Range, SimulationProfile


NORMAL_PROFILE = SimulationProfile(
    name="Normal",

    event_count=10000,

    provider_distribution={
        "OpenAI": 0.60,
        "Anthropic": 0.30,
        "Google": 0.10,
    },

    prompt_token_range=Range(
        min_value=500,
        max_value=1_500,
    ),

    retrieved_chunk_range=Range(
        min_value=3,
        max_value=8,
    ),

    cache_hit_rate=0.35,

    retrieval_latency_range_ms=Range(
        min_value=10,
        max_value=40,
    ),

    rerank_latency_range_ms=Range(
        min_value=5,
        max_value=20,
    ),

    llm_latency_range_ms=Range(
        min_value=150,
        max_value=450,
    ),

    failure_rate=0.01,
)
