import json

from datetime import UTC, datetime

import pytest

from shared.enums import RequestStatus
from shared.models import (
    EventMetadata,
    InferenceTelemetryEvent,
    PerformanceMetrics,
    RagMetrics,
    RequestMetadata,
    RequestOutcome,
    TokenMetrics,
)
from shared.serializer import TelemetrySerializer


def create_test_event() -> InferenceTelemetryEvent:
    return InferenceTelemetryEvent(
        metadata=EventMetadata(
            request_id="req-123",
            timestamp=datetime(2026, 7, 3, 18, 30, tzinfo=UTC),
        ),
        request=RequestMetadata(
            provider="OpenAI",
            model="gpt-4o",
            tenant_id="acme-corp",
            session_id="session-123",
        ),
        performance=PerformanceMetrics(
            retrieval_latency_ms=20,
            rerank_latency_ms=15,
            llm_latency_ms=350,
            total_latency_ms=385,
        ),
        tokens=TokenMetrics(
            prompt_tokens=1200,
            completion_tokens=350,
        ),
        rag=RagMetrics(
            retrieved_chunks=10,
            reranked_chunks=5,
            tool_calls=2,
            cache_hit=False,
        ),
        outcome=RequestOutcome(
            status=RequestStatus.SUCCESS,
            error_code=None,
        ),
    )


def test_round_trip_serialization():
    event = create_test_event()

    serialized = TelemetrySerializer.serialize(event)
    reconstructed = TelemetrySerializer.deserialize(serialized)

    assert reconstructed == event


def test_serialize_returns_bytes():
    event = create_test_event()

    serialized = TelemetrySerializer.serialize(event)

    assert isinstance(serialized, bytes)


def test_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        TelemetrySerializer.deserialize(
            b"This is not JSON"
        )


def test_invalid_enum():
    event = create_test_event()

    serialized = TelemetrySerializer.serialize(event)

    event_dict = json.loads(serialized.decode("utf-8"))

    event_dict["outcome"]["status"] = "INVALID_STATUS"

    corrupted = json.dumps(event_dict).encode("utf-8")

    with pytest.raises(ValueError):
        TelemetrySerializer.deserialize(corrupted)


def test_datetime_round_trip():
    event = create_test_event()

    serialized = TelemetrySerializer.serialize(event)

    reconstructed = TelemetrySerializer.deserialize(serialized)

    assert (
        reconstructed.metadata.timestamp
        == event.metadata.timestamp
    )
