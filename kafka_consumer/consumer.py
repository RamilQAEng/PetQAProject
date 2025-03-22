from kafka import KafkaConsumer
import json

def start_consumer():
    consumer = KafkaConsumer(
        'tasks',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("Consumer started. Waiting for messages...")
    for message in consumer:
        print(f"Received message: {message.value}")

if __name__ == "__main__":
    start_consumer()
