from profiles.normal import NORMAL_PROFILE

from generator.synthetic_telemetry_generator import (
    SyntheticTelemetryGenerator,
)

from shared.serializer import TelemetrySerializer

from kafka_client.producer import TelemetryProducer
from kafka_client.producer_config import ProducerConfig

from profiles.normal import NORMAL_PROFILE

from shared.serializer import TelemetrySerializer

def main():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    serializer = TelemetrySerializer()
    event_count = NORMAL_PROFILE.event_count

    config = ProducerConfig(
        bootstrap_servers="localhost:9092",
        client_id="telemetry-generator",
    )

    producer = TelemetryProducer(config)
    
    for _ in range(NORMAL_PROFILE.event_count):

        event = generator.generate()

        serialized = serializer.serialize(event)

        producer.send(serialized)

    producer.close()

if __name__ == "__main__":
    main()
