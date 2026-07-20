#Test 1 — Vehicle ↔ Complaint

from app.db.base import Base
from app.models import *
from app.db.session import engine
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )


def test_vehicle_complaint_relationship(db,):
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

    db.refresh(vehicle)

    assert len(vehicle.complaints) == 1

    assert (
        vehicle.complaints[0].complaint_id
        == complaint.complaint_id
    )

    assert (
        complaint.vehicle.vehicle_id
        == vehicle.vehicle_id
    )



#Test 2 — Complaint ↔ Inspection
def test_complaint_inspection_relationship(db,):

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


    assert len(complaint.inspections) == 1

    assert (
        inspection.complaint.complaint_id
        == complaint.complaint_id
    )

#Test 3 — Employee ↔ Inspection
def test_employee_inspection_relationship(db,):

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

    db.refresh(inspection)


    assert len(
        technician.inspections
    ) == 1

    assert (
        technician.inspections[0]
        .inspection_id
        == inspection.inspection_id
    )

    assert (
        inspection.technician.employee_id
        == technician.employee_id
    )
# Test 4 — Vehicle ↔ Job Card
def test_vehicle_jobcard_relationship( db,):

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

    db.add_all([vehicle, driver])
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
    db.refresh(vehicle)
    db.refresh(driver)
    db.refresh(complaint)
    db.refresh(technician)

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


    assert len(
        vehicle.job_cards
    ) == 1

    assert (
        jobcard.vehicle.vehicle_id
        == vehicle.vehicle_id
    )
#Test 5 — Job Card ↔ Parts
def test_jobcard_part_relationship( db,):

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
    db.refresh(vehicle)
    db.refresh(driver)
    db.refresh(complaint)
    db.refresh(technician)
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

    jc_part = JobCardPart(
        job_card_id=jobcard.job_card_id,
        part_id=part.part_id,
        quantity=1,
        unit_price=100,
    )

    db.add(jc_part)
    db.commit()

    db.refresh(jobcard)

    assert len(jobcard.parts) == 1

    assert (
        jc_part.job_card.job_card_id
        == jobcard.job_card_id
    )
#Test 6 — Vehicle ↔ PM Checklist
def test_vehicle_checklist_relationship( db,):

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


    db.add(vehicle)
    db.add(driver)
    db.add(complaint)
    db.add(technician)
    db.commit()
    db.refresh(vehicle)
    db.refresh(driver)
    db.refresh(complaint)
    db.refresh(technician)
    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Dead Battery",
    )
    db.add(inspection)
    db.commit()


    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=vehicle.vehicle_id,
            technician_id=technician.employee_id,
        )
    )

    db.add(checklist)
    db.commit()

    db.refresh(vehicle)

    assert (
        len(
            vehicle.pm_checklists
        )
        == 1
    )

    assert (
        checklist.vehicle.vehicle_id
        == vehicle.vehicle_id
    )

def test_full_maintenance_flow(db):

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
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech User",
        phone_number="8888888888",
    )

    part = PartMaster(
        part_code=f"P-{rand_n_digits(6)}",
        part_name="Battery",
    )

    db.add_all(
        [
            technician,
            part,
        ]
    )

    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Failure",
    )

    db.add(complaint)
    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Battery Dead",
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

    jc_part = JobCardPart(
        job_card_id=jobcard.job_card_id,
        part_id=part.part_id,
        quantity=1,
        unit_price=100,
        total_price=100,
    )

    db.add(jc_part)

    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=vehicle.vehicle_id,
            technician_id=technician.employee_id,
        )
    )

    db.add(checklist)

    db.commit()

    db.refresh(vehicle)
    db.refresh(complaint)
    db.refresh(inspection)
    db.refresh(jobcard)

    assert len(vehicle.complaints) == 1

    assert (
        complaint.vehicle.vehicle_id
        == vehicle.vehicle_id
    )

    assert len(complaint.inspections) == 1

    assert (
        inspection.complaint.complaint_id
        == complaint.complaint_id
    )

    assert (
        inspection.technician.employee_id
        == technician.employee_id
    )

    assert (
        jobcard.vehicle.vehicle_id
        == vehicle.vehicle_id
    )

    assert (
        jobcard.inspection.inspection_id
        == inspection.inspection_id
    )

    assert len(jobcard.parts) == 1

    assert (
        jc_part.job_card.job_card_id
        == jobcard.job_card_id
    )

    assert len(vehicle.pm_checklists) == 1

    assert (
        checklist.vehicle.vehicle_id
        == vehicle.vehicle_id
    )