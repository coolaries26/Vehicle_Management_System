from kafka import KafkaConsumer
import json
from config import KAFKA_TOPIC, KAFKA_BROKER
from transform.transform import process_gps_data, process_fuel_data, process_maintenance
from Vehicle_Management_System.app.db.postgres import insert_gps, insert_fuel, insert_maintenance
from alerts.alerts import check_alerts

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

print("✅ Consumer started...")

for msg in consumer:
    try:
        raw_data = msg.value

        # Transform
        data = process_gps_data(raw_data)

        if data:
            insert_gps(data)
            check_alerts(data)

    except Exception as e:
        print("Error:", e)

## Fuel Consumer Integration

# inside loop
if raw_data.get("type") == "fuel":
    fuel_data = process_fuel_data(raw_data)
    if fuel_data:
        insert_fuel(fuel_data)

## maintenance integration
if raw_data.get("type") == "maintenance":
    m_data = process_maintenance(raw_data)
    if m_data:
        insert_maintenance(m_data)
