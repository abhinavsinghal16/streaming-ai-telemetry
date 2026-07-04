from dataclasses import dataclass

from catalog.providers import PROVIDERS


@dataclass(frozen=True)
class Range:
    """
    Represents an inclusive numeric range.
    """

    min_value: int
    max_value: int

    def __post_init__(self) -> None:
        if self.min_value > self.max_value:
            raise ValueError(
                "Range minimum must be less than or equal to maximum."
            )


@dataclass(frozen=True)
class SimulationProfile:
    """
    Defines the characteristics of a simulated AI inference workload.

    The profile specifies the independent variables used to generate
    telemetry events. The generator derives all dependent values
    (such as total latency and completion tokens) from these inputs.
    """

    name: str

    event_count: int

    provider_distribution: dict[str, float]

    prompt_token_range: Range

    retrieved_chunk_range: Range

    cache_hit_rate: float

    retrieval_latency_range_ms: Range

    rerank_latency_range_ms: Range

    llm_latency_range_ms: Range

    failure_rate: float

    def __post_init__(self) -> None:

        if self.event_count <= 0:
            raise ValueError(
                "event_count must be greater than zero."
            )

        total = sum(self.provider_distribution.values())

        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                "Provider distribution must sum to 1.0."
            )

        for provider in self.provider_distribution:

            if provider not in PROVIDERS:
                raise ValueError(
                    f"Unknown provider '{provider}'."
                )

        for field_name, value in (
            ("cache_hit_rate", self.cache_hit_rate),
            ("failure_rate", self.failure_rate),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{field_name} must be between 0.0 and 1.0."
                )
