from kafka import KafkaConsumer
from config import Config

consumer = KafkaConsumer(
    "inventory_topic",
    bootstrap_servers=
    Config.KAFKA_SERVER
)

for message in consumer:

    print(
        message.value.decode()
    )