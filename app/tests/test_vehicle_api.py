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


def test_create_vehicle():
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
    body = response.json()
    assert body["vehicle_id"] is not None
    assert (
        body["rc_number"]
        == payload["rc_number"]
    )


def test_get_vehicle():

    vehicle = create_vehicle()

    vehicle_id = vehicle["vehicle_id"]

    response = client.get(
        f"/api/v1/vehicles/{vehicle_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["vehicle_id"]
        == vehicle_id
    )


def test_get_all_vehicles():

    create_vehicle()

    response = client.get(
        "/api/v1/vehicles"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(
        body,
        list,
    )

    assert len(body) > 0


def test_update_vehicle():

    vehicle = create_vehicle()

    vehicle_id = vehicle["vehicle_id"]

    response = client.put(
        f"/api/v1/vehicles/{vehicle_id}",
        json={
            "fuel_capacity": 45
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["vehicle_id"]
        == vehicle_id
    )


def test_delete_vehicle():

    vehicle = create_vehicle()

    vehicle_id = vehicle["vehicle_id"]

    response = client.delete(
        f"/api/v1/vehicles/{vehicle_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/vehicles/{vehicle_id}"
    )

    assert get_response.status_code == 404


def test_get_vehicle_not_found():

    response = client.get(
        "/api/v1/vehicles/999999999"
    )

    assert response.status_code == 404


def test_update_vehicle_not_found():

    response = client.put(
        "/api/v1/vehicles/999999999",
        json={
            "fuel_capacity": 40
        },
    )

    assert response.status_code == 404


def test_delete_vehicle_not_found():

    response = client.delete(
        "/api/v1/vehicles/999999999"
    )

    assert response.status_code == 404


def test_duplicate_vehicle():

    rc = f"TEST-{rand_n_digits(6)}"

    payload = {
        "rc_number": rc,
        "engine_no": f"ENG-{rand_n_digits(6)}",
        "chassis_no": f"CH-{rand_n_digits(6)}",
    }

    response1 = client.post(
        "/api/v1/vehicles",
        json=payload,
    )

    assert response1.status_code == 201

    response2 = client.post(
        "/api/v1/vehicles",
        json=payload,
    )

    assert response2.status_code in [
        400,
        409,
    ]
