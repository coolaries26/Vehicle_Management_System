from fastapi.testclient import (    TestClient,)    #type: ignore

from app.main import app
client = TestClient(app)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )
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

def test_create_part():

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


def test_get_all_parts():

    response = client.get(
        "/api/v1/parts"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(
        data,
        list,
    )


def test_get_part_by_id():

    create_response = client.post(
        "/api/v1/parts",
        json={
        "part_code": f"PART-{rand_n_digits(6)}",
        "part_name": "Engine Oil",
        "active_flag": True,
        },
    )

    part_id = (
        create_response
        .json()["part_id"]
    )

    response = client.get(
        f"/api/v1/parts/{part_id}"
    )

    assert response.status_code == 200

    result = response.json()

    assert (
        result["part_id"]
        == part_id
    )


def test_update_part():

    create_response = client.post(
        "/api/v1/parts",
        json={
            "part_code": f"PART-{rand_n_digits(6)}",
            "part_name": "Old Name",
            "active_flag": True,
        },
    )

    part_id = (
        create_response
        .json()["part_id"]
    )

    response = client.put(
        f"/api/v1/parts/{part_id}",
        json={
            "part_name":
                "New Name",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert (
        result["part_name"]
        == "New Name"
    )


def test_deactivate_part():

    create_response = client.post(
        "/api/v1/parts",
        json={
            "part_code": f"PART-{rand_n_digits(6)}",
            "part_name": "Battery",
            "active_flag": True,
        },
    )

    part_id = (
        create_response
        .json()["part_id"]
    )

    response = client.put(
        f"/api/v1/parts/{part_id}",
        json={
            "active_flag":
                False,
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert (
        result["active_flag"]
        is False
    )