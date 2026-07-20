from sqlalchemy.orm import Session

from app.models.maintenance import (
    PreventiveMaintenanceChecklist,
)

from app.repositories.base_repository import (
    BaseRepository,
)


class ChecklistRepository(
    BaseRepository[
        PreventiveMaintenanceChecklist
    ]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            PreventiveMaintenanceChecklist,
            db,
        )

    def get_by_id( self, checklist_id: int,) -> PreventiveMaintenanceChecklist | None:
        return (self.db.query(
            PreventiveMaintenanceChecklist
            )
            .filter(
                PreventiveMaintenanceChecklist.checklist_id
                == checklist_id
            )
            .first()
        )

    def get_by_vehicle(self, vehicle_id: int,) -> PreventiveMaintenanceChecklist|None:
        return(self.db.query(
                PreventiveMaintenanceChecklist
            )
            .filter(
                PreventiveMaintenanceChecklist.vehicle_id
                == vehicle_id
            )
            .all()
        )

    def get_by_technician(self,technician_id: int,) -> PreventiveMaintenanceChecklist | None:
        return(self.db.query(
                PreventiveMaintenanceChecklist
            )
            .filter(
                PreventiveMaintenanceChecklist.technician_id
                == technician_id
            )
            .all()
        )

    def exists(
        self,
        checklist_id: int,
    ) -> bool:

        return (
            self.db.query(
                PreventiveMaintenanceChecklist
            )
            .filter(
                PreventiveMaintenanceChecklist.checklist_id
                == checklist_id
            )
            .first()
            is not None
        )

    def update_checklist(
        self,
        checklist: PreventiveMaintenanceChecklist,
        data: dict,
    ) -> PreventiveMaintenanceChecklist:

        for key, value in data.items():

            setattr(
                checklist,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            checklist
        )

        return checklist

    def delete_checklist(
        self,
        checklist: PreventiveMaintenanceChecklist,
    ) -> None:

        self.db.delete(
            checklist
        )

        self.db.commit()