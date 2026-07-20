from app.models.master import (
    DriverMaster,
    VehicleMaster,
)
from app.repositories.complaint_repository import (ComplaintRepository,)
from app.repositories.driver_repository import (DriverRepository,)
from app.repositories.vehicle_repository import (VehicleRepository,)
from app.schemas.complaint import (ComplaintCreate,)
from app.services.complaint_service import (ComplaintService,)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )


def test_create_complaint_service(
    db
):
    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
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

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    payload = ComplaintCreate(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Problem",
    )

    complaint = (
        service.create_complaint(
            payload
        )
    )

    assert complaint.complaint_id