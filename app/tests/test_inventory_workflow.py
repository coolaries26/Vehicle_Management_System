from app.models.inventory import PartMaster, PartRequest
from app.models.master import VehicleMaster,EmployeeMaster
from app.db.session import SessionLocal
from datetime import datetime
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def inventory_workflow_test(db):
    #create
    part = PartMaster(
        part_code=f"BAT-{datetime.now().timestamp()}",
        part_name="Battery"
    )
    db.add(part)
    employee = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech User",
        phone_number="8888888888",
        )
    db.add(employee)

    vehicle = VehicleMaster(
        rc_number= f"TEST-{rand_n_digits(6)}",
        engine_no= f"ENG-{rand_n_digits(6)}",
        chassis_no= f"CH-{rand_n_digits(6)}",
    )
    db.add(vehicle)
    

    #then
    request = PartRequest(
        request_number=f"REQ-{rand_n_digits(6)}",
        vehicle_id=vehicle.vehicle_id,
        request_id=employee.employee_id
    )
    db.add(request)
    db.commit()
