

from app.models.master import VehicleMaster
from app.repositories.vehicle_repository import (
    VehicleRepository,
)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )


def test_get_by_rc_number(db):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    repo = VehicleRepository(db)
    repo.create(vehicle)
    result = repo.get_by_rc_number(
        vehicle.rc_number
    )

    assert result is not None
    assert (result.rc_number == vehicle.rc_number)
def test_get_active_vehicles(db):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    repo = VehicleRepository(db)
    repo.create(vehicle)
    result = repo.get_active_vehicles(
        vehicle.rc_number
    )
    assert result is not None
    assert isinstance(result, list)
    assert any(
    v.rc_number == vehicle.rc_number
    for v in result
    )

def test_update_vehicle(db):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    repo = VehicleRepository(db)
    repo.create(vehicle)
    updated = repo.update_vehicle(
        vehicle,
        {
            "fuel_capacity": 43
        }
    )
    db.add(vehicle)
    db.commit()

    assert (
        updated.fuel_capacity
        == 43
    )

def test_get_by_id(db):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    repo = VehicleRepository(db)
    repo.create(vehicle)
    result = repo.get_by_id(
        vehicle.vehicle_id
    )

    assert result is not None
    assert (result.vehicle_id == vehicle.vehicle_id)
    
def test_delete_vehicle(db):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )
    repo = VehicleRepository(db)
    repo.create(vehicle)
    result = repo.delete_vehicle(
        vehicle
    )

    result = repo.get_by_id(
    vehicle.vehicle_id
    )

    assert result is None
