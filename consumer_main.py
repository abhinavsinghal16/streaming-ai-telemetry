from kafka_client.consumer import TelemetryConsumer
from kafka_client.consumer_config import ConsumerConfig


def main():

    config = ConsumerConfig(
        bootstrap_servers="localhost:9092",
        group_id="telemetry-consumer-group",
    )

    consumer = TelemetryConsumer(
        config,
        ["llm-inference-events"],
    )

    print("Waiting for messages...")

    try:
        while True:

            records = consumer.poll()

            if not records:
                continue

            for topic_partition, messages in records.items():

                for message in messages:

                    print(
                        f"Partition={message.partition} "
                        f"Offset={message.offset}"
                    )
                    print(message.value.decode("utf-8"))
                    print("-" * 80)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
