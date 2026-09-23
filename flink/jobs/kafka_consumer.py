from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
import json

from pyflink.datastream import (
    StreamExecutionEnvironment,
)

from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)

def parse_event(message):
    event = json.loads(message)

    return (
        event["request"]["model"],
        event["performance"]["total_latency_ms"],
        event["outcome"]["status"],
    )

def status_count(event):
    status = event[2]
    return (status, 1)

def latency_stats(event):

    model = event[0]
    latency = event[1]

    return (
        model,
        latency,
        1,
    )

def compute_average(record):

    model = record[0]
    total_latency = record[1]
    count = record[2]

    return (
        model,
        round(total_latency / count, 2),
    )

env = StreamExecutionEnvironment.get_execution_environment()

source = (
    KafkaSource.builder()
    .set_bootstrap_servers("kafka:9092")
    .set_topics("llm-inference-events")
    .set_group_id("flink-demo")
    .set_starting_offsets(
        KafkaOffsetsInitializer.earliest()
    )
    .set_value_only_deserializer(
        SimpleStringSchema()
    )
    .build()
)

stream = env.from_source(
    source,
    WatermarkStrategy.no_watermarks(),
    "Kafka Source",
)

parsed_stream = stream.map(parse_event)

# Demo 1: Basic transformation
status_stream = parsed_stream.map(status_count)

status_stream.map(
    lambda x: f"STATUS: {x}"
).print()

# Demo 2: Stateful aggregation
latency_stream = parsed_stream.map(
    latency_stats
)

aggregated = (
    latency_stream
    .key_by(lambda x: x[0])
    .reduce(
        lambda a, b: (
            a[0],
            a[1] + b[1],
            a[2] + b[2],
        )
    )
)

average_latency = aggregated.map(
    compute_average
)

average_latency.map(
    lambda x: f"AVG_LATENCY: {x}"
).print()

env.execute("Kafka Consumer Test")
