from profiles.normal import NORMAL_PROFILE

from generator.synthetic_telemetry_generator import (
    SyntheticTelemetryGenerator,
)

from shared.serializer import TelemetrySerializer


def main():

    generator = SyntheticTelemetryGenerator(
        NORMAL_PROFILE
    )

    serializer = TelemetrySerializer()
    event_count = NORMAL_PROFILE.event_count

    for _ in range(NORMAL_PROFILE.event_count):

        event = generator.generate()

        serialized = serializer.serialize(event)

        print(serialized.decode())


if __name__ == "__main__":
    main()
