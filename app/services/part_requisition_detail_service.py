from fastapi import HTTPException #type: ignore

from app.models.part_requisition import (
    PartRequisitionDetail,
)

from app.repositories.part_requisition_detail_repository import (
    PartRequisitionDetailRepository,
)


class PartRequisitionDetailService:

    def __init__(
        self,
        repository:
        PartRequisitionDetailRepository,
    ):
        self.repository = repository

    def create(
        self,
        payload,
    ):

        detail = (
            PartRequisitionDetail(
                requisition_id=
                payload.requisition_id,

                part_id=
                payload.part_id,

                quantity_required=
                payload.quantity_required,

                quantity_returned=
                payload.quantity_returned,

                required_serial_number=
                payload.required_serial_number,

                returned_serial_number=
                payload.returned_serial_number,

                remarks=
                payload.remarks,
            )
        )

        return self.repository.create(
            detail
        )

    def get_all(
        self,
    ):

        return self.repository.get_all()

    def get_by_id(
        self,
        requisition_detail_id: int,
    ):

        detail = (
            self.repository.get_by_id(
                requisition_detail_id
            )
        )

        if not detail:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Requisition Detail not found",
            )

        return detail

    def update(
        self,
        requisition_detail_id: int,
        payload,
    ):

        detail = self.get_by_id(
            requisition_detail_id
        )

        data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                detail,
                key,
                value,
            )

        return self.repository.update(
            detail
        )

    def delete(
        self,
        requisition_detail_id: int,
    ):

        detail = self.get_by_id(
            requisition_detail_id
        )

        detail.active_flag = False

        return self.repository.update(
            detail
        )