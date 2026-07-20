from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.jobcard_part_repository import (
    JobCardPartRepository,
)
from app.repositories.complaint_repository import ( ComplaintRepository )
from app.repositories.inspection_repository import (InspectionRepository )
from app.repositories.vehicle_repository import (VehicleRepository )
from app.schemas.jobcard_part import (
    JobCardPartCreate,
    JobCardPartResponse,
    JobCardPartUpdate
)

from app.services.jobcard_part_service import (
    JobCardPartService
)
from app.api.dependencies import get_current_user_id


router = APIRouter(
    prefix="/api/v1/jobcard-parts",
    tags=["Job Card Part"]
)

#POST   /
#Create JobCardPart
@router.post(
    "",
    response_model=JobCardPartResponse,
    status_code=201,
)
def create_JobCardPart(
    payload: JobCardPartCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = JobCardPartService(
        JobCardPartRepository(db),
    )

    return service.create_jobcard_part(
        payload
    )
#Get All
@router.get(
    "",
    response_model=list[JobCardPartResponse],
)
def get_all_JobCardParts(
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return (
        service.get_all_jobcard_parts()
    )

#GET    /{JobCardPart_id}
#Get JobCardPart
@router.get(
    "/{JobCardPart_id}",
    response_model=JobCardPartResponse,
)
def get_JobCardPart(
    JobCardPart_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return service.get_jobcard_part(
        JobCardPart_id
    )

#PUT    /{JobCardPart_id}
#Update JobCardPart
@router.put(
    "/{JobCardPart_id}",
    response_model=JobCardPartResponse,
)
def update_JobCardPart(
    JobCardPart_id: int,
    payload: JobCardPartUpdate,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return service.update_jobcard_part(
        JobCardPart_id,
        payload,
    )

#DELETE /{JobCardPart_id}
#Delete JobCardPart
@router.delete(
    "/{JobCardPart_id}"
)
def delete_JobCardPart(
    JobCardPart_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    service.delete_jobcard_part(
        JobCardPart_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
