from app.db.session import SessionLocal 
from fastapi.testclient import (TestClient,)   #type: ignore

from app.main import app

client = TestClient(app)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def create_vehicle():
    payload = {
        "rc_number": f"TEST-{rand_n_digits(6)}",
        "engine_no": f"ENG-{rand_n_digits(6)}",
        "chassis_no": f"CH-{rand_n_digits(6)}",
    }
    response = client.post( "/api/v1/vehicles", json=payload,  )
    assert response.status_code == 201
    return response.json()

def create_employee():
    payload ={
    "employee_type" : "TECHNICIAN",
    "full_name"     : f"Test-EMP-{rand_n_digits(6)}",
    "phone_number"  : f"901{rand_n_digits(7)}",
    }
    response = client.post( "/api/v1/employees",  json=payload, )
    assert response.status_code == 201
    return response.json()

def test_create_checklist():
    vehicle = create_vehicle()
    employee = create_employee()

    response = client.post(
        "/api/v1/checklists",
        json={
            "vehicle_id": vehicle["vehicle_id"],
            "technician_id": employee["employee_id"]
        }
    )
    assert response.status_code == 201