from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.inspection_repository import (    InspectionRepository,)

from app.repositories.complaint_repository import (    ComplaintRepository,)

from app.repositories.employee_repository import ( EmployeeRepository,)
from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
)

from app.services.inspection_service import (
    InspectionService,
)

from app.api.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/v1/inspections",
    tags=["Inspection"]
)

#POST   /
#Create Inspection
@router.post(
    "",
    response_model=InspectionResponse,
    status_code=201,
)
def create_Inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = InspectionService(
        InspectionRepository(db),
        ComplaintRepository(db),
        EmployeeRepository(db),
    )

    return service.create_inspection(
        payload
    )
#Get All
@router.get(
    "",
#    response_model=list[InspectionResponse],
)
def get_all_Inspections(
    db: Session = Depends(get_db),
):

    service = InspectionService(
        InspectionRepository(db),
        ComplaintRepository(db),
        EmployeeRepository(db),
    )
#return service.get_all_inspections()
    return (
        service.get_all_inspections()
    )

#GET    /{Inspection_id}
#Get Inspection
@router.get(
    "/{Inspection_id}",
    response_model=InspectionResponse,
)
def get_Inspection(
    Inspection_id: int,
    db: Session = Depends(get_db),
):

    service = InspectionService(
        InspectionRepository(db),
        ComplaintRepository(db),
        EmployeeRepository(db),
    )

    return service.get_inspection(
        Inspection_id
    )

#PUT    /{Inspection_id}
#Update Inspection
@router.put(
    "/{Inspection_id}",
    response_model=InspectionResponse,
)
def update_Inspection(
    Inspection_id: int,
    payload: InspectionUpdate,
    db: Session = Depends(get_db),
):

    service = InspectionService(
        InspectionRepository(db),
        ComplaintRepository(db),
        EmployeeRepository(db),
    )

    return service.update_inspection(
        Inspection_id,
        payload,
    )

#DELETE /{Inspection_id}
#Delete Inspection
@router.delete(
    "/{Inspection_id}"
)
def delete_Inspection(
    Inspection_id: int,
    db: Session = Depends(get_db),
):

    service = InspectionService(
        InspectionRepository(db),
        ComplaintRepository(db),
        EmployeeRepository(db),
    )

    service.delete_inspection(
        Inspection_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
