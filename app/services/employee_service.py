from app.models.master import EmployeeMaster

from app.repositories.employee_repository import (
    EmployeeRepository,
)

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
)

from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
)


class EmployeeService:

    def __init__(
        self,
        employee_repo: EmployeeRepository,
    ):

        self.employee_repo = (
            employee_repo
        )

    def create_employee(
        self,
        payload: EmployeeCreate,
        user_id: int| None = None,
    ):

        existing = (
            self.employee_repo.get_by_phone(
                payload.phone_number
            )
        )

        if existing:

            raise DuplicateRecordException(
                "Employee already exists"
            )

        employee = EmployeeMaster(
            employee_type=
            payload.employee_type,

            full_name=
            payload.full_name,

            phone_number=
            payload.phone_number,
            
            modified_by=
            user_id,
        )

        return (
            self.employee_repo.create(
                employee
            )
        )

    def get_employee(
        self,
        employee_id: int,
    ):

        employee = (
            self.employee_repo.get_by_id(
                employee_id
            )
        )

        if not employee:

            raise NotFoundException(
                "Employee not found"
            )

        return employee

    def get_all_employees(self):

        return (
            self.employee_repo.get_all()
        )

    def update_employee(
        self,
        employee_id: int,
        payload: EmployeeUpdate,
        user_id: int| None = None,
    ):

        employee = (
            self.get_employee(
                employee_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.employee_repo
            .update_employee(
                employee,
                update_data,
            )
        )

    def delete_employee(
        self,
        employee_id: int,
    ):

        employee = (
            self.get_employee(
                employee_id
            )
        )

        self.employee_repo.delete(
            employee
        )