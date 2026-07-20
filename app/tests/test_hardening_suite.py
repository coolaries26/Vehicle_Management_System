from fastapi.testclient import TestClient

from app.main import app

import random

client = TestClient(app)


# =========================================================
# Helpers
# =========================================================

def rand_n_digits(n: int) -> int:

    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )


def create_vehicle():

    payload = {
        "rc_number": f"TEST-{rand_n_digits(8)}",
        "engine_no": f"ENG-{rand_n_digits(8)}",
        "chassis_no": f"CH-{rand_n_digits(8)}",
    }

    response = client.post(
        "/api/v1/vehicles",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def create_driver():

    payload = {
        "driver_name":
        f"Driver-{rand_n_digits(6)}",

        "mobile_number":
        f"999{rand_n_digits(7)}",

        "dl_number":
        f"DL-{rand_n_digits(8)}",
    }

    response = client.post(
        "/api/v1/drivers",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def create_employee():

    payload = {
        "employee_type":
        "TECHNICIAN",

        "full_name":
        f"Tech-{rand_n_digits(6)}",

        "phone_number":
        f"888{rand_n_digits(7)}",
    }

    response = client.post(
        "/api/v1/employees",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def create_complaint():

    vehicle = create_vehicle()

    driver = create_driver()

    payload = {
        "vehicle_id":
        vehicle["vehicle_id"],

        "driver_id":
        driver["driver_id"],

        "issue_description":
        "Battery failure",
    }

    response = client.post(
        "/api/v1/complaints",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def create_inspection():

    complaint = create_complaint()

    employee = create_employee()

    payload = {
        "complaint_id":
        complaint["complaint_id"],

        "technician_id":
        employee["employee_id"],

        "observed_issue":
        "Battery dead",

        "status":
        "OPEN"
    }

    response = client.post(
        "/api/v1/inspections",
        json=payload,
    )

    assert response.status_code == 201

    return (
        response.json(),
        complaint,
        employee,
    )


def create_jobcard():

    inspection, complaint, _ = (
        create_inspection()
    )

    payload = {
        "complaint_id":
        complaint["complaint_id"],

        "inspection_id":
        inspection["inspection_id"],

        "vehicle_id":
        complaint["vehicle_id"],
    }

    response = client.post(
        "/api/v1/jobcards",
        json=payload,
    )

    assert response.status_code == 201

    return (
        response.json(),
        complaint,
        inspection,
    )

# def test_database_constraints():
#     assert complaint.vehicle_id.nullable is False
#     assert complaint.driver_id.nullable is False
# 
#     assert inspection.complaint_id.nullable is False
#     assert inspection.technician_id.nullable is False

# =========================================================
# Health Endpoint
# =========================================================

def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    body = response.json()

    assert "status" in body


# =========================================================
# OpenAPI
# =========================================================

def test_openapi_document():

    response = client.get(
        "/openapi.json"
    )

    assert response.status_code == 200

    body = response.json()

    assert "paths" in body


# =========================================================
# Complaint Validation
# =========================================================

def test_create_complaint_missing_driver():

    vehicle = create_vehicle()

    response = client.post(
        "/api/v1/complaints",
        json={
            "vehicle_id":
            vehicle["vehicle_id"],

            "issue_description":
            "Battery Issue",
        }
    )

    assert response.status_code == 422


def test_create_complaint_missing_vehicle():

    driver = create_driver()

    response = client.post(
        "/api/v1/complaints",
        json={
            "driver_id":
            driver["driver_id"],

            "issue_description":
            "Battery Issue",
        }
    )

    assert response.status_code == 422


# =========================================================
# Inspection Validation
# =========================================================

def test_create_inspection_invalid_complaint():

    employee = create_employee()

    response = client.post(
        "/api/v1/inspections",
        json={
            "complaint_id": 999999999,
            "technician_id":
            employee["employee_id"],
        }
    )

    assert response.status_code == 404


def test_create_inspection_invalid_technician():

    complaint = create_complaint()

    response = client.post(
        "/api/v1/inspections",
        json={
            "complaint_id":
            complaint["complaint_id"],

            "technician_id":
            999999999,
        }
    )

    assert response.status_code == 404


# =========================================================
# JobCard Validation
# =========================================================

def test_create_jobcard_invalid_vehicle():

    inspection, complaint, _ = (
        create_inspection()
    )

    response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id":
            complaint["complaint_id"],

            "inspection_id":
            inspection["inspection_id"],

            "vehicle_id":
            999999999,
        }
    )

    assert response.status_code == 404


def test_create_jobcard_invalid_complaint():

    inspection, _, _ = (
        create_inspection()
    )

    response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id":
            999999999,

            "inspection_id":
            inspection["inspection_id"],

            "vehicle_id":
            1,
        }
    )

    assert response.status_code == 404


