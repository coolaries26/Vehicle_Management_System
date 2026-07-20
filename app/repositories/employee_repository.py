from sqlalchemy.orm import Session

from app.models.master import EmployeeMaster

from app.repositories.base_repository import (
    BaseRepository,
)


class EmployeeRepository(
    BaseRepository[EmployeeMaster]
):

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(
            EmployeeMaster,
            db,
        )

    def get_by_id(
        self,
        employee_id: int,
    ) -> EmployeeMaster | None:

        return (
            self.db.query(
                EmployeeMaster
            )
            .filter(
                EmployeeMaster.employee_id
                == employee_id
            )
            .first()
        )

    def get_by_phone(
        self,
        phone_number: str,
    ) -> EmployeeMaster | None:

        return (
            self.db.query(
                EmployeeMaster
            )
            .filter(
                EmployeeMaster.phone_number
                == phone_number
            )
            .first()
        )

    def update_employee(
        self,
        employee: EmployeeMaster,
        data: dict,
    ):
        for key, value in data.items():
            setattr(
                employee,
                key,
                value,
            )

        self.db.commit()
        self.db.refresh(
            employee
        )
        return employee
    
    def exists(
    self,
    employee_id: int
    ) -> bool:
    
        return (
            self.get_by_id(employee_id)
            is not None
        )