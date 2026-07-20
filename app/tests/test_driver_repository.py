

from app.models.master import DriverMaster
from app.repositories.driver_repository import (
    DriverRepository,
)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )


def test_driver_by_dl(db):

    driver = DriverMaster(
        driver_name=     f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=   f"901{rand_n_digits(7)}",
        dl_number=       f"DL-{rand_n_digits(6)}",
    )

    repo = DriverRepository(db)

    repo.create(driver)

    assert driver.dl_number is not None
    
    result = repo.get_by_dl_number(
        driver.dl_number
    )
    assert result is not None
