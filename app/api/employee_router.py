from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.employee_repository import (
    EmployeeRepository,
)

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)

from app.services.employee_service import (
    EmployeeService,
)
from app.api.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employee"],
)
#Create
@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=201,
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = EmployeeService(
        EmployeeRepository(db)
    )

    return service.create_employee(
        payload
    )
#Get
@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):

    service = EmployeeService(
        EmployeeRepository(db)
    )

    return service.get_employee(
        employee_id
    )
#Get all
@router.get(
    "",
   response_model=list[EmployeeResponse],
)
def get_all_employees(
    db: Session = Depends(get_db),
):

    service = EmployeeService(
        EmployeeRepository(db)
    )

    return service.get_all_employees()
#Update
@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
):

    service = EmployeeService(
        EmployeeRepository(db)
    )

    return service.update_employee(
        employee_id,
        payload,
    )
#Delete
@router.delete(
    "/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):

    service = EmployeeService(
        EmployeeRepository(db)
    )

    service.delete_employee(
        employee_id
    )

    return {
        "success": True
    }
