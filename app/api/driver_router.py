from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverResponse,
)

from app.services.driver_service import (
    DriverService,
)
from app.api.dependencies import get_current_user_id


router = APIRouter(
    prefix="/api/v1/drivers",
    tags=["Driver"],
)

#POST   /
#Create Driver
@router.post(
    "",
    response_model=DriverResponse,
    status_code=201,
)
def create_driver(
    payload: DriverCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = DriverService(
        DriverRepository(db)
    )

    return service.create_driver(
        payload
    )
#GET    /{driver_id}
#Get Driver
@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
):

    service = DriverService(
        DriverRepository(db)
    )

    return service.get_driver(
        driver_id
    )
#GET    /
#Get All
@router.get(
    "",
    response_model=list[DriverResponse],
)
def get_all_drivers(
    db: Session = Depends(get_db),
):

    service = DriverService(
        DriverRepository(db)
    )

    return (
        service.get_all_drivers()
    )

#PUT    /{driver_id}
#Update Driver
@router.put(
    "/{driver_id}",
    response_model=DriverResponse,
)
def update_driver(
    driver_id: int,
    payload: DriverUpdate,
    db: Session = Depends(get_db),
):

    service = DriverService(
        DriverRepository(db)
    )

    return service.update_driver(
        driver_id,
        payload,
    )
#DELETE /{driver_id}
#Delete Driver
@router.delete(
    "/{driver_id}"
)
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
):

    service = DriverService(
        DriverRepository(db)
    )

    service.delete_driver(
        driver_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
