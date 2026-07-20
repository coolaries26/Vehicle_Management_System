from app.models.maintenance import (
    VehicleComplaint,
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse
)

from app.services.exceptions import (
    NotFoundException,
)


class ComplaintService:

    def __init__(
        self,
        complaint_repo: ComplaintRepository,
        vehicle_repo: VehicleRepository,
        driver_repo: DriverRepository,
    ):

        self.complaint_repo = (
            complaint_repo
        )

        self.vehicle_repo = (
            vehicle_repo
        )

        self.driver_repo = (
            driver_repo
        )

    def create_complaint(
        self,
        payload: ComplaintCreate,
        user_id: int| None = None,
    ):

        if not self.vehicle_repo.exists(
            payload.vehicle_id
        ):
            raise (
                NotFoundException(
                    "Vehicle not found"
                )
            )

        if not self.driver_repo.exists(
            payload.driver_id
        ):
            raise (
                NotFoundException(
                    "Driver not found"
                )
            )

        complaint = (
            VehicleComplaint(
                vehicle_id=payload.vehicle_id,
                driver_id=payload.driver_id,
                issue_description=(
                    payload.issue_description
                ),
                driver_reason=(
                    payload.driver_reason
                ),
                modified_by=user_id,
            )
        )

        return (
            self.complaint_repo
            .create(
                complaint
            )
        )

    def get_complaint(
        self,
        complaint_id: int
    ):
        complaint = (
            self.complaint_repo
            .get_by_id(
                complaint_id
            )
        )
        if not complaint:
            raise (
                NotFoundException(
                    "Complaint not found"
                )
            )
        return complaint

    def get_all_complaint(self):
        return (
            self.complaint_repo.get_all()
        )


    def get_vehicle_complaints(
        self,
        vehicle_id: int
    ):

        return (
            self.complaint_repo
            .get_by_vehicle(
                vehicle_id
            )
        )

    def update_complaint(
        self,
        complaint_id: int,
        payload: ComplaintUpdate,
        user_id: int| None = None,
    ):

        complaint = (
            self.get_complaint(
                complaint_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        return (
            self.complaint_repo
            .update_complaint(
                complaint,
                update_data
            )
        )
    def delete_complaint(
        self,
        complaint_id: int
    ):

        complaint = (
            self.get_complaint(
                complaint_id
            )
        )

        self.complaint_repo.delete(
            complaint
        )