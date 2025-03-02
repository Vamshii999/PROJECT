from kafka import KafkaConsumer

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'csv-data-topic',  # Topic to subscribe to
    bootstrap_servers='localhost:9092',
    group_id='csv-consumer-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,  # Ensure automatic offset commits
    value_deserializer=lambda v: v.decode('utf-8')  # Decode bytes to string
)

print("Listening for messages...")

try:
    for msg in consumer:
        print(f"Received message: {msg.value}")

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()
