import pytest

from app.db.session import SessionLocal
from app.models.master import VehicleMaster, EmployeeMaster, DriverMaster 
from app.db.mixins import AuditMixin, TimestampMixin
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

@pytest.fixture
def vehicle(db):

    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@pytest.fixture
def driver(db):

    driver = DriverMaster(
        driver_name=     f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=   f"901{rand_n_digits(7)}",
        dl_number=       f"DL-{rand_n_digits(6)}",
    )

    db.add(driver)
    db.commit()

    return driver

@pytest.fixture
def employee(db):

    employee = EmployeeMaster(
        full_name=f"Test-Employee-{rand_n_digits(6)}",
        phone_number=f"901{rand_n_digits(7)}",
        employee_type="TEST_TECH"
    )

    db.add(employee)
    db.commit()

    return employee


@pytest.fixture
def db():

    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
