from dataclasses import dataclass


@dataclass(frozen=True)
class ConsumerConfig:
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = "earliest"
