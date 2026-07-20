# app/repositories/vehicle_repository.py

from sqlalchemy.orm import Session

from app.models.master import VehicleMaster
from app.repositories.base_repository import BaseRepository


class VehicleRepository(
    BaseRepository[VehicleMaster]
):

    def __init__(self, db: Session):

        super().__init__(VehicleMaster, db)

    def get_by_rc_number(
        self,
        rc_number: str
    ) -> VehicleMaster | None:

        return (
            self.db.query(VehicleMaster)
            .filter(
                VehicleMaster.rc_number == rc_number
            )
            .first()
        )

    def get_active_vehicles(self,rc_number: str) -> VehicleMaster | None:

        return (
            self.db.query(VehicleMaster)
            .filter(
                VehicleMaster.active_flag.is_(True)
            )
            .all()
        )

    def update_vehicle(
        self,
        vehicle: VehicleMaster,
        data: dict
    ) -> VehicleMaster | None:

        for key, value in data.items():

            setattr(
                vehicle,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle
    def get_by_id(
    self,
    vehicle_id: int
        ) -> VehicleMaster | None:
        return (
            self.db.query(VehicleMaster)
            .filter(
                VehicleMaster.vehicle_id == vehicle_id
            )
            .first()
        )
    def exists(
    self,
    vehicle_id: int
    ) -> bool:
    
        return (
            self.get_by_id(vehicle_id)
            is not None
        )
    def delete_vehicle(
        self,
        vehicle: VehicleMaster,
    ) -> None:

        self.db.delete(
            vehicle
        )

        self.db.commit()
