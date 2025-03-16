from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['feed_ranking_db']
collection = db['reviews']

# Kafka consumer setup
consumer = KafkaConsumer(
    'csv-data-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages and store in MongoDB
def consume_and_store_reviews():
    for message in consumer:
        review = message.value
        print(f"Received: {review}")
        collection.insert_one(review)
        print(f"Stored in MongoDB: {review}")

if __name__ == "__main__":
    consume_and_store_reviews()