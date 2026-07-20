from app.models.master import DriverMaster
from app.models.master import VehicleMaster
from app.models.master import EmployeeMaster
from app.models.maintenance import (PreventiveMaintenanceChecklist)
from app.repositories.checklist_repository import (ChecklistRepository,)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

#test_get_checklist_by_id()
def test_get_checklist_by_id(db):

    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()
    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=        vehicle.vehicle_id,
            technician_id=     technician.employee_id,
            observation=       "test.observation",
            issue_found=       True,
            issue_description= "test.issue_description",
        )
    )

    repo = ChecklistRepository(db)

    repo.create(checklist)

    result = repo.get_by_id(
        checklist.checklist_id
    )
    assert result is not None
    assert result.checklist_id == checklist.checklist_id


#test_get_by_vehicle()
def test_get_by_vehicle_id(db):

    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()
    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=        vehicle.vehicle_id,
            technician_id=     technician.employee_id,
            observation=       "test.observation",
            issue_found=       True,
            issue_description= "test.issue_description",
        )
    )

    repo = ChecklistRepository(db)

    repo.create(checklist)

    result = repo.get_by_vehicle(
        checklist.vehicle_id
    )
    assert result is not None
    assert result[0].checklist_id == checklist.checklist_id

#test_get_by_technician()
def test_get_by_technician(db):

    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()
    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=        vehicle.vehicle_id,
            technician_id=     technician.employee_id,
            observation=       "test.observation",
            issue_found=       True,
            issue_description= "test.issue_description",
        )
    )

    repo = ChecklistRepository(db)

    repo.create(checklist)

    result = repo.get_by_technician(
        checklist.technician_id
    )
    assert result is not None
    assert result[0].technician_id == checklist.technician_id

#test_update_checklist()
def test_update_checklist(db,):
    repo = ChecklistRepository(db)
    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()
    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=        vehicle.vehicle_id,
            technician_id=     technician.employee_id,
            observation=       "test.observation",
            issue_found=       True,
            issue_description= "test.issue_description",
        )
    )

    db.add(checklist)
    db.commit()

    updated = repo.update_checklist(
        checklist,
        {
            "issue_description": "UPDATED"
        }
    )
    db.add(checklist)
    db.commit()

    assert (
        updated.issue_description
        == "UPDATED"
    )

#test_delete_checklist()
def test_delete_checklist(db):
    repo = ChecklistRepository(
        db
    )
    vehicle = VehicleMaster(
        rc_number=  f"TEST-{rand_n_digits(6)}",
        engine_no=  f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )

    db.add(vehicle)
    db.commit()
    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech",
        phone_number="9999999998",
    )
    db.add(technician)
    db.commit()
    checklist = (
        PreventiveMaintenanceChecklist(
            vehicle_id=        vehicle.vehicle_id,
            technician_id=     technician.employee_id,
            observation=       "test.observation",
            issue_found=       True,
            issue_description= "test.issue_description",
        )
    )

    db.add(checklist)
    db.commit()

    repo.delete_checklist (
        checklist
    )

    result = repo.get_by_id(
        checklist.checklist_id
    )

    assert result is None