def test_create_jobcard_invalid_inspection():

    complaint = create_complaint()

    response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id":
            complaint["complaint_id"],

            "inspection_id":
            999999999,

            "vehicle_id":
            complaint["vehicle_id"],
        }
    )

    assert response.status_code == 404


# =========================================================
# Checklist Validation
# =========================================================

def test_create_checklist_invalid_vehicle():

    employee = create_employee()

    response = client.post(
        "/api/v1/checklists",
        json={
            "vehicle_id":
            999999999,

            "technician_id":
            employee["employee_id"],
        }
    )

    assert response.status_code == 404


def test_create_checklist_invalid_technician():

    vehicle = create_vehicle()
    

    response = client.post(
        "/api/v1/checklists",
        json={
            "vehicle_id":
            vehicle["vehicle_id"],

            "technician_id":
            999999999,
        }
    )

    assert response.status_code == 404


# =========================================================
# Data Integrity Tests
# =========================================================

def test_no_orphan_complaints():

    response = client.get(
        "/api/v1/complaints"
    )

    assert response.status_code == 200

    for complaint in response.json():

        assert (
            complaint["vehicle_id"]
            is not None
        )

        assert (
            complaint["driver_id"]
            is not None
        )


def test_no_orphan_inspections():

    response = client.get(
        "/api/v1/inspections"
    )

    assert response.status_code == 200

    for inspection in response.json():

        assert (
            inspection["complaint_id"]
            is not None
        )

        assert (
            inspection["technician_id"]
            is not None
        )


def test_no_orphan_jobcards():

    response = client.get(
        "/api/v1/jobcards"
    )

    assert response.status_code == 200

    for jobcard in response.json():
#        print(jobcard)
        assert (
            jobcard["vehicle_id"]
            is not None
        )

        assert (
            jobcard["complaint_id"]
            is not None
        )

        assert (
            jobcard["inspection_id"]
            is not None
        )


# =========================================================
# Full REST Workflow
# =========================================================

def test_full_api_workflow():

    vehicle = create_vehicle()

    driver = create_driver()

    employee = create_employee()

    complaint_response = client.post(
        "/api/v1/complaints",
        json={
            "vehicle_id":
            vehicle["vehicle_id"],

            "driver_id":
            driver["driver_id"],

            "issue_description":
            "Battery issue",
        }
    )

    assert complaint_response.status_code == 201

    complaint = (
        complaint_response.json()
    )

    inspection_response = client.post(
        "/api/v1/inspections",
        json={
            "complaint_id":
            complaint["complaint_id"],

            "technician_id":
            employee["employee_id"],

            "observed_issue":
            "Battery dead",
        }
    )

    assert inspection_response.status_code == 201

    inspection = (
        inspection_response.json()
    )

    jobcard_response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id":
            complaint["complaint_id"],

            "inspection_id":
            inspection["inspection_id"],

            "vehicle_id":
            vehicle["vehicle_id"],
        }
    )

    assert jobcard_response.status_code == 201

# =========================================================
# Full REST Workflow
# =========================================================
def test_create_jobcard_missing_vehicle():

    response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id": 1,
            "inspection_id": 1
        }
    )

    assert response.status_code == 422