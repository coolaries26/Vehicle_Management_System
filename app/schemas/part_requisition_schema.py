from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore
from datetime import datetime


class PartRequisitionBase(BaseModel):
    vehicle_id: int
    job_card_id: int
    technician_id: int | None = None
    remarks: str | None = None
    status: str | None = "OPEN"

class PartRequisitionCreate(
    BaseModel
):
    vehicle_id: int
    job_card_id: int
    technician_id: int | None
    remarks: str | None
    status: str | None

class PartRequisitionUpdate(
    BaseModel
):
    vehicle_id: int | None = None
    job_card_id: int | None = None
    technician_id: int | None = None
    remarks: str | None = None
    status: str | None = None
    active_flag: bool | None = None


class PartRequisitionResponse(
    PartRequisitionBase
):
    requisition_id: int
    requisition_number: str | None
    requisition_date: datetime
    active_flag: bool
    created_by: int | None
    created_at: datetime
    modified_by: int | None
    modified_at: datetime
    model_config = {
        "from_attributes": True
    }
