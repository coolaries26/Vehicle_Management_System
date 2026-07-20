from app.models.master import VehicleMaster
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_vehicle(db):

    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    assert vehicle.vehicle_id is not None

