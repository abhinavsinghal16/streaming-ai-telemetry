from dataclasses import dataclass


@dataclass(frozen=True)
class ProducerConfig:

    bootstrap_servers: str

    client_id: str

    acks: str = "all"

    retries: int = 3
