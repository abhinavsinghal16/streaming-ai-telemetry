import json

from kafka_client.consumer import TelemetryConsumer
from kafka_client.consumer_config import ConsumerConfig
from storage.parquet_writer import ParquetWriter


BATCH_SIZE = 100


def main() -> None:
    config = ConsumerConfig(
        bootstrap_servers="localhost:9092",
        group_id="storage-group",
        auto_offset_reset="latest",
    )

    consumer = TelemetryConsumer(
        config=config,
        topics=["llm-inference-events"],
    )

    writer = ParquetWriter(
        "storage/telemetry.parquet"
    )

    buffer = []

    print("Waiting for messages...")

    try:
        while True:
            records = consumer.poll()

            for _, messages in records.items():
                for message in messages:
                    payload = json.loads(
                        message.value.decode("utf-8")
                    )

                    buffer.append(payload)

                    if len(buffer) >= BATCH_SIZE:
                        writer.write(buffer)

                        print(
                            f"Wrote {len(buffer)} records to parquet"
                        )

                        buffer.clear()

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
