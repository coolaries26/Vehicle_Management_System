from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore

#Create JobCard
class JobCardCreate(BaseModel):
    complaint_id: int
    inspection_id: int
    vehicle_id: int
    maintenance_type_id: int | None = None
    severity_id: int | None = None
    labour_charges: float | None = None
    description: str | None = None
    active_flag: bool | None = True

#Update
class JobCardUpdate(BaseModel):
    severity_id: int | None = None
    labour_charges: float | None = None
    job_status: str | None = None
    job_card_status: str | None = None
    description: str | None = None
    downtime_hours: float | None = None
    completion_date: date | None = None
    active_flag: bool | None = True


#Response
class JobCardResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    job_card_id: int
    vehicle_id: int
    complaint_id: int
    inspection_id: int

    description: str | None = None
    labour_charges: float | None = None

    maintenance_type_id: int | None = None
    severity_id: int | None = None
    completion_date: date | None = None
    active_flag: bool | None = True

    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None