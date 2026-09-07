from kafka import KafkaProducer
from kafka_client.producer_config import ProducerConfig

class TelemetryProducer:

    def __init__(
        self,
        config: ProducerConfig,
    ):

        self.config = config

        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            client_id=config.client_id,
            acks=config.acks,
            retries=config.retries,
        )

    def send(
        self,
        message: bytes,
        topic: str = "llm-inference-events",
    ) -> None:

        self.producer.send(
            topic,
            value=message,
        )

    def flush(self) -> None:
        self.producer.flush()

    def close(self) -> None:
        self.producer.flush()
        self.producer.close()
