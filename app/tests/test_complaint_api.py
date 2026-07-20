from fastapi.testclient import TestClient

from app.main import app

import random

client = TestClient(app)


def rand_n_digits(n: int) -> int:
    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )


def create_vehicle():
    payload = {
        "rc_number": f"TEST-{rand_n_digits(6)}",
        "engine_no": f"ENG-{rand_n_digits(6)}",
        "chassis_no": f"CH-{rand_n_digits(6)}",
    }
    response = client.post(
        "/api/v1/vehicles",
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def create_driver():
    payload = {
        "driver_name":        f"Test-Driver-{rand_n_digits(6)}",
        "mobile_number":        f"901{rand_n_digits(7)}",
        "dl_number":        f"DL-{rand_n_digits(6)}",
    }
    response = client.post(
        "/api/v1/drivers",
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def create_complaint():
    vehicle = create_vehicle()
    driver = create_driver()
    payload = {
        "vehicle_id":        vehicle["vehicle_id"],
        "driver_id":         driver["driver_id"],
        "issue_description": "Battery issue",
    }
    response = client.post(
        "/api/v1/complaints",
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def test_create_complaint():
    vehicle = create_vehicle()
    driver = create_driver()
    payload = {
        "vehicle_id":        vehicle["vehicle_id"],
        "driver_id":        driver["driver_id"],
        "issue_description":       "Battery issue",
    }
    response = client.post(
        "/api/v1/complaints",
        json=payload,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["complaint_id"] is not None
    assert (
        body["vehicle_id"]
        == payload["vehicle_id"]
    )
    assert (
        body["driver_id"]
        == payload["driver_id"]
    )
    assert (
        body["issue_description"]
        == payload["issue_description"]
    )


def test_get_complaint():
    complaint = create_complaint()
    complaint_id = (
        complaint["complaint_id"]
    )
    response = client.get(
        f"/api/v1/complaints/{complaint_id}"
    )
    assert response.status_code == 200
    body = response.json()
    assert (
        body["complaint_id"]
        == complaint_id
    )

def test_get_all_complaints():
    create_complaint()
    response = client.get(
        "/api/v1/complaints"
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0


def test_update_complaint():
    complaint = create_complaint()
    complaint_id = (
        complaint["complaint_id"]
    )
    response = client.put(
        f"/api/v1/complaints/{complaint_id}",
        json={
            "issue_description":
            "Updated complaint"
        },
    )
    assert response.status_code == 200
    body = response.json()

    assert (
        body["complaint_id"]
        == complaint_id
    )
    assert (
        body["issue_description"]
        == "Updated complaint"
    )


def test_delete_complaint():
    complaint = create_complaint()
    complaint_id = (
        complaint["complaint_id"]
    )
    response = client.delete(
        f"/api/v1/complaints/{complaint_id}"
    )
    assert response.status_code == 200
    response = client.get(
        f"/api/v1/complaints/{complaint_id}"
    )
    assert response.status_code == 404


def test_get_complaint_not_found():
    response = client.get(
        "/api/v1/complaints/999999999"
    )
    assert response.status_code == 404


def test_update_complaint_not_found():
    response = client.put(
        "/api/v1/complaints/999999999",
        json={
            "issue_description":
            "Updated complaint"
        },
    )
    assert response.status_code == 404


def test_delete_complaint_not_found():
    response = client.delete(
        "/api/v1/complaints/999999999"
    )
    assert response.status_code == 404


def test_create_complaint_invalid_vehicle():
    driver = create_driver()
    payload = {
        "vehicle_id": 999999999,
        "driver_id":
        driver["driver_id"],

        "issue_description":
        "Invalid vehicle test",
    }
    response = client.post(
        "/api/v1/complaints",
        json=payload,
    )
    assert response.status_code == 404


def test_create_complaint_invalid_driver():
    vehicle = create_vehicle()
    payload = {
        "vehicle_id": vehicle["vehicle_id"],
        
        "driver_id": 999999999,

        "issue_description":
        "Invalid Driver test",
    }
    response = client.post(
        "/api/v1/complaints",
        json=payload,
    )
    assert response.status_code == 404

def test_create_complaint_missing_vehicle():

    response = client.post(
        "/api/v1/complaints",
        json={
            "driver_id": 1,
            "issue_description":
            "Battery"
        }
    )

    assert response.status_code == 422

def test_no_orphan_complaints():

    response = client.get(
        "/api/v1/complaints"
    )

    complaints = response.json()

    for complaint in complaints:

        assert (
            complaint["vehicle_id"]
            is not None
        )

        assert (
            complaint["driver_id"]
            is not None
        )