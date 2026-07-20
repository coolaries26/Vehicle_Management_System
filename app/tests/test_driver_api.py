from fastapi.testclient import (
    TestClient,
)
import random

def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

from app.models.master import DriverMaster
from app.main import app

client = TestClient(app)


def create_driver():

    payload = {
        "driver_name" : f"Test-Driver-{rand_n_digits(6)}",
        "mobile_number" : f"901{rand_n_digits(7)}",
        "dl_number" : f"DL-{rand_n_digits(6)}"
    }

    response = client.post(
        "/api/v1/drivers",
        json=payload,
    )

    assert ( response.status_code == 201 )
    return response.json()

def test_create_driver():
    payload = {
        "driver_name" : f"Test-Driver-{rand_n_digits(6)}",
        "mobile_number" : f"901{rand_n_digits(7)}",
        "dl_number" : f"DL-{rand_n_digits(6)}"
    }
    response = client.post(
        "/api/v1/drivers",
        json=payload,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["dl_number"] is not None
    assert (
        body["dl_number"]
        == payload["dl_number"]
    )


def test_get_driver():

    driver = create_driver()

    driver_id = driver["driver_id"]

    response = client.get(
        f"/api/v1/drivers/{driver_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["driver_id"]
        == driver_id
    )


def test_get_all_drivers():

    create_driver()

    response = client.get(
        "/api/v1/drivers"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(
        body,
        list,
    )

    assert len(body) > 0


def test_update_driver():

    driver = create_driver()

    driver_id = driver["driver_id"]

    response = client.put(
        f"/api/v1/drivers/{driver_id}",
        json={
            "dl_issue_city": "Delhi"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["driver_id"]
        == driver_id
    )


def test_delete_driver():

    driver = create_driver()

    driver_id = driver["driver_id"]

    response = client.delete(
        f"/api/v1/drivers/{driver_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/drivers/{driver_id}"
    )

    assert get_response.status_code == 404


def test_get_driver_not_found():

    response = client.get(
        "/api/v1/drivers/999999999"
    )

    assert response.status_code == 404


def test_update_driver_not_found():

    response = client.put(
        "/api/v1/drivers/999999999",
        json={
            "fuel_capacity": 40
        },
    )

    assert response.status_code == 404


def test_delete_driver_not_found():

    response = client.delete(
        "/api/v1/drivers/999999999"
    )

    assert response.status_code == 404


def test_duplicate_driver():

    dl_number = f"DL-{rand_n_digits(6)}"

    payload = {
        "dl_number" : dl_number,
        "driver_name" : f"Test-Driver-{rand_n_digits(6)}",
        "mobile_number" : f"901{rand_n_digits(7)}"
    }

    response1 = client.post(
        "/api/v1/drivers",
        json=payload,
    )

    assert response1.status_code == 201

    response2 = client.post(
        "/api/v1/drivers",
        json=payload,
    )

    assert response2.status_code in [
        400,
        409,
    ]
