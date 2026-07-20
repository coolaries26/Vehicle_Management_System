import psycopg2
from config import POSTGRES_CONFIG

def get_conn():
    return psycopg2.connect(**POSTGRES_CONFIG)

def insert_gps(data):
    conn = get_conn()
    cur = conn.cursor()

    query = """
    INSERT INTO timeseries.gps_raw_data
    (vehicle_rc_id, gps_timestamp, latitude, longitude, speed)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        data["vehicle_rc_id"],
        data["timestamp"],
        data["latitude"],
        data["longitude"],
        data["speed"]
    ))

    conn.commit()
    cur.close()
    conn.close()
    
## Add Fuel Insert Function
def insert_fuel(data):
    conn = get_conn()
    cur = conn.cursor()

    query = """
    INSERT INTO transaction.fuel_transactions
    (vehicle_rc_id, fuel_date, fuel_quantity, fuel_price_per_unit,
     total_fuel_cost, odometer_reading)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        data["vehicle_rc_id"],
        data["fuel_date"],
        data["fuel_quantity"],
        data["fuel_price_per_unit"],
        data["total_fuel_cost"],
        data["odometer_reading"]
    ))

    conn.commit()
    cur.close()
    conn.close()

## Insert salary
def insert_salary(data):
    conn = get_conn()
    cur = conn.cursor()

    query = """
    INSERT INTO transaction.employee_salary
    (employee_id, salary_month, base_salary,
     allowances, deductions, net_salary, payment_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        data["employee_id"],
        data["salary_month"],
        data["base_salary"],
        data["allowances"],
        data["deductions"],
        data["net_salary"],
        data.get("payment_status", "PENDING")
    ))

    conn.commit()
    cur.close()
    conn.close()

## Insert maintenance data
def insert_maintenance(data):
    conn = get_conn()
    cur = conn.cursor()

    query = """
    INSERT INTO transaction.maintenance_job_card
    (vehicle_rc_id, maintenance_type_id, labour_charges,
     description, approval_required, completion_date, downtime_hours)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING job_card_id
    """

    cur.execute(query, (
        data["vehicle_rc_id"],
        data["maintenance_type_id"],
        data["labour_charges"],
        data["description"],
        data["approval_required"],
        data.get("completion_date"),
        data.get("downtime_hours")
    ))

    job_card_id = cur.fetchone()[0]

    # Insert parts
    for part in data.get("parts", []):
        cur.execute("""
        INSERT INTO transaction.maintenance_parts_usage
        (job_card_id, spare_part_id, quantity, total_cost)
        VALUES (%s, %s, %s, %s)
        """, (
            job_card_id,
            part["spare_part_id"],
            part["quantity"],
            part["quantity"] * part.get("price", 0)
        ))

    conn.commit()
    cur.close()
    conn.close()