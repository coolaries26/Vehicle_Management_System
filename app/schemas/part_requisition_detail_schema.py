from pydantic import BaseModel #type: ignore


class PartRequisitionDetailBase(
    BaseModel
):
    requisition_id: int

    part_id: int

    quantity_required: float | None = None

    quantity_returned: float | None = None

    required_serial_number: str | None = None

    returned_serial_number: str | None = None

    remarks: str | None = None


class PartRequisitionDetailCreate(
    PartRequisitionDetailBase
):
    pass


class PartRequisitionDetailUpdate(
    BaseModel
):

    requisition_id: int | None = None

    part_id: int | None = None

    quantity_required: float | None = None

    quantity_returned: float | None = None

    required_serial_number: str | None = None

    returned_serial_number: str | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class PartRequisitionDetailResponse(
    PartRequisitionDetailBase
):

    requisition_detail_id: int

    active_flag: bool

    model_config = {
        "from_attributes": True
    }