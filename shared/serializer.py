import json

from dataclasses import asdict
from datetime import datetime
from enum import Enum

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


class TelemetrySerializer:

    @staticmethod
    def serialize(event: InferenceTelemetryEvent) -> bytes:
        event_dict = asdict(event)
        normalized = TelemetrySerializer._normalize(event_dict)
        json_string = json.dumps(normalized, separators=(",", ":"))

        return json_string.encode("utf-8")

    @staticmethod
    def deserialize(data: bytes) -> InferenceTelemetryEvent:
        json_string = data.decode("utf-8")
        event_dict = json.loads(json_string)

        metadata_dict = event_dict["metadata"]
        request_dict = event_dict["request"]
        performance_dict = event_dict["performance"]
        tokens_dict = event_dict["tokens"]
        rag_dict = event_dict["rag"]
        outcome_dict = event_dict["outcome"]

        metadata = EventMetadata(
            request_id=metadata_dict["request_id"],
            timestamp=datetime.fromisoformat(metadata_dict["timestamp"]),
        )

        request = RequestMetadata(
            provider=request_dict["provider"],
            model=request_dict["model"],
            tenant_id=request_dict["tenant_id"],
            session_id=request_dict["session_id"],
            region=request_dict["region"],
        )

        performance = PerformanceMetrics(
            retrieval_latency_ms=performance_dict["retrieval_latency_ms"],
            rerank_latency_ms=performance_dict["rerank_latency_ms"],
            llm_latency_ms=performance_dict["llm_latency_ms"],
            total_latency_ms=performance_dict["total_latency_ms"],
        )

        tokens = TokenMetrics(
            prompt_tokens=tokens_dict["prompt_tokens"],
            completion_tokens=tokens_dict["completion_tokens"],
        )

        rag = RagMetrics(
            retrieved_chunks=rag_dict["retrieved_chunks"],
            reranked_chunks=rag_dict["reranked_chunks"],
            tool_calls=rag_dict["tool_calls"],
            cache_hit=rag_dict["cache_hit"],
        )

        outcome = RequestOutcome(
            status=RequestStatus(outcome_dict["status"]),
            error_code=(
                ErrorCode(outcome_dict["error_code"])
                if outcome_dict["error_code"] is not None
                else None
            ),
        )

        return InferenceTelemetryEvent(
            metadata=metadata,
            request=request,
            performance=performance,
            tokens=tokens,
            rag=rag,
            outcome=outcome,
        )

    @staticmethod
    def _normalize(value):
        if isinstance(value, dict):
            return {
                key: TelemetrySerializer._normalize(val)
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [
                TelemetrySerializer._normalize(item)
                for item in value
            ]

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, Enum):
            return value.value

        return value
