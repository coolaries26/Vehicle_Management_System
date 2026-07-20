from app.models.maintenance import PreventiveMaintenanceChecklist

from app.repositories.checklist_repository import (
    ChecklistRepository,
)
from app.repositories.vehicle_repository import ( VehicleRepository)
from app.schemas.checklist import (
    PMChecklistCreate,
    PMChecklistResponse,
    PMChecklistUpdate
)

from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
)

from app.services.checklist_service import (
    PreventiveMaintenanceChecklist
)

class ChecklistService:

    def __init__(
        self,
        checklist_repo,
        vehicle_repo,
        employee_repo,
    ):

        self.checklist_repo = (
            checklist_repo
        )

        self.vehicle_repo = (
            vehicle_repo
        )

        self.employee_repo = (
            employee_repo
        )
    
    def create_checklist(
        self,
        payload,
        user_id: int| None = None,
    ):
        if not self.vehicle_repo.exists(
            payload.vehicle_id
        ):
            raise NotFoundException(
                "Vehicle not found"
            )
        
        if not self.employee_repo.exists(
            payload.technician_id
        ):
            raise NotFoundException(
                "Technician not found"
            )
        
        checklist = (
            PreventiveMaintenanceChecklist(
                vehicle_id=
                payload.vehicle_id,

                technician_id=
                payload.technician_id,

                observation=
                payload.observation,

                issue_found=
                payload.issue_found,

                issue_description=
                payload.issue_description,

                modified_by=user_id
            )
        )

        return (
            self.checklist_repo
            .create(checklist)
        )
    def get_checklist(
        self,
        checklist_id: int
    ):

        checklist = (
            self.checklist_repo
            .get_by_id(checklist_id)
        )

        if not checklist:

            raise NotFoundException(
                f"PMChecklist "
                f"{checklist_id}"
                f" not found"
            )

        return checklist

    def get_all_checklists(self):

        return (
            self.checklist_repo.get_all()
        )

    def update_checklist(
        self,
        checklist_id: int,
        payload: PMChecklistUpdate,
        user_id: int| None = None,
    ):

        checklist = (
            self.get_checklist(
                checklist_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        return (
            self.checklist_repo
            .update_checklist(
                checklist,
                update_data
            )
        )

    def delete_checklist(
        self,
        checklist_id: int
    ):

        checklist = (
            self.get_checklist(
                checklist_id
            )
        )

        self.checklist_repo.delete(
            checklist
        )