from app.repositories.jobcard_repository import (
    JobCardRepository,
)
from app.models.maintenance import(
    MaintenanceJobCard,
)
from app.models import *

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_get_jobcard_by_id(
    db,
):

    repo = JobCardRepository(
        db
    )
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


    complaint = VehicleComplaint(
    vehicle_id=vehicle.vehicle_id,
    driver_id=driver.driver_id,
    issue_description="Battery Issue",
    )

    db.add(complaint)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Dead Battery",
    )
    db.add(inspection)
    db.commit()

    jobcard = MaintenanceJobCard(
        complaint_id=complaint.complaint_id,
        inspection_id=inspection.inspection_id,
        vehicle_id=vehicle.vehicle_id,
    )

    db.add(jobcard)
    db.commit()

   
    result = repo.get_by_id(
        jobcard.job_card_id
    )
    assert result is not None
    assert (
        result.job_card_id
        == jobcard.job_card_id
    )

def test_get_jobcard_by_vehicle(
    db,
):

    repo = JobCardRepository(
        db
    )

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
    complaint = VehicleComplaint(
    vehicle_id=vehicle.vehicle_id,
    driver_id=driver.driver_id,
    issue_description="Battery Issue",
    )

    db.add(complaint)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )


    db.add(technician)
    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Dead Battery",
    )
    db.add(inspection)
    db.commit()


    jobcard = MaintenanceJobCard(
        complaint_id=complaint.complaint_id,
        inspection_id=inspection.inspection_id,
        vehicle_id=vehicle.vehicle_id,
    )

    db.add(jobcard)
    db.commit()
#    print("Vehicle ID:", vehicle.vehicle_id)
#    print("JobCard Vehicle ID:", jobcard.vehicle_id)

    result = repo.get_by_vehicle(
        vehicle.vehicle_id
    )
    result = repo.get_by_vehicle(
        vehicle.vehicle_id
    )
    assert result is not None
    assert len(result) == 1

def test_update_jobcard(
    db,
):

    repo = JobCardRepository(
        db
    )
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
    complaint = VehicleComplaint(
    vehicle_id=vehicle.vehicle_id,
    driver_id=driver.driver_id,
    issue_description="Battery Issue",
    )

    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )


    db.add(complaint)
    db.add(technician)
    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Dead Battery",
    )
    db.add(inspection)
    db.commit()
    jobcard = MaintenanceJobCard(
        complaint_id=complaint.complaint_id,
        inspection_id=inspection.inspection_id,
        vehicle_id=vehicle.vehicle_id,
    )

    db.add(jobcard)
    db.commit()

    updated = repo.update_jobcard(
        jobcard,
        {
            "labour_charges": 500.00
        }
    )
    db.add(jobcard)
    db.commit()

    assert (
        updated.labour_charges
        == 500.00
    )

def test_delete_jobcard(
    db,
):

    repo = JobCardRepository(
        db
    )
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
    complaint = VehicleComplaint(
    vehicle_id=vehicle.vehicle_id,
    driver_id=driver.driver_id,
    issue_description="Battery Issue",
    )

    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )


    db.add(complaint)
    db.add(technician)
    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Dead Battery",
    )
    db.add(inspection)
    db.commit()
    jobcard = MaintenanceJobCard(
        complaint_id=complaint.complaint_id,
        inspection_id=inspection.inspection_id,
        vehicle_id=vehicle.vehicle_id,
    )

    db.add(jobcard)
    db.commit()

    repo.delete_jobcard(
        jobcard
    )

    result = repo.get_by_id(
        jobcard.job_card_id
    )

    assert result is None