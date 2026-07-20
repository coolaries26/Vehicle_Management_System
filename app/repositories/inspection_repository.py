from sqlalchemy.orm import Session

from app.models.maintenance import (
    TechnicianInspection,
)

from app.repositories.base_repository import (
    BaseRepository,
)

from typing import List

class InspectionRepository(
    BaseRepository[TechnicianInspection]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            TechnicianInspection,
            db,
        )

    def get_by_id(
        self,
        inspection_id: int,
    ) -> TechnicianInspection | None:

        return (
            self.db.query(
                TechnicianInspection
            )
            .filter(
                TechnicianInspection.inspection_id
                == inspection_id
            )
            .first()
        )

    def get_by_complaint(
		self,
		complaint_id: int,
    ) -> List[TechnicianInspection] | None:

        return (
            self.db.query(
                TechnicianInspection
            )
            .filter(
                TechnicianInspection.complaint_id
                == complaint_id
            )
            .all()
        )

    def get_by_technician(
        self,
        technician_id: int,
    ) -> List[TechnicianInspection] | None:

        return (
            self.db.query(
                TechnicianInspection
            )
            .filter(
                TechnicianInspection.technician_id
                == technician_id
            )
            .all()
        )

    def update_inspection(
        self,
        inspection: TechnicianInspection,
        data: dict,
    ) -> TechnicianInspection:

        for key, value in data.items():
            setattr(
                inspection,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            inspection
        )

        return inspection

    def delete_inspection(
        self,
        inspection: TechnicianInspection,
    ) -> None:

        self.db.delete(
            inspection
        )

        self.db.commit()

    def exists(
    self,
    inspection_id: int
    ) -> bool:
    
        return (
            self.get_by_id(inspection_id)
            is not None
        )