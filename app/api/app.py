from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
import json
from pydantic import BaseModel
from config import KAFKA_BROKER, KAFKA_TOPIC

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class GPSData(BaseModel):
    vehicle_rc_id: str
    timestamp: str
    latitude: float
    longitude: float
    speed: float

@app.post("/ingest")
def ingest(data: GPSData):
    try:
        producer.send(KAFKA_TOPIC, value=data.dict())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))