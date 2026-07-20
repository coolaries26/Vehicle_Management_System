✅ Zookeeper  
✅ Kafka  
✅ PostgreSQL  
✅ FastAPI  
✅ dbt + Airflow (optional but recommended)  
✅ Folder structure + execution steps

***

# ⚙️ Fleet Management Platform – Setup Guide

***

# 🧱 1. Prerequisites

## ✅ System Requirements

* OS: Linux (Ubuntu 20+) / Mac / WSL (recommended)
* RAM: Minimum **8 GB** (16 GB recommended)
* Disk: Minimum **50 GB**
* Python: **3.9+**

***

## ✅ Install Core Dependencies
## ✅ 2.1 Recommended Stable Stack (Tested Together)

| Component    | Version           |
| ------------ | ----------------- |
| Python       | ✅ **3.9 or 3.10** |
| Kafka        | ✅ 3.3 – 3.6       |
| psycopg2     | ✅ latest          |
| kafka-python | ✅ 2.0.x           |
| FastAPI      | ✅ 0.100+          |
| uvicorn      | ✅ 0.22+           |
| dbt-postgres | ✅ 1.5 – 1.7       |
| Airflow      | ✅ 2.6 – 2.8       |
| Streamlit    | ✅ 1.30+           |

***


```bash
sudo apt update

sudo apt install -y \
    openjdk-11-jdk \
    python3-pip \
    postgresql \
    postgresql-contrib \
    wget \
    curl \
    git
```

***

# 🐘 2. PostgreSQL Setup

## ✅ Start PostgreSQL

```bash
sudo service postgresql start
```

***

## ✅ Create Database & User

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE fms;

CREATE USER fleet_user WITH PASSWORD 'FleetUser@2024!';

ALTER ROLE fleet_user SET client_encoding TO 'utf8';
ALTER ROLE fleet_user SET default_transaction_isolation TO 'read committed';

GRANT ALL PRIVILEGES ON DATABASE fms TO fleet_user;
```

***

## ✅ Enable Extensions (Optional but recommended)

```sql
\c fleet_db;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

***

## ✅ Apply Schema

```bash
psql -U fleet_user -d fleet_db -f schema.sql
```

***

# 🐘 3. Zookeeper Setup

## ✅ Download Kafka (includes Zookeeper)

```bash
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xvf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0
```
##  configure Kafka (`config/server.properties`)

By default, Kafka works out-of-the-box — but for your **ETL + GPS streaming system**, you *should update configs* for stability, scalability, and correctness.

### 🔧 Critical Updates (MUST for your use case)

```properties
broker.id=1
listeners=PLAINTEXT://localhost:9092
log.dirs=/var/lib/kafka-logs

# Zookeeper connection
zookeeper.connect=localhost:2181
```
## 🚀 High-Impact Tuning (IMPORTANT for ETL)

### ✅ 1. Topic & Throughput

```properties
num.partitions=3
default.replication.factor=1
```

👉 For GPS:

* Use **3–6 partitions minimum**
* Scale with vehicles

***

### ✅ 2. Log Retention (VERY IMPORTANT)

```properties
log.retention.hours=168   # 7 days
log.segment.bytes=1073741824
```

👉 Prevents Kafka from growing indefinitely

***

### ✅ 3. Consumer Performance

```properties
auto.create.topics.enable=true
group.initial.rebalance.delay.ms=0
```

***

### ✅ 4. Message Size (IMPORTANT for payload growth)

```properties
message.max.bytes=2000000
replica.fetch.max.bytes=2000000
```

***

### ✅ 5. Durability (VERY IMPORTANT for production)

```properties
acks=all
min.insync.replicas=1
```

***

## ⚠️ Production Upgrades (Future)

| Feature              | Recommendation                         |
| -------------------- | -------------------------------------- |
| SSL                  | Enable encryption                      |
| SASL                 | Enable authentication                  |
| Multi-broker cluster | For HA                                 |
| KRaft mode           | Replace Zookeeper (new Kafka versions) |


***

## ✅ 1.1 Zookeeper (`config/zookeeper.properties`)

### 🔧 Recommended Updates

```properties
dataDir=/tmp/zookeeper   # change for production
clientPort=2181
maxClientCnxns=60

# ✅ Improve stability
tickTime=2000
initLimit=10
syncLimit=5
```
### ⚠️ Production Improvements

| Parameter                   | Why                                            |
| --------------------------- | ---------------------------------------------- |
| `dataDir`                   | Move out of `/tmp` → e.g. `/var/lib/zookeeper` |
| `maxClientCnxns`            | Increase for multiple services                 |
| `autopurge.snapRetainCount` | Prevent disk overflow                          |
| `autopurge.purgeInterval`   | Enable cleanup                                 |


## ✅ Start Zookeeper

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

***

# 🧵 4. Kafka Setup

## ✅ Start Kafka Broker

```bash
bin/kafka-server-start.sh config/server.properties
```

***

## ✅ Create Topic

```bash
bin/kafka-topics.sh \
--create \
--topic gps_data \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1
```

***

## ✅ Verify Topic

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

***

# 🐍 5. Python Environment Setup
## 🐍 Version Compatibility (CRITICAL)

Yes — **version compatibility is VERY important**, especially with:

* Airflow
* dbt
* Python
* Kafka client libs


## ⚠️ IMPORTANT Compatibility Notes

***

