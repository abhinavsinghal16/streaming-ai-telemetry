from catalog.providers import PROVIDERS

from generator.synthetic_telemetry_generator import (
    SyntheticTelemetryGenerator,
)
from profiles.normal import NORMAL_PROFILE
from shared.enums import RequestStatus
from shared.models import InferenceTelemetryEvent


def test_generate_returns_event():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    assert isinstance(
        event,
        InferenceTelemetryEvent,
    )


def test_provider_is_valid():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    assert event.request.provider in PROVIDERS


def test_model_matches_provider():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    assert (
        event.request.model
        in PROVIDERS[event.request.provider]
    )


def test_total_latency_is_valid():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    p = event.performance

    assert (
        p.total_latency_ms
        >=
        p.retrieval_latency_ms
        + p.rerank_latency_ms
        + p.llm_latency_ms
    )


def test_reranked_chunks_never_exceed_retrieved_chunks():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    assert (
        event.rag.reranked_chunks
        <=
        event.rag.retrieved_chunks
    )


def test_success_has_no_error():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    for _ in range(100):

        event = generator.generate()

        if event.outcome.status == RequestStatus.SUCCESS:

            assert event.outcome.error_code is None


def test_failure_has_error():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    for _ in range(500):

        event = generator.generate()

        if event.outcome.status == RequestStatus.FAILED:

            assert event.outcome.error_code is not None

def test_total_latency_includes_network_overhead():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    event = generator.generate()

    p = event.performance

    network_overhead = (
        p.total_latency_ms
        - p.retrieval_latency_ms
        - p.rerank_latency_ms
        - p.llm_latency_ms
    )

    assert (
        generator.NETWORK_OVERHEAD_RANGE_MS.min_value
        <= network_overhead
        <= generator.NETWORK_OVERHEAD_RANGE_MS.max_value
    )
