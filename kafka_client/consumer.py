from kafka import KafkaConsumer

from kafka_client.consumer_config import ConsumerConfig


class TelemetryConsumer:
    def __init__(
        self,
        config: ConsumerConfig,
        topics: list[str],
    ) -> None:
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.group_id,
            auto_offset_reset=config.auto_offset_reset,
        )

    def poll(self):
        return self.consumer.poll(timeout_ms=1000)

    def close(self) -> None:
        self.consumer.close()
