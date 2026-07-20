from app.models.maintenance import VehicleComplaint
from app.models.master import VehicleMaster,DriverMaster, EmployeeMaster

from app.db.session import SessionLocal 


from fastapi.testclient import (
    TestClient,
)

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
        "rc_number":  f"TEST-{rand_n_digits(6)}",
        "engine_no":  f"ENG-{rand_n_digits(6)}",
        "chassis_no": f"CH-{rand_n_digits(6)}",
    }
    response = client.post( "/api/v1/vehicles", json=payload, )
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

def create_driver():
    payload = {
        "driver_name":     f"Test-Driver-{rand_n_digits(6)}",
        "mobile_number":   f"901{rand_n_digits(7)}",
        "dl_number":       f"DL-{rand_n_digits(6)}",
    }
    response = client.post( "/api/v1/drivers", json=payload, )
    assert response.status_code == 201
    return response.json()

def create_complaint():
    vehicle = create_vehicle()
    driver = create_driver()
    payload = {
        "vehicle_id":         vehicle["vehicle_id"],
        "driver_id":          driver["driver_id"],
        "issue_description": "Battery issue",
    }
    response = client.post( "/api/v1/complaints",  json=payload, )
    assert response.status_code == 201
    return response.json()

def test_create_inspection():
    vehicle = create_vehicle()
    driver = create_driver()
    employee = create_employee()
    complaint = create_complaint()
    assert vehicle["vehicle_id"] is not None
    assert complaint["complaint_id"] is not None
    
    payload={

            "complaint_id"   : complaint["complaint_id"],
            "technician_id"  : employee["employee_id"],
            "Observerd Issue": "Dead Battery",
            "operator_notes" : "Needs replacement",
            "status"         : "OPEN"
    }
    response = client.post( "/api/v1/inspections",  json=payload )

    assert response.status_code == 201

def test_create_inspection_missing_complaint():

    response = client.post(
        "/api/v1/inspections",
        json={
            "technician_id": 1
        }
    )

    assert response.status_code == 422

def test_no_orphan_inspections():

    response = client.get(
        "/api/v1/inspections"
    )

    inspections = response.json()

    for inspection in inspections:

        assert (
            inspection["complaint_id"]
            is not None
        )

        assert (
            inspection["technician_id"]
            is not None
        )