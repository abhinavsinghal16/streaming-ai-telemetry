import random
import uuid
from datetime import datetime, UTC

from catalog.providers import PROVIDERS
from profiles.profile_schema import Range, SimulationProfile

from shared.enums import ErrorCode, RequestStatus
from shared.models import (
    EventMetadata,
    InferenceTelemetryEvent,
    PerformanceMetrics,
    RagMetrics,
    RequestMetadata,
    RequestOutcome,
    TokenMetrics,
)

class SyntheticTelemetryGenerator:

    MIN_COMPLETION_RATIO = 0.25
    MAX_COMPLETION_RATIO = 1.5

    TIMEOUT_THRESHOLD_MS = 1000

    NETWORK_OVERHEAD_RANGE_MS = Range(min_value=5, max_value=30)

    def __init__(self, profile: SimulationProfile):
        self.profile = profile

    def generate(self) -> InferenceTelemetryEvent:

        metadata = self._generate_metadata()

        request = self._generate_request()

        tokens = self._generate_tokens()

        rag = self._generate_rag_metrics()

        performance = self._generate_performance_metrics(rag)

        outcome = self._generate_outcome(performance)

        return InferenceTelemetryEvent(
            metadata=metadata,
            request=request,
            performance=performance,
            tokens=tokens,
            rag=rag,
            outcome=outcome,
        )

    def _generate_metadata(self) -> EventMetadata:

        return EventMetadata(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(UTC),
        )

    def _generate_request(self) -> RequestMetadata:

        provider = self._choose_provider()

        model = self._choose_model(provider)

        return RequestMetadata(
            provider=provider,
            model=model,
            tenant_id=self._generate_tenant_id(),
            session_id=str(uuid.uuid4()),
            region=self._generate_region(),
        )

    def _generate_region(self) -> str:

        return random.choice(
            (
                "us-east-1",
                "us-west-2",
                "eu-west-1",
            )
        )

    def _choose_provider(self) -> str:

        providers = list(
            self.profile.provider_distribution.keys()
        )

        probabilities = list(
            self.profile.provider_distribution.values()
        )

        return random.choices(
            providers,
            weights=probabilities,
            k=1,
        )[0]

    def _choose_model(
        self,
        provider: str,
    ) -> str:

        return random.choice(
            PROVIDERS[provider]
        )

    def _generate_tenant_id(self) -> str:
        return f"tenant-{random.randint(1, 100)}"

    def _generate_tokens(self) -> TokenMetrics:

        prompt_tokens = self._generate_prompt_tokens()

        completion_tokens = self._generate_completion_tokens(
            prompt_tokens
        )

        return TokenMetrics(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )


    def _generate_prompt_tokens(self) -> int:

        return random.randint(
            self.profile.prompt_token_range.min_value,
            self.profile.prompt_token_range.max_value,
        )


    def _generate_completion_tokens(
        self,
        prompt_tokens: int,
    ) -> int:

        minimum = int(prompt_tokens * self.MIN_COMPLETION_RATIO)
        maximum = int(prompt_tokens * self.MAX_COMPLETION_RATIO)

        return random.randint(
            minimum,
            maximum,
        )

    def _generate_rag_metrics(self) -> RagMetrics:

        retrieved_chunks = self._generate_retrieved_chunks()

        reranked_chunks = self._generate_reranked_chunks(
            retrieved_chunks
        )

        return RagMetrics(
            retrieved_chunks=retrieved_chunks,
            reranked_chunks=reranked_chunks,
            tool_calls=self._generate_tool_calls(),
            cache_hit=self._generate_cache_hit(),
        )


    def _generate_retrieved_chunks(self) -> int:

        return random.randint(
            self.profile.retrieved_chunk_range.min_value,
            self.profile.retrieved_chunk_range.max_value,
        )


    def _generate_reranked_chunks(
        self,
        retrieved_chunks: int,
    ) -> int:

        return random.randint(
            1,
            retrieved_chunks,
        )


    def _generate_tool_calls(self) -> int:

        return random.randint(0, 3)


    def _generate_cache_hit(self) -> bool:

        return (
            random.random()
            < self.profile.cache_hit_rate
        )

    def _generate_performance_metrics(
        self,
        rag: RagMetrics,
    ) -> PerformanceMetrics:

        retrieval_latency = self._generate_retrieval_latency(
            rag.retrieved_chunks
        )

        rerank_latency = self._generate_rerank_latency(
            rag.reranked_chunks
        )

        llm_latency = self._generate_llm_latency(
            rag.cache_hit
        )

        network_overhead = self._generate_network_overhead()

        total_latency = (
            retrieval_latency
            + rerank_latency
            + llm_latency
            + network_overhead
        )

        return PerformanceMetrics(
            retrieval_latency_ms=retrieval_latency,
            rerank_latency_ms=rerank_latency,
            llm_latency_ms=llm_latency,
            total_latency_ms=total_latency,
        )

    def _generate_retrieval_latency(
        self,
        retrieved_chunks: int,
    ) -> int:

        base = random.randint(
            self.profile.retrieval_latency_range_ms.min_value,
            self.profile.retrieval_latency_range_ms.max_value,
        )

        return base + random.randint(
            retrieved_chunks,
            retrieved_chunks * 2,
        )

    def _generate_rerank_latency(
        self,
        reranked_chunks: int,
    ) -> int:

        base = random.randint(
            self.profile.rerank_latency_range_ms.min_value,
            self.profile.rerank_latency_range_ms.max_value,
        )

        return base + reranked_chunks

    def _generate_llm_latency(
        self,
        cache_hit: bool,
    ) -> int:

        latency = random.randint(
            self.profile.llm_latency_range_ms.min_value,
            self.profile.llm_latency_range_ms.max_value,
        )

        if cache_hit:
            latency = int(latency * 0.30)

        return latency

    def _generate_network_overhead(self) -> int:

        return random.randint(
            self.NETWORK_OVERHEAD_RANGE_MS.min_value,
            self.NETWORK_OVERHEAD_RANGE_MS.max_value,
        )

    def _generate_outcome(
        self,
        performance: PerformanceMetrics,
    ) -> RequestOutcome:

        if random.random() >= self.profile.failure_rate:
            return RequestOutcome(
                status=RequestStatus.SUCCESS,
                error_code=None,
            )

        return RequestOutcome(
            status=RequestStatus.FAILED,
            error_code=self._generate_error_code(
                performance
            ),
        )

    def _generate_error_code(
        self,
        performance: PerformanceMetrics,
    ) -> ErrorCode:

        if (performance.total_latency_ms > self.TIMEOUT_THRESHOLD_MS):
            return ErrorCode.TIMEOUT

        return random.choice(
            (
                ErrorCode.MODEL_ERROR,
                ErrorCode.RETRIEVAL_ERROR,
                ErrorCode.RATE_LIMITED,
            )
        )
