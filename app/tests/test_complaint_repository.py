
from app.models.master import DriverMaster
from app.models.master import VehicleMaster

from app.models.maintenance import (
    VehicleComplaint
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )



def test_get_complaint_by_vehicle(db):

    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    driver = DriverMaster(
        driver_name=     f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=   f"901{rand_n_digits(7)}",
        dl_number=       f"DL-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.add(driver)

    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Issue"
    )

    repo = ComplaintRepository(db)

    repo.create(complaint)

    result = repo.get_by_vehicle(
        vehicle.vehicle_id
    )

    assert len(result) == 1