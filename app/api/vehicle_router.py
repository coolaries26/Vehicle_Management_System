from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)

from app.services.vehicle_service import (
    VehicleService,
)
from app.api.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["Vehicle"],
)
#Create Vehicle
@router.post(
    "",
    response_model=VehicleResponse,
    status_code=201,
)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = VehicleService(
        VehicleRepository(db)
    )

    return service.create_vehicle(
        payload
    )
#Get Vehicle
@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
):

    service = VehicleService(
        VehicleRepository(db)
    )

    return service.get_vehicle(
        vehicle_id
    )
#Get All
@router.get(
    "",
    response_model=list[VehicleResponse],
)
def get_all_vehicles(
    db: Session = Depends(get_db),
):

    service = VehicleService(
        VehicleRepository(db)
    )

    return (
        service.get_all_vehicles()
    )
#Update Vehicle
@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
):

    service = VehicleService(
        VehicleRepository(db)
    )

    return service.update_vehicle(
        vehicle_id,
        payload,
    )
#Delete Vehicle
@router.delete(
    "/{vehicle_id}"
)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
):

    service = VehicleService(
        VehicleRepository(db)
    )

    service.delete_vehicle(
        vehicle_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
