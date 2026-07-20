from app.models.maintenance import MaintenanceJobCard
from app.schemas.jobcard import JobCardCreate,JobCardUpdate,JobCardResponse
from app.services.exceptions import NotFoundException
from app.repositories.jobcard_repository import JobCardRepository
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.inspection_repository import InspectionRepository

class JobCardService:
    def __init__(
        self,
        jobcard_repo: JobCardRepository,
        complaint_repo: ComplaintRepository,
        vehicle_repo: VehicleRepository,
        inspection_repo: InspectionRepository,
    ):
        self.jobcard_repo = (          jobcard_repo)
        self.complaint_repo = (        complaint_repo)
        self.inspection_repo = (       inspection_repo)
        self.vehicle_repo = (          vehicle_repo)

    def create_jobcard(
        self,
        payload,
        user_id: int| None = None,
    ) -> MaintenanceJobCard:

        if not self.vehicle_repo.exists(  payload.vehicle_id
        ):
            raise NotFoundException(        "Vehicle not found")

        if not self.complaint_repo.exists(
            payload.complaint_id
        ):
            raise NotFoundException(         "Complaint not found")

        if not self.inspection_repo.exists(
            payload.inspection_id
        ):
            raise NotFoundException(          "Inspection not found")
 
        jobcard = (
            MaintenanceJobCard(
                complaint_id=
                payload.complaint_id,
                inspection_id=
                payload.inspection_id,
                vehicle_id=
                payload.vehicle_id,
                labour_charges=
                payload.labour_charges,
                description=
                payload.description,
                modified_by=
                user_id,
            )
        )

        return (
            self.jobcard_repo
            .create(
                jobcard
            )
        )

    def get_jobcard(
        self,
        jobcard_id: int,
    ) :

        jobcard = (
            self.jobcard_repo.get_by_id(
                jobcard_id
            )
        )

        if not jobcard:
            raise NotFoundException(
                f"Inspection "
                f"{jobcard_id} "
                f"not found"
            )

        return jobcard

    def get_all_jobcard(
        self,
    ):

        return (
            self.jobcard_repo.get_all()
        )

    def get_by_complaint(
        self,
        complaint_id: int,
    ):

        return (
            self.jobcard_repo
            .get_by_complaint(
                complaint_id
            )
        )

    def update_jobcard(
        self,
        jobcard_id: int,
        payload: JobCardUpdate,
        user_id: int| None = None,
    ):

        update = (
            self.get_jobcard(
                jobcard_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.jobcard_repo
            .update_jobcard(
                update,
                update_data
            )
        )

    def delete_jobcard(
        self,
        jobcard_id: int,
    ) -> None:

        jobcard = (
            self.get_jobcard(
                jobcard_id
            )
        )

        self.jobcard_repo.delete(
            jobcard
        )