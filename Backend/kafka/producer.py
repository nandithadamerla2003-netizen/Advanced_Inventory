from kafka import KafkaProducer
from config import Config

producer = KafkaProducer(
    bootstrap_servers=
    Config.KAFKA_SERVER
)

def send_event(message):

    producer.send(
        "inventory_topic",
        message.encode()
    )

    producer.flush()