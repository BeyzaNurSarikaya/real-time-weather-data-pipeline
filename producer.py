import json
import time
import requests
from kafka import KafkaProducer

# Settings
API_KEY = "API-KEY"
CITY = "Amsterdam"
TOPIC_NAME = "weather_topic"

# Kafka Producer connection
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
    response = requests.get(url)
    data = response.json()
    
    # We are filtering the requested data
    filtered_data = {
        "city": data['location']['name'],
        "temp": data['current']['temp_c'],
        "humidity": data['current']['humidity'],
        "wind_speed": data['current']['wind_kph'],
        "local_time": data['location']['localtime'],
        "last_updated": data['current']['last_updated']
    }
    return filtered_data

print("Weather data is being sent... (Press Ctrl+C to stop)")
while True:
    weather_data = get_weather()
    producer.send(TOPIC_NAME, value=weather_data)
    print(f"Sent: {weather_data}")
    time.sleep(60) # 60-second waiting period