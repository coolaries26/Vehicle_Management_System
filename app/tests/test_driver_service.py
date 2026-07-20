

from app.schemas.driver import (
    DriverCreate,
)

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.services.driver_service import (
    DriverService,
)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_driver_service(
    db
):

    repo = DriverRepository(db)

    service = DriverService(
        repo
    )

    payload = DriverCreate(
        driver_name=     f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=   f"901{rand_n_digits(7)}",
        dl_number=       f"DL-{rand_n_digits(6)}",
    )

    driver = (
        service.create_driver(
            payload
        )
    )

    assert driver.driver_id