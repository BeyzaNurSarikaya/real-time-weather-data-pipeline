import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'weather_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', # Read from the beginning
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Wind speed is expected...")
for message in consumer:
    data = message.value
    print(f"City: {data['city']} | Wind Speed: {data['wind_speed']} km/h")