from app.models.master import VehicleMaster
from app.repositories.vehicle_repository import (
    VehicleRepository,
)
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
)
from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
)


class VehicleService:

    def __init__(
        self,
        vehicle_repository: VehicleRepository
    ):
        self.vehicle_repo = (
            vehicle_repository
        )

    def create_vehicle(
        self,
        payload: VehicleCreate,
        user_id: int| None = None,
    ) -> VehicleMaster:

        existing_vehicle = (
            self.vehicle_repo.get_by_rc_number(
                payload.rc_number
            )
        )

        if existing_vehicle:

            raise DuplicateRecordException(
                f"Vehicle already exists "
                f"with RC "
                f"{payload.rc_number}"
            )
        vehicle = VehicleMaster(
            vehicle_type_id=payload.vehicle_type_id,
            fuel_type_id=payload.fuel_type_id,
            vehicle_status_id=payload.vehicle_status_id,

            rc_number=payload.rc_number,

            purchase_date=payload.purchase_date,
            rc_expiry_date=payload.rc_expiry_date,

            engine_no=payload.engine_no,
            chassis_no=payload.chassis_no,
            gps_id=payload.gps_id,

            fuel_capacity=payload.fuel_capacity,
            modified_by=user_id,
        )

        return self.vehicle_repo.create(
            vehicle
        )

    def get_vehicle(
        self,
        vehicle_id: int
    ) -> VehicleMaster:

        vehicle = (
            self.vehicle_repo.get_by_id(
                vehicle_id
            )
        )

        if not vehicle:

            raise NotFoundException(
                f"Vehicle "
                f"{vehicle_id} "
                f"not found"
            )

        return vehicle

    def get_all_vehicles(self):

        return (
            self.vehicle_repo.get_all()
        )

    def update_vehicle(
        self,
        vehicle_id: int,
        payload: VehicleUpdate,
        user_id: int| None = None,
    ):

        vehicle = (
            self.get_vehicle(
                vehicle_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.vehicle_repo
            .update_vehicle(
                vehicle,
                update_data
            )
        )

    def delete_vehicle(
        self,
        vehicle_id: int
    ):

        vehicle = (
            self.get_vehicle(
                vehicle_id
            )
        )

        self.vehicle_repo.delete(
            vehicle
        )