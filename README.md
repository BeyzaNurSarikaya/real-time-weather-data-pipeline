# 🌦️ Real-Time Weather Data Pipeline (Kafka & Spark Streaming)

This project is an end-to-end data engineering pipeline that ingests real-time weather data from a local environment and streams it to **Microsoft Fabric (Spark Streaming)** using **Apache Kafka** and **Ngrok**.

## 🏗️ Architecture Overview

The pipeline integrates the following components to bridge the gap between local infrastructure and the cloud:

1. **Data Source:** OpenWeatherMap API (or a similar weather service).
<img width="1919" height="181" alt="Screenshot 2026-02-03 171200" src="https://github.com/user-attachments/assets/f5164bf4-9666-4c63-9733-5993578cdcb3" />

2. **Producer:** A Python script that fetches live data and sends it to Kafka.
<img width="1317" height="183" alt="Screenshot 2026-02-03 172818" src="https://github.com/user-attachments/assets/9b882367-dc1e-4598-9b9e-e8cd79ea7e0d" />

3. **Message Broker:** **Apache Kafka & Zookeeper** running inside **Docker** containers.
<img width="1919" height="1020" alt="Screenshot 2026-02-03 163052" src="https://github.com/user-attachments/assets/b3266fa4-f52e-4d3c-a268-356a217ee574" />
<img width="1919" height="1017" alt="Screenshot 2026-02-03 163147" src="https://github.com/user-attachments/assets/8b13e234-6cb0-4e86-9a5a-4e4c96196504" />

4. **Tunneling:** **Ngrok (TCP Tunneling)** to expose the local Kafka broker to the public internet.
<img width="1919" height="864" alt="Screenshot 2026-02-03 170546" src="https://github.com/user-attachments/assets/1809e9db-ffa6-40d0-803a-1d612335ac35" />

5. **Consumer & Processing:** **PySpark Structured Streaming** running on Microsoft Fabric.

6. **Storage:** Processed data stored in a **Lakehouse (Delta Table)** for analytical use.

---

## ⚠️ CRITICAL CONFIGURATION (Action Required)

Since Microsoft Fabric (Cloud) needs to communicate with your local machine, the **Ngrok address is the bridge**. Every time you restart Ngrok, you **must** update the address in the following two places:

1. **`docker-compose.yml`**:
Update the `KAFKA_ADVERTISED_LISTENERS` variable:
```yaml
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092,EXTERNAL://0.tcp.eu.ngrok.io:XXXXX

```


*(Replace `0.tcp.eu.ngrok.io:XXXXX` with your active Ngrok URL. Do not include `tcp://` prefix.)*
2. **Fabric Notebook**:
Update the Kafka bootstrap server option:
```python
.option("kafka.bootstrap.servers", "0.tcp.eu.ngrok.io:XXXXX")

```



> **Note:** After updating the `docker-compose.yml`, you must restart your containers for changes to take effect:
> `docker compose down && docker compose up -d`

---

## 🚀 Installation and Setup

### 1. Local Setup

Start the Docker containers:

```bash
docker compose up -d

```

Install dependencies and start the Producer:

```bash
pip install kafka-python requests
python producer.py

```

### 2. Ngrok Connection

Start a TCP tunnel to expose Kafka's external port:

```bash
ngrok tcp 9093

```

### 3. Microsoft Fabric (Spark) Configuration

* Create a new Notebook in your Fabric Workspace.
* Define the **Schema** for the incoming JSON data.
* Apply a **5-minute sliding window** with a **1-minute slide duration**.
* Write the stream to a **Delta Table** in your Lakehouse.

---

## 📊 Data Processing Logic (Windowing)

The Spark Structured Streaming engine processes the data using:

* **Window Duration:** 5 Minutes
* **Slide Duration:** 1 Minute
* **Aggregation:** `avg(temperature)`

This calculates a rolling average updated every minute, providing real-time insights into weather trends.

---

## 🛠️ Technology Stack

* **Python:** Data Generation & Kafka Producer.
* **Apache Kafka:** Distributed Message Queue.
* **Docker:** Containerization of Kafka & Zookeeper.
* **Ngrok:** Secure Network Tunneling.
* **Microsoft Fabric:** Cloud-native Data Platform.
* **PySpark:** Real-time Structured Streaming.
* **Delta Lake:** Storage Layer.

---

## 📌 Key Highlights

* **Hybrid Cloud Connectivity:** Bridging local Kafka with Microsoft Fabric.
* **Real-Time Analytics:** On-the-fly transformations and windowed aggregations.
* **Modern Architecture:** Utilizing industry-standard Big Data tools.
