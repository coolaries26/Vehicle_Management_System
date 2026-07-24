from fastapi.testclient import (    TestClient,)    #type: ignore
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
    assert response.status_code == 201
    return response.json()

def create_inspection():
    complaint = create_complaint()
    employee = create_employee()
    assert complaint["complaint_id"] is not None
    assert employee["employee_id"] is not None
    payload = {
        "complaint_id"   : complaint["complaint_id"],
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

def create_requisition():
    vehicle = create_vehicle()
    employee = create_employee()
    job_card=create_jobcard()
    assert vehicle["vehicle_id"] is not None
    assert employee["employee_id"] is not None
    assert job_card["job_card_id"] is not None
    
    payload = {
        "vehicle_id": vehicle["vehicle_id"],
        "job_card_id": job_card["job_card_id"],
        "technician_id": employee["employee_id"],

        "remarks":
        "Oil Filter Required",
        "status":
        "OPEN",
    }

    response = client.post(
        "/api/v1/requisitions",
        json=payload,
    )
    result =  response.json()
    assert (response.status_code == 200)
    assert (
        result["vehicle_id"]==payload["vehicle_id"])
    assert (
        result["job_card_id"] == payload["job_card_id"])
    assert (
        result["technician_id"]==payload["technician_id"])
    return response.json()

def create_part():
    payload = {
        "part_code": f"PART-{rand_n_digits(6)}",
        "part_name": "Engine Oil",
        "active_flag": True,
    }
    response = client.post(
        "/api/v1/parts",
        json=payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert (
        data["part_name"]
        == "Engine Oil"
    )
    return data

def test_create_requisition_detail():

    requisition = create_requisition()

    part = create_part()

    payload = {

        "requisition_id":
        requisition[
            "requisition_id"
        ],

        "part_id":
        part["part_id"],

        "quantity_required":
        2,

        "quantity_returned":
        0,

        "required_serial_number":
        "REQ-SN-001",

        "returned_serial_number":
        "",

        "remarks":
        "Battery Required",
    }

    response = client.post(
        "/api/v1/requisition-details",
        json=payload,
    )

    assert (        response.status_code == 200)

    result = response.json()
#    print(result)
    assert (
        result["part_id"] == part["part_id"])


def test_get_all_requisition_details():

    response = client.get(
        "/api/v1/requisition-details"
    )

    assert (
        response.status_code == 200)


def test_get_requisition_detail_not_found():

    response = client.get(
        "/api/v1/requisition-details/999999"
    )

    assert (
        response.status_code
        == 404
    )


def test_get_requisition_detail():

    requisition = create_requisition()

    part = create_part()

    create_response = client.post(
        "/api/v1/requisition-details",
        json={
            "requisition_id":
            requisition[
                "requisition_id"
            ],

            "part_id":
            part["part_id"],

            "quantity_required":
            1,
        },
    )

    detail = create_response.json()

    response = client.get(
        f"/api/v1/requisition-details/"
        f"{detail['requisition_detail_id']}"
    )

    assert (
        response.status_code
        == 200
    )


def test_update_requisition_detail():

    requisition = create_requisition()

    part = create_part()

    create_response = client.post(
        "/api/v1/requisition-details",
        json={
            "requisition_id":
            requisition[
                "requisition_id"
            ],

            "part_id":
            part["part_id"],

            "quantity_required":
            1,
        },
    )

    detail = create_response.json()

    response = client.put(
        f"/api/v1/requisition-details/"
        f"{detail['requisition_detail_id']}",
        json={
            "quantity_required":
            5,
        },
    )

    assert (response.status_code == 200)

    result = response.json()

    assert (
        result["quantity_required"] == 5)


def test_delete_requisition_detail():

    requisition = create_requisition()

    part = create_part()

    create_response = client.post(
        "/api/v1/requisition-details",
        json={
            "requisition_id":
            requisition[
                "requisition_id"
            ],

            "part_id":
            part["part_id"],

            "quantity_required":
            1,
        },
    )

    detail = create_response.json()

    response = client.delete(
        f"/api/v1/requisition-details/"
        f"{detail['requisition_detail_id']}"
    )

    assert (
        response.status_code == 200)

    result = response.json()

    assert (
        result["active_flag"] is False)


def test_update_requisition_detail_not_found():

    response = client.put(
        "/api/v1/requisition-details/999999",
        json={
            "quantity_required":
            10,
        },
    )

    assert (
        response.status_code == 404)


def test_delete_requisition_detail_not_found():

    response = client.delete(
        "/api/v1/requisition-details/999999"
    )

    assert (
        response.status_code == 404)