from fastapi.testclient import TestClient
from app.main import app
import random
client = TestClient(app)


def rand_n_digits(
    n: int,
) -> int:

    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )


def create_employee():
    payload = {
        "employee_type":  "TECHNICIAN",
        "full_name"    :  f"Tech-{rand_n_digits(6)}",
        "phone_number" :  f"999{rand_n_digits(7)}",
    }
    response = client.post( "/api/v1/employees", json=payload,  )
    assert response.status_code == 201
    return response.json()


def test_create_employee():
    employee = create_employee()
    assert (
        employee["employee_id"]
        is not None
    )

def test_get_employee():

    employee = create_employee()

    employee_id = employee["employee_id"]

    response = client.get(
        f"/api/v1/employees/{employee_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["employee_id"]
        == employee_id
    )


def test_get_all_employees():

#    create_employee()

    response = client.get(
        "/api/v1/employees"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(
        body,
        list,
    )

    assert len(body) > 0


def test_update_employee():

    employee = create_employee()

    employee_id = employee["employee_id"]

    response = client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "employee_type": "TECH_TEST"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["employee_id"]
        == employee_id
    )


def test_delete_employee():

    employee = create_employee()

    employee_id = employee["employee_id"]

    response = client.delete(
        f"/api/v1/employees/{employee_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/employees/{employee_id}"
    )

    assert get_response.status_code == 404


def test_get_employee_not_found():

    response = client.get(
        "/api/v1/employees/999999999"
    )

    assert response.status_code == 404


def test_update_employee_not_found():

    response = client.put(
        "/api/v1/employees/999999999",
        json={
            "employee_type": "TECH_TEST"
        },
    )

    assert response.status_code == 404


def test_delete_employee_not_found():

    response = client.delete(
        "/api/v1/employees/999999999"
    )

    assert response.status_code == 404


def test_duplicate_employee():


    payload = {
        "employee_type":  "TECHNICIAN",
        "full_name"    :  f"Tech-{rand_n_digits(6)}",
        "phone_number" :  f"999{rand_n_digits(7)}",
    }

    response1 = client.post(
        "/api/v1/employees",
        json=payload,
    )

    assert response1.status_code == 201

    response2 = client.post(
        "/api/v1/employees",
        json=payload,
    )

    assert response2.status_code in [
        400,
        409,
    ]
