
from app.models.master import DriverMaster

import random

def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_driver(db):

    driver = DriverMaster(
        driver_name=f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=f"901{rand_n_digits(6)}",
        dl_number=f"DL-{rand_n_digits(6)}"
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)

    assert driver.driver_id is not None
