from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintCreate(BaseModel):
    vehicle_id: int
    driver_id: int 
    issue_description: str
    driver_reason: str | None = None
    active_flag: bool | None = True



class ComplaintUpdate(BaseModel):
    issue_description: str | None = None
    driver_reason: str | None = None
    vehicle_received_at: datetime | None = None
    active_flag: bool | None = True


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    complaint_id: int
    vehicle_id: int
    driver_id: int
    issue_description: str | None = None
    driver_reason: str | None = None
    active_flag: bool | None = True
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None