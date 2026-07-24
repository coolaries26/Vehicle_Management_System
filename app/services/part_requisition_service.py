from datetime import datetime

from fastapi import HTTPException   #type:  ignore

from app.models.part_requisition import (
    PartRequisition,
)

from app.repositories.part_requisition_repository import (
    PartRequisitionRepository,
)


class PartRequisitionService:

    def __init__(
        self,
        repository:
        PartRequisitionRepository,
    ):
        self.repository = (
            repository
        )

    def _generate_number(
        self,
    ):

        year = (
            datetime.now().year
        )

        count = len(
            self.repository
            .get_all()
        ) + 1

        return (
            f"PR-"
            f"{year}-"
            f"{count:06d}"
        )

    def create(
        self,
        payload,
    ):

        requisition = (
            PartRequisition(
                requisition_number=
                self._generate_number(),

                vehicle_id=
                payload.vehicle_id,

                job_card_id=
                payload.job_card_id,

                technician_id=
                payload.technician_id,

                remarks=
                payload.remarks,

                status=
                payload.status,
            )
        )

        return (
            self.repository
            .create(
                requisition
            )
        )

    def get_all(
        self,
    ):
        return (
            self.repository
            .get_all()
        )

    def get_by_id(
        self,
        requisition_id: int,
    ):

        requisition = (
            self.repository
            .get_by_id(
                requisition_id
            )
        )

        if not requisition:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Requisition not found",
            )

        return requisition

    def update(
        self,
        requisition_id,
        payload,
    ):

        requisition = (
            self.get_by_id(
                requisition_id
            )
        )

        data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for key, value in (
            data.items()
        ):
            setattr(
                requisition,
                key,
                value,
            )

        return (
            self.repository
            .update(
                requisition
            )
        )

    def delete(
        self,
        requisition_id,
    ):

        requisition = (
            self.get_by_id(
                requisition_id
            )
        )

        requisition.active_flag = (
            False
        )

        return (
            self.repository
            .update(
                requisition
            )
        )
