from app.models.master import EmployeeMaster
from app.db.session import SessionLocal
employee = EmployeeMaster(
    employee_type="TECHNICIAN",
    full_name="Test Employee",
    phone_number="9999999999"
)

session = SessionLocal()
session.add(employee)
session.commit()