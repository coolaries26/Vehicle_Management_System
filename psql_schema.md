***

# 🧱 2. PostgreSQL Schema (Initial DDL)

Below is a **production-ready starter schema** aligned with your POC and design.

***
# DB setup

```sql
CREATE DATABASE fms;

CREATE USER fleet_user WITH PASSWORD 'password';

ALTER ROLE fleet_user SET client_encoding TO 'utf8';
ALTER ROLE fleet_user SET default_transaction_isolation TO 'read committed';

GRANT ALL PRIVILEGES ON DATABASE fms TO fleet_user;
```

```sql
\c fleet_db;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

***

## 1. Schema Setup

```sql
CREATE SCHEMA master;
CREATE SCHEMA reference;
CREATE SCHEMA transaction;
CREATE SCHEMA timeseries;
```

***

## 2. Reference Tables

```sql
CREATE TABLE reference.vehicle_type_ref (
    vehicle_type_id SERIAL PRIMARY KEY,
    vehicle_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE reference.maintenance_type_ref (
    maintenance_type_id SERIAL PRIMARY KEY,
    maintenance_type_name VARCHAR(50) UNIQUE NOT NULL
);
```

***

## 3. Master Tables

### Vehicle Master

```sql
CREATE TABLE master.vehicle_master (
    vehicle_rc_id VARCHAR(20) PRIMARY KEY,
    vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    gps_id VARCHAR(50) UNIQUE,
    fuel_type VARCHAR(20),
    fuel_capacity NUMERIC,
    last_pm_date DATE,
    last_workshop_date DATE,
    last_job_card_id INT,
    last_breakdown_id INT,
    puc_last_date DATE,
    fit_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

***

### Employee Master

```sql
CREATE TABLE master.employee_master (
    employee_id SERIAL PRIMARY KEY,
    employee_type VARCHAR(30),
    full_name VARCHAR(100),
    phone_number VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

***

## 4. Transaction Tables

### GPS Raw Data (Time-Series)

```sql
CREATE TABLE timeseries.gps_raw_data (
    id BIGSERIAL PRIMARY KEY,
    vehicle_rc_id VARCHAR(20) REFERENCES master.vehicle_master(vehicle_rc_id),
    gps_timestamp TIMESTAMP NOT NULL,
    latitude NUMERIC,
    longitude NUMERIC,
    speed NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gps_vehicle_time 
ON timeseries.gps_raw_data(vehicle_rc_id, gps_timestamp DESC);
```

***

### Maintenance Job Card

```sql
CREATE TABLE transaction.maintenance_job_card (
    job_card_id SERIAL PRIMARY KEY,
    vehicle_rc_id VARCHAR(20) REFERENCES master.vehicle_master(vehicle_rc_id),
    maintenance_type_id INT REFERENCES reference.maintenance_type_ref(maintenance_type_id),
    labour_charges NUMERIC,
    description TEXT,
    approval_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

***

### Inventory Table

```sql
CREATE TABLE transaction.inventory (
    spare_part_id SERIAL PRIMARY KEY,
    vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    quantity INT NOT NULL,
    part_type VARCHAR(50),
    price NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

***

### Spare Parts Mapping (Job Card)

```sql
CREATE TABLE transaction.job_card_parts (
    id SERIAL PRIMARY KEY,
    job_card_id INT REFERENCES transaction.maintenance_job_card(job_card_id),
    spare_part_id INT REFERENCES transaction.inventory(spare_part_id),
    quantity INT NOT NULL
);
```
## Fuel Rate Reference

```sql
CREATE TABLE reference.fuel_rate_reference (
    id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(20) NOT NULL,
    price_per_unit NUMERIC(10,2) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fuel_rate_type_date
ON reference.fuel_rate_reference (fuel_type, effective_date DESC);
```

***

## Fuel Transactions

```sql
CREATE TABLE transaction.fuel_transactions (
    fuel_txn_id SERIAL PRIMARY KEY,
    vehicle_rc_id VARCHAR(20) NOT NULL,
    fuel_date DATE NOT NULL,
    fuel_quantity NUMERIC(10,2) NOT NULL,
    fuel_price_per_unit NUMERIC(10,2),
    total_fuel_cost NUMERIC(12,2),
    odometer_reading NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fuel_vehicle
    FOREIGN KEY (vehicle_rc_id)
    REFERENCES master.vehicle_master(vehicle_rc_id)
);

CREATE INDEX idx_fuel_vehicle_date
ON transaction.fuel_transactions (vehicle_rc_id, fuel_date DESC);
```

***

## Employee Salary

```sql
CREATE TABLE transaction.employee_salary (
    salary_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    salary_month DATE NOT NULL,

    base_salary NUMERIC(12,2) NOT NULL,
    allowances NUMERIC(12,2) DEFAULT 0,
    deductions NUMERIC(12,2) DEFAULT 0,
    net_salary NUMERIC(12,2),

    payment_status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_salary_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);

CREATE INDEX idx_salary_employee_month
ON transaction.employee_salary (employee_id, salary_month DESC);
```

***

## Attendance Tracking

```sql
CREATE TABLE transaction.attendance_tracking (
    attendance_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,

    status VARCHAR(20) CHECK (status IN ('PRESENT', 'ABSENT', 'LEAVE')),
    shift_hours NUMERIC(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attendance_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);

CREATE INDEX idx_attendance_employee_date
ON transaction.attendance_tracking (employee_id, attendance_date DESC);
```
# 🛠️ 1. Extend ETL for Maintenance Analytics

We’ll enhance your pipeline to:

* Capture **job card details**
* Track **parts usage**
* Compute **derived maintenance metrics**
* Trigger **alerts**

***

## ✅ 1.1 Extend Maintenance Table (if not already done)

```sql
ALTER TABLE transaction.maintenance_job_card
ADD COLUMN job_card_status VARCHAR(20),
ADD COLUMN completion_date DATE,
ADD COLUMN downtime_hours NUMERIC(6,2);
```

***

## ✅ 1.2 Add Spare Parts Consumption Table

```sql
CREATE TABLE transaction.maintenance_parts_usage (
    id SERIAL PRIMARY KEY,
    job_card_id INT REFERENCES transaction.maintenance_job_card(job_card_id),
    spare_part_id INT REFERENCES transaction.inventory(spare_part_id),
    quantity INT NOT NULL,
    total_cost NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parts_job_card
ON transaction.maintenance_parts_usage(job_card_id);
```

***

## 5. Roles & Access (Starter)

```sql
CREATE ROLE admin;
CREATE ROLE workshop_user;
CREATE ROLE driver_user;
CREATE ROLE management_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA master TO admin;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA transaction TO workshop_user;
GRANT SELECT ON ALL TABLES IN SCHEMA timeseries TO management_user;
```

***

# ✅ Next Step (Recommended)

We now move into **actual build**. Choose one:

### 🚀 Option 1 (Best Next Step)

➡️ *“Generate ETL pipeline code”*  
→ I’ll give:

* FastAPI ingestion code
* Kafka producer/consumer
* Postgres writer

### 🚀 Option 2

➡️ *“Create Streamlit dashboard app”*

### 🚀 Option 3

➡️ *“Enhance schema with analytics layer + dbt models”*

***

You now have:
✅ Client-ready proposal  
✅ Executable schema foundation

Let’s build 🚀
