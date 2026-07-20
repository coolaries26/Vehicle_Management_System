from app.models import *
from app.models.maintenance import MaintenanceJobCard,VehicleComplaint, TechnicianInspection
from app.models.master import VehicleMaster,DriverMaster,EmployeeMaster
from app.db.session import SessionLocal

from fastapi.testclient import (
    TestClient,
)
import random

def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )
from app.main import app
client = TestClient(app)

def test_create_jobcard_part(db):

    vehicle = VehicleMaster(
        rc_number=f"TEST-{rand_n_digits(6)}",
        engine_no=f"ENG-{rand_n_digits(6)}",
        chassis_no=f"CH-{rand_n_digits(6)}"
    )

    driver = DriverMaster(
        driver_name=     f"Test-Driver-{rand_n_digits(6)}",
        mobile_number=   f"901{rand_n_digits(7)}",
        dl_number=       f"DL-{rand_n_digits(6)}",
    )


    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )

    db.add(vehicle)
    db.add(driver)
    db.add(technician)
    db.commit()

    db.refresh(vehicle)
    db.refresh(driver)
    db.refresh(technician)

    complaint = VehicleComplaint(
    vehicle_id=vehicle.vehicle_id,
    driver_id=driver.driver_id,
    issue_description="Battery Issue",
    )
    db.add(complaint)
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
    db.add(inspection)
    db.add(jobcard)
    db.commit()


    part = PartMaster(
        part_code=f"PART-{rand_n_digits(6)}",
        part_name="Battery",
    )

    db.add(part)
    db.commit()
    jobcard_part = JobCardPart(
        job_card_id=jobcard.job_card_id,
        part_id=part.part_id,
        quantity=1,
        unit_price=100,
        total_price=100,
    )
    
    db.add(jobcard_part)
    db.commit()


    db.refresh(jobcard)

    assert len(jobcard.parts) == 1


    response = client.post(
        "/api/v1/jobcard-parts",
        json={
            "job_card_id": jobcard.job_card_id,
            "part_id": part.part_id,
            "quantity": 2,
            "unit_price": 100,
        }
    )

    assert response.status_code == 201