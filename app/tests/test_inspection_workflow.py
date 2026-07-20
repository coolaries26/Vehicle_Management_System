from app.models.maintenance import TechnicianInspection, VehicleComplaint
from app.models.master import VehicleMaster,DriverMaster, EmployeeMaster

from app.db.session import SessionLocal 

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_complaint(db):
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

    employee = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech User",
        phone_number="8888888888",
    )

    db.add_all([vehicle, driver, employee])
    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery issue"
    )

    db.add(complaint)
    db.commit()


    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=employee.employee_id,
        observed_issue="Dead Battery"
    )

    db.add(inspection)
    db.commit()

