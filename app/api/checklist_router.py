from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.checklist_repository import (
    ChecklistRepository,)
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.vehicle_repository import ( VehicleRepository)
from app.models.maintenance import PreventiveMaintenanceChecklist

from app.schemas.checklist import (
    PMChecklistCreate,
    PMChecklistResponse,
    PMChecklistUpdate,
)

from app.services.checklist_service import (
    ChecklistService,
    PreventiveMaintenanceChecklist
)

from app.api.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/v1/checklists",
    tags=["Preventive Maintenance"]
)

#POST
@router.post(
    "",
    response_model=PMChecklistResponse,
    status_code=201,
)
def create_checklist(
    payload: PMChecklistCreate,
    db: Session = Depends(get_db),
):

    service = ChecklistService(
        ChecklistRepository(db),
        VehicleRepository(db),
        EmployeeRepository(db),
    )

    return service.create_checklist(
        payload
    )

#GET BY ID
@router.get(
    "/{checklist_id}",
    response_model=PMChecklistResponse,
)
def get_checklist(
    checklist_id: int,
    db: Session = Depends(get_db),
):

    service = ChecklistService(
        ChecklistRepository(db),
        VehicleRepository(db),
        EmployeeRepository(db),
    )

    return service.get_checklist(
        checklist_id
    )
#GET    /
#Get All
@router.get(
    "",
    response_model=list[PMChecklistResponse],
)
def get_all_checklists(
    db: Session = Depends(get_db),
):

    service = ChecklistService(
        ChecklistRepository(db),
        VehicleRepository(db),
        EmployeeRepository(db),
    )

    return (
        service.get_all_checklists()
    )

#PUT
@router.put(
    "/{checklist_id}",
    response_model=PMChecklistResponse,
)
def update_checklist(
    checklist_id: int,
    payload: PMChecklistUpdate,
    db: Session = Depends(get_db),
):

    service = ChecklistService(
        ChecklistRepository(db),
        VehicleRepository(db),
        EmployeeRepository(db),
    )

    return service.update_checklist(
        checklist_id,
        payload,
    )

#DELETE
@router.delete(
    "/{checklist_id}"
)
def delete_checklist(
    checklist_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = ChecklistService(
        ChecklistRepository(db),
        VehicleRepository(db),
        EmployeeRepository(db),
    )

    service.delete_checklist(
        checklist_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
