from app.models.operations import DriverVehicleAssignment
from app.models.master import DriverMaster, VehicleMaster

import random

def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_driver_assignment_fk(db):

    driver = DriverMaster(
        driver_name=f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=f"901{rand_n_digits(7)}",
        dl_number=f"DL-{rand_n_digits(6)}"
    )
    db.add(driver)
    db.commit()

    vehicle = VehicleMaster(
        rc_number=f"TEST-{rand_n_digits(6)}",
        engine_no=f"ENG-{rand_n_digits(6)}",
        chassis_no=f"CH-{rand_n_digits(6)}"
    )

    db.add(driver)
    db.add(vehicle)
    db.commit()

    assignment = DriverVehicleAssignment(
        driver_id=driver.driver_id,
        vehicle_id=vehicle.vehicle_id
    )

    db.add(assignment)
    db.commit()

    assert assignment.assignment_id is not None