### ❗ Python Version Constraints

| Tool        | Supported Python       |
| ----------- | ---------------------- |
| Airflow 2.x | ⚠️ **3.8 – 3.10 only** |
| dbt         | ✅ 3.8 – 3.11           |
| Streamlit   | ✅ 3.8+                 |

👉 ❗ Avoid Python 3.11+ for Airflow (issues still exist in many setups)

***

### ❗ Airflow Constraints (VERY STRICT)

Airflow requires exact dependency versions:

✅ Always install via constraints:

```bash
pip install apache-airflow==2.7.0 \
  --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.7.0/constraints-3.9.txt
```

👉 If you don’t → dependency conflicts (very common)

***

### ❗ dbt Compatibility

```bash
pip install dbt-postgres==1.6.0
```

👉 Ensure Postgres adapter + dbt version match

***

### ❗ kafka-python vs Kafka Server

| Kafka Server | kafka-python  |
| ------------ | ------------- |
| 3.x          | ✅ Works fine  |
| 4.x (future) | ❌ Might break |

***

### ❗ Streamlit Notes

* No strict constraints
* Avoid mixing with Airflow env → use separate env

***

# 🧠 3. Recommended Setup Strategy (Very Important)

👉 DO NOT install everything in one environment

***

## ✅ Best Practice: Separate Environments

| Component             | Environment   |
| --------------------- | ------------- |
| ETL (FastAPI + Kafka) | env-etl       |
| dbt                   | env-dbt       |
| Airflow               | env-airflow   |
| Streamlit             | env-dashboard |

***

## ✅ Example

```bash
python3 -m venv env-etl
python3 -m venv env-airflow
python3 -m venv env-dbt
```

***

# 🌐 6. FastAPI Setup

## ✅ Run API Server

```bash
uvicorn api.app:app --reload --port 8000
```

***

## ✅ Test API

```bash
curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{
  "vehicle_rc_id":"TRUCK_1",
  "timestamp":"2026-06-30T10:00:00",
  "latitude":12.9716,
  "longitude":77.5946,
  "speed":50
}'
```

***

# 📡 7. Kafka Consumer Setup

## ✅ Run Consumer

```bash
python consumer/consumer.py
```

***

## ✅ Expected Output

```
✅ Consumer started...
Data inserted into PostgreSQL
🚨 ALERT: Overspeed detected
```

***

# 🚚 8. GPS Simulator

```bash
python producer/gps_simulator.py
```

✅ This generates continuous test data

***

# 🧱 9. dbt Setup

## ✅ Initialize dbt

```bash
dbt init fleet_dbt
cd fleet_dbt
```

***

## ✅ Configure `profiles.yml`

```yaml
fleet_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: fleet_user
      password: password
      dbname: fleet_db
      schema: public
      port: 5432
```

***

## ✅ Run dbt

```bash
dbt run
dbt test
```

***

# ⏱️ 10. Airflow Setup (Optional but Recommended)

## ✅ Initialize Airflow

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
```

***

## ✅ Start Services

```bash
airflow webserver --port 8080
airflow scheduler
```

***

## ✅ Access UI

```
http://localhost:8080
```

***

# 🚨 11. Alerting Setup

## ✅ Current Implementation

* Console-based alerts

***

## ✅ Extend to Email

```python
import smtplib

def send_email_alert(message):
    print("Sending email:", message)
```

***

## ✅ Extend to Webhook

```python
import requests

def send_webhook(data):
    requests.post("http://alert-service", json=data)
```

***

# 📊 12. Streamlit Dashboard Setup

```bash
pip install streamlit
```

```bash
streamlit run dashboard/app.py
```

***

# 🔄 13. End-to-End Flow (After Setup)

```
Simulator → FastAPI → Kafka → Consumer → PostgreSQL
                                          ↓
                                       dbt
                                          ↓
                                      Dashboard
                                          ↓
                                       Alerts
```

***

# ✅ 14. Verification Checklist

| Component  | Status Check      |
| ---------- | ----------------- |
| PostgreSQL | ✅ Tables created  |
| Kafka      | ✅ Topic available |
| FastAPI    | ✅ API responding  |
| Consumer   | ✅ Data flowing    |
| dbt        | ✅ Models running  |
| Alerts     | ✅ Triggered       |
| Dashboard  | ✅ UI visible      |

***

# 🚀 15. Production Hardening (Next Steps)

## ✅ Required Improvements

* Dockerize all components
* Add retry + dead letter queue (DLQ)
* Add centralized logging (ELK)
* Add metrics (Prometheus)
* Enable SSL for Kafka & DB
* Add role-based security

***

# 🧠 16. Recommended Folder Structure

```
fleet-platform/
│
├── api/
├── consumer/
├── producer/
├── transform/
├── alerts/
├── db/
├── dbt/
├── airflow/
├── dashboard/
└── scripts/
```

***

# ✅ Final Outcome

After this setup, you will have:

✅ Real-time streaming pipeline  
✅ Transactional DB + analytics layer  
✅ Batch + real-time processing  
✅ Alerting system  
✅ Dashboard-ready outputs

***
# 🚨 Common Mistakes (Avoid These)

❌ Running Kafka with default `/tmp` storage  
❌ Using Python 3.11 with Airflow  
❌ Mixing dbt + Airflow dependencies  
❌ Not setting log retention → disk full  
❌ Not setting partitions → poor scalability

***
