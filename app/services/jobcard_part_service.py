from app.models.maintenance import (
    JobCardPart,
)

from app.repositories.jobcard_part_repository import (
    JobCardPartRepository,
)

from app.schemas.jobcard_part import (
    JobCardPartCreate,
)

from app.services.exceptions import (
    NotFoundException,
)


class JobCardPartService:

    def __init__(
        self,
        jobcard_part_repo: JobCardPartRepository,
    ):

        self.jobcard_part_repo = (
            jobcard_part_repo
        )

    def create_jobcard_part(
        self,
        payload: JobCardPartCreate,
        user_id: int| None = None,
    ):

        jobcard_part = JobCardPart(
            job_card_id=payload.job_card_id,
            part_id=payload.part_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price,
            total_price=(
                payload.quantity
                * payload.unit_price
            ),
            modified_by=user_id,
        )

        return (
            self.jobcard_part_repo.create(
                jobcard_part
            )
        )

    def get_jobcard_part(
        self,
        jobcard_part_id: int,
    ):

        jobcard_part = (
            self.jobcard_part_repo.get_by_id(
                jobcard_part_id
            )
        )

        if not jobcard_part:
            raise NotFoundException(
                f"JobCardPart "
                f"{jobcard_part_id} "
                f"not found"
            )

        return jobcard_part

    def get_all_jobcard_parts(
        self,
    ):

        return (
            self.jobcard_part_repo.get_all()
        )

    def get_parts_by_part_id(
        self,
        part_id: int,
    ):

        return (
            self.jobcard_part_repo.get_by_part(
                part_id
            )
        )

    def update_jobcard_part(
        self,
        jobcard_part_id: int,
        payload,
        user_id: int| None = None,
    ):

        jobcard_part = (
            self.get_jobcard_part(
                jobcard_part_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        return (
            self.jobcard_part_repo
            .update_jobcard_part(
                jobcard_part,
                update_data,
            )
        )

    def delete_jobcard_part(
        self,
        jobcard_part_id: int,
    ):

        jobcard_part = (
            self.get_jobcard_part(
                jobcard_part_id
            )
        )

        self.jobcard_part_repo.delete(
            jobcard_part
        )
