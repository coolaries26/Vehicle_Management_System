from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.complaint_repository import (
    ComplaintRepository,
)
from app.repositories.driver_repository import (
    DriverRepository,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)

from app.services.complaint_service import (
    ComplaintService,
    VehicleComplaint,
)
from app.api.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/v1/complaints",
    tags=["Complaint"],
)

#Create
#Post
@router.post(
    "",
    response_model=ComplaintResponse,
    status_code=201
)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    return service.create_complaint(
        payload
    )
#GET
@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    return service.get_complaint(
        complaint_id
    )

#get all
@router.get(
    "",
    response_model=list[ComplaintResponse],
)
def get_all_complaint(
    db: Session = Depends(get_db),
):

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    complaints = service.get_all_complaint()
#    print(complaints)
    return complaints

#    return  (
#        service.get_all_complaint()
#    ) 


#Update Driver
@router.put(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def update_complaint(
    complaint_id: int,
    payload: ComplaintUpdate,
    db: Session = Depends(get_db),
):

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    return service.update_complaint(
        complaint_id,
        payload,
    )
#DELETE /{driver_id}
#Delete Driver
@router.delete(
    "/{complaint_id}"
)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),

    )

    service.delete_complaint(
        complaint_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
