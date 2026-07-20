# app/repositories/jobcard_repository.py


from sqlalchemy.orm import Session

from app.models.maintenance import (
    MaintenanceJobCard,
)

from app.repositories.base_repository import (
    BaseRepository,
)


class JobCardRepository(
    BaseRepository[MaintenanceJobCard]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            MaintenanceJobCard,
            db,
        )

    def get_by_id(
        self,
        job_card_id: int,
    ) -> MaintenanceJobCard | None:

        return (
            self.db.query(
                MaintenanceJobCard
            )
            .filter(
                MaintenanceJobCard.job_card_id
                == job_card_id
            )
            .first()
        )

    def get_by_vehicle(
        self,
        vehicle_id: int,
    ) -> list:
        return (
            self.db.query(
                MaintenanceJobCard
            )
            .filter(
                MaintenanceJobCard.vehicle_id
                == vehicle_id
            )
            .all()
        )

    def get_by_complaint(
        self,
        complaint_id: int,
    ) -> list|None:
        return (
            self.db.query(
                MaintenanceJobCard
            )
            .filter(
                MaintenanceJobCard.complaint_id
                == complaint_id
            )
            .all()
        )

    def get_by_inspection(
        self,
        inspection_id: int,
    ) -> list|None:
        return (
            self.db.query(
                MaintenanceJobCard
            )
            .filter(
                MaintenanceJobCard.inspection_id
                == inspection_id
            )
            .all()
        )

    def update_jobcard(
        self,
        jobcard: MaintenanceJobCard,
        data: dict,
    ) -> MaintenanceJobCard:

        for key, value in data.items():

            setattr(
                jobcard,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            jobcard
        )

        return jobcard

    def delete_jobcard(
        self,
        jobcard: MaintenanceJobCard,
    ) -> None:

        self.db.delete(
            jobcard
        )

        self.db.commit()
    
    def exists(
    self,
    job_card_id: int
    ) -> bool:
    
        return (
            self.get_by_id(job_card_id)
            is not None
        )