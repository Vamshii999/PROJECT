import pandas as pd
from kafka import KafkaProducer
import json

# Kafka configuration
bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker address
topic = 'csv-data-topic'  # Kafka topic to produce messages to

# Create a Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON to bytes
)
#df['Summary'] = df['Summary'].fillna('')
# Function to send a row to Kafka
def produce_row_to_kafka(row):
    # Convert the row to a dictionary
    row_dict = row.to_dict()
    
    # Send the JSON data to the Kafka topic
    producer.send(topic, value=row_dict)
    print(f"Produced: {row_dict}")

# Read the CSV file
csv_file = 'reviews.csv'
df = pd.read_csv(csv_file)

# Iterate over each row in the DataFrame and produce to Kafka
for index, row in df.iterrows():
    produce_row_to_kafka(row)


# Flush the producer to ensure all messages are sent
producer.flush()

# Close the producer
producer.close()