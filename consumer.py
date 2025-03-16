from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers
import json
import re


# Kafka consumer configuration
consumer = KafkaConsumer(
    'csv-data-topic',  # Kafka topic name
    bootstrap_servers='localhost:9092',  # Kafka broker address
    auto_offset_reset='earliest',  # Start reading from the earliest message
    enable_auto_commit=True,
    group_id='product-review-group',  # Consumer group ID
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
)



# Main consumer loop
def consume_messages():
    for message in consumer:
        data = message.value  # Get the message value (data)
        print(f"Consumed data: {data}")
        
       

# Run the consumer
if __name__ == "__main__":
    consume_messages()