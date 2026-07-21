from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
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
#    res=response.json()
#    print(res)
    assert response.status_code == 201
    return response.json()

def create_inspection():
    complaint = create_complaint()
    employee = create_employee()
#    driver = create_driver()
    assert complaint["complaint_id"] is not None
#    assert driver["driver_id"] is not None
    assert employee["employee_id"] is not None
    payload = {
        "complaint_id"   : complaint["complaint_id"],
#        "technician_id"  : driver["driver_id"],
        "technician_id"  : employee["employee_id"],
        "observed_issue" : "Battery dead",
        "operator_notes" : "Needs replacement",
        "status"         : "OPEN"
        }
    response = client.post( "/api/v1/inspections",  json=payload, )
    assert response.status_code == 201
    return response.json()

def create_jobcard():
    vehicle = create_vehicle()
    complaint = create_complaint()
    inspection =  create_inspection()
    driver = create_driver()
    trchnician = create_employee()
    assert vehicle["vehicle_id"] is not None
    assert complaint["complaint_id"] is not None
    assert inspection["inspection_id"] is not None
    payload={
        "complaint_id": complaint["complaint_id"],
        "inspection_id": inspection["inspection_id"],
        "vehicle_id": vehicle["vehicle_id"],
        "driver_id": driver["driver_id"],
        "technician_id": trchnician["employee_id"],
        "maintenance_type": "PREVENTIVE",
    }
    response = client.post("/api/v1/jobcards", json=payload )
    assert response.status_code == 201
    return response.json()

def test_create_jobcard():
    vehicle = create_vehicle()
    complaint = create_complaint()
    inspection =  create_inspection()
    driver = create_driver()
    technician = create_employee()
    assert vehicle["vehicle_id"] is not None
    assert complaint["complaint_id"] is not None
    assert inspection["inspection_id"] is not None
    assert driver["driver_id"] is not None
    assert technician["employee_id"] is not None
    payload={
        "complaint_id": complaint["complaint_id"],
        "inspection_id": inspection["inspection_id"],
        "vehicle_id": vehicle["vehicle_id"],
        "driver_id": driver["driver_id"],
        "technician_id": technician["employee_id"],
        "maintenance_type": "PREVENTIVE",
    }
    response = client.post("/api/v1/jobcards", json=payload )
    assert response.status_code == 201


def test_get_jobcard():
    jobcard = create_jobcard()
    job_card_id = (
        jobcard["job_card_id"]
    )
    print(job_card_id)
    response = client.get(
        f"/api/v1/jobcards/{job_card_id}"
    )
#    print(response)
    assert response.status_code == 200
    body = response.json()
    assert (
        body["job_card_id"]
        == job_card_id
    )


def test_get_all_jobcards():
    create_jobcard()
    response = client.get(
        "/api/v1/jobcards"
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0


def test_update_jobcard():
    jobcard = create_jobcard()
    job_card_id = (
        jobcard["job_card_id"]
    )
    response = client.put(
        f"/api/v1/jobcards/{job_card_id}",
        json={
            "description":
            "Updated jobcard"
        },
    )
    assert response.status_code == 200
    body = response.json()
    
    assert (
        body["job_card_id"]
        == job_card_id
    )
    assert (
        body["description"]
        == "Updated jobcard"
    )


def test_delete_jobcard():
    jobcard = create_jobcard()
    job_card_id = (
        jobcard["job_card_id"]
    )
    response = client.delete(
        f"/api/v1/jobcards/{job_card_id}"
    )
    assert response.status_code == 200
    response = client.get(
        f"/api/v1/jobcards/{job_card_id}"
    )
    assert response.status_code == 404


def test_get_jobcard_not_found():
    response = client.get(
        "/api/v1/jobcards/999999999"
    )
    assert response.status_code == 404


def test_update_jobcard_not_found():
    response = client.put(
        "/api/v1/jobcards/999999999",
        json={
            "description":
            "Updated jobcard"
        },
    )
    assert response.status_code == 404


def test_delete_jobcard_not_found():
    job_card_id=999999999
    response = client.delete(
        f"/api/v1/jobcards/{job_card_id}"
    )
    assert response.status_code == 404

def test_create_jobcard_extended_fields():

    vehicle = create_vehicle()
    complaint = create_complaint()
    inspection =  create_inspection()
    driver = create_driver()
    technician = create_employee()
    assert vehicle["vehicle_id"] is not None
    assert complaint["complaint_id"] is not None
    assert inspection["inspection_id"] is not None
    assert driver["driver_id"] is not None
    assert technician["employee_id"] is not None
    payload={
        "complaint_id": complaint["complaint_id"],
        "inspection_id": inspection["inspection_id"],
        "vehicle_id": vehicle["vehicle_id"],
        "driver_id": driver["driver_id"],
        "technician1_id": technician["employee_id"],
        "technician2_id": technician["employee_id"],
    
        "maintenance_type": "PREVENTIVE",

        "zone_area": "Zone A",

        "mileage_hours": "15000",

        "issue_reported": "Brake Issue",

        "problem_found_action_taken":
            "Brake pads replaced",

        "requisition_slip_number":
            "REQ-1001",
    }

    response = client.post(
        "/api/v1/jobcards",
        json=payload,
    )

    assert response.status_code == 201

    result = response.json()
    print(f'create driver: {driver["driver_id"]}')
    print(f'payload driver: {payload["driver_id"]}')
    print(result)
    assert result["driver_id"] == driver["driver_id"]

    assert (
        result["maintenance_type"]
        == "PREVENTIVE"
    )

    assert (
        result["requisition_slip_number"]
        == "REQ-1001"
    )

