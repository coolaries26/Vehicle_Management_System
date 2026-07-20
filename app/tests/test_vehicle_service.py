

from app.schemas.vehicle import (
    VehicleCreate,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.services.vehicle_service import (
    VehicleService,
)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_vehicle_service(
    db
):

    repo = VehicleRepository(db)

    service = VehicleService(
        repo
    )

    payload = VehicleCreate(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    vehicle = (
        service.create_vehicle(
            payload
        )
    )

    assert vehicle.vehicle_id