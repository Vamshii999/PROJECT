import csv
from kafka import KafkaProducer

# Kafka Configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    client_id='csv-producer',
    key_serializer=str.encode,  # Convert key to bytes
    value_serializer=str.encode  # Convert message to bytes
)

topic = 'csv-data-topic'

# Function to handle delivery reports
def on_send_success(record_metadata):
    print(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}]")

def on_send_error(excp):
    print(f"Message delivery failed: {excp}")

# Read CSV file and send data to Kafka
with open('amazon.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)  # Read header row

    for row in csv_reader:
        message = ','.join(row)
        future = producer.send(topic, key=row[0], value=message)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)

producer.flush()  # Flush after loop to optimize performance
print("CSV data successfully sent to Kafka!")
