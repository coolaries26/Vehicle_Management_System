# app/repositories/complaint_repository.py

from sqlalchemy.orm import Session

from app.models.maintenance import VehicleComplaint
from app.repositories.base_repository import BaseRepository


class ComplaintRepository(
    BaseRepository[VehicleComplaint]
):

    def __init__(self, db: Session):

        super().__init__(
            VehicleComplaint,
            db
        )

    def get_by_vehicle(
        self,
        vehicle_id: int
    ):
        return (
            self.db.query(
                VehicleComplaint
            )
            .filter(
                VehicleComplaint.vehicle_id
                == vehicle_id
            )
            .all()
        )

    def get_by_driver(
        self,
        driver_id: int
    ):
        return (
            self.db.query(
                VehicleComplaint
            )
            .filter(
                VehicleComplaint.driver_id
                == driver_id
            )
            .all()
        )

    def update_complaint(
        self,
        complaint: VehicleComplaint,
        data: dict
    ):

        for key, value in data.items():

            setattr(
                complaint,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(
            complaint
        )

        return complaint

    def get_by_id(
    self,
    complaint_id: int
    ) -> VehicleComplaint | None:
    
        return (
            self.db.query(VehicleComplaint)
            .filter(
                VehicleComplaint.complaint_id
                == complaint_id
            )
            .first()
        )

    def exists(
    self,
    complaint_id: int
    ) -> bool:
    
        return (
            self.get_by_id(complaint_id)
            is not None
        )
