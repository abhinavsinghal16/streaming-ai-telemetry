FROM flink:2.1

RUN apt-get update && \
    apt-get install -y python3 python3-pip wget && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install apache-flink==2.1.0

RUN ln -s /usr/bin/python3 /usr/local/bin/python

# Flink Kafka connector
RUN wget -P /opt/flink/lib \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/5.0.0-2.1/flink-connector-kafka-5.0.0-2.1.jar

# Kafka client dependency
RUN wget -P /opt/flink/lib \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/4.2.0/kafka-clients-4.2.0.jar