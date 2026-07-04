from dataclasses import dataclass
from datetime import datetime

from shared.enums import RequestStatus, ErrorCode


@dataclass(frozen=True)
class EventMetadata:
    request_id: str
    timestamp: datetime


@dataclass(frozen=True)
class RequestMetadata:
    provider: str
    model: str
    tenant_id: str
    session_id: str
    region: str


@dataclass(frozen=True)
class PerformanceMetrics:
    retrieval_latency_ms: int
    rerank_latency_ms: int
    llm_latency_ms: int
    total_latency_ms: int


@dataclass(frozen=True)
class TokenMetrics:
    prompt_tokens: int
    completion_tokens: int


@dataclass(frozen=True)
class RagMetrics:
    retrieved_chunks: int
    reranked_chunks: int
    tool_calls: int
    cache_hit: bool


@dataclass(frozen=True)
class RequestOutcome:
    status: RequestStatus
    error_code: ErrorCode | None

@dataclass(frozen=True)
class InferenceTelemetryEvent:
    metadata: EventMetadata
    request: RequestMetadata
    performance: PerformanceMetrics
    tokens: TokenMetrics
    rag: RagMetrics
    outcome: RequestOutcome
