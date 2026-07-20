from fastapi import APIRouter   #type: ignore
from fastapi import Depends     #type: ignore
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.part_repository import (
    PartRepository,
)
from app.repositories.inspection_repository import (
    InspectionRepository,
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)
from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.schemas.part import (
    PartCreate,
    PartResponse,
    PartUpdate,
)

from app.services.part_service import (
    PartService,
)
from app.api.dependencies import get_current_user_id


router = APIRouter(
    prefix="/api/v1/parts",
    tags=["Parts"]
)

#POST   /
#Create Part
@router.post(
    "",
    response_model=PartResponse,
    status_code=201,
)
def create_Part(
    payload: PartCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = PartService(
        PartRepository(db),
    )

    return service.create_part(
        payload
    )
#Get All
@router.get(
    "",
#    response_model=list[PartResponse],
)
def get_all_Parts(
    db: Session = Depends(get_db),
):

    service = PartService(
        PartRepository(db),
    )
#    res=service.get_all_jobcard()
#    for item in res:
#        print(item.__dict__)
#return service.get_all_inspections()
    return (
        service.get_all_parts()
    )

#GET    /{Part_id}
#Get Part
@router.get(
    "/{Part_id}",
    response_model=PartResponse,
)
def get_Part(
    Part_id: int,
    db: Session = Depends(get_db),
):

    service = PartService(
        PartRepository(db),
    )

    return service.get_part_by_id(
        Part_id
    )

#PUT    /{Part_id}
#Update Part
@router.put(
    "/{Part_id}",
    response_model=PartResponse,
)
def update_Part(
    Part_id: int,
    payload: PartUpdate,
    db: Session = Depends(get_db),
):

    service = PartService(
        PartRepository(db),
    )

    return service.update_part(
        Part_id,
        payload,
    )

#DELETE /{Part_id}
#Delete Part
@router.delete(
    "/{Part_id}"
)
def delete_Part(
    Part_id: int,
    db: Session = Depends(get_db),
):

    service = PartService(
        PartRepository(db),
    )

    service.delete_part(
        Part_id
    )

    return {
        "success": True,
        "message":
        "Part deleted successfully",
    }